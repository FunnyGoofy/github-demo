#ifndef __EVENTS_DEFINITIONS_H__
#define __EVENTS_DEFINITIONS_H__

std::string cid_file_path = "../subnet.ssnet.relay.abb_event_parser.unit_test/abb_relay/conf.xml";
std::ifstream cid_file(cid_file_path);

const char *blank_event_file = "";

const char *no_eventmonitoring_file = "<Events>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>10< / Value>\
<Time>2016.08.25 01:13 : 08.077< / Time>\
<No>3< / No>\
<Clr>N< / Clr>\
< / Event>\
<Event code = \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1< / Value>\
<Time>2016.08.25 01:13 : 11.270< / Time>\
<No>4< / No>\
<Clr>N< / Clr>\
< / Event>\
<Event code = \"LD0.TCSSCBR2.CirAlm.stVal\">\
<Value>1< / Value>\
<Time>2016.08.25 01:13 : 11.270< / Time>\
<No>5< / No>\
<Clr>N< / Clr>\
< / Event>\
</Events>";

const char *no_events_file = "<EventMonitoring>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>10< / Value>\
<Time>2016.08.25 01:13 : 08.077< / Time>\
<No>3< / No>\
<Clr>N< / Clr>\
< / Event>\
<Event code = \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1< / Value>\
<Time>2016.08.25 01:13 : 11.270< / Time>\
<No>4< / No>\
<Clr>N< / Clr>\
< / Event>\
<Event code = \"LD0.TCSSCBR2.CirAlm.stVal\">\
<Value>1< / Value>\
<Time>2016.08.25 01:13 : 11.270< / Time>\
<No>5< / No>\
<Clr>N< / Clr>\
< / Event>\
<EventMonitoring>";

const char *no_event_file = "<EventMonitoring>\
<Events>\
< / Events>\
<EventMonitoring>";

const char *no_code_file = "<EventMonitoring>\
<Events>\
<Event>\
<Value>10</Value>\
<Time>2016.08.25 01:13 : 08.077</Time>\
<No>3</No>\
<Clr>N</Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
< / Events>\
<EventMonitoring>";

const char *code_empty_file = "<EventMonitoring>\
<Events>\
<Event code = \"\">\
<Value>10</Value>\
<Time>2016.08.25 01:13 : 08.077</Time>\
<No>3</No>\
<Clr>N</Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
< / Events>\
<EventMonitoring>";

const char *unidentified_element_event_file = "<EventMonitoring>\
<Events>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value1>10</Value>\
<Time2>2016.08.25 01:13 : 08.077</Time>\
<No3>3</No>\
<Clr4>N</Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
< / Events>\
<EventMonitoring>";


const char *value_element_no_value_event_file = "<EventMonitoring>\
<Events>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value></Value>\
<Time>2016.08.25 01:13 : 08.077</Time>\
<No>3</No>\
<Clr>N</Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
< / Events>\
<EventMonitoring>";

const char *time_element_no_value_event_file = "<EventMonitoring>\
<Events>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>10</Value>\
<Time></Time>\
<No>3</No>\
<Clr>N</Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
< / Events>\
<EventMonitoring>";

const char *no_element_no_value_event_file = "<EventMonitoring>\
<Events>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>10</Value>\
<Time>2016.08.25 01:13 : 08.077</Time>\
<No></No>\
<Clr>N</Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
< / Events>\
<EventMonitoring>";

const char *crl_element_no_value_event_file = "<EventMonitoring>\
<Events>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>10</Value>\
<Time>2016.08.25 01:13 : 08.077</Time>\
<No>3</No>\
<Clr></Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
< / Events>\
<EventMonitoring>";


const char *no_matched_key_in_cid_file = "<EventMonitoring>\
<Events>\
<Event code = \"LD0.LPHD1.PhyHealth100.stVal\">\
<Value>10</Value>\
<Time>2016.08.25 01:13 : 08.077</Time>\
<No>3</No>\
<Clr>N</Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
< / Events>\
<EventMonitoring>";

const char *seven_events_file_stream = "<EventMonitoring>\
<Events>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>10</Value>\
<Time>2016.08.25 01:13 : 08.077</Time>\
<No>3</No>\
<Clr>N</Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR2.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>5</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.DIAGLCCH1.ChLiv.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 32.730</Time>\
<No>6</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"CTRL.LLN0.LocRem.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:16 : 11.782</Time>\
<No>7</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"CTRL.LLN0.LocRem.stVal\">\
<Value>2</Value>\
<Time>2016.08.25 01:16 : 12.782</Time>\
<No>8</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"CTRL.LLN0.LocRem.stVal\">\
<Value>0</Value>\
<Time>2016.08.25 01:16 : 18.432</Time>\
<No>9</No>\
<Clr>N</Clr>\
</Event>\
</Events>\
</EventMonitoring>";

const char *right_7_events_file_stream = "<EventMonitoring>\
<Events>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>10</Value>\
<Time>2016.08.25 01:13 : 08.077</Time>\
<No>3</No>\
<Clr>N</Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR2.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>5</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.DIAGLCCH1.ChLiv.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 32.730</Time>\
<No>6</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"CTRL.LLN0.LocRem.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:16 : 11.782</Time>\
<No>7</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"CTRL.LLN0.LocRem.stVal\">\
<Value>2</Value>\
<Time>2016.08.25 01:16 : 12.782</Time>\
<No>8</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"CTRL.LLN0.LocRem.stVal\">\
<Value>0</Value>\
<Time>2016.08.25 01:16 : 18.432</Time>\
<No>9</No>\
<Clr>N</Clr>\
</Event>\
</Events>\
</EventMonitoring>";

const char *big_twentyfour_events_file_stream = "<EventMonitoring>\
<Events>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>10</Value>\
<Time>2016.08.25 01:13 : 08.077</Time>\
<No>3</No>\
<Clr>N</Clr>\
</Event>\
<Event code= \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>4</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR2.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 11.270</Time>\
<No>5</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.DIAGLCCH1.ChLiv.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:13 : 32.730</Time>\
<No>6</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"CTRL.LLN0.LocRem.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:16 : 11.782</Time>\
<No>7</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"CTRL.LLN0.LocRem.stVal\">\
<Value>2</Value>\
<Time>2016.08.25 01:16 : 12.782</Time>\
<No>8</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"CTRL.LLN0.LocRem.stVal\">\
<Value>0</Value>\
<Time>2016.08.25 01:16 : 18.432</Time>\
<No>9</No>\
<Clr>N</Clr>\
</Event>\
<Event code=\"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>11</Value>\
<Time>2016.08.25 01:21 : 13.905</Time>\
<No>10</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>11</Value>\
<Time>2016.08.25 01:21 : 22.784</Time>\
<No>11</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:21 : 25.966</Time>\
<No>12</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR2.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:21 : 25.966</Time>\
<No>13</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.DIAGLCCH1.ChLiv.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:21 : 43.336</Time>\
<No>14</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>11</Value>\
<Time>2016.08.25 01:22 : 40.827</Time>\
<No>15</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:22 : 44.047</Time>\
<No>16</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR2.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:22 : 44.047</Time>\
<No>17</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.DIAGLCCH1.ChLiv.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:22 : 55.902</Time>\
<No>18</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.LPHD1.PhyHealth1.stVal\">\
<Value>11</Value>\
<Time>2016.08.25 01:25 : 50.276</Time>\
<No>19</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:25 : 53.494</Time>\
<No>20</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR2.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:25 : 53.494</Time>\
<No>21</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.DIAGLCCH1.ChLiv.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:26 : 05.339</Time>\
<No>22</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.GSAL1.AuthAcsD.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:28 : 31.654</Time>\
<No>23</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR1.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:28 : 42.085</Time>\
<No>24</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.TCSSCBR2.CirAlm.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:28 : 42.085</Time>\
<No>25</No>\
<Clr>N</Clr>\
</Event>\
<Event code = \"LD0.DIAGLCCH1.ChLiv.stVal\">\
<Value>1</Value>\
<Time>2016.08.25 01:29 : 04.225</Time>\
<No>26</No>\
<Clr>N</Clr>\
</Event>\
</Events>\
</EventMonitoring>";


#endif // __EVENTS_DEFINITIONS_H__
