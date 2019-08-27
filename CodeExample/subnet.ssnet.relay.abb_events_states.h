#ifndef  __ABB_EVENT_STATES_H__
#define __ABB_EVENT_STATES_H__

#include "subnet\subnet.ssnet.relay.abb_events_parser\subnet.ssnet.relay.abb_events_parser.h"

using namespace osa;
using namespace osa::xml;
using namespace std;

namespace abb_event_parser_ns
{	
	///////////////////////////////////////////////////////////////////////////////
	// event_node state
	class event_node : public event_state
	{
	public:
		event_node(events_content_handler_fsm *fsm, sax_callbacks::element& e);
		virtual ~event_node();

		virtual void SAX2StartElementNs(sax_callbacks::element &e) override;
		virtual void SAX2EndElementNs(sax_callbacks::element &e) override;
		virtual void SAX2Characters(std::string &ch) override;
		void set_code(const std::string &code);
	private:
		enum text_state { VALUE_STATE, TIME_STATE, NO_STATE, CLR_STATE, STATE_UNKNOWN };
		text_state _self_state;
		event_info _event_info;
	};

	///////////////////////////////////////////////////////////////////////////////
	// event state
	class event : public event_state
	{
	public:
		event(events_content_handler_fsm *fsm, sax_callbacks::element &e);
		virtual ~event();

		virtual void SAX2StartElementNs(sax_callbacks::element &e) override;
		virtual void SAX2EndElementNs(sax_callbacks::element &e) override;

	private:
		// Event objects to add to the main list
		std::vector<std::unique_ptr<event_info>> _events;
	};
	
	class events : public event_state
	{
	public:
		events(events_content_handler_fsm* fsm);
		virtual ~events();

		virtual void SAX2StartElementNs(sax_callbacks::element &e) override;
		virtual void SAX2EndElementNs(sax_callbacks::element &e) override;
	};

	class eventmonitoring : public event_state
	{
	public:
		eventmonitoring(events_content_handler_fsm* fsm);
		virtual ~eventmonitoring();

		virtual void SAX2StartElementNs(sax_callbacks::element &e) override;
		virtual void SAX2EndElementNs(sax_callbacks::element &e) override;
	};
} 

#endif //__ABB_EVENT_STATES_H__