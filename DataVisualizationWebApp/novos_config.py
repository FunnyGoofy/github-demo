# Create a polynomial line graph with those arguments
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

def update_counts(novos_config_table, novos_config_variables,  selected_job = -1):
    counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if novos_config_table.empty:
        pass
    else:
        selected_job_table = None
        if selected_job == -1: #currently, this case does not exist
            selected_job_table = novos_config_table
        else:
            job_target = []
            job_target.append(int(selected_job))
            job_target.append('')
            jobs_query = "{} in @job_target".format(uHelper.job_id_str)
            selected_job_table = novos_config_table.query(jobs_query)
        counts = []
        for item in uHelper.novos_config_variables:
            max_count = 0
            variable_table = None
            if selected_job == -1: #TODO: more logic in future
                variable_table = selected_job_table[selected_job_table['variable'] == item]
            else:
                variables_table = selected_job_table
                if variables_table.empty:
                    max_count = 0
                else:     
                    variable_table = variables_table[variables_table['variable'] == item]
                    if variable_table.empty:
                        max_count = 0
                    else:
                        max_count = variable_table['change'].max()
            counts.append(max_count)
    return counts
        
@gen.coroutine
def update_novos_config_value_and_units(novos_config_table, \
                                        selected_rig = -1, \
                                        selected_job = -1, \
                                        selected_hole_depth = -1):
    if novos_config_table.empty:
        novos_value_list = ["N/A", "N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
        novos_config_hole_depth_ft_list = ["N/A", "N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
        uHelper.novos_value_list = novos_value_list
        uHelper.novos_config_hole_depth_ft_list = novos_config_hole_depth_ft_list 
    else:
        coefficient_foot_metre = 0.3048
        country = uHelper.rig_lookup_by_country_dict[str(selected_rig)]
        selected_job_table = None
        if selected_job == -1: # this is not a case, 
            selected_job_table = novos_config_table
        else:
            selected_job_table = novos_config_table[novos_config_table['job_id'] == int(selected_job)]

        if selected_job_table.empty:
            novos_value_list = ["N/A", "N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
            novos_config_hole_depth_ft_list = ["N/A", "N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
            uHelper.novos_value_list = novos_value_list
            uHelper.novos_config_hole_depth_ft_list = novos_config_hole_depth_ft_list 
        else:
            variables_table = None
            if selected_hole_depth == -1:
                variables_table = selected_job_table
            else:
                variables_table = selected_job_table.ix[abs((round((selected_job_table['hole_depth_ft'] * coefficient_foot_metre), 2) - selected_hole_depth) <= 0.01),\
                                                 ['variable', 'value', 'units', 'hole_depth_ft', 'change']]

            uHelper.novos_value_list = []
            uHelper.novos_counts = []
            uHelper.novos_config_hole_depth_ft_list = []
            item_value = 'N/A'
            item_change = 0
            hole_depth_ft = 'N/A' 
            for item in uHelper.novos_config_variables:
                variable_table = variables_table[variables_table['variable'] == item]
                if variable_table.empty:
                    item_value = 'N/A'
                    item_change =  0
                    hole_depth_ft = 'N/A' 
                else:
                    variable_holedepth_list = variable_table['hole_depth_ft'].tolist()
                    variable_holedepth_list = list(set(variable_holedepth_list))
                    variable_holedepth_list.sort(key = float)
                    #get the last one
                    change_list = []
                    #unit_list = []
                    value_list = []
                    hole_depth_ft_list = []
                    for item in variable_holedepth_list:
                        variable_holedepth_table = variable_table[abs(variable_table['hole_depth_ft'] - float(item)) <= 0.001]
                        max_index = -1
                        change = variable_holedepth_table['change'].get_values()[max_index]
                        value = variable_holedepth_table['value'].get_values()[max_index]
                        unit = variable_holedepth_table['units'].get_values()[max_index]
                        hole_depth_ft = variable_holedepth_table['hole_depth_ft'].get_values()[max_index]
                        change_list.append(int(change))
                        value_list.append(value)
                        hole_depth_ft_list.append(hole_depth_ft)
                                       
                    index = 0
                    if selected_hole_depth == -1:
                        index = 0
                    else:
                        index = -1
                    item_value = str(value_list[index])
                    hole_depth_ft = str(hole_depth_ft_list[index])
                    item_change = str(change_list[index])

                uHelper.novos_value_list.append(item_value)
                uHelper.novos_counts.append(item_change)
                uHelper.novos_config_hole_depth_ft_list.append(hole_depth_ft)
    
    format_hole_depth_list = []
    for item in uHelper.novos_config_hole_depth_ft_list:
       if item == 'N/A':
           format_hole_depth_list.append(item)
       else:
           format_hole_depth_list.append("{0:.2f}".format(coefficient_foot_metre * float(item)).rstrip('0').rstrip('.'))
    
    uHelper.novos_config_value_and_units_source.data = dict(variable = uHelper.novos_config_variables, \
                                                            hole_depth_ft = format_hole_depth_list, \
                                                            value = uHelper.novos_value_list, \
                                                            unit = uHelper.novos_unit_list) 
    return

#@gen.coroutine         
def update_novos_config_counts(novos_config_source, novos_config_table, novos_config_variables, selected_job = -1):
    counts = update_counts(novos_config_table, novos_config_variables,  selected_job)   
    #if max_counts <= 5:
    #    uHelper.novos_config_plot.x_range.start = 5 
    #else:
    #    uHelper.novos_config_plot.x_range.start = max_counts
    novos_config_source.data = dict(x = uHelper.novos_config_variables, \
                                    hBarColors = uHelper.hBar_color_list, \
                                    counts = counts, \
                                    nclegends = uHelper.novos_config_legends)
    #max_counts = max(uHelper.novos_counts)
   
    return counts

