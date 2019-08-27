#include "stdafx.h"
#include "CppUnitTest.h"
#include "subnet\subnet.ssnet.relay.abb_events_parser\subnet.ssnet.relay.abb_events_parser.h"
#include "events_definitions.h"
#include <istream>



using namespace Microsoft::VisualStudio::CppUnitTestFramework;
using namespace std;
using namespace abb_event_parser_ns;

namespace subnetssnetrelayabb_event_parser_unit_test
{
	TEST_CLASS(abb_decoder_test)
	{
	public:		
		TEST_METHOD(test_blank_event_file)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(blank_event_file);
			
			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}

		TEST_METHOD(test_no_eventmonitoring_node)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(no_eventmonitoring_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
				int test = 2;
			}
			catch (invalid_argument &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}

		TEST_METHOD(test_no_events_node)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(no_events_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (invalid_argument &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}

		TEST_METHOD(test_no_event_node)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(no_event_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}

		
		TEST_METHOD(test_no_code_event_file)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(no_code_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}

		TEST_METHOD(test_empty_code_event_file)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(code_empty_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}

		TEST_METHOD(test_unidentified_element_in_event_node_event_file)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(unidentified_element_event_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}


		TEST_METHOD(test_value_element_no_value_event_file)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(value_element_no_value_event_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}
		
		TEST_METHOD(test_time_node_no_value_event_file)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(time_element_no_value_event_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}


		TEST_METHOD(test_no_node_no_value_event_file)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(no_element_no_value_event_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}


		TEST_METHOD(test_crl_node_no_value_event_file)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(crl_element_no_value_event_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}
		
		TEST_METHOD(test_no_match_key_found_from_cid_file)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(no_matched_key_in_cid_file);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}

		TEST_METHOD(test_no_target_message_in_cid_file)
		{
			bool no_exception_thrown = true;
			std::stringstream evtss(right_7_events_file_stream);
			std::string cid_file_path = "../subnet.ssnet.relay.abb_event_parser.unit_test/abb_relay/nomatchedinfoconf.xml";
			std::ifstream cid_file(cid_file_path);

			try
			{
				decoder d(evtss, cid_file);
				vector<event_info> &events = d.get_matched_events();
			}
			catch (runtime_error &e)
			{
				const char* message = e.what();
				Logger::WriteMessage(message);
				no_exception_thrown = false;
			}
			Assert::IsFalse(no_exception_thrown);
		}

		TEST_METHOD(test_7_events_size)
		{
			std::stringstream evtss(seven_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			Assert::IsTrue(events.size() == 7);
			Logger::WriteMessage("event_size is verified");
		}

		TEST_METHOD(test_events_ldevice_name)
		{
			std::stringstream evtss(right_7_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			std::string ldvice_name_0 = "A1LD0";
			std::string ldvice_name_4 = "A1CTRL";
			Assert::AreEqual(events.at(0)._ldvice_name, ldvice_name_0);
			Assert::AreEqual(events.at(4)._ldvice_name, ldvice_name_4);
			Logger::WriteMessage("ldevice_name is verified");
		}
		
		TEST_METHOD(test_event_0_desc_enum)
		{
			std::stringstream evtss(right_7_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			event_info event_ref;
			event_ref._value_desc = "Watchdog reset";
			Assert::AreEqual(events.at(0)._value_desc, event_ref._value_desc);

			Logger::WriteMessage("event_desc_enum is verified");
		}

		TEST_METHOD(test_event_1_desc_enum)
		{
			std::stringstream evtss(right_7_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			event_info event_ref;
			event_ref._value_desc = "True";
			Assert::AreEqual(events.at(1)._value_desc, event_ref._value_desc);

			Logger::WriteMessage("event_desc_enum is verified");
		}

		TEST_METHOD(test_event_5_desc_enum)
		{
			std::stringstream evtss(right_7_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			event_info event_ref;
			event_ref._value_desc = "Local";
			Assert::AreEqual(events.at(4)._value_desc, event_ref._value_desc);

			Logger::WriteMessage("event_desc_enum is verified");
		}

		TEST_METHOD(test_event_6_desc_enum)
		{
			std::stringstream evtss(right_7_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			event_info event_ref;
			event_ref._value_desc = "Remote";
			Assert::AreEqual(events.at(5)._value_desc, event_ref._value_desc);

			Logger::WriteMessage("event_desc_enum is verified");
		}

		TEST_METHOD(test_event_7_desc_enum)
		{
			std::stringstream evtss(right_7_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			event_info event_ref;
			event_ref._value_desc = "Off";
			Assert::AreEqual(events.at(6)._value_desc, event_ref._value_desc);

			Logger::WriteMessage("event_desc_enum is verified");
		}

		TEST_METHOD(test_event_8_desc_enum)
		{
			std::stringstream evtss(big_twentyfour_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			event_info event_ref;
			event_ref._value_desc = "Power down det.";
			Assert::AreEqual(events.at(7)._value_desc, event_ref._value_desc);

			Logger::WriteMessage("event_desc_enum is verified");
		}

		TEST_METHOD(test_event_9_desc_enum)
		{
			std::stringstream evtss(big_twentyfour_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			event_info event_ref;
			event_ref._value_desc = "Power down det.";
			Assert::AreEqual(events.at(8)._value_desc, event_ref._value_desc);

			Logger::WriteMessage("event_desc_enum is verified");
		}

		TEST_METHOD(test_event_type_enum)
		{
			std::stringstream evtss(big_twentyfour_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			event_info event_ref;
			event_ref._ldvice_name = "A1LD0";
			event_ref._code = "LPHD1$PhyHealth1$stVal";
			event_ref._value = "10";
			event_ref._time = "2016.08.25 01:13 : 08.077";
			event_ref._no = "3";
			event_ref._clr = "N";
			event_ref._point_name = "";
			event_ref._value_desc = "Watchdog reset";
			Assert::AreEqual(events.at(0)._ldvice_name, event_ref._ldvice_name);
			Assert::AreEqual(events.at(0)._code, event_ref._code);
			Assert::AreEqual(events.at(0)._value, event_ref._value);
			Assert::AreEqual(events.at(0)._time, event_ref._time);
			Assert::AreEqual(events.at(0)._no, event_ref._no);
			Assert::AreEqual(events.at(0)._clr, event_ref._clr);
			Assert::AreEqual(events.at(0)._point_name, event_ref._point_name);
			Assert::AreEqual(events.at(0)._value_desc, event_ref._value_desc);

			Logger::WriteMessage("event_type_enum is verified");
		}

		TEST_METHOD(test_event_type_boolean)
		{
			std::stringstream evtss(big_twentyfour_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			event_info event_ref;
			event_ref._ldvice_name = "A1LD0";
			event_ref._code = "TCSSCBR1$CirAlm$stVal";
			event_ref._value = "1";
			event_ref._time = "2016.08.25 01:13 : 11.270";
			event_ref._no = "4";
			event_ref._clr = "N";
			event_ref._point_name = "";
			event_ref._value_desc = "True";
			Assert::AreEqual(events.at(1)._ldvice_name, event_ref._ldvice_name);
			Assert::AreEqual(events.at(1)._code, event_ref._code);
			Assert::AreEqual(events.at(1)._value, event_ref._value);
			Assert::AreEqual(events.at(1)._time, event_ref._time);
			Assert::AreEqual(events.at(1)._no, event_ref._no);
			Assert::AreEqual(events.at(1)._clr, event_ref._clr);
			Assert::AreEqual(events.at(1)._point_name, event_ref._point_name);
			Assert::AreEqual(events.at(1)._value_desc, event_ref._value_desc);

			Logger::WriteMessage("event_type_boolean is verified");
		}

		TEST_METHOD(test_whole_events_stream)
		{
			std::stringstream evtss(big_twentyfour_events_file_stream);
			decoder d(evtss, cid_file);
			vector<event_info> &events = d.get_matched_events();
			event_info event_ref;
			event_ref._ldvice_name = "A1LD0";
			event_ref._code = "TCSSCBR1$CirAlm$stVal";
			event_ref._value = "1";
			event_ref._time = "2016.08.25 01:13 : 11.270";
			event_ref._no = "4";
			event_ref._clr = "N";
			event_ref._point_name = "";
			event_ref._value_desc = "True";
			Assert::IsTrue(events.size() == 24);
			Assert::AreEqual(events.at(1)._ldvice_name, event_ref._ldvice_name);
			Assert::AreEqual(events.at(1)._code, event_ref._code);
			Assert::AreEqual(events.at(1)._value, event_ref._value);
			Assert::AreEqual(events.at(1)._time, event_ref._time);
			Assert::AreEqual(events.at(1)._no, event_ref._no);
			Assert::AreEqual(events.at(1)._clr, event_ref._clr);
			Assert::AreEqual(events.at(1)._point_name, event_ref._point_name);
			Assert::AreEqual(events.at(1)._value_desc, event_ref._value_desc);

			Logger::WriteMessage("big_24_events_stream is verified");
		}		
	};
}