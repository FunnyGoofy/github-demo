import pandas as pd
from functools import  partial
from tornado import gen
from bokeh.models import ColumnDataSource
from bokeh.document import without_document_lock
from bokeh.util.string import encode_utf8
from bokeh.plotting import figure
from bokeh.models import FactorRange
from bokeh.core.properties import value
import threading
from DataVisualizationWebApp import utility as uHelper


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
import copy
import numpy as np

def update_checkBx_groups_dict(all_connection_dict, \
                               selected_rig, \
                               selected_job, \
                               checkbox_group_1_selections = [], \
                               checkbox_group_2_selections = [], \
                               connection_type_selected = 'disable'):
    #1. get jobs table
    #TODO: use all_connection_table
    all_connection_table = {}
    all_connection_table = pd.DataFrame.from_dict(all_connection_dict)
     
    rig_target = []
    rig_target.append(int(selected_rig))
    rig_target.append('')
    rigs_query = "{} in @rig_target".format(uHelper.rig_id_str)
    selected_rig_table = all_connection_table.query(rigs_query)

    job_target = []
    job_target.append(int(selected_job))
    job_target.append('')
    jobs_query = "{} in @job_target".format(uHelper.job_id_str)
    selected_job_table = selected_rig_table.query(jobs_query)

    #2. generate a table based on selections from 3 groups
    plot_group1_dict = {}
    group_1_table = selected_job_table
    if not checkbox_group_1_selections:
        group_1_query = '{} in ["Build", "Vertical", "Lateral"]'.format(uHelper.well_selection_str)
        plot_group1_dict = group_1_table.query(group_1_query).to_dict('dict')
    else:
        for selected in checkbox_group_1_selections:
            if selected == 'Build':
                build_dict={}
                build_query = '{} in ["Build",]'.format(uHelper.well_selection_str)
                build_dict = group_1_table.query(build_query).to_dict('dict')
                #to merge multiple dicts with same key
                if not bool(plot_group1_dict):
                    plot_group1_dict = build_dict
                else:
                    plot_group1_dict = uHelper.merge(plot_group1_dict, build_dict)
            elif selected == 'Vertical':
                vertical_dict={}
                vertical_query = '{} in ["Vertical",]'.format(uHelper.well_selection_str)
                vertical_dict = group_1_table.query(vertical_query).to_dict('dict')
                if not bool(plot_group1_dict):
                    plot_group1_dict = vertical_dict
                else:
                    plot_group1_dict = uHelper.merge(plot_group1_dict, vertical_dict)
            elif selected == "Lateral":
                lateral_dict={}
                lateral_query = '{} in ["Lateral",]'.format(uHelper.well_selection_str)
                lateral_dict = group_1_table.query(lateral_query).to_dict('dict')
                if not bool(plot_group1_dict):
                    plot_group1_dict = lateral_dict
                else:
                    plot_group1_dict = uHelper.merge(plot_group1_dict, lateral_dict)
    
    plot_group2_dict = {}
    plot_group2_driller_dict = {}
    plot_group2_hybrid_dict = {}
    plot_group2_novos_dict = {}
    
    if connection_type_selected == 'disable':
        group_2_table = pd.DataFrame.from_dict(plot_group1_dict)
        group_2_query = '{} in ["Driller", "Hybrid", "Novos"]'.format(uHelper.connection_type_str)
        plot_group2_dict = group_2_table.query(group_2_query).to_dict('dict')

        group_2_table = pd.DataFrame.from_dict(plot_group1_dict)
        driller_query = '{} in ["Driller",]'.format(uHelper.connection_type_str)
        plot_group2_driller_dict = group_2_table.query(driller_query).to_dict('dict')
                    
        hybrid_query = '{} in ["Hybrid",]'.format(uHelper.connection_type_str)
        plot_group2_hybrid_dict = group_2_table.query(hybrid_query).to_dict('dict')
        
        novos_query = '{} in ["Novos",]'.format(uHelper.connection_type_str)
        plot_group2_novos_dict = group_2_table.query(novos_query).to_dict('dict')

        group_1_query = '{} in ["Build", "Vertical", "Lateral"]'.format(uHelper.well_selection_str)
        plot_group1_dict = group_1_table.query(group_1_query).to_dict('dict')

    else:
        group_2_table = pd.DataFrame.from_dict(plot_group1_dict)
        if not checkbox_group_2_selections:
            group_2_query = '{} in ["Driller", "Hybrid", "Novos"]'.format(uHelper.connection_type_str)
            plot_group2_dict = group_2_table.query(group_2_query).to_dict('dict')
        else:
            for selected in checkbox_group_2_selections:
                if selected == 'Driller':
                    driller_dict = {}
                    driller_query = '{} in ["Driller",]'.format(uHelper.connection_type_str)
                    driller_dict = group_2_table.query(driller_query).to_dict('dict')
                    if not bool(plot_group2_dict):
                        plot_group2_dict = driller_dict
                    else:
                        plot_group2_dict = uHelper.merge(plot_group2_dict, driller_dict)
                    
                elif selected == 'Hybrid':
                    hybrid_dict = {}
                    hybrid_query = '{} in ["Hybrid",]'.format(uHelper.connection_type_str)
                    hybrid_dict = group_2_table.query(hybrid_query).to_dict('dict')
                    if not bool(plot_group2_dict):
                        plot_group2_dict = hybrid_dict
                    else:
                        plot_group2_dict = uHelper.merge(plot_group2_dict, hybrid_dict)

                elif selected == "Novos":
                    novos_dict = {}
                    novos_query = '{} in ["Novos",]'.format(uHelper.connection_type_str)
                    novos_dict = group_2_table.query(novos_query).to_dict('dict')
                    if not bool(plot_group2_dict):
                        plot_group2_dict = novos_dict
                    else:
                        plot_group2_dict = uHelper.merge(plot_group2_dict, novos_dict)

    return plot_group2_dict,  plot_group2_driller_dict, plot_group2_hybrid_dict, plot_group2_novos_dict, plot_group1_dict   





def update_driller_hybrid_novos_vs_plot_dict(in_plot_dict, checkbox_group_3_selections = []):
    "update main dict"
    wellSel_connType_groups_table = {}
    wellSel_connType_groups_table = pd.DataFrame.from_dict(in_plot_dict)
    
    depth_list = []
    depth_list_display = []
    b2s_list = []
    s2s_list = []
    s2b_list = []
    survey_list = []
    ream_list = []    
    frictiontest_list = []
        
    depth_list = list(map(float, wellSel_connType_groups_table[uHelper.hole_depth_str]))
    depth_list.sort(key=float)
    depth_list_length = len(depth_list)
    depth_list_display = list(map(float, wellSel_connType_groups_table[uHelper.visualization_depth_str]))
    depth_list_display.sort(key=float)
    b2s_list = list(map(float, wellSel_connType_groups_table[uHelper.pre_slip_time_str]))
    s2s_list = list(map(float, wellSel_connType_groups_table[uHelper.slip_to_slip_str]))
    s2b_list = list(map(float, wellSel_connType_groups_table[uHelper.post_slip_time_str]))
    survey_list = list(map(float, wellSel_connType_groups_table[uHelper.survey_time_str]))
    ream_list = list(map(float, wellSel_connType_groups_table[uHelper.backream_time_str]))
    frictiontest_list = list(map(float, wellSel_connType_groups_table[uHelper.frictiontest_time_str]))
    
    hole_depth_list_redunent_indices, hole_depth_list_unique = uHelper.remove_redundant_items(depth_list)
    depth_list = []
    depth_list = hole_depth_list_unique.copy()

    depth_list_redunent_indices, depth_list_unique = uHelper.remove_redundant_items(depth_list_display)
    depth_list_display = []
    depth_list_display = depth_list_unique.copy()
    b2s_list = uHelper.delete_redundant_items(depth_list_redunent_indices, b2s_list)
    s2s_list = uHelper.delete_redundant_items(depth_list_redunent_indices, s2s_list)
    s2b_list = uHelper.delete_redundant_items(depth_list_redunent_indices, s2b_list)
    survey_list = uHelper.delete_redundant_items(depth_list_redunent_indices, survey_list)
    ream_list = uHelper.delete_redundant_items(depth_list_redunent_indices, ream_list)
    frictiontest_list = uHelper.delete_redundant_items(depth_list_redunent_indices, frictiontest_list)

    # could be a function
    driller_hybrid_novos_vs_dict = {}
    driller_hybrid_novos_vs_dict['HoleDepthRef'] = []
    driller_hybrid_novos_vs_dict['HoleDepth'] = []
    driller_hybrid_novos_vs_dict['B2S'] = []
    driller_hybrid_novos_vs_dict['S2S'] = []
    driller_hybrid_novos_vs_dict['S2B'] = []
    driller_hybrid_novos_vs_dict['Survey'] = []
    driller_hybrid_novos_vs_dict['BackReam'] =[]
    driller_hybrid_novos_vs_dict['FrictionTest'] =[]
       
    driller_hybrid_novos_vs_dict['HoleDepthRef'] = depth_list
    driller_hybrid_novos_vs_dict['HoleDepth'] = depth_list_display
    if not checkbox_group_3_selections:
        driller_hybrid_novos_vs_dict['B2S'] = b2s_list
        driller_hybrid_novos_vs_dict['S2S'] = s2s_list
        driller_hybrid_novos_vs_dict['S2B'] = s2b_list
        driller_hybrid_novos_vs_dict['Survey'] = survey_list
        driller_hybrid_novos_vs_dict['BackReam'] = ream_list 
        driller_hybrid_novos_vs_dict['FrictionTest'] = frictiontest_list 
    else:
        for selected in checkbox_group_3_selections:
            if selected == 'B2S':
                driller_hybrid_novos_vs_dict['B2S'] = b2s_list
            elif selected == 'S2S':
                driller_hybrid_novos_vs_dict['S2S'] = s2s_list
            elif selected == "S2B":
                driller_hybrid_novos_vs_dict['S2B'] = s2b_list
            elif selected == "Survey":
                driller_hybrid_novos_vs_dict['Survey'] = survey_list
            elif selected == "BackReam":
                driller_hybrid_novos_vs_dict['BackReam'] = ream_list
            elif selected == "Friction Test":
                driller_hybrid_novos_vs_dict['FrictionTest'] = frictiontest_list 

    if(len(driller_hybrid_novos_vs_dict['B2S']) == 0):
        driller_hybrid_novos_vs_dict['B2S'] = [0 for item in b2s_list]

    if(len(driller_hybrid_novos_vs_dict['S2S']) == 0):
        driller_hybrid_novos_vs_dict['S2S'] = [0 for item in s2s_list]

    if(len(driller_hybrid_novos_vs_dict['S2B']) == 0):
        driller_hybrid_novos_vs_dict['S2B'] = [0 for item in s2b_list]

    if(len(driller_hybrid_novos_vs_dict['Survey']) == 0):
        driller_hybrid_novos_vs_dict['Survey'] = [0 for item in survey_list]

    if(len(driller_hybrid_novos_vs_dict['BackReam']) == 0):
        driller_hybrid_novos_vs_dict['BackReam'] = [0 for item in ream_list]
    
    if(len(driller_hybrid_novos_vs_dict['FrictionTest']) == 0):
        driller_hybrid_novos_vs_dict['FrictionTest'] = [0 for item in frictiontest_list]

    depth_list_length = len(depth_list)    
    depth_list_display_length = len(depth_list_display)
    b2s_list_length =   len(b2s_list) 
    s2s_list_length =   len(s2s_list) 
    s2b_list_length =   len(s2b_list) 
    survey_list_length = len(survey_list)
    ream_list_length =  len(ream_list)
    return driller_hybrid_novos_vs_dict, depth_list_display, depth_list

@without_document_lock
def update_driller_source(driller_vs_plot, \
                          driller_vs_plot_source, \
                          driller_vs_plot_dict, \
                          display_depth_list, \
                          checkbox_group_1_selections, \
                          checkbox_group_2_selections,\
                          checkbox_group_3_selections):
    depth_list = []
    if len(driller_vs_plot_dict['HoleDepth']) > 0 :
        depth_list = driller_vs_plot_dict['HoleDepth']
        depth_list = ["{0:.2f}".format(item).rstrip('0').rstrip('.') for item in depth_list]
        depth_list = [str(x) for x in depth_list]
        driller_vs_plot_dict['HoleDepth'] = []
        driller_vs_plot_dict['HoleDepth'] = depth_list
        driller_vs_plot.x_range.factors = driller_vs_plot_dict['HoleDepth']
    else:
        depth_list = display_depth_list
        depth_list = [str(x) for x in depth_list]
        driller_vs_plot_dict['HoleDepth'] = []
        driller_vs_plot_dict['HoleDepth'] = depth_list
        driller_vs_plot.x_range.factors = driller_vs_plot_dict['HoleDepth']
        
    
    B2S_list = driller_vs_plot_dict['B2S']
    S2S_list = driller_vs_plot_dict['S2S']
    S2B_list = driller_vs_plot_dict['S2B']
    Survey_list = driller_vs_plot_dict['Survey']
    BackReam_list = driller_vs_plot_dict['BackReam']
    FrictionTest_list = driller_vs_plot_dict['FrictionTest']
    driller_vs_plot_source.data = dict(HoleDepthRef = driller_vs_plot_dict['HoleDepthRef'], \
                                    HoleDepth = driller_vs_plot_dict['HoleDepth'],\
                                    B2S = B2S_list, \
                                    S2S = S2S_list, \
                                    S2B = S2B_list, \
                                    Survey = Survey_list, \
                                    BackReam = BackReam_list, \
                                    FrictionTest = FrictionTest_list)
    connection_counts = len(depth_list)
    target_list = []
    if 1 <= connection_counts :
        target_list = np.array(B2S_list) \
                    + np.array(S2S_list) \
                    + np.array(S2B_list) \
                    + np.array(Survey_list) \
                    + np.array(BackReam_list)  \
                    + np.array(FrictionTest_list)
    target_listwithout_zero = []
    target_listwithout_zero = target_list[np.nonzero(target_list)]
    counts = len(target_listwithout_zero)
    averagetime, mediantime, besttime = uHelper.calculate_times(counts, target_listwithout_zero)
    driller_vs_plot_textbox_text = uHelper.update_plot_textbox_text(counts, averagetime, mediantime, besttime)
    x = [35, 35, 35, 35, 35, 35, 35, 35]
    y = [708, 690, 665, 645, 620, 605, 580, 560]
    uHelper.update_textbox_source(x = x, \
                                  y = y, \
                                  plot_textbox_source = uHelper.driller_vs_textbox_source, \
                                  plot_textbox_text = driller_vs_plot_textbox_text)

    x2 = [30, 30]
    y2 = [775, 750]
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
        if ((0 == connection_phase_length) or (uHelper.ALL_CONNECTION_PHASE == connection_phase_length)):
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
    vs_ckbx_textbox_text = [well_selection, connection_phase]
    uHelper.vs_ckbx_textbox_source.data = dict(x = x2, \
                                               y = y2, \
                                               txt = vs_ckbx_textbox_text) 

@without_document_lock  
def update_hybrid_source(hybrid_vs_plot, hybrid_vs_plot_source, hybrid_vs_plot_dict, display_depth_list):
    depth_list = []
    if len(hybrid_vs_plot_dict['HoleDepth']) > 0 :
        depth_list = hybrid_vs_plot_dict['HoleDepth']
        depth_list = ["{0:.2f}".format(item).rstrip('0').rstrip('.') for item in depth_list]
        depth_list = [str(x) for x in depth_list]
        hybrid_vs_plot_dict['HoleDepth'] = []
        hybrid_vs_plot_dict['HoleDepth'] = depth_list
        hybrid_vs_plot.x_range.factors = hybrid_vs_plot_dict['HoleDepth']
    else:
        depth_list = display_depth_list
        depth_list = [str(x) for x in depth_list]
        hybrid_vs_plot_dict['HoleDepth'] = []
        hybrid_vs_plot_dict['HoleDepth'] = depth_list
        hybrid_vs_plot.x_range.factors = hybrid_vs_plot_dict['HoleDepth']
        
    B2S_list = hybrid_vs_plot_dict['B2S']
    S2S_list = hybrid_vs_plot_dict['S2S']
    S2B_list = hybrid_vs_plot_dict['S2B']
    Survey_list = hybrid_vs_plot_dict['Survey']
    BackReam_list = hybrid_vs_plot_dict['BackReam']
    FrictionTest_list = hybrid_vs_plot_dict['FrictionTest']
    hybrid_vs_plot_source.data = dict(HoleDepthRef = hybrid_vs_plot_dict['HoleDepthRef'], \
                                    HoleDepth = hybrid_vs_plot_dict['HoleDepth'],\
                                    B2S = B2S_list, \
                                    S2S = S2S_list, \
                                    S2B = S2B_list, \
                                    Survey = Survey_list, \
                                    BackReam = BackReam_list, \
                                    FrictionTest = FrictionTest_list)
    connection_counts = len(depth_list)
    target_list = []
    if 1 <= connection_counts :
        target_list = np.array(B2S_list) \
                    + np.array(S2S_list) \
                    + np.array(S2B_list) \
                    + np.array(Survey_list) \
                    + np.array(BackReam_list) \
                    + np.array(FrictionTest_list)
    
    target_listwithout_zero = []
    target_listwithout_zero = target_list[np.nonzero(target_list)]
    counts = len(target_listwithout_zero)
    averagetime, mediantime, besttime = uHelper.calculate_times(counts, target_listwithout_zero)
    hybrid_vs_plot_textbox_text = uHelper.update_plot_textbox_text(counts, averagetime, mediantime, besttime)
    x = [35, 35, 35, 35, 35, 35, 35, 35]
    y = [468, 450, 425, 405, 380, 350, 335, 315]
    uHelper.update_textbox_source(x = x, \
                                  y = y, \
                                  plot_textbox_source = uHelper.hybrid_vs_textbox_source, \
                                  plot_textbox_text = hybrid_vs_plot_textbox_text)
    
@without_document_lock
def update_novos_source(novos_vs_plot, novos_vs_plot_source, novos_vs_plot_dict, display_depth_list):
    depth_list = []
    if len(novos_vs_plot_dict['HoleDepth']) > 0 :
        depth_list = novos_vs_plot_dict['HoleDepth']
        depth_list = ["{0:.2f}".format(item).rstrip('0').rstrip('.') for item in depth_list]
        depth_list = [str(x) for x in depth_list]
        novos_vs_plot_dict['HoleDepth'] = []
        novos_vs_plot_dict['HoleDepth'] = depth_list
        novos_vs_plot.x_range.factors = novos_vs_plot_dict['HoleDepth']
    else:
        depth_list = display_depth_list
        depth_list = [str(x) for x in depth_list]
        novos_vs_plot_dict['HoleDepth'] = []
        novos_vs_plot_dict['HoleDepth'] = depth_list
        novos_vs_plot.x_range.factors = novos_vs_plot_dict['HoleDepth']
        
    B2S_list = novos_vs_plot_dict['B2S']
    S2S_list = novos_vs_plot_dict['S2S']
    S2B_list = novos_vs_plot_dict['S2B']
    Survey_list = novos_vs_plot_dict['Survey']
    BackReam_list = novos_vs_plot_dict['BackReam']
    FrictionTest_list = novos_vs_plot_dict['FrictionTest']
    novos_vs_plot_source.data = dict(HoleDepthRef = novos_vs_plot_dict['HoleDepthRef'], \
                                        HoleDepth = novos_vs_plot_dict['HoleDepth'],\
                                        B2S = B2S_list, \
                                        S2S = S2S_list, \
                                        S2B = S2B_list, \
                                        Survey = Survey_list, \
                                        BackReam = BackReam_list, \
                                        FrictionTest = FrictionTest_list)
    connection_counts = len(depth_list)
    target_list = []
    if 1 <= connection_counts :
        target_list = np.array(B2S_list) \
                    + np.array(S2S_list) \
                    + np.array(S2B_list) \
                    + np.array(Survey_list) \
                    + np.array(BackReam_list) \
                    + np.array(FrictionTest_list)
    
    target_listwithout_zero = []
    target_listwithout_zero = target_list[np.nonzero(target_list)]
    counts = len(target_listwithout_zero)
    averagetime, mediantime, besttime = uHelper.calculate_times(counts, target_listwithout_zero)
    
    novos_vs_plot_textbox_text = uHelper.update_plot_textbox_text(counts, averagetime, mediantime, besttime)
    x = [35, 35, 35, 35, 35, 35, 35, 35]
    y = [218, 200, 175, 155, 130, 110, 85, 65]
    uHelper.update_textbox_source(x = x, \
                                  y = y, \
                                  plot_textbox_source = uHelper.novos_vs_textbox_source, \
                                  plot_textbox_text = novos_vs_plot_textbox_text)
    

@gen.coroutine    
def update_driller_hybrid_novos_vs_plot_source( driller_vs_plot, \
                                                driller_vs_plot_source, \
                                                hybrid_vs_plot, \
                                                hybrid_vs_plot_source, \
                                                novos_vs_plot, \
                                                novos_vs_plot_source, 
                                                driller_vs_plot_dict, \
                                                hybrid_vs_plot_dict, \
                                                novos_vs_plot_dict, \
                                                display_depth_list, \
                                                depth_ref_list, \
                                                checkbox_group_1_selections, \
                                                checkbox_group_2_selections,\
                                                checkbox_group_3_selections):
    update_driller_source(driller_vs_plot, \
                          driller_vs_plot_source, \
                          driller_vs_plot_dict, \
                          display_depth_list,\
                          checkbox_group_1_selections, \
                          checkbox_group_2_selections,\
                          checkbox_group_3_selections)
    update_hybrid_source(hybrid_vs_plot, \
                         hybrid_vs_plot_source, \
                         hybrid_vs_plot_dict, \
                         display_depth_list)
    update_novos_source(novos_vs_plot, \
                        novos_vs_plot_source, \
                        novos_vs_plot_dict, \
                        display_depth_list)

def format_dict(in_all_dict, in_sub_dict):
    in_all_dict_copy = copy.deepcopy(in_all_dict)
    sub_idx = 0
    for idx, val in enumerate(in_all_dict_copy['HoleDepth']):
        if val in in_sub_dict['HoleDepth']:
            in_all_dict['B2S'][idx] = in_sub_dict['B2S'][sub_idx]
            in_all_dict['S2S'][idx] = in_sub_dict['S2S'][sub_idx]
            in_all_dict['S2B'][idx] = in_sub_dict['S2B'][sub_idx]
            in_all_dict['Survey'][idx] = in_sub_dict['Survey'][sub_idx]
            in_all_dict['BackReam'][idx] = in_sub_dict['BackReam'][sub_idx]
            in_all_dict['FrictionTest'][idx] = in_sub_dict['FrictionTest'][sub_idx]
            sub_idx = sub_idx + 1
        else:
            in_all_dict['B2S'][idx] = 0
            in_all_dict['S2S'][idx] = 0
            in_all_dict['S2B'][idx] = 0
            in_all_dict['Survey'][idx] = 0
            in_all_dict['BackReam'][idx] = 0
            in_all_dict['FrictionTest'][idx] = 0

    return in_all_dict, in_all_dict_copy


@without_document_lock
def update_driller_hybrid_novos_vs_charts(doc,\
                                        update_driller_hybrid_novos_vs_event, \
                                        driller_vs_plot, \
                                        driller_vs_plot_source, \
                                        hybrid_vs_plot, \
                                        hybrid_vs_plot_source, \
                                        novos_vs_plot, \
                                        novos_vs_plot_source, 
                                        checkbox_group_1_selections, \
                                        checkbox_group_2_selections,\
                                        checkbox_group_3_selections, \
                                        all_connection_dict,\
                                        selected_rig, \
                                        selected_job, \
                                        from_comboBx_group):
    update_driller_hybrid_novos_vs_event.wait()
    display_depth_list = []
    display_depth_list_1 = []
    display_depth_list_2 = []
    display_depth_list_3 = []
    plot_group2_dict = {}
    plot_group2_driller_dict = {}
    plot_group2_hybrid_dict = {} 
    plot_group2_novos_dict = {}  
    plot_all_dict = {}

    if from_comboBx_group == True:
        plot_group2_dict, \
        plot_group2_driller_dict, \
        plot_group2_hybrid_dict, \
        plot_group2_novos_dict, \
        plot_group1_dict = update_checkBx_groups_dict(all_connection_dict, \
                                                            selected_rig, \
                                                            selected_job, \
                                                            checkbox_group_1_selections, \
                                                            checkbox_group_2_selections, \
                                                            connection_type_selected = 'disable')
        
        length_1 = len(plot_group2_dict[uHelper.visualization_depth_str])
        length_2 = len(plot_group2_driller_dict[uHelper.visualization_depth_str])
        length_3 = len(plot_group2_hybrid_dict[uHelper.visualization_depth_str])
        length_4 = len(plot_group2_novos_dict[uHelper.visualization_depth_str])

        plot_all_dict, display_depth_list, depth_ref_list = update_driller_hybrid_novos_vs_plot_dict(plot_group2_dict, \
                                                                                                     checkbox_group_3_selections)
        uHelper.driller_vs_plot_dict, display_depth_list_1, depth_ref_list = update_driller_hybrid_novos_vs_plot_dict(plot_group2_driller_dict,
                                                                                                            checkbox_group_3_selections)
        uHelper.hybrid_vs_plot_dict, display_depth_list_2, depth_ref_list = update_driller_hybrid_novos_vs_plot_dict(plot_group2_hybrid_dict, \
                                                                                                           checkbox_group_3_selections)
        uHelper.novos_vs_plot_dict, display_depth_list_3, depth_ref_list = update_driller_hybrid_novos_vs_plot_dict(plot_group2_novos_dict, \
                                                                                                          checkbox_group_3_selections)
        job_dict, display_depth_list, depth_ref_list = update_driller_hybrid_novos_vs_plot_dict(plot_group1_dict, \
                                                                                                     checkbox_group_3_selections)
        
    else:
        plot_group2_dict, \
        plot_group2_driller_dict, \
        plot_group2_hybrid_dict, \
        plot_group2_novos_dict, \
        plot_group1_dict = update_checkBx_groups_dict(all_connection_dict, \
                                                            selected_rig, \
                                                            selected_job, \
                                                            connection_type_selected = 'disable')
        
        length_1 = len(plot_group2_dict[uHelper.visualization_depth_str])
        length_2 = len(plot_group2_driller_dict[uHelper.visualization_depth_str])
        length_3 = len(plot_group2_hybrid_dict[uHelper.visualization_depth_str])
        length_4 = len(plot_group2_novos_dict[uHelper.visualization_depth_str])

        plot_all_dict, display_depth_list, depth_ref_list  = update_driller_hybrid_novos_vs_plot_dict(plot_group2_dict)
        uHelper.driller_vs_plot_dict, display_depth_list_1, depth_ref_list  = update_driller_hybrid_novos_vs_plot_dict(plot_group2_driller_dict)
        uHelper.hybrid_vs_plot_dict, display_depth_list_2, depth_ref_list = update_driller_hybrid_novos_vs_plot_dict(plot_group2_hybrid_dict)
        uHelper.novos_vs_plot_dict, display_depth_list_3, depth_ref_list = update_driller_hybrid_novos_vs_plot_dict(plot_group2_novos_dict)
        job_dict, display_depth_list, depth_ref_list = update_driller_hybrid_novos_vs_plot_dict(plot_group1_dict)
    temp_plot_all_dict_1 = {}
    uHelper.driller_vs_plot_dict, temp_plot_all_dict_1 = format_dict(plot_all_dict, uHelper.driller_vs_plot_dict)
    temp_plot_all_dict_2 = {}
    uHelper.hybrid_vs_plot_dict, temp_plot_all_dict_2 = format_dict(temp_plot_all_dict_1, uHelper.hybrid_vs_plot_dict) 
    temp_plot_all_dict_3 = {}
    uHelper.novos_vs_plot_dict, temp_plot_all_dict_3 = format_dict(temp_plot_all_dict_2, uHelper.novos_vs_plot_dict)
    temp_plot_all_dict_1 = {}
    temp_plot_all_dict_2 = {}
    temp_plot_all_dict_3 = {}
    plot_all_dict = {}

    display_depth_list = ["{0:.2f}".format(item).rstrip('0').rstrip('.') for item in display_depth_list]
    depth_ref_list = [str(item) for item in depth_ref_list]
    doc.add_next_tick_callback(partial(update_driller_hybrid_novos_vs_plot_source, \
                                    driller_vs_plot, \
                                    driller_vs_plot_source, \
                                    hybrid_vs_plot, \
                                    hybrid_vs_plot_source, \
                                    novos_vs_plot, \
                                    novos_vs_plot_source, 
                                    uHelper.driller_vs_plot_dict, \
                                    uHelper.hybrid_vs_plot_dict, \
                                    uHelper.novos_vs_plot_dict, \
                                    display_depth_list, \
                                    depth_ref_list, \
                                    checkbox_group_1_selections, \
                                    checkbox_group_2_selections,\
                                    checkbox_group_3_selections))
    
    
