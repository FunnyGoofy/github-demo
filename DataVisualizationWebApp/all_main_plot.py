# Create a polynomial line graph with those arguments
import flask
from bokeh.models import FactorRange, Spacer
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import pandas as pd
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models.widgets import PreText, Select, CheckboxGroup
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
import threading
from bokeh.client import session
from functools import  partial
from tornado import gen
from bokeh.document import without_document_lock
from timeit import timeit
from DataVisualizationWebApp import utility as uHelper
import itertools
import copy
import numpy as np

lock = threading.RLock()
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
slip_to_slip_str = "slip_to_slip"
frictiontest_time_str = "frictiontest_time"
depth_ft_str = "depth_ft"
edr_depth_ft = 'edr_depth_ft'
selected_rig = ''
selected_job  = ''
main_plot = None
visualization_depth_str = "visualization_depth"

def get_all_dataset(all_connection_dict):
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
    
    hole_depth_list = list(map(float, all_connection_table[hole_depth_str]))
    hole_depth_list.sort(key=float)
    display_depth_list = list(map(float, all_connection_table[visualization_depth_str]))
    display_depth_list.sort(key=float)
    b2s_list = list(map(float, all_connection_table[pre_slip_time_str]))
    s2s_list = list(map(float, all_connection_table[slip_to_slip_str]))
    s2b_list = list(map(float, all_connection_table[post_slip_time_str]))
    survey_list = list(map(float, all_connection_table[survey_time_str]))
    ream_list = list(map(float, all_connection_table[backream_time_str]))
    frictiontest_list = list(map(float, all_connection_table[frictiontest_time_str]))

    hole_depth_list_redunent_indices, hole_depth_list_unique = uHelper.remove_redundant_items(hole_depth_list)
    hole_depth_list = []
    hole_depth_list = hole_depth_list_unique.copy()

    depth_list_redunent_indices, depth_list_unique = uHelper.remove_redundant_items(display_depth_list)
    display_depth_list = []
    display_depth_list = depth_list_unique.copy()
    b2s_list = uHelper.delete_redundant_items(depth_list_redunent_indices, b2s_list)
    s2s_list = uHelper.delete_redundant_items(depth_list_redunent_indices, s2s_list)
    s2b_list = uHelper.delete_redundant_items(depth_list_redunent_indices, s2b_list)
    survey_list = uHelper.delete_redundant_items(depth_list_redunent_indices, survey_list)
    ream_list = uHelper.delete_redundant_items(depth_list_redunent_indices, ream_list)
    frictiontest_list = uHelper.delete_redundant_items(depth_list_redunent_indices, frictiontest_list)

    # could be a function
    rig_job_dict = {}
    rig_job_dict['HoleDepthRef'] = []
    rig_job_dict['HoleDepth'] = []
    rig_job_dict['B2S'] = []
    rig_job_dict['S2S'] = []
    rig_job_dict['S2B'] = []
    rig_job_dict['Survey'] = []
    rig_job_dict['BackReam'] =[]
    rig_job_dict['FrictionTest'] =[]

    rig_job_dict['HoleDepthRef'] = hole_depth_list
    rig_job_dict['HoleDepth'] = display_depth_list
    rig_job_dict['B2S'] = b2s_list
    rig_job_dict['S2S'] = s2s_list
    rig_job_dict['S2B'] = s2b_list
    rig_job_dict['Survey'] = survey_list
    rig_job_dict['BackReam'] = ream_list
    rig_job_dict['FrictionTest'] = frictiontest_list

    #get_all_data_event.set()    
    return rig_job_dict, display_depth_list


def update_checkBx_groups_dict(all_connection_table, \
                               rig, \
                               job, \
                               checkbox_group_1_selections = [], \
                               checkbox_group_2_selections = []):
    #1. get jobs table
    
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

    #2. generate a table based on selections from 3 groups
    global well_selection_str 
    main_plot_group1_dict = {}
    group_1_table = selected_job_table
    if not checkbox_group_1_selections:
        group_1_query = '{} in ["Build", "Vertical", "Lateral"]'.format(well_selection_str)
        main_plot_group1_dict = group_1_table.query(group_1_query).to_dict('dict')
    else:
        for selected in checkbox_group_1_selections:
            if selected == 'Build':
                build_dict={}
                build_query = '{} in ["Build",]'.format(well_selection_str)
                build_dict = group_1_table.query(build_query).to_dict('dict')
                #to merge multiple dicts with same key
                if not bool(main_plot_group1_dict):
                    main_plot_group1_dict = build_dict
                else:
                    main_plot_group1_dict = uHelper.merge(main_plot_group1_dict, build_dict)
            elif selected == 'Vertical':
                vertical_dict={}
                vertical_query = '{} in ["Vertical",]'.format(well_selection_str)
                vertical_dict = group_1_table.query(vertical_query).to_dict('dict')
                if not bool(main_plot_group1_dict):
                    main_plot_group1_dict = vertical_dict
                else:
                    main_plot_group1_dict = uHelper.merge(main_plot_group1_dict, vertical_dict)
            elif selected == "Lateral":
                lateral_dict={}
                lateral_query = '{} in ["Lateral",]'.format(well_selection_str)
                lateral_dict = group_1_table.query(lateral_query).to_dict('dict')
                if not bool(main_plot_group1_dict):
                    main_plot_group1_dict = lateral_dict
                else:
                    main_plot_group1_dict = uHelper.merge(main_plot_group1_dict, lateral_dict)

        
    global connection_type_str
    main_plot_group2_dict = {}
    group_2_table = pd.DataFrame.from_dict(main_plot_group1_dict)
    if not checkbox_group_2_selections:
        group_2_query = '{} in ["Driller", "Hybrid", "Novos"]'.format(connection_type_str)
        main_plot_group2_dict = group_2_table.query(group_2_query).to_dict('dict')
    else:
        for selected in checkbox_group_2_selections:
            if selected == 'Driller':
                driller_dict = {}
                driller_query = '{} in ["Driller",]'.format(connection_type_str)
                driller_dict = group_2_table.query(driller_query).to_dict('dict')
                if not bool(main_plot_group2_dict):
                    main_plot_group2_dict = driller_dict
                else:
                    main_plot_group2_dict = uHelper.merge(main_plot_group2_dict, driller_dict)
                    
            elif selected == 'Hybrid':
                hybrid_dict = {}
                hybrid_query = '{} in ["Hybrid",]'.format(connection_type_str)
                hybrid_dict = group_2_table.query(hybrid_query).to_dict('dict')
                if not bool(main_plot_group2_dict):
                    main_plot_group2_dict = hybrid_dict
                else:
                    main_plot_group2_dict = uHelper.merge(main_plot_group2_dict, hybrid_dict)

            elif selected == "Novos":
                novos_dict = {}
                novos_query = '{} in ["Novos",]'.format(connection_type_str)
                novos_dict = group_2_table.query(novos_query).to_dict('dict')
                if not bool(main_plot_group2_dict):
                    main_plot_group2_dict = novos_dict
                else:
                    main_plot_group2_dict = uHelper.merge(main_plot_group2_dict, novos_dict)

    return main_plot_group2_dict   

def update_main_plot_dict(in_main_plot_dict, \
                          novos_config_table, \
                          selected_rig, \
                          selected_job, \
                          checkbox_group_3_selections = []):
    "update main dict"
    wellSel_connType_groups_table = pd.DataFrame.from_dict(in_main_plot_dict)
        
    global hole_depth_str
    global pre_slip_time_str 
    global post_slip_time_str
    global survey_time_str
    global backream_time_str 
    global frictiontest_time_str 
    global slip_to_slip_str
    global visualization_depth_str

    depth_list = []
    depth_list_display = []
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
        
    
    hole_depth_list_ft_ref = list(map(float, wellSel_connType_groups_table[hole_depth_str]))
    hole_depth_list_display_ref = list(map(float, wellSel_connType_groups_table[visualization_depth_str]))
    job_holedepth_list = copy.deepcopy(hole_depth_list_display_ref) 
   
    job_holedepth_list = np.round(job_holedepth_list, 2)
    job_holedepth_list = job_holedepth_list.tolist()
    unique_novosconfig_holedepth_ft_list = uHelper.get_novosconfig_holedepth_list(novos_config_table, selected_rig, selected_job)
    unique_novosconfig_holedepth_ft_list.sort(key = float)
    unique_novosconfig_holedepth_list = []
    coefficient_foot_metre = 0.3048
    uHelper.all_connection_max_holedepth = max(job_holedepth_list) / coefficient_foot_metre
    country = uHelper.rig_lookup_by_country_dict[str(selected_rig)]
    if country == 'Canada':
        unique_novosconfig_holedepth_list = [item * coefficient_foot_metre for item in unique_novosconfig_holedepth_ft_list]
    else:
        unique_novosconfig_holedepth_list = copy.deepcopy(unique_novosconfig_holedepth_ft_list)

    unique_novosconfig_holedepth_list = np.round(unique_novosconfig_holedepth_list, 2)
    unique_novosconfig_holedepth_list = unique_novosconfig_holedepth_list.tolist()
        
    depth_list_display = list(set(unique_novosconfig_holedepth_list).union(set(job_holedepth_list))) 
    depth_list_display.sort(key = float)
    if country == 'Canada':
        depth_list = [ item / coefficient_foot_metre for item in depth_list_display]
    else:
        depth_list = copy.deepcopy(depth_list_display)
	  
    b2s_list = list(map(float, wellSel_connType_groups_table[pre_slip_time_str]))
    b2s_list_length = len(b2s_list)
    s2s_list = list(map(float, wellSel_connType_groups_table[slip_to_slip_str]))
    s2b_list = list(map(float, wellSel_connType_groups_table[post_slip_time_str]))
    survey_list = list(map(float, wellSel_connType_groups_table[survey_time_str]))
    ream_list = list(map(float, wellSel_connType_groups_table[backream_time_str]))
    frictiontest_list = list(map(float, wellSel_connType_groups_table[frictiontest_time_str]))
    difference_list = list(set(unique_novosconfig_holedepth_list).difference(set(job_holedepth_list)))
    for index, item in enumerate(depth_list_display):
        if item in difference_list:
            b2s_list.insert(index, 0.0)
            s2s_list.insert(index, 0.0) 
            s2b_list.insert(index, 0.0) 
            survey_list.insert(index, 0.0)
            ream_list.insert(index, 0.0)
            frictiontest_list.insert(index, 0.0)
    
    # could be a function
    main_plot_dict = {}
    main_plot_dict['VBarTop'] = []
    main_plot_dict['VBarBottom'] = []
    main_plot_dict['VBarColors'] = []
    main_plot_dict['VBarType'] = []
    main_plot_dict['HoleDepth'] = []
    main_plot_dict['HoleDepthRef'] = []
        
    main_plot_list = []
    main_plot_depth_list = [] 
    main_plot_depth_list_ref = [] 
    main_plot_top_list = []
    main_plot_bottom_list = []
    main_plot_color_list = []
    main_plot_type_list = []
    if not checkbox_group_3_selections:
        b2s_s2s_list = list(map(add, b2s_list, s2s_list))
        b2s_s2s_s2b_list = list(map(add, b2s_s2s_list, s2b_list))
        b2s_s2s_s2b_survey_list = list(map(add, b2s_s2s_s2b_list, survey_list))
        b2s_s2s_s2b__survey_ream_list = list(map(add, b2s_s2s_s2b_survey_list, ream_list))
        b2s_s2s_s2b__survey_ream_frictiontest_list = list(map(add, b2s_s2s_s2b__survey_ream_list, frictiontest_list))

        main_plot_depth_list = depth_list_display + depth_list_display \
                             + depth_list_display + depth_list_display  \
                             + depth_list_display + depth_list_display
        main_plot_depth_list_ref = depth_list + depth_list \
                                 + depth_list + depth_list \
                                 + depth_list + depth_list
        main_plot_top_list = b2s_list \
                           + b2s_s2s_list \
                           + b2s_s2s_s2b_list \
                           + b2s_s2s_s2b_survey_list \
                           + b2s_s2s_s2b__survey_ream_list \
                           + b2s_s2s_s2b__survey_ream_frictiontest_list
        main_plot_bottom_list = [ 0 for item in b2s_list] \
                              + b2s_list + b2s_s2s_list \
                              + b2s_s2s_s2b_list \
                              + b2s_s2s_s2b_survey_list  \
                              + b2s_s2s_s2b__survey_ream_list
        main_plot_color_list = [ "#01B8AA" for item in b2s_list] \
                            +  [ "#000000" for item in b2s_s2s_list] \
                            +  [ "#FD625E" for item in b2s_s2s_s2b_list] \
                            +  [ "#F2C80F" for item in b2s_s2s_s2b_survey_list] \
                            +  [ "#A66999" for item in b2s_s2s_s2b__survey_ream_list] \
                            +  [ "#6fff00" for item in b2s_s2s_s2b__survey_ream_frictiontest_list]

        main_plot_type_list = ['B2S' for item in b2s_list] \
                                    + ['S2S' for item in s2s_list] \
                                    + ['S2B' for item in s2b_list] \
                                    + ['Survey' for item in survey_list] \
                                    + ['BackReam' for item in ream_list] \
                                    + ['FrictionTest' for item in frictiontest_list] 
    else:
        for selected in checkbox_group_3_selections:
            if selected == 'B2S':
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + b2s_list
                main_plot_type_list = main_plot_type_list + ['B2S' for item in b2s_list] 
                main_plot_color_list = main_plot_color_list  + [ "#01B8AA" for item in b2s_list]

            elif selected == 'S2S':
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + s2s_list
                main_plot_type_list = main_plot_type_list + ['S2S' for item in s2s_list] 
                main_plot_color_list = main_plot_color_list  + [ "#000000" for item in s2s_list]

            elif selected == "S2B":
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + s2b_list
                main_plot_type_list = main_plot_type_list + ['S2B' for item in s2b_list] 
                main_plot_color_list = main_plot_color_list  + [ "#FD625E" for item in s2b_list]

            elif selected == "Survey":
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + survey_list
                main_plot_type_list = main_plot_type_list + ['Survey' for item in survey_list] 
                main_plot_color_list = main_plot_color_list  + [ "#F2C80F" for item in survey_list]

            elif selected == "BackReam":
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + ream_list
                main_plot_type_list = main_plot_type_list + ['BackReam' for item in ream_list] 
                main_plot_color_list = main_plot_color_list  + [ "#A66999" for item in ream_list]
             
            elif selected == "Friction Test":
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + frictiontest_list
                main_plot_type_list = main_plot_type_list + ['FrictionTest' for item in frictiontest_list] 
                main_plot_color_list = main_plot_color_list  + [ "#6fff00" for item in frictiontest_list]

        # generate top&bottom values  
        section_length = len(depth_list_display)
        section_length_ref = len(depth_list)
        main_plot_top_list = main_plot_list
        connectionPhase_selections = int(len(main_plot_list) / len(depth_list_display))
        connectionPhase_selections_ref = int(len(main_plot_list) / len(depth_list))
        for i in range(0, connectionPhase_selections):
            if i > 0 :
                prev_section_head = (i - 1) * section_length
                current_section_head = i * section_length
                temp_list = [(main_plot_top_list[prev_section_head + k] + main_plot_list[current_section_head + k]) for k in range(0, section_length)]
                main_plot_top_list = main_plot_top_list + temp_list
            else:
                main_plot_top_list = [main_plot_list[k] for k in range(0, section_length)]
                    
        bottom_list_slice_upbound = (connectionPhase_selections - 1) * section_length
        main_plot_bottom_list = [ 0 for k in range(0, section_length)]
        if (connectionPhase_selections - 1) > 0:
            main_plot_bottom_list = main_plot_bottom_list + main_plot_top_list[:bottom_list_slice_upbound]
        else:
            main_plot_bottom_list = main_plot_bottom_list
        
    main_plot_dict['HoleDepthRef'] = main_plot_depth_list_ref
    main_plot_dict['HoleDepth'] = main_plot_depth_list
    main_plot_dict['VBarTop'] = main_plot_top_list
    main_plot_dict['VBarBottom'] = main_plot_bottom_list
    main_plot_dict['VBarColors'] = main_plot_color_list
    main_plot_dict['VBarType'] = main_plot_type_list
    
    main_plot_depth_list_length = len(main_plot_depth_list)
    main_plot_top_list_length = len(main_plot_top_list)
    return main_plot_dict, depth_list_display, depth_list

def updateSourceData(in_mainplot_data_type, in_mainplot_data, depth_list_latest):
    new_list = []

    in_mainplot_data_length = len(in_mainplot_data[in_mainplot_data_type])
    i = 0
    for item in depth_list_latest: 
        if item != '-1':
            if i >= in_mainplot_data_length:
                if in_mainplot_data_type == 'VBarColors':
                    new_list.append('white')
                else:
                    new_list.append('')
            else:  
                var = in_mainplot_data[in_mainplot_data_type][i]
                new_list.append(var)
                i = i + 1
        else:
            if in_mainplot_data_type == 'VBarColors':
                new_list.append('white')
            else:
                new_list.append('')
   
    return new_list
 

def update_holeDepth_list(mainplot_data, mainplot_data_all, display_depth_list, depth_ref_list):
    mainplot_data_length = len(mainplot_data['HoleDepth'])
    mainplot_data_all_length = len(mainplot_data_all['HoleDepth'])
    mainplot_data_holeDepth_list = []
    mainplot_data_holeDepthRef_list = []

    display_depth_list = display_depth_list.copy()
    depth_ref_list = depth_ref_list.copy()
    depth_list_length = len(display_depth_list)
    depth_ref_list_length = len(depth_ref_list)
    for item in mainplot_data_all['HoleDepth']:
        if type(item) is str:
            pass
        else:
            item = "{0:.2f}".format(item)
        if item in display_depth_list:
            mainplot_data_holeDepth_list.append(item)
            ind = display_depth_list.index(item)
            mainplot_data_holeDepthRef_list.append(depth_ref_list[ind])
        else:
            mainplot_data_holeDepth_list.append('-1')
            mainplot_data_holeDepthRef_list.append('-1')
    
    return mainplot_data_holeDepth_list, mainplot_data_holeDepthRef_list   

@gen.coroutine 
def update_main_plot_source(main_plot, main_plot_dict, display_depth_list, mainplot_source):
    depth_ref_list = []
    depth_display_list = []
    VBarTop_list = []
    VBarBottom_list = [] 
    VBarColors_list = []
    VBarType_list = []
    main_plot.x_range.factors = display_depth_list[:]
    
    depth_ref_list = copy.deepcopy(main_plot_dict['HoleDepthRef'])
    depth_display_list = copy.deepcopy(main_plot_dict['HoleDepth'])
    VBarTop_list = copy.deepcopy(main_plot_dict['VBarTop'])
    connection_counts = len(display_depth_list)
    target_listwithout_zero = []
    if 1 <= connection_counts :
        target_list = copy.deepcopy(VBarTop_list[-connection_counts:])
        target_array = np.array(target_list)
        target_listwithout_zero = target_array[target_array != 0]
    
    connection_counts = len(target_listwithout_zero)
    averagetime, mediantime, besttime = uHelper.calculate_times(connection_counts, target_listwithout_zero) 
    depth_display_list = ["{0:.2f}".format(item).rstrip('0').rstrip('.') for item in depth_display_list]
    VBarBottom_list =  copy.deepcopy(main_plot_dict['VBarBottom'])
    VBarColors_list = copy.deepcopy(main_plot_dict['VBarColors'])
    VBarType_list = copy.deepcopy(main_plot_dict['VBarType'])
    periods_list = list(np.array(VBarTop_list) - np.array(VBarBottom_list))
    mainplot_source.data = dict(HoleDepthRef = depth_ref_list, \
                            HoleDepth = depth_display_list, \
                            VBarTop = VBarTop_list, \
                            VBarBottom = VBarBottom_list, \
                            VBarColors = VBarColors_list, \
                            VBarType = VBarType_list, \
                            Periods = periods_list)

    plot_textbox_text = uHelper.update_plot_textbox_text(connection_counts, averagetime, mediantime, besttime)
    x = [30, 30, 30, 30, 30, 30, 30, 30]
    y = [180, 165, 145, 130, 110, 95, 75, 60]     
    uHelper.update_textbox_source(x = x, \
                                  y = y, \
                                  plot_textbox_source = uHelper.main_plot_textbox_source, \
                                  plot_textbox_text = plot_textbox_text)


@without_document_lock
def update_main_plot_chart( doc, \
                            update_main_plot_event, \
                            mainplot_source, \
                            main_plot, \
                            checkbox_group_1_selections, \
                            checkbox_group_2_selections,\
                            checkbox_group_3_selections, \
                            all_connection_table,\
                            rig, \
                            job, \
                            from_comboBx_group, \
                            novos_config_table):
    update_main_plot_event.wait()        
    
    main_plot_dict = {}
    display_depth_list = []
    depth_ref_list = []

    if from_comboBx_group == True:
        main_plot_dict = update_checkBx_groups_dict(all_connection_table, \
                                                    rig, \
                                                    job, \
                                                    checkbox_group_1_selections, \
                                                    checkbox_group_2_selections)
        main_plot_dict, display_depth_list, depth_ref_list = update_main_plot_dict(main_plot_dict, novos_config_table, rig, job, checkbox_group_3_selections)
    else:
        main_plot_dict = update_checkBx_groups_dict(all_connection_table, \
                                                    rig, \
                                                    job)
        main_plot_dict, display_depth_list, depth_ref_list  = update_main_plot_dict(main_plot_dict, novos_config_table, rig, job)
        
    display_depth_list = ["{0:.2f}".format(item).rstrip('0').rstrip('.') for item in display_depth_list]
    depth_ref_list = ["{0:.2f}".format(item) for item in depth_ref_list]
    depth_list_length = len(display_depth_list)
    depth_ref_list_length = len(depth_ref_list)
    uHelper.latest_x_range_display = copy.deepcopy(display_depth_list)
    uHelper.latest_x_range_ft = copy.deepcopy(depth_ref_list)
    
    doc.add_next_tick_callback(partial(update_main_plot_source, \
                                       main_plot = main_plot,  \
                                       main_plot_dict = main_plot_dict, \
                                       display_depth_list = display_depth_list, \
                                       mainplot_source = mainplot_source))

    
