#include <iostream>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>

#include <subnet/subnet.ssnet.relay.abb_events_parser/subnet.ssnet.relay.abb_events_parser.h>
#include <subnet/subnet.ssnet.relay.abb_events_parser/subnet.ssnet.relay.abb_events_states.h>

using namespace std;
using namespace abb_event_parser_ns;
using namespace iec61850_cid_objects_ns;

///////////////////////////////////////////////////////////////////////////////
// event_state
event_state::event_state(events_content_handler_fsm *fsm)
	:_fsm(fsm)
{
}

event_state::~event_state()
{
}

void event_state::SAX2StartElementNs(osa::xml::sax_callbacks::element &e)
{
}

void event_state::SAX2EndElementNs(osa::xml::sax_callbacks::element &e)
{
}

void event_state::SAX2Characters(std::string &ch)
{
}

void event_state::SAX2CDataBlock(string &value)
{
}

///////////////////////////////////////////////////////////////////////////////
// events_content_handler_fsm
events_content_handler_fsm::events_content_handler_fsm(std::istream &is, abb_event_parser* parser)
	:_parser(parser)
{
	if (0 == is.rdbuf()->in_avail())
	{
		throw runtime_error("event stream is empty");
	}
	push_state(new eventmonitoring(this));
}

void events_content_handler_fsm::SAX2StartElementNs(sax_callbacks::element &e)
{
	_state_stack.top()->SAX2StartElementNs(e);
}

void events_content_handler_fsm::SAX2EndElementNs(sax_callbacks::element &e)
{
	_state_stack.top()->SAX2EndElementNs(e);
}

void events_content_handler_fsm::SAX2Characters(string &ch)
{
	_state_stack.top()->SAX2Characters(ch);
}

void events_content_handler_fsm::SAX2CDataBlock(string &value)
{
	_state_stack.top()->SAX2CDataBlock(value);
}

void events_content_handler_fsm::push_state(event_state *next_state)
{
	unique_ptr<event_state> _cs(next_state);
	_state_stack.push(move(_cs)); 
}

void events_content_handler_fsm::pop_state()
{
	_state_stack.pop();
}

void events_content_handler_fsm::add_event(event_info &ev)
{
	_events.emplace_back(ev);
}

///////////////////////////////////////////////////////////////////////////////
// abb_event_parser
abb_event_parser::abb_event_parser(std::istream &is)
	:_echf(is, this), _reader(is, _echf)
{
	_reader.parse();
}


///////////////////////////////////////////////////////////////////////////////
// decoder
decoder::decoder(std::istream &event_file_stream, std::istream &cid_file_stream)
	:_abb_parser(event_file_stream), _stfb(nullptr), _cid_parser(cid_file_stream,_stfb)
{
	clear_containers();
}

void decoder::clear_containers()
{
	_abb_logical_device_point.clear();
	_decode_nodes.clear();
	_matched_events.clear();
	_logical_devices.clear();
	_lnode_map.clear();
	_do_type_map.clear();
	_enumval_map.clear();
	_event_type_map.clear();
}

vector<event_info>& decoder::get_matched_events()
{ 
	decode();
	return _abb_parser.events(); 
}
char decoder::get_delimiter(const string &code) const
{
	char token;
	for (char ch : code)
	{
		if (!((ch <= '9' && ch >= '0') || (ch <= 'z' && ch >= 'a') || (ch <= 'Z' && ch >= 'A')))
		{
			token = ch;
			break;
		}
	}
	return token;
}

void decoder::split_code_to_components()
{
	vector<event_info>& events = _abb_parser.events();
	if (events.size() == 0)
	{
		throw runtime_error("no event available");
	}

	char token = get_delimiter(events[0]._code);
	for (event_info &event : events)
	{
		std::size_t code_length = event._code.length();
		if (code_length == 0)
		{
			throw runtime_error("Wrong format - no code element");
		}
		std::string rest_code = event._code;
		do
		{
			std::size_t token_pos = rest_code.find_first_of(token);
			std::string component = rest_code.substr(0, token_pos);
			rest_code = rest_code.substr((token_pos + 1), code_length);
			code_length = rest_code.length();
			event._code_components.push_back(component);
		} while (rest_code.find(token) != std::string::npos);
		//last item
		event._code_components.push_back(rest_code);
	}
}

void decoder::match_delimiter()
{
	auto& events = _abb_parser.events();
	char event_token = get_delimiter(events[0]._code);
	iec_device& device = static_cast<iec_device&>(_cid_parser.device());
	char cid_token = get_delimiter(device.logical_devices[0].points.get_key(0));

	for (auto &event : events)
	{
		std::size_t first_dot_pos = event._code.find_first_of(event_token);
		std::size_t code_length = event._code.length();
		std::string ldevice_name = event._code.substr(0, first_dot_pos);
		event._ldvice_name = ldevice_name;
		event._ldvice_name.insert(0, device.name);
		event._code = event._code.substr((first_dot_pos + 1), code_length);
		std::replace(event._code.begin(), event._code.end(), event_token, cid_token);
	}

}

///////////////////////////////////////////////////////////////////////////////
// function_code is always in the second place of the key string
void decoder::remove_function_code_from_cid_key(std::string &key, char &cid_token) const
{
	std::size_t first_cid_token_pos = key.find_first_of(cid_token);
	std::string key_header = key.substr(0, (first_cid_token_pos + 1)); //plus token
	const size_t key_place = 2;

	for (int i = 0; i < key_place; i++)
	{
		std::size_t key_length = key.length();
		key = key.substr((first_cid_token_pos + 1), key_length);
		first_cid_token_pos = key.find_first_of(cid_token);
	}
	key.insert(0, key_header);
}

void decoder::pair_key_intype_in_logical_device(const std::string event_code, iec_logical_device &logical_device)
{
	if (0 == logical_device.points.size())
	{
		throw runtime_error("no points available in logical device");
	}

	;
	char cid_token = get_delimiter(logical_device.points.get_key(0));

	vector_map<std::string, iec_point> logical_device_point = logical_device.points;
	if (0 == logical_device_point.size())
	{
		throw runtime_error("no points in logical devices");
	}
	
	for (auto point_iter = logical_device_point.begin(), point_end = logical_device_point.end(); point_iter != point_end; ++point_iter)
	{
		std::string key = point_iter.get_key();
		iec_point _iec_points = logical_device.points[key];
		std::string _ln_type = _iec_points.ln_type;
		remove_function_code_from_cid_key(key, cid_token);
		std::map<std::string, std::string>::const_iterator itor = _abb_logical_device_point.find(key);
		if (itor == _abb_logical_device_point.end())
		{
			std::pair<std::string, std::string> abb_point = std::pair<std::string, std::string>(key, _ln_type);
			_abb_logical_device_point.insert(abb_point);
			if (event_code.compare(key) == 0)
			{
				break;
			}
		}
	}
}

xml_node* decoder::get_nodes(const std::string &node_key, std::vector<xml_node> &nodes) const
{
	std::map<std::string, std::string>::const_iterator itor;
	std::string attribute_name;
	if (nodes.empty())
	{
		throw runtime_error("The size of nodes is zero");
	}
	for (auto &node : nodes)
	{
		if (node._name.compare("EnumVal") == 0)
		{
			itor = node._attribute_values.find("ord");
			if (itor == node._attribute_values.end())
			{
				throw runtime_error("value does not exist in node: " + node_key);
			}
			attribute_name = itor->second;
		}
		else
		{
			itor = node._attribute_values.find("name");
			if (itor == node._attribute_values.end())
			{
				throw runtime_error("name does not exist in node:" + node_key);
			}
			attribute_name = itor->second;
		}

		if (attribute_name.compare(node_key) == 0)
		{
			return &node;
		}
	}
	return nullptr;
}

void decoder::create_type_map(std::map<std::string, int> &event_type_map)
{	
	event_type_map.insert(pair<std::string, int>("Enum", 1));
	event_type_map.insert(pair<std::string, int>("BOOLEAN", 2));
	event_type_map.insert(pair<std::string, int>("INT128", 3));
	event_type_map.insert(pair<std::string, int>("Quality", 4));
	event_type_map.insert(pair<std::string, int>("Timestamp", 5));
	event_type_map.insert(pair<std::string, int>("Struct", 6));
	event_type_map.insert(pair<std::string, int>("FLOAT32", 7));
	event_type_map.insert(pair<std::string, int>("VisString255", 8));
	event_type_map.insert(pair<std::string, int>("INT32U", 9));
	event_type_map.insert(pair<std::string, int>("Dbpos", 10));
	event_type_map.insert(pair<std::string, int>("INT8U", 11));
	event_type_map.insert(pair<std::string, int>("Check", 12));
	event_type_map.insert(pair<std::string, int>("Octet64", 13));
	event_type_map.insert(pair<std::string, int>("INT32", 14));
}

void decoder::fill_event_desc(std::string code_element, std::vector<xml_node> &nodes, event_info &event)
{
	
	const xml_node * da_type = da_type = get_nodes(code_element, nodes);
	std::map<std::string, std::string>::const_iterator itor = da_type->_attribute_values.find("bType");
	if (itor == da_type->_attribute_values.end())
	{
		throw runtime_error("can not bType in da_map");
	}

	switch (_event_type_map.find(itor->second)->second)
	{
	case 1:
	{
		itor = da_type->_attribute_values.find("type");
		if (itor == da_type->_attribute_values.end())
		{
			throw runtime_error("can not type in da_map");
		}
		nodes = _enumval_map[itor->second]._nodes;
		const xml_node * enum_type = get_nodes(event._value, nodes);
		if (!enum_type)
		{
			throw runtime_error("can not find target message in enum_map");
		}
		event._value_desc = enum_type->_value;
		break;
	}
	case 2:
	{
		int event_value = std::stoi(event._value);
		if (event_value == 1)
		{
			event._value_desc = "True";
		}
		else
		{
			event._value_desc = "False";
		}
		break;
	}
	case 3:
	case 4:
	case 5:
	case 6:
	case 7:
	case 8:
	case 9:
	case 10:
	case 11:
	case 12:
	case 13:
	case 14:
	{
		event._value_desc = event._value;
		break;
	}
	}
}

void decoder::get_da_type(vector<xml_node> &nodes, const event_info &event, std::size_t &code_element_start)
{
	std::string code_element = event._code_components.at(code_element_start);
	const xml_node *da_or_sdo_type = get_nodes(code_element, nodes);
	std::map<std::string, std::string>::const_iterator itor = da_or_sdo_type->_attribute_values.find("type");
	if (itor == da_or_sdo_type->_attribute_values.end())
	{
		throw runtime_error("can not type in do_map");
	}

	nodes = _do_type_map[itor->second]._nodes;
	code_element_start++;
	code_element = event._code_components.at(code_element_start);
	da_or_sdo_type = get_nodes(code_element, nodes);

	if (da_or_sdo_type->_name.compare("DA") == 0)
	{
		return;
	}
	else if (da_or_sdo_type->_name.compare("SDO") == 0)
	{
		get_da_type(nodes, event, code_element_start);
	}
	return;
}

std::string decoder::get_final_type(iec_logical_device &logical_device, const event_info &event, std::vector<xml_node> &nodes)
{	
	std::map<std::string, std::string>::const_iterator itor = _abb_logical_device_point.find(event._code);
	if (itor == _abb_logical_device_point.end())
	{
		pair_key_intype_in_logical_device(event._code, logical_device);
	}

	std::string ln_type = _abb_logical_device_point[event._code];
	if (ln_type.empty())
	{
		throw runtime_error("no match key in cid file");
	}

	nodes = _lnode_map[ln_type]._nodes;
	std::size_t code_element_start = 2;
	std::string code_element = event._code_components.at(code_element_start);
	const xml_node * do_type = get_nodes(code_element, nodes);
	if (!do_type)
	{
		throw runtime_error("can not find do_type in lnode_map");
	}
	if (do_type->_name.compare("DO") != 0)
	{
		throw runtime_error("Wrong format: no DOTYPE element in cid file");
	}

	get_da_type(nodes, event, code_element_start);
	code_element = event._code_components.at(code_element_start);
	const xml_node * da_type = get_nodes(code_element, nodes);
	if (!da_type)
	{
		throw runtime_error("can not find da_type");
	}
	return code_element;
}

void decoder::fill_events(std::vector<event_info> &events)
{
	for (auto &event : events)
	{
		if (event._value.empty())
		{
			throw runtime_error("Wrong format - no Value value");
		}
		if (event._time.empty())
		{
			throw runtime_error("Wrong format - no time value");
		}
		if (event._no.empty())
		{
			throw runtime_error("Wrong format - no No value");
		}
		if (event._clr.empty())
		{
			throw runtime_error("Wrong format - no Crl value");
		}
		for (iec_logical_device &logical_device : _logical_devices)
		{
			if (0 == logical_device.name.compare(event._ldvice_name))
			{
				std::vector<xml_node> nodes;
				std::string code_element = get_final_type(logical_device, event, nodes);
				fill_event_desc(code_element, nodes, event);
				break;
			}
		}
	}
}

void decoder::hookup()
{	
	iec_device& device = static_cast<iec_device&>(_cid_parser.device());
	_logical_devices = device.logical_devices;
	_enumval_map = _cid_parser.get_datatype_templates()._enumtypes;
	_lnode_map = _cid_parser.get_datatype_templates()._lnodetypes;
	_do_type_map = _cid_parser.get_datatype_templates()._dotypes;
	create_type_map(_event_type_map);

	auto &events = _abb_parser.events();
	fill_events(events);
}

void decoder::decode()
{
	split_code_to_components();
	_cid_parser.parse();
	match_delimiter();
	hookup();
}



