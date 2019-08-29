#ifndef __ABB_EVENT_PARSER_H__
#define __ABB_EVENT_PARSER_H__

#ifdef WIN32
#ifdef ABB_EVENTS_PARSER_EXPORTS
#define ABB_EVENT_PARSER_DLL_API __declspec(dllexport)
#else
#define ABB_EVENT_PARSER_DLL_API __declspec(dllimport)
#endif
#else
#define ABB_EVENT_PARSER_DLL_API
#endif

#include <fstream>
#include <istream>
#include <stack>
#include <vector>
#include <string>

#include <subnet/subnet.osa/inc/subnet.osa_portable.h>
#include <subnet/subnet.osa_xml/inc/subnet.osa_xml.h>
#include <subnet/subnet.ssnet.iec61850_cid_objects/inc/subnet.ssnet.iec61850_cid_objects.h>
#include <subnet/subnet.ssnet.iec61850_cid_parser/inc/subnet.ssnet.iec61850_cid_parser.h>


namespace abb_event_parser_ns
{
	///////////////////////////////////////////////////////////////////////////////
	// forward declarations
	class abb_event_parser;
	class events_content_handler_fsm;

	///////////////////////////////////////////////////////////////////////////////
	// event_info
	struct event_info
	{
		event_info() {}
		~event_info() {}
		std::string _ldvice_name;
		std::string _code;
		std::string _value;
		std::string _time;
		std::string _no;
		std::string _clr;
		std::string _point_name; // from .d or web or local HMI
		std::string _value_desc;
		std::vector<std::string> _code_components;
	};	

	///////////////////////////////////////////////////////////////////////////////
	// event_state
	// base state class for fsm
	class event_state
	{
	public:
		event_state(events_content_handler_fsm *fsm);
		virtual ~event_state();

		virtual void SAX2StartElementNs(osa::xml::sax_callbacks::element &e);
		virtual void SAX2EndElementNs(osa::xml::sax_callbacks::element &e);
		virtual void SAX2Characters(std::string &ch);
		virtual void SAX2CDataBlock(std::string &value);

	protected:
		events_content_handler_fsm *_fsm;
	};

	///////////////////////////////////////////////////////////////////////////////
	// events_content_handler_fsm
	// sax callback handler and finite state machine
	class events_content_handler_fsm : public osa::xml::sax_callbacks
	{
	public:
		events_content_handler_fsm(std::istream &is, abb_event_parser* parser);

		virtual void SAX2StartElementNs(osa::xml::sax_callbacks::element &e) override;
		virtual void SAX2EndElementNs(osa::xml::sax_callbacks::element &e) override;
		virtual void SAX2Characters(std::string &ch) override;
		virtual void SAX2CDataBlock(std::string &value) override;

		void push_state(event_state *next_state);
		void pop_state();

		std::vector<event_info>& events() { return _events; }
		
		void add_event(event_info &ev);
		abb_event_parser* _parser;

	private:
		std::vector<event_info> _events;
		std::stack<std::unique_ptr<event_state>> _state_stack;
		events_content_handler_fsm(const events_content_handler_fsm&) {}
		events_content_handler_fsm& operator=(const events_content_handler_fsm&) { return *this; }
	};


	///////////////////////////////////////////////////////////////////////////////
	// abb_event_parser
	class  abb_event_parser
	{
	public:
		abb_event_parser(std::istream &is);		
		std::vector<event_info>& events() { return _echf.events(); }
		
	private:
		events_content_handler_fsm _echf;
		osa::xml::sax_reader	_reader;
	};

	class non_copyable
	{
	public:
		non_copyable() {}
	private:
		non_copyable(const non_copyable&) {}
		non_copyable& operator=(const non_copyable &) {}
	};

	//This information can be stored in a decoded event data structure 
	//that contains the following:
	// - the original event info
	// - the human readable point name
	// - the human readable value representation.
	class ABB_EVENT_PARSER_DLL_API decoder : public non_copyable
	{
	public:
		decoder(std::istream &event_file_stream, std::istream &cid_file_stream);
		std::vector<event_info>& get_matched_events();
		~decoder() { clear_containers(); }

	private:
		std::map<std::string, std::string> _abb_logical_device_point;
		std::vector<event_info> _decode_nodes;
		abb_event_parser _abb_parser;
		iec61850_cid_objects_ns::safe_task_feedback _stfb;
		iec61850_cid_parser_ns::iec61850_cid_parser _cid_parser;
		std::vector<event_info> _matched_events;
		std::vector<iec61850_cid_objects_ns::iec_logical_device> _logical_devices;
		std::map<std::string, iec61850_cid_objects_ns::xml_node> _lnode_map;
		std::map<std::string, iec61850_cid_objects_ns::xml_node> _do_type_map;
		std::map<std::string, iec61850_cid_objects_ns::xml_node> _enumval_map;
		std::map<std::string, int> _event_type_map;

	private:
		void clear_containers();
		char get_delimiter(const std::string &code) const;
		void split_code_to_components();
		void match_delimiter();
		void remove_function_code_from_cid_key(std::string &key, char &cid_token) const;
		void pair_key_intype_in_logical_device(const std::string event_code, iec61850_cid_objects_ns::iec_logical_device &logical_device);
		iec61850_cid_objects_ns::xml_node* get_nodes(const std::string &node_key, std::vector<iec61850_cid_objects_ns::xml_node> &nodes) const;
		void get_da_type(vector<iec61850_cid_objects_ns::xml_node> &nodes, const event_info &event, std::size_t &code_element_start);
		void create_type_map(std::map<std::string, int> &event_type_map);
		void fill_events(std::vector<event_info>& events);
		void fill_event_desc(std::string code_element, std::vector<iec61850_cid_objects_ns::xml_node> &nodes, event_info &event);
		std::string get_final_type(iec61850_cid_objects_ns::iec_logical_device &logical_device, const event_info &event, std::vector<iec61850_cid_objects_ns::xml_node> &nodes);
		void hookup();
		void decode();
	};
}

#endif // __ABB_EVENT_PARSER_H__