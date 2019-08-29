#include "subnet\subnet.ssnet.relay.abb_events_parser\subnet.ssnet.relay.abb_events_states.h"
#include <string>

using namespace std;
using namespace abb_event_parser_ns;

///////////////////////////////////////////////////////////////////////////////
// event_node state
event_node::event_node(events_content_handler_fsm *fsm, sax_callbacks::element& e) :
	event_state(fsm), _self_state(STATE_UNKNOWN)
{
	
}

event_node::~event_node()
{

}

void event_node::SAX2StartElementNs(sax_callbacks::element &e)
{
	// Make sure our node is in the global namespace as other namespaces
	// can use the same element name
	if (e.get_element_prefix().length() != 0)
		return;	
	
	if (_stricmp(e.get_element_name().c_str(), "Value") == 0)
	{
		_self_state = VALUE_STATE;
	}
	else if (_stricmp(e.get_element_name().c_str(), "Time") == 0)
	{
		_self_state = TIME_STATE;
	}
	else if (_stricmp(e.get_element_name().c_str(), "No") == 0)
	{
		_self_state = NO_STATE;
	}
	else if (_stricmp(e.get_element_name().c_str(), "Clr") == 0)
	{
		_self_state = CLR_STATE;
	}
	else 
	{
		_self_state = STATE_UNKNOWN;
		throw runtime_error("Wrong format - element can not be identified");
	}
}

void event_node::SAX2EndElementNs(sax_callbacks::element &e)
{
	if (e.get_element_prefix().length() == 0)
	{
		if (e.get_element_name().compare("Event") == 0)
		{
			_fsm->add_event(_event_info);
			_fsm->pop_state();
		}

	}
}

void event_node::SAX2Characters(std::string &str)
{
	if (str.find_last_not_of(" \n\r\t") == string::npos)
		return;

	switch (_self_state)
	{
	case STATE_UNKNOWN:
		return;
	case VALUE_STATE:
		_event_info._value = str;
		return;
	case TIME_STATE:
		_event_info._time = str;
		return;
	case NO_STATE:
		_event_info._no = str;
		return;
	case CLR_STATE:
		_event_info._clr = str;
		return;
	}
}

void event_node::set_code(const std::string &code)
{
	_event_info._code = code;
}


///////////////////////////////////////////////////////////////////////////////
// event
event::event(events_content_handler_fsm *fsm, sax_callbacks::element &e) :
	event_state(fsm)
{
	
}

event::~event()
{

}

void event::SAX2StartElementNs(sax_callbacks::element &e)
{
	// Make sure our node is in the global namespace as 
	// other namespaces can use the same element name
	if (e.get_element_prefix().length() == 0)
	{
		if (e.get_element_name().compare("Event") == 0)
		{
			pair<string, string> code_pair = e.get_attribute_value_pair("code");
			if (!code_pair.first.empty())
			{
				if (!code_pair.second.empty())
				{
					event_node *_node = new event_node(_fsm, e);
					_node->set_code(code_pair.second);
					_fsm->push_state(_node);
				}
				else
				{
					throw runtime_error("Wrong format - code string empty");
				}
			}
			else
			{
				throw runtime_error("Wrong format - no code element");
			}
		}
		else
		{
			throw invalid_argument("The format is wrong  --- no Event");
		}
	}
}


void event::SAX2EndElementNs(sax_callbacks::element &e)
{
	if (e.get_element_prefix().length() == 0 && e.get_element_name().compare("Event") == 0)
	{
		_fsm->pop_state();
	}
}

////////////////////////////////////////////////////////////////////////////////
/// events
events::events(events_content_handler_fsm* fsm) :event_state(fsm)
{

}
events::~events()
{

}

void events::SAX2StartElementNs(sax_callbacks::element &e)
{
	if (e.get_element_prefix().length() != 0)
		return;

	if (e.get_element_name().compare("Events") == 0)
	{
		_fsm->push_state(new event(_fsm, e));
	}
	else
	{
		throw invalid_argument("The format is wrong  --- no Events");
	}
}

void events::SAX2EndElementNs(sax_callbacks::element &e)
{
	if (e.get_element_prefix().length() == 0 && e.get_element_name().compare("Events") == 0)
	{
		_fsm->pop_state();
	}
}


////////////////////////////////////////////////////////////////////////////////
/// eventmonitoring
eventmonitoring::eventmonitoring(events_content_handler_fsm* fsm) :event_state(fsm)
{
}

eventmonitoring::~eventmonitoring() 
{
}

void eventmonitoring::SAX2StartElementNs(sax_callbacks::element &e)
{
	if (e.get_element_prefix().length() != 0)
		return;

	if (e.get_element_name().compare("EventMonitoring") == 0)		
	{
		_fsm->push_state(new events(_fsm));
	}
	else
	{
		throw invalid_argument("The format is wrong --- no EventMonitoring");
	}
}

void eventmonitoring::SAX2EndElementNs(sax_callbacks::element &e)
{
	if (e.get_element_prefix().length() == 0 && e.get_element_name().compare("EventMonitoring") == 0)
	{
		_fsm->pop_state();
	}
}
