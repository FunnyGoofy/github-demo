from bokeh.models  import CategoricalTicker
from bokeh.core.properties import Int
from bokeh.models import FactorRange, Spacer, Legend
from bokeh.embed import components
from bokeh.plotting import figure, curdoc
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import pandas as pd
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models import ColumnDataSource, TapTool, VBar, Rect
from bokeh.models.widgets import PreText, Select, CheckboxGroup
from bokeh.models.widgets import Panel, Tabs  
from bokeh.io.state import curstate
from bokeh.resources import Resources
from bokeh.themes import Theme
from bokeh import  events
from bokeh.events import Event, Tap
from bokeh.models.widgets import Div
from pandas import DataFrame
from bokeh.core.properties import value
from bokeh.layouts import layout
from bokeh.plotting import figure
from bokeh.models import HoverTool, Range1d
from numpy import pi
from operator import add
from bokeh.models import Arrow, NormalHead, VeeHead, Text
from bokeh.models.callbacks import CustomJS
from bokeh.models.glyphs import Text, Line
from itertools import chain
import pypyodbc
from threading import Thread
import queue
import threading
from DataVisualizationWebApp import drillingconn_wellsect_plot
from DataVisualizationWebApp import b2s_s2b_plot
from DataVisualizationWebApp import all_main_plot
from DataVisualizationWebApp import sub_novos_plot
from tornado import gen
from bokeh.models import TickFormatter
from DataVisualizationWebApp import import_data
from bokeh.models import LabelSet, Label
import timeit
from DataVisualizationWebApp import driller_hybrid_novos_vs_plot
from DataVisualizationWebApp import novos_config
import math
import copy
import numpy as np
from bokeh.document import without_document_lock
from functools import  partial

screen_width = None
plot_width = 1400
version = None
width_coefficient = 0.90
rig_id_str = "rig_id"
job_id_str = 'job_id'
crew_shift_str = 'crew_shift'
well_selection_str = "well_section"
connection_type_str = "connection_type"
connection_phase_str = "connection_phase"
type_str = "type"
status_str = "status"
hole_depth_str = 'hole_depth'
pre_slip_time_str = 'pre_slip_time'
post_slip_time_str = "post_slip_time"
survey_time_str = "survey_time"
backream_time_str = "backream_time"
frictiontest_time_str = "frictiontest_time"
slip_to_slip_str = "slip_to_slip"
depth_ft_str = "depth_ft"
edr_depth_ft = 'edr_depth_ft'
selected_rig = ''
selected_job  = ''
sizing_mode = 'scale_width'
visualization_depth_str = "visualization_depth"
rigs_combx = None
jobs_combx = None

all_connection_dict = {}
all_connection_table = None
novos_connection_table = None
rigs_list = []
jobs_list = []
crewshift_list = []
novos_source = None 
main_plot = None
mainplot_source = None
well_connnection_source = None
db_records_rig_queue = None
db_records_rig_event = None
update_drillingconn_wellsect_queue = None
update_drillingconn_wellsect_event = None
update_drillingconn_wellsect_thread = None
drillingconn_wellsect_condition = None    
update_b2s_s2b_queue = None 
update_b2s_s2b_event = None
update_main_plot_queue = None
update_main_plot_event = None
mainplot_data_all_reference = None
checkbox_group_1_selections = None 
checkbox_group_2_selections = None 
checkbox_group_3_selections = None 
all_connection_dict = None 
well_connection_textbox_source = None
default_rig_number = ''
rigs_list = []
default_job_number = ''
jobs_list = []
main_layout = None
checkbox_group_1 = None
checkbox_group_2 = None
checkbox_group_3 = None
m_color_white = "white"
sub_plot = None
b2s_datasource = None
update_b2s_s2b_queue = None
update_b2s_s2b_event = None
s2b_datasource = None
update_drillingconn_wellsect_queue  = None
update_drillingconn_wellsect_event  = None
well_connection_textbox_source      = None
m_well_selection = None
m_well_connection = None
m_well_conn_phase = None
spacer_1 = None
spacer_2 = None
spacer_3 = None
spacer_4 = None
menu_column_1_layout = None
well_selection_layout = None
well_connection_layout = None
well_conn_phase_layout = None
menu_column_2_layout = None
menu_middle_layout = None
menu_top_layout = None
menu_bottom_layout = None
menu_layout = None
sidebar_layout = None
main_row = None
hide_subplot_callback = None
subplot_colors_length = 15
tapcallback = None
ticker_cb_reset = None
ticker_cb = None
main_plot_dict = {}
depth_ref_list = []
driller_vs_plot = None
driller_vs_plot_source = None
hybrid_vs_plot = None
hybrid_vs_plot_source = None
novos_vs_plot = None
novos_vs_plot_source = None
driller_vs_dataset = None
color_list = ["#01B8AA", "#000000", "#FD625E", "#F2C80F", "#A66999", "#6fff00"]
connection_phase_list = ["B2S", "S2S", "S2B", "Survey", "BackReam", "FrictionTest"]
update_driller_hybrid_novos_vs_queue = None
update_driller_hybrid_novos_vs_event = None
driller_hybrid_novos_vs_plot_dict = None
driller_vs_plot_dict = None
hybrid_vs_plot_dict = None
novos_vs_plot_dict = None 
x_range = ['1', '2', '3', '4', '5']
tabs = None
database_que = None
get_all_data_queue = None 
get_all_data_event = None 
get_all_data_thread = None
novos_config_variables = ['HoistBlockSpeedOffBottomTarget', 'HoistBlockSpeedSlowTarget', 'HoistElevatorDestinationOpenSlipsOffset',\
                          'LowerElevationDestinationCloseSlipsOffset', 'MpCirculateMaxSlope', 'MpStandpipePressureMaxSlope',\
                          'TagBottomAutoDrillEngageHeight', 'TagBottomBlockSpeedTarget', 'TagBottomRopTarget', \
                          'TdRotateMaxAcceleration', 'UnweightBitWobPercentage', 'ReamCycles', \
                          'FrictionTestEnable']

novos_config_legends = ['HBS', 'HBSS', 'HED',\
                          'Low', 'MpC', 'MpS',\
                          'TBA', 'TBB', 'TBR', \
                          'TdR', 'Unw', 'Rea', \
                          'Fic']

novos_config_plot = None
hBar_color_list = ["#01B8AA", "#374649", "#FD625E", "#F2C80F", \
                   "#5F6B6D", "#8AD4EB", "#FE9666", "#A66999", \
                   "#3599B8", "#DFBFBF", "#4AC5BB", "#5F6B6D", \
                   "#F2C80F"]
novos_config_row = None
novos_config_table = pd.DataFrame()
novos_config_dict = None
novos_value_list = ["N/A", "N/A", "N/A", "N/A",\
                    "N/A", "N/A", "N/A", "N/A",\
                    "N/A", "N/A", "N/A", "N/A", \
                    "N/A"]
novos_unit_list = ["ft/min", "ft/min","ft","ft",\
                   "GPM_us/s","psi/s","ft","ft/min",\
                   "ft/h","rpm/s", "None", "None", \
                   "None"]
novos_counts = [0, 0, 0, 0, \
                0, 0, 0, 0, \
                0, 0, 0, 0, \
                0]
novos_config_hole_depth_ft_list = ["N/A", "N/A", "N/A", "N/A",\
                                   "N/A", "N/A", "N/A", "N/A", \
                                   "N/A", "N/A", "N/A", "N/A", \
                                   "N/A"]
novos_config_source = None
novos_config_value_and_units_source = None
inverted_triangle_source = None
novos_config_inverted_triangle_plot = None
b2s_connection_phase = ['OffBottom', 'UnWeightBit', 'ClearBit', 'CleanHole', 'SetBoxHeight', 'SetWeight']
s2b_connection_phase = ['AddStand', 'TakeWeight', 'FlowSetpoint', 'RotateDrill', 'TagBottom']
HoistBlockSpeedOffBottomTargetSource = None
HoistBlockSpeedSlowTargetSource = None
HoistElevatorDestinationOpenSlipsOffsetSource = None
LowerElevationDestinationCloseSlipsOffsetSource = None
MpCirculateMaxSlopeSource = None
MpStandpipePressureMaxSlopeSource = None
TagBottomAutoDrillEngageHeightSource = None
TagBottomBlockSpeedTargetSource = None
TagBottomRopTargetSource = None
TdRotateMaxAccelerationSource = None
UnweightBitWobPercentageSource = None
ReamCyclesSource = None
FrictionTestEnableSource = None
all_novosconfig_circle_source = []
latest_x_range_display = []
latest_x_range_ft = []

sub_plot_textbox_source = None
sub_plot_textbox = None
sub_plot_textbox_text = None #leave them empty strings
sub_plot_queue = None
sub_plot_event = None
sub_plot_thread = None
sub_plot_rects_source = None
novosconfig_queue = None
novosconfig_event = None
novosconfig_thread = None
conn_type_comp_txtbx_offset = 200
main_plot_textbox_source = None
main_textbox = None
plot_textbox_text = ['Counts', '', 'Average (min)', '', 'Median (min)', '', 'Best (min)', ''] #leave them empty strings
main_plot_row = None
main_textbox_plot = None
driller_vs_textbox_source = None
hybrid_vs_textbox_source = None
novos_vs_textbox_source = None
vs_ckbx_textbox_source = None
plot_ckbx_textbox_text = ['', 'W2W']
connection = None
main_plot_ckbx_txtbx_source = None
all_connection_max_holedepth = -1
ALL_CONNECTION_PHASE = 6

rig_lookup_by_country_dict = {'7' : 'USA', 
                              '45 '  : 'USA',
                              '49 '  : 'USA',
                              '50 '  : 'USA',
                              '86 '  : 'USA',
                              '96 '  : 'USA',
                              '97 '  : 'USA',
                              '99 '  : 'USA',
                              '101'  : 'USA',
                              '102'  : 'Canada',
                              '103'  : 'USA',
                              '104'  : 'USA',
                              '105'  : 'USA',
                              '106'  : 'Canada',
                              '107'  : 'USA',
                              '108'  : 'USA',
                              '109'  : 'USA',
                              '110'  : 'USA',
                              '116'  : 'Canada',
                              '117'  : 'Canada',
                              '118'  : 'Canada',
                              '120'  : 'Canada',
                              '130'  : 'Canada',
                              '131'  : 'Canada',
                              '132'  : 'Canada',
                              '133'  : 'Canada',
                              '135'  : 'Canada',
                              '137'  : 'Canada',
                              '140'  : 'Canada',
                              '141'  : 'Canada',
                              '144'  : 'Canada',
                              '145'  : 'Canada',
                              '146'  : 'Canada',
                              '147'  : 'Canada',
                              '148'  : 'Canada',
                              '149'  : 'Canada',
                              '150'  : 'Canada',
                              '151'  : 'Canada',
                              '152'  : 'Canada',
                              '153'  : 'Canada',
                              '154'  : 'Canada',
                              '155'  : 'Canada',
                              '156'  : 'Canada',
                              '157'  : 'Canada',
                              '158'  : 'USA',
                              '159'  : 'Canada',
                              '171'  : 'Canada',
                              '180'  : 'Canada',
                              '181'  : 'USA',
                              '182'  : 'Canada',
                              '183'  : 'Canada',
                              '184'  : 'Canada',
                              '185'  : 'Canada',
                              '186'  : 'Canada',
                              '187'  : 'Canada',
                              '188'  : 'Canada',
                              '189'  : 'Canada',
                              '190'  : 'Canada',
                              '191'  : 'Canada',
                              '192'  : 'Canada',
                              '193'  : 'Canada',
                              '194'  : 'USA',
                              '195'  : 'Canada',
                              '196'  : 'Canada',
                              '197'  : 'Canada',
                              '198'  : 'Canada',
                              '199'  : 'Canada',
                              '204'  : 'Canada',
                              '205'  : 'Canada',
                              '207'  : 'USA',
                              '209'  : 'USA',
                              '212'  : 'Canada',
                              '220'  : 'Canada',
                              '225'  : 'Canada',
                              '226'  : 'Canada',
                              '228'  : 'USA',
                              '229'  : 'Canada',
                              '231'  : 'Canada',
                              '236'  : 'Canada',
                              '237'  : 'Canada',
                              '238'  : 'Canada',
                              '239'  : 'Canada',
                              '241'  : 'Canada',
                              '254'  : 'Canada',
                              '255'  : 'Canada',
                              '256'  : 'Canada',
                              '275'  : 'Canada',
                              '285'  : 'Canada',
                              '288'  : 'Canada',
                              '290'  : 'Canada',
                              '292'  : 'Canada',
                              '293'  : 'Canada',
                              '294'  : 'Canada',
                              '295'  : 'Canada',
                              '296'  : 'Canada',
                              '297'  : 'Canada',
                              '298'  : 'Canada',
                              '299'  : 'Canada',
                              '300'  : 'Canada',
                              '309'  : 'Canada',
                              '312'  : 'USA',
                              '322'  : 'Canada',
                              '324'  : 'Canada',
                              '327'  : 'Canada',
                              '330'  : 'Canada',
                              '340'  : 'Canada',
                              '377'  : 'Canada',
                              '379'  : 'Canada',
                              '382'  : 'Canada',
                              '391'  : 'Canada',
                              '393'  : 'Canada',
                              '395'  : 'Canada',
                              '399'  : 'Canada',
                              '403'  : 'Canada',
                              '404'  : 'USA',
                              '405'  : 'USA',
                              '406'  : 'USA',
                              '407'  : 'Canada',
                              '428'  : 'Canada',
                              '430'  : 'Canada',
                              '460'  : 'USA',
                              '461'  : 'USA',
                              '462'  : 'USA',
                              '463'  : 'Canada',
                              '465'  : 'Canada',
                              '501'  : 'Canada',
                              '509'  : 'Canada',
                              '512'  : 'Canada',
                              '515'  : 'USA',
                              '516'  : 'Canada',
                              '519'  : 'Canada',
                              '520'  : 'Canada',
                              '521'  : 'Canada',
                              '522'  : 'USA',
                              '523'  : 'USA',
                              '524'  : 'Canada',
                              '525'  : 'USA',
                              '526'  : 'Canada',
                              '527'  : 'Canada',
                              '528'  : 'USA',
                              '529'  : 'Canada',
                              '530'  : 'Canada',
                              '531'  : 'Canada',
                              '532'  : 'USA',
                              '533'  : 'Canada',
                              '534'  : 'Canada',
                              '535'  : 'Canada',
                              '536'  : 'USA',
                              '537'  : 'USA',
                              '538'  : 'Canada',
                              '539'  : 'USA',
                              '540'  : 'Canada',
                              '541'  : 'Canada',
                              '542'  : 'Canada',
                              '543'  : 'Canada',
                              '544'  : 'Canada',
                              '545'  : 'Canada',
                              '546'  : 'Canada',
                              '547'  : 'Canada',
                              '548'  : 'USA',
                              '549'  : 'USA',
                              '550'  : 'USA',
                              '551'  : 'USA',
                              '552'  : 'USA',
                              '553'  : 'USA',
                              '554'  : 'USA',
                              '555'  : 'USA',
                              '556'  : 'USA',
                              '557'  : 'USA',
                              '559'  : 'USA',
                              '560'  : 'USA',
                              '561'  : 'USA',
                              '562'  : 'USA',
                              '563'  : 'USA',
                              '564'  : 'USA',
                              '565'  : 'USA',
                              '566'  : 'USA',
                              '567'  : 'USA',
                              '568'  : 'USA',
                              '569'  : 'USA',
                              '570'  : 'Canada',
                              '571'  : 'Canada',
                              '572'  : 'USA',
                              '573'  : 'Canada',
                              '574'  : 'Canada',
                              '575'  : 'USA',
                              '576'  : 'USA',
                              '577'  : 'USA',
                              '578'  : 'USA',
                              '579'  : 'USA',
                              '580'  : 'USA',
                              '581'  : 'USA',
                              '582'  : 'USA',
                              '584'  : 'USA',
                              '590'  : 'USA',
                              '591'  : 'USA',
                              '592'  : 'USA',
                              '593'  : 'USA',
                              '594'  : 'USA',
                              '595'  : 'USA',
                              '596'  : 'USA',
                              '597'  : 'USA',
                              '598'  : 'USA',
                              '599'  : 'USA',
                              '600'  : 'USA',
                              '601'  : 'USA',
                              '607'  : 'USA',
                              '608'  : 'USA',
                              '612'  : 'USA',
                              '613'  : 'USA',
                              '615'  : 'Canada',
                              '621'  : 'Canada',
                              '622'  : 'Canada',
                              '623'  : 'Canada',
                              '630'  : 'Canada',
                              '632'  : 'Canada',
                              '639'  : 'Canada',
                              '750'  : 'USA',
                              '754'  : 'USA',
                              '820'  : 'USA',
                              '821'  : 'USA',
                              '822'  : 'USA',
                              '823'  : 'USA',
                              '824'  : 'USA',
                              '825'  : 'USA',
                              '826'  : 'USA',
                              '827'  : 'USA',
                              '829'  : 'USA',
                              '840'  : 'USA',
                              '867'  : 'Canada'
    }                               

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a




def customize_ticker():
    JS_CODE = """
        import {CategoricalTicker} from "models/tickers/categorical_ticker"
        import * as p from "core/properties"

        export class MyTicker extends CategoricalTicker
            type: "MyTicker"
        
            @define {
            nth: [ p.Int, 1 ]
            }
        
            get_ticks: (start, end, range, cross_loc) ->
                ticks = super(start, end, range, cross_loc)
                ticks.major = ticks.major.filter((element, index) => index % this.nth == 0)
                return ticks
        """

    class MyTicker(CategoricalTicker):
        __implementation__ = JS_CODE
        nth = Int(default=1)

    mTicker = MyTicker(nth = 5)
    return mTicker 

def get_default_value(all_connection_table, comboBx, selectedRig = '', selectedJob = ''):
    global rig_id_str
    global job_id_str
    global crew_shift_str

    default_number = ''
    comboBx_list = []
    if comboBx == 'Rigs':
        comboBx_list = all_connection_table[rig_id_str].unique().tolist()
    elif comboBx == 'Jobs':
        target = []
        selectedRig = int(selectedRig)
        target.append(selectedRig)
        target.append('')
        rigs_query = "{} in @target".format(rig_id_str)
        selected_rig_table = all_connection_table.query(rigs_query)
        comboBx_list = selected_rig_table[job_id_str].unique().tolist()
    elif comboBx == 'CrewShift':
        #TODO need to test
        rigs_query = "{} in @selectedRig".format(rig_id_str)
        selected_rig_table = all_connection_table.query(rigs_query)
        jobs_query = "{} in @selectedJob".format(job_id_str)
        selected_job_table = selected_rig_table.query(jobs_query)

        comboBx_list = selected_job_table[crew_shift_str].unique().tolist()
        comboBx_list.insert(0, ' ')

    # maybe need logic to handle no records in table. it is 0
    if len(comboBx_list) >= 1:
        default_number = comboBx_list[0]

    return default_number, comboBx_list

def get_data(all_connection_dict, rig = -1, job = -1):
    global hole_depth_str
    global pre_slip_time_str 
    global post_slip_time_str
    global survey_time_str
    global backream_time_str 
    global frictiontest_time_str 
    global slip_to_slip_str
    global visualization_depth_str

    all_connection_table = {}
    all_connection_table = pd.DataFrame.from_dict(all_connection_dict)
        
    depth_ref_list = []
    depth_list = []
    b2s_list = []
    s2s_list = []
    s2b_list = []
    survey_list = []
    ream_list = []
    frictiontest_list = []

    b2s_s2s_list = []
    b2s_s2s_s2b_list = []
    b2s_s2s_s2b_survey_list = []
    b2s_s2s_s2b__survey_ream_list = []
    b2s_s2s_s2b__survey_ream_frictiontest_list = []

    if(( rig == -1) or (job == -1)):
        depth_ref_list = list(map(float, all_connection_table[hole_depth_str]))
        depth_ref_list.sort(key=float)
        depth_list = list(map(float, all_connection_table[visualization_depth_str]))
        depth_list.sort(key=float)
        b2s_list = list(map(float, all_connection_table[pre_slip_time_str]))
        s2s_list = list(map(float, all_connection_table[slip_to_slip_str]))
        s2b_list = list(map(float, all_connection_table[post_slip_time_str]))
        survey_list = list(map(float, all_connection_table[survey_time_str]))
        ream_list = list(map(float, all_connection_table[backream_time_str]))
        frictiontest_list = list(map(float, all_connection_table[frictiontest_time_str]))

    else:
        global rig_id_str
        global job_id_str
            
        rig_target = []
        rig_target.append(int(rig))
        rig_target.append('')
        rigs_query = "{} in @rig_target".format(rig_id_str)
        selected_rig_table = all_connection_table.query(rigs_query)

        job_target = []
        job_target.append(int(job))
        job_target.append('')
        jobs_query = "{} in @job_target".format(job_id_str)
        selected_job_table = selected_rig_table.query(jobs_query)

        depth_ref_list = list(map(float, selected_job_table[hole_depth_str]))
        depth_ref_list.sort(key=float)
        depth_list = list(map(float, selected_job_table[visualization_depth_str]))
        depth_list.sort(key=float)
        b2s_list = list(map(float, selected_job_table[pre_slip_time_str]))
        s2s_list = list(map(float, selected_job_table[slip_to_slip_str]))
        s2b_list = list(map(float, selected_job_table[post_slip_time_str]))
        survey_list = list(map(float, all_connection_table[survey_time_str]))
        ream_list = list(map(float, all_connection_table[backream_time_str]))
        frictiontest_list = list(map(float, all_connection_table[frictiontest_time_str]))

    b2s_s2s_list = list(map(add, b2s_list, s2s_list))
    b2s_s2s_s2b_list = list(map(add, b2s_s2s_list, s2b_list))
    b2s_s2s_s2b_survey_list = list(map(add, b2s_s2s_s2b_list, survey_list))
    b2s_s2s_s2b__survey_ream_list = list(map(add, b2s_s2s_s2b_survey_list, ream_list))
    b2s_s2s_s2b__survey_ream_frictiontest_list = list(map(add, b2s_s2s_s2b__survey_ream_list, frictiontest_list))
        
    # could be a function
    rig_job_dict = {}
    rig_job_dict['VBarTop'] = []
    rig_job_dict['VBarBottom'] = []
    rig_job_dict['VBarColors'] = []
    rig_job_dict['VBarType'] = []
    rig_job_dict['HoleDepthRef'] = depth_ref_list + depth_ref_list \
                                 + depth_ref_list + depth_ref_list \
                                 + depth_ref_list  + depth_ref_list
    rig_job_dict['HoleDepth'] = depth_list + depth_list \
                              + depth_list + depth_list \
                              + depth_list  + depth_list

    rig_job_dict['VBarTop'] = b2s_list \
                            + b2s_s2s_list \
                            + b2s_s2s_s2b_list \
                            + b2s_s2s_s2b_survey_list \
                            + b2s_s2s_s2b__survey_ream_list \
                            + b2s_s2s_s2b__survey_ream_frictiontest_list
    rig_job_dict['VBarBottom'] = [ 0 for item in b2s_list] \
                               + b2s_list \
                               + b2s_s2s_list \
                               + b2s_s2s_s2b_list \
                               + b2s_s2s_s2b_survey_list \
                               + b2s_s2s_s2b__survey_ream_list
    rig_job_dict['VBarColors'] = [ "#01B8AA" for item in b2s_list] \
                            +  [ "#000000" for item in b2s_s2s_list] \
                            +  [ "#FD625E" for item in b2s_s2s_s2b_list] \
                            +  [ "#F2C80F" for item in b2s_s2s_s2b_survey_list] \
                            +  [ "#A66999" for item in b2s_s2s_s2b__survey_ream_list] \
                            +  [ "#6fff00" for item in b2s_s2s_s2b__survey_ream_frictiontest_list]

    rig_job_dict['VBarType'] =  ['B2S' for item in b2s_s2s_s2b_list] \
                            + ['S2S' for item in b2s_s2s_s2b_list] \
                            + ['S2B' for item in b2s_s2s_s2b_list] \
                            + ['Survey' for item in b2s_s2s_s2b_list] \
                            + ['BackReam' for item in b2s_s2s_s2b_list] \
                            + ['FrictionTest' for item in frictiontest_list] 

        
    return rig_job_dict, depth_list 

def update(all_connection_dict, rig = -1, job = -1, selected = None):
    rig_job_dict = {}
    depth_list = []
    if selected != None:
        rig_job_dict, depth_list = get_data(all_connection_dict)
    else:
        rig_job_dict, depth_list = get_data(all_connection_dict, rig, job)
    return rig_job_dict, depth_list

def update_combBx_values(val, lst, columnName = ''):
    global selected_rig
    global rig_id_str
    global job_id_str
    global all_connection_table
    global jobs_list
    global crewShift_list

    if val == '':
        return [x for x in lst]
    else:
        target = []
        target.append(int(val))
        target.append('')
        if columnName == 'JobNumber':
            selected_rig = int(val)
            rigs_query = "{} in @target".format(rig_id_str)
            selected_rig_table = all_connection_table.query(rigs_query)
            jobs_list = selected_rig_table[job_id_str].unique().tolist()
            return jobs_list
        elif columnName == 'CrewShift':
            selected_rig = str(selected_rig)
            rigs_query = "{} in @selected_rig".format(rig_id_str)
            selected_rig_table = all_connection_table.query(rigs_query)
            jobs_query = "{} in @target".format(job_id_str)
            selected_job_table = selected_rig_table.query(jobs_query)
            crewShift_list = selected_job_table[crew_shift_str].unique().tolist()
            return crewShift_list
    
@gen.coroutine
def update_1st_chart(selected_rig, selected_job):
    global update_drillingconn_wellsect_queue
    global update_drillingconn_wellsect_event
    global all_connection_dict
    global well_connnection_source
    global well_connection_textbox_source

    update_drillingconn_wellsect_queue.put(drillingconn_wellsect_plot.update_well_selection_data(update_drillingconn_wellsect_event, all_connection_dict, selected_rig, selected_job))
    update_drillingconn_wellsect_event.wait()
    well_connection_colors, x, well_connnection_counts, well_connnection_data = update_drillingconn_wellsect_queue.get()
    well_connnection_source.data = dict(colors = well_connection_colors, \
                                        x = x, \
                                        counts = well_connnection_counts)

    well_connection_textbox_source.data = dict(x = [600,], \
                                                y = [250,], \
                                                txt = [('Total Connections: %d' % sum(well_connnection_counts)),] )

@gen.coroutine
def update_2nd_chart(selected_rig, selected_job):
    global update_b2s_s2b_queue 
    global update_b2s_s2b_event 
    global novos_connection_table
    global b2s_datasource
    global s2b_datasource

    update_b2s_s2b_queue.put(b2s_s2b_plot.update_b2s_s2b_data(update_b2s_s2b_event, \
                                                              novos_connection_table, \
                                                              selected_rig, selected_job))
    update_b2s_s2b_event.wait()
    b2s_canceled_list, b2s_completed_list, \
    b2s_exception_list,b2s_failed_list, \
    s2b_canceled_list, s2b_completed_list, \
    s2b_exception_list, s2b_failed_list = update_b2s_s2b_queue.get()

    b2s_datasource.data = dict(Canceled = b2s_canceled_list, \
                                Completed = b2s_completed_list, \
                                Exception = b2s_exception_list, \
                                Failed = b2s_failed_list)

    s2b_datasource.data = dict(Canceled = s2b_canceled_list, \
                                Completed = s2b_completed_list, \
                                Exception = s2b_exception_list, \
                                Failed = s2b_failed_list)

@gen.coroutine
def update_main_plot(selected_rig, \
                selected_job, \
                from_comboBx_group, \
                checkbox_group_1_selections = [],\
                checkbox_group_2_selections = [], \
                checkbox_group_3_selections = []):
    global update_main_plot_event
    global mainplot_source 
    global main_plot 
    global all_connection_table
    global update_main_plot_queue
    global novos_config_table
   
    doc = curdoc()
    update_main_plot_queue.put(all_main_plot.update_main_plot_chart(doc, \
                                            update_main_plot_event, \
                                            mainplot_source, \
                                            main_plot, \
                                            checkbox_group_1_selections, \
                                            checkbox_group_2_selections,\
                                            checkbox_group_3_selections, \
                                            all_connection_table,\
                                            selected_rig, \
                                            selected_job, \
                                            from_comboBx_group, \
                                            novos_config_table))
    update_main_plot_event.set()

def update_driller_hybrid_novos_vs_plot(selected_rig, \
                                        selected_job, \
                                        from_comboBx_group, \
                                        checkbox_group_1_selections = [],\
                                        checkbox_group_2_selections = [], \
                                        checkbox_group_3_selections = []):
    global update_driller_hybrid_novos_vs_event
    global update_driller_hybrid_novos_vs_queue
    global driller_vs_plot
    global driller_vs_plot_source
    global hybrid_vs_plot
    global hybrid_vs_plot_source
    global novos_vs_plot
    global novos_vs_plot_source

    doc = curdoc()
    update_driller_hybrid_novos_vs_queue.put(driller_hybrid_novos_vs_plot.\
                                             update_driller_hybrid_novos_vs_charts(doc,\
                                                                                 update_driller_hybrid_novos_vs_event, \
                                                                                 driller_vs_plot, \
                                                                                 driller_vs_plot_source, \
                                                                                 hybrid_vs_plot, \
                                                                                 hybrid_vs_plot_source, \
                                                                                 novos_vs_plot, \
                                                                                 novos_vs_plot_source, \
                                                                                 checkbox_group_1_selections, \
                                                                                 checkbox_group_2_selections,\
                                                                                 checkbox_group_3_selections, \
                                                                                 all_connection_dict,\
                                                                                 selected_rig, \
                                                                                 selected_job, \
                                                                                 from_comboBx_group))
    update_driller_hybrid_novos_vs_event.set()  


def update_novosconfig_lists(merged_list, \
                             unique_novosconfig_holedepth_ft_list, \
                             novos_config_table, \
                             variable, \
                             selected_rig, \
                             selected_job = -1):
    change_list = [0 for item in merged_list]
    value_list = copy.deepcopy(change_list)
    size_list = copy.deepcopy(change_list)

    if novos_config_table.empty:
        return change_list, value_list, size_list  
    else:   
        target_table_1 = None
        if selected_job == -1:
            target_table_1 = novos_config_table  
        else:
            target_table_1 = novos_config_table[novos_config_table['job_id'] == int(selected_job)]
        
        if target_table_1.empty:
            return change_list, value_list, size_list  

        target_table_2 = target_table_1[target_table_1['variable'] == str(variable)]
        if target_table_2.empty:
            return change_list, value_list, size_list  

        target_table_3 = target_table_2[pd.notnull(target_table_2['hole_depth_ft'])]
        
        if target_table_3.empty:
            return change_list, value_list, size_list  
        else:
            coefficient_foot_metre = 0.3048
            unique_novosconfig_holedepth_list = ["{0:.2f}".format(float(item) * coefficient_foot_metre).rstrip('0').rstrip('.') for item in unique_novosconfig_holedepth_ft_list]
            for index, item in enumerate(merged_list):
                if item not in unique_novosconfig_holedepth_list:
                    change_list[index] = -1
                    value_list[index] = -1
                    size_list[index] = 0
                else:
                    target_table_4 = target_table_3[abs(round((target_table_3['hole_depth_ft'] * coefficient_foot_metre), 2) - float(item)) <= 0.01]
                    selected_novosconfig_holedepth_list = target_table_4['hole_depth_ft'].tolist()
                    length = len(selected_novosconfig_holedepth_list)
                    if 1 <= length: 
                        max_index = -1
                        target_change = target_table_4['change'].get_values()[max_index]
                        target_value = target_table_4['value'].get_values()[max_index]
                        change_list[index] = float(target_change)
                        value_list[index] = 0 # there are some problems in database: false, true, silent
                        size_list[index] = 10
                    else:
                        change_list[index] = -1
                        value_list[index] = -1
                        size_list[index] = 0
    return change_list, value_list, size_list


def update_novosconfig_all_circle_source(all_novosconfig_circle_source, \
                                         x_list, \
                                         unique_novosconfig_holedepth_ft_list, \
                                         novos_config_table, \
                                         variable_list, \
                                         selected_rig, \
                                         selected_job):
    y_offset = 0
    for index, variable in enumerate(variable_list) :
        change_list, value_list, size_list = update_novosconfig_lists(x_list \
                                                                , unique_novosconfig_holedepth_ft_list \
                                                                , novos_config_table \
                                                                , variable \
                                                                , selected_rig \
                                                                , selected_job )
        index_list = [index for index,  item in enumerate(size_list) if item != 0]
        
        previous_change = -1
        for m_index, item in enumerate(index_list):
            if m_index == 0:
                previous_change = change_list[item]
                size_list[item] = 10
                continue
            else:
                if previous_change == change_list[item]:
                    size_list[item] = 0
                else:
                    previous_change = change_list[item]
                    size_list[item] = 10

        y_list = [y_offset for item in size_list]
        x_list = [str(x) for x in x_list]
        y_offset = y_offset + 0.5
        all_novosconfig_circle_source[index].data = dict(HoleDepth = x_list, \
                                                        y = y_list, \
                                                        size = size_list, \
                                                        changes = change_list, \
                                                        values = value_list)


def rigs_combx_change(attrname, old, new):
    global selected_rig
    global selected_job
    
    selected_rig = int(new)
    import_data.retrieve_data(selected_rig)    

    global get_all_data_queue 
    global get_all_data_event
    global all_connection_dict
    global all_connection_table
    global novos_config_table
    global jobs_list
    
    new_jobs_list = update_combBx_values(new, jobs_list, 'JobNumber')
    new_jobs_list = [str(x) for x in new_jobs_list]
    jobs_combx.options = new_jobs_list
    if len(new_jobs_list) > 0:
        first_selected_job = new_jobs_list[0]
    else:
        first_selected_job = '0'
    
    rig, job = new, first_selected_job
    selected_rig = rig
    selected_job = job
    jobs_combx.value = first_selected_job

def jobs_combx_change(attrname, old, new):
    global all_connection_dict
    global well_connnection_source
    global selected_rig
    global selected_job
    global novos_config_plot
    global novos_config_table
    global mainplot_data_all_reference
    global novos_config_variables

    rig, job = rigs_combx.value, new
    selected_rig = rig
    selected_job = job

    checkbox_group_1.active = []
    checkbox_group_3.active = []
    update_1st_chart(selected_rig, selected_job)
    update_2nd_chart(selected_rig, selected_job)
    novos_counts = novos_config.update_novos_config_counts(novos_config_source, novos_config_table, novos_config_variables, selected_job)
    novos_config.update_novos_config_value_and_units(novos_config_table, selected_rig, selected_job)
    from_comboBx_group = False
    update_main_plot(selected_rig, selected_job, from_comboBx_group)  
    
    global main_plot_ckbx_txtbx_source
    doc = curdoc()
    update_main_plot_ckbx_txtbx(doc, \
                                main_plot_ckbx_txtbx_source)

    global all_novosconfig_circle_source
    global latest_x_range_display
    update_novosconfig_circles(all_novosconfig_circle_source, \
                               latest_x_range_display, \
                               novos_config_table, \
                               selected_rig, \
                               selected_job)
    update_driller_hybrid_novos_vs_plot(selected_rig, selected_job, from_comboBx_group)
    max_counts = 0
    for item in novos_counts:
        if math.isnan(item):
            max_counts = 0
            continue
        if max_counts <= int(item):
            max_counts = item
    if max_counts <= 5:
        novos_config_plot.x_range.start = 5 
    else:
        novos_config_plot.x_range.start = max_counts

def crewshift_combx_change(attrname, old, new):
    pass

def checkbox_callback_1(attr, old, new):
    checkbox_group_1_selections = [checkbox_group_1.labels[i] for i in 
                    checkbox_group_1.active]
    checkbox_group_2_selections = [checkbox_group_2.labels[i] for i in 
                    checkbox_group_2.active]
    checkbox_group_3_selections = [checkbox_group_3.labels[i] for i in 
                    checkbox_group_3.active]

    selected_rig, selected_job = rigs_combx.value, jobs_combx.value
    from_comboBx_group = True
    update_main_plot(selected_rig, \
                     selected_job, \
                     from_comboBx_group, \
                     checkbox_group_1_selections, \
                     checkbox_group_2_selections, \
                     checkbox_group_3_selections) 
    update_driller_hybrid_novos_vs_plot(selected_rig, \
                                        selected_job, \
                                        from_comboBx_group, \
                                        checkbox_group_1_selections,\
                                        checkbox_group_2_selections, \
                                        checkbox_group_3_selections)
    global main_plot_ckbx_txtbx_source
    doc = curdoc()
    update_main_plot_ckbx_txtbx(doc, \
                                main_plot_ckbx_txtbx_source, \
                                checkbox_group_1_selections,\
                                checkbox_group_2_selections, \
                                checkbox_group_3_selections)
 
def checkbox_callback_2(attr, old, new):
    checkbox_group_1_selections = [checkbox_group_1.labels[i] for i in 
                    checkbox_group_1.active]
    checkbox_group_2_selections = [checkbox_group_2.labels[i] for i in 
                    checkbox_group_2.active]
    checkbox_group_3_selections = [checkbox_group_3.labels[i] for i in 
                    checkbox_group_3.active]

    selected_rig, selected_job = rigs_combx.value, jobs_combx.value
    from_comboBx_group = True
    update_main_plot(selected_rig, \
                     selected_job, \
                     from_comboBx_group, \
                     checkbox_group_1_selections, \
                     checkbox_group_2_selections, \
                     checkbox_group_3_selections) 
    update_driller_hybrid_novos_vs_plot(selected_rig, \
                                        selected_job, \
                                        from_comboBx_group, \
                                        checkbox_group_1_selections,\
                                        checkbox_group_2_selections, \
                                        checkbox_group_3_selections)
    global main_plot_ckbx_txtbx_source
    doc = curdoc()
    update_main_plot_ckbx_txtbx(doc, \
                                main_plot_ckbx_txtbx_source, \
                                checkbox_group_1_selections,\
                                checkbox_group_2_selections, \
                                checkbox_group_3_selections) 

def checkbox_callback_3(attr, old, new):   
    checkbox_group_1_selections = [checkbox_group_1.labels[i] for i in \
                    checkbox_group_1.active]
    checkbox_group_2_selections = [checkbox_group_2.labels[i] for i in \
                    checkbox_group_2.active]
    checkbox_group_3_selections = [checkbox_group_3.labels[i] for i in \
                    checkbox_group_3.active]
    selected_rig, selected_job = rigs_combx.value, jobs_combx.value
    from_comboBx_group = True
    update_main_plot(selected_rig, \
                     selected_job, \
                     from_comboBx_group, \
                     checkbox_group_1_selections, \
                     checkbox_group_2_selections, \
                     checkbox_group_3_selections) 
    update_driller_hybrid_novos_vs_plot(selected_rig, \
                                        selected_job, \
                                        from_comboBx_group, \
                                        checkbox_group_1_selections,\
                                        checkbox_group_2_selections, \
                                        checkbox_group_3_selections)
    global main_plot_ckbx_txtbx_source
    doc = curdoc()
    update_main_plot_ckbx_txtbx(doc, \
                                main_plot_ckbx_txtbx_source, \
                                checkbox_group_1_selections,\
                                checkbox_group_2_selections, \
                                checkbox_group_3_selections)
def get_novos_job_table(novos_connection_table, selected_rig, selected_job):
    global rig_id_str
    global job_id_str

    rig = selected_rig
    job = selected_job
    rig_target = []
    rig_target.append(int(rig))
    rig_target.append('')
    rigs_query = "{} in @rig_target".format(rig_id_str)
    selected_rig_table = novos_connection_table.query(rigs_query)

    job_target = []
    job_target.append(int(job))
    job_target.append('')
    jobs_query = "{} in @job_target".format(job_id_str)
    selected_job_table = selected_rig_table.query(jobs_query)
    return selected_job_table


def reset_xAxis_ticker():
    global main_plot
    global ticker_cb_reset

    ticker_cb_reset = CustomJS(args=dict(ticker = main_plot.xaxis[0].ticker),\
                                         code="""
                                                ticker.nth = 10
                                            """)

def hide_subplot():
    global sub_plot_rects_source
    global subplot_colors_length
    global novos_length
    global sub_plot
    global m_color_white
    global hide_subplot_callback

    hide_subplot_callback =  CustomJS(args=dict(m_color = m_color_white, \
                                                subplot = sub_plot, \
                                                subplotColorsLength = subplot_colors_length, \
                                                subplotSource = sub_plot_rects_source), code="""
                                                    for(i = 0; i < subplotColorsLength; i++) {
                                                        subplotSource.data['rectcolors'][i] = 'white' 
                                                        subplotSource.data['text'][i] = '' 
    
                                                    }
                                                    subplotSource.change.emit()
                                                    subplot.background_fill_color = 'white' 
                                                """)


def set_xAxis_ticker():
    global main_plot
    global ticker_cb

    ticker_cb = CustomJS(args=dict(ticker = main_plot.xaxis[0].ticker), \
                                code="""
                                if (Math.abs(cb_obj.start-cb_obj.end) > 20000) {
                                    ticker.nth = 200
                                }else if (Math.abs(cb_obj.start-cb_obj.end) > 2000) {
                                    ticker.nth = 20
                                }else if (Math.abs(cb_obj.start-cb_obj.end) > 30) {
                                    ticker.nth = 10
                                }else {
                                    ticker.nth = 1
                                }
                          """)


def remove_redundant_items(list_raw):
    list_redundant_indices = []
    list_unique = []
    i = 0
    for item in list_raw:
        if item not in list_unique:
            list_unique.append(item)
        else:
            list_redundant_indices.append(i)
        i = i + 1
    return list_redundant_indices, list_unique

def delete_redundant_items(list_indices, list_target):
    list_target_length = len(list_target)
    for index in list_indices:
        if index < list_target_length:
            del list_target[index]
        else:
            break
    return list_target

def get_all_dataset(all_connection_dict):
    global hole_depth_str
    global pre_slip_time_str 
    global post_slip_time_str
    global survey_time_str
    global backream_time_str 
    global slip_to_slip_str
    global visualization_depth_str

    all_connection_table = {}
    all_connection_table = pd.DataFrame.from_dict(all_connection_dict)
    
    hole_depth_list = list(map(float, all_connection_table[hole_depth_str]))
    hole_depth_list.sort(key=float)
    display_depth_list = list(map(float, all_connection_table[visualization_depth_str]))
    display_depth_list.sort(key=float)
    b2s_list = list(map(float, all_connection_table[pre_slip_time_str]))
    s2s_list = list(map(float, all_connection_table[slip_to_slip_str]))
    s2b_list = list(map(float, all_connection_table[post_slip_time_str]))
    survey_list = list(map(float, all_connection_table[survey_time_str]))
    ream_list = list(map(float, all_connection_table[backream_time_str]))

    hole_depth_list_redunent_indices, hole_depth_list_unique = remove_redundant_items(hole_depth_list)
    hole_depth_list = []
    hole_depth_list = hole_depth_list_unique.copy()

    depth_list_redunent_indices, depth_list_unique = remove_redundant_items(display_depth_list)
    display_depth_list = []
    display_depth_list = depth_list_unique.copy()
    b2s_list = delete_redundant_items(depth_list_redunent_indices, b2s_list)
    s2s_list = delete_redundant_items(depth_list_redunent_indices, s2s_list)
    s2b_list = delete_redundant_items(depth_list_redunent_indices, s2b_list)
    survey_list = delete_redundant_items(depth_list_redunent_indices, survey_list)
    ream_list = delete_redundant_items(depth_list_redunent_indices, ream_list)

    # could be a function
    rig_job_dict = {}
    rig_job_dict['HoleDepthRef'] = []
    rig_job_dict['HoleDepth'] = []
    rig_job_dict['B2S'] = []
    rig_job_dict['S2S'] = []
    rig_job_dict['S2B'] = []
    rig_job_dict['Survey'] = []
    rig_job_dict['BackReam'] =[]
    rig_job_dict['HoleDepthRef'] = hole_depth_list
    rig_job_dict['HoleDepth'] = display_depth_list
    rig_job_dict['B2S'] = b2s_list
    rig_job_dict['S2S'] = s2s_list
    rig_job_dict['S2B'] = s2b_list
    rig_job_dict['Survey'] = survey_list
    rig_job_dict['BackReam'] = ream_list
    
    #get_all_data_event.set()    
    return rig_job_dict, display_depth_list

def grey_out_connection_type_callback(attr, old, new):
    if new == 2:
        checkbox_group_2.disabled = True
    else:
        checkbox_group_2.disabled = False

def update_mainplot_dict(new_mainplot_list, mainplot_dict):
    for index, item in enumerate(new_mainplot_list):
        if item == -1:
            mainplot_dict['HoleDepthRef'].insert(index, -1)
            mainplot_dict['VBarTop'].insert(index, 0)
            mainplot_dict['VBarBottom'].insert(index, 0)
            mainplot_dict['VBarColors'].insert(index, '#01B8AA') # TODO: good idea?
            mainplot_dict['VBarType'].insert(index, 'B2S') # TODO: good idea?

    return mainplot_dict

def get_variables_holedepth(variable_list, selected_job_table):
    #already checked in retrivev_data()
    novosconfig_holedepth_ft_list = []
    selected_job_table_nonull = selected_job_table[pd.notnull(selected_job_table['hole_depth_ft'])]
    if selected_job_table_nonull.empty:
        return novosconfig_holedepth_ft_list    
    
    for variable in variable_list :
        variable_table = selected_job_table_nonull[selected_job_table_nonull['variable'] == str(variable)]
        if variable_table.empty:
            continue  

        variable_holedepth_table_nonull = variable_table[pd.notnull(variable_table['hole_depth_ft'])]
        if variable_holedepth_table_nonull.empty:
            continue  

        variable_raw_holedepth_ft_list = variable_holedepth_table_nonull['hole_depth_ft'].tolist()
        unique_hole_depth_ft_set = set(variable_raw_holedepth_ft_list)
        hole_depth_ft_list = []
        hole_depth_ft_list = list(unique_hole_depth_ft_set)
        hole_depth_ft_list.sort(key = float)

        variable_holedepth_ft_list = []
        previous_change = -1
        previous_value = -1
        max_index = -1
        for index, item in enumerate(hole_depth_ft_list):
            one_job_table = variable_holedepth_table_nonull[abs(variable_holedepth_table_nonull['hole_depth_ft'] - float(item)) <= 0.01]
            change_list = []
            change_list = one_job_table['change'].tolist()
            if 1 <= len(change_list):
                change = one_job_table['change'].get_values()[max_index]
                value = one_job_table['value'].get_values()[max_index]
            else:
                continue
            if index == 0:
                previous_change = change
                previous_value = value
                variable_holedepth_ft_list.append(item)
            else:
                if previous_change == change:
                    continue
                else:
                    previous_change = change
                    variable_holedepth_ft_list.append(item) 
        novosconfig_holedepth_ft_list = novosconfig_holedepth_ft_list + variable_holedepth_ft_list
    return novosconfig_holedepth_ft_list


def get_novosconfig_holedepth_list(novos_config_table, selected_rig, selected_job = -1):
    hole_depth_ft_list = [] 
    if novos_config_table.empty:
        return hole_depth_ft_list        
    else:   
        selected_job_table = None
        if selected_job == -1:
            selected_job_table = novos_config_table  
        else:
            selected_job_table = novos_config_table[novos_config_table['job_id'] == int(selected_job)]
        
        if selected_job_table.empty:
            return hole_depth_ft_list        
     
    global novos_config_variables
    hole_depth_ft_list = get_variables_holedepth(novos_config_variables, selected_job_table)
    if 1 < len(hole_depth_ft_list):
        unique_hole_depth_ft_set = set(hole_depth_ft_list)
        hole_depth_ft_list = []
        hole_depth_ft_list = list(unique_hole_depth_ft_set)
        hole_depth_ft_list.sort(key = float)
        global all_connection_max_holedepth
        hole_depth_ft_list = [item for item in hole_depth_ft_list if item <= all_connection_max_holedepth]
    return hole_depth_ft_list

def format_merged_list(reference_list, target_list):
    new_list = target_list[:]
    for index, item in enumerate(reference_list):
        if item in target_list:
            continue
        else:
            new_list.insert(index, -1)
    
    new_list.sort(key = float)
    return new_list


def create_novosconfig_circle_source():
    targetSource = ColumnDataSource(data = dict(HoleDepth = [], \
                                                y = [], \
                                                size = [], \
                                                changes = [], \
                                                values = [])) 
    return targetSource

def create_novosconfig_all_circle_source(variable_list):
    
    all_circle_source = []
    for variable in variable_list:
        target_source = create_novosconfig_circle_source()
        all_circle_source.append(target_source)
    return all_circle_source

def create_novosconfig_circles(main_plot, all_circle_source):
    global hBar_color_list

    for index, target_source in enumerate(all_circle_source) :
        main_plot.circle(x = 'HoleDepth', \
                        y = 'y', \
                        color = hBar_color_list[index], \
                        size = 'size',
                        source = target_source)

@gen.coroutine
def update_novosconfig_circles_source(all_novosconfig_circle_source, \
                                      latest_x_range_display, \
                                      novos_config_table, \
                                      selected_rig, \
                                      selected_job, \
                                      novos_config_hole_depth_value):
    global main_plot
    global hBar_color_list
    global novos_config_variables
    
    unique_novosconfig_holedepth_list = get_novosconfig_holedepth_list(novos_config_table, selected_rig, selected_job)
    unique_novosconfig_holedepth_list = list(np.float_(unique_novosconfig_holedepth_list))
    selected_unique_novosconfig_holedepth_list = []
    if novos_config_hole_depth_value != -1 :
        coefficient_foot_metre = 0.3048
        novos_config_hole_depth_ft_value = novos_config_hole_depth_value / coefficient_foot_metre 
        selected_unique_novosconfig_holedepth_list = [item for item in unique_novosconfig_holedepth_list if  item <= novos_config_hole_depth_ft_value]
    else:
        selected_unique_novosconfig_holedepth_list = copy.deepcopy(unique_novosconfig_holedepth_list)

    latest_x_range_display_set = set(latest_x_range_display)
    latest_x_range_display = list(latest_x_range_display_set)
    latest_x_range_display_float = list(np.float_(latest_x_range_display))
    latest_x_range_display_float.sort(key = float)
    latest_x_range_display = [str(item) for item in latest_x_range_display_float]
    
    update_novosconfig_all_circle_source(all_novosconfig_circle_source, \
                                         latest_x_range_display, \
                                         selected_unique_novosconfig_holedepth_list, \
                                         novos_config_table, \
                                         novos_config_variables, \
                                         selected_rig, \
                                         selected_job)

@without_document_lock
def update_novosconfig_circles_chart(doc, \
                               novosconfig_event, \
                               all_novosconfig_circle_source, \
                               latest_x_range_display, \
                               novos_config_table, \
                               selected_rig, \
                               selected_job, \
                               novos_config_hole_depth_value = -1):
    novosconfig_event.wait()
    doc.add_next_tick_callback(partial(update_novosconfig_circles_source, \
                                       all_novosconfig_circle_source, \
                                       latest_x_range_display, \
                                       novos_config_table, \
                                       selected_rig, \
                                       selected_job, \
                                       novos_config_hole_depth_value))

@gen.coroutine
def update_novosconfig_circles(all_novosconfig_circle_source, \
                               latest_x_range_display, \
                               novos_config_table, \
                               selected_rig, \
                               selected_job, \
                               novos_config_hole_depth_value = -1):
    global novosconfig_event
    global novosconfig_queue
   
    doc = curdoc()
    novosconfig_queue.put(update_novosconfig_circles_chart(doc, \
                               novosconfig_event, \
                               all_novosconfig_circle_source, \
                               latest_x_range_display, \
                               novos_config_table, \
                               selected_rig, \
                               selected_job, \
                               novos_config_hole_depth_value))
    novosconfig_event.set()

@gen.coroutine
def update_sub_plot_textbox_source(sub_plot_textbox_source = sub_plot_textbox_source, \
                                   sub_plot_textbox_text = sub_plot_textbox_text):
    sub_plot_textbox_source.data = dict(x = [550, 550, 550, 550], \
                                        y = [280, 250, 220, 190],  \
                                        txt = sub_plot_textbox_text)

@without_document_lock 
def get_sub_plot_textbox_text(connection_type = '', conn_type = '', holedepth = ''):
    sub_plot_textbox_text = []
    if not conn_type:
        sub_plot_textbox_text = ['', '', '', '']
    else:
        if conn_type == 'S2S':
            sub_plot_textbox_text = ['Connection Type: {}'.format(connection_type),\
                                     'Connection Phase: {}'.format(conn_type),\
                                     'Hole Depth:      {}'.format(holedepth),\
                                     'No Novos Activities']
        elif conn_type == 'S2B' or conn_type == 'B2S':
            sub_plot_textbox_text = ['Connection Type: {}'.format(connection_type),\
                                     'Connection Phase: {}'.format(conn_type),\
                                     'Hole Depth:      {}'.format(holedepth),\
                                     '']
   
    return sub_plot_textbox_text
     

def update_sub_plot_rects_source(attr, old, new):
    return ""

def update_sub_plot_all_source(attr = None, old = None, new = None):
    global sub_plot_textbox_source
    sub_plot_textbox_text = ['', '', '']
    if attr is not None:
        sub_plot_textbox_text = update_sub_plot_rects_source(attr, old, new)
    else:
        update_sub_plot_rects_source(attr, old, new)
    update_sub_plot_textbox_source(sub_plot_textbox_source , sub_plot_textbox_text)

@without_document_lock
def update_sub_plot_chart(doc, \
                        sub_plot_event, \
                        attr, \
                        old, \
                        new):
    sub_plot_event.wait()
    doc.add_next_tick_callback(partial(update_sub_plot_all_source,
                                       attr, \
                                       old, \
                                       new))
     
def update_sub_plot(attr, \
                    old, \
                    new):
    global sub_plot_queue
    global sub_plot_event

    doc = curdoc()

    sub_plot_queue.put(update_sub_plot_chart(doc, \
                                            sub_plot_event, \
                                            attr, \
                                            old, \
                                            new))
    sub_plot_event.set()

def calculate_times(connection_counts, target_list):
    besttime = 0.0
    mediantime = 0.0
    averagetime = 0.0
    if 1 <= connection_counts:
        besttime = min(target_list)
        mediantime = np.median(np.array(target_list))
        averagetime = np.average(target_list)     

    return averagetime, mediantime, besttime

@without_document_lock
def update_plot_textbox_text(counts, averagetime, mediantime, besttime):
    plot_textbox_text = ['Counts', \
                         str(counts), \
                         'Average (min)', \
                         '{0:.2f}'.format(averagetime),\
                         'Median (min)', \
                         '{0:.2f}'.format(mediantime),\
                         'Best (min)', \
                         '{0:.2f}'.format(besttime)]
   
    return plot_textbox_text

@gen.coroutine
def update_textbox_source(x, \
                          y, \
                          plot_textbox_source, \
                          plot_textbox_text):
    plot_textbox_source.data = dict(x = x, \
                                    y = y,  \
                                    txt = plot_textbox_text)

def get_ckbx_txt(checkbox_group_1_selections,\
                 checkbox_group_2_selections, \
                 checkbox_group_3_selections):
    well_selection = ''
    if (checkbox_group_1_selections is not None):
        well_selection_length = len(checkbox_group_1_selections)
        if ((0 == well_selection_length) or (3 == well_selection_length)):
            pass
        else:
            for item in checkbox_group_1_selections:
                if not well_selection:
                    well_selection = item  
                else:
                    well_selection = well_selection + " + " +  item 

    connection_phase = ''
    if (checkbox_group_3_selections is not None):
        connection_phase_length = len(checkbox_group_3_selections)
        if ((0 == connection_phase_length) or (ALL_CONNECTION_PHASE == connection_phase_length)):
            pass
        else:
            for item in checkbox_group_3_selections:
                if item == "Survey":
                    item = 'Svy'
                elif item == 'BackReam':
                    item = 'Brm'
                elif item == 'Friction Test':
                    item = 'Frict'

                if not connection_phase:
                    connection_phase = item  
                else:
                    connection_phase = connection_phase + "+" +  item 

    if not connection_phase:
        connection_phase = 'W2W'
    ckbx_txtbx_text = [well_selection, connection_phase]
    return ckbx_txtbx_text

@without_document_lock
def update_main_plot_ckbx_txtbx(doc, \
                                main_plot_ckbx_txtbx_source, \
                                checkbox_group_1_selections = [],\
                                checkbox_group_2_selections = [], \
                                checkbox_group_3_selections = []):
    ckbx_txtbx_text = get_ckbx_txt(checkbox_group_1_selections,\
                                   checkbox_group_2_selections, \
                                   checkbox_group_3_selections)
    x = [30, 30]
    y = [230, 210]    
    doc.add_next_tick_callback(partial(update_textbox_source, \
                                       x, \
                                       y, \
                                       main_plot_ckbx_txtbx_source, \
                                       ckbx_txtbx_text))