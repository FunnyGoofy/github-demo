from bokeh.models import FactorRange, Spacer, Legend
from bokeh.embed import components
from bokeh.resources import INLINE
import pandas as pd
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models import ColumnDataSource, TapTool, VBar, Rect
from bokeh.models.widgets import PreText, Select, CheckboxGroup
from bokeh.models.widgets import Panel, Tabs  
from bokeh.io.state import curstate
from bokeh.resources import Resources
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
from DataVisualizationWebApp import utility as uHelper
from bokeh.layouts import widgetbox
import ctypes
import math
import asyncio
import time
from bokeh.models.widgets import DataTable, TableColumn
from DataVisualizationWebApp import novos_config
import copy

def on_server_loaded(server_context):
    ''' If present, this function is called when the server first starts. '''    
    pass

def on_server_unloaded(server_context):
    ''' If present, this function is called when the server shuts down. '''
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("on_server_unloaded")

def on_session_created(session_context):
    ''' If present, this function is called when a session is created. '''    
    import_data.retrieve_data()
    rigs_list = []
    rigs_list = [str(item) for item in uHelper.rigs_list]
    default_rig_number = ''
    if 1 <= len(rigs_list):
        default_rig_number = rigs_list[0]
    uHelper.rigs_combx = Select(title='Rigs:', value=default_rig_number, width = 120, sizing_mode = uHelper.sizing_mode, options = uHelper.update_combBx_values('', rigs_list))

    jobs_list = []
    jobs_list = [str(item) for item in uHelper.jobs_list]
    default_job_number = ''
    if 1 <= len(jobs_list):
        default_job_number = jobs_list[0]
    uHelper.default_job_number = default_job_number
    uHelper.jobs_list = jobs_list
    uHelper.jobs_combx = Select(title='Jobs:', value=default_job_number, width=120, sizing_mode = uHelper.sizing_mode, options = uHelper.update_combBx_values('', jobs_list))

    # 2. checkbox group
    uHelper.checkbox_group_1 = CheckboxGroup(labels=["Build", "Lateral", "Vertical"], \
                                             active=[], \
                                             name = 'wellSelection')

    uHelper.checkbox_group_2 = CheckboxGroup(labels=["Driller", "Novos", "Hybrid"], \
                                             active=[], \
                                             name = 'connectionType')
    
    uHelper.checkbox_group_3 = CheckboxGroup(labels=["B2S", "S2S", "S2B", "Survey", "BackReam", "Friction Test"], \
                                             active=[], \
                                             name = 'connectionPhase')
    
    rig, job = uHelper.rigs_combx.value, uHelper.jobs_combx.value

    # 1st chart
    uHelper.update_drillingconn_wellsect_queue = queue.Queue()
    uHelper.update_drillingconn_wellsect_event = threading.Event()
    update_drillingconn_wellsect_thread = Thread(name = 'update_drillingconn_wellsect_thread', \
                                                 target =  lambda q, arg1, arg2, arg3, arg4: \
                                                           q.put(drillingconn_wellsect_plot.update_well_selection_data(arg1, arg2, arg3, arg4)), \
                                                 args = (uHelper.update_drillingconn_wellsect_queue, \
                                                         uHelper.update_drillingconn_wellsect_event, \
                                                         uHelper.all_connection_dict, rig, job))
    update_drillingconn_wellsect_thread.start()
    uHelper.update_drillingconn_wellsect_event.wait()
    well_connection_colors, x, well_connnection_counts, well_connnection_data = uHelper.update_drillingconn_wellsect_queue.get()
    uHelper.well_connnection_source = ColumnDataSource(data = dict(colors = well_connection_colors, \
                                                                   x = x, \
                                                                   counts = well_connnection_counts))
    well_connection_chart = figure(x_range = FactorRange(*x), \
                                   plot_width = uHelper.plot_width, \
                                   plot_height = 430, \
                                   sizing_mode = uHelper.sizing_mode, \
                                   title = "Drilling Connection Breakdown By Well Section")
    well_connection_chart.vbar(x = 'x', \
                               width = 0.2, \
                               bottom = 0, \
                               top = 'counts', \
                               color = 'colors', \
                               source = uHelper.well_connnection_source)
    
    total_connections = sum(well_connnection_counts)
    uHelper.well_connection_textbox_source = ColumnDataSource(data = dict(x = [600,], \
                                                              y = [250,],  \
                                                              txt = ['Total Connections: %d' % (total_connections),]))
    well_connection_chart_textbox = LabelSet(x = 'x', \
                                             y = 'y', \
                                             x_units = 'screen', \
                                             y_units = 'screen', \
                                             text = 'txt', \
                                             source = uHelper.well_connection_textbox_source,\
                                             text_font_size = "12pt", border_line_color='black', \
                                             border_line_width = 1,\
                                             text_font_style = 'bold')
    well_connection_chart.add_layout(well_connection_chart_textbox)
    well_connection_chart.title.align = 'center'
    well_connection_chart.title.text_font_size = '15pt'
    well_connection_chart.toolbar.active_drag = None
    well_connection_chart.toolbar.logo = None
    well_connection_chart.toolbar_location = None
    well_connection_chart.y_range.start = 0
    well_connection_chart.x_range.range_padding = 0.1
    well_connection_chart.xaxis.major_label_orientation = 1
    well_connection_chart.xgrid.grid_line_color = None

    for well_item in well_connnection_data['well_selection']:
        for sub_item in well_connnection_data['Driller']:
            well_connection_chart.add_tools(HoverTool(tooltips=[(str(well_item), "@counts")]))
    
    ### 2nd chart(b2s s2b)    
    uHelper.update_b2s_s2b_queue = queue.Queue()
    uHelper.update_b2s_s2b_event = threading.Event()
    update_b2s_s2b_thread = threading.Thread(name = 'update_b2s_s2b_thread', \
                                             target =  lambda q, arg1, arg2, arg3, arg4: \
                                                       q.put(b2s_s2b_plot.update_b2s_s2b_data(arg1, arg2, arg3, arg4)), \
                                             args = (uHelper.update_b2s_s2b_queue, \
                                                     uHelper.update_b2s_s2b_event, \
                                                     uHelper.novos_connection_table, \
                                                     rig, \
                                                     job))
    update_b2s_s2b_thread.start()
    uHelper.update_b2s_s2b_event.wait()

    b2s_canceled_list, b2s_completed_list, \
    b2s_exception_list,b2s_failed_list, \
    s2b_canceled_list, s2b_completed_list, \
    s2b_exception_list, s2b_failed_list = uHelper.update_b2s_s2b_queue.get()

    uHelper.b2s_s2b_status = ["Canceled", "Completed", "Exception", "Failed"]
    uHelper.b2s_s2b_colors = ["#F2C80F", "#00ff0d", "#F2C80F", "#ff4600"]
    b2s_figure = figure(x_range = uHelper.b2s_connection_phase, \
                        plot_width = 600, \
                        plot_height = 430, \
                        sizing_mode = uHelper.sizing_mode, \
                        title = "Bottom to Slip")
    uHelper.b2s_datasource = ColumnDataSource(data = dict(b2s_connection_phase = uHelper.b2s_connection_phase, \
                                                          Canceled = b2s_canceled_list, \
                                                          Completed = b2s_completed_list, \
                                                          Exception = b2s_exception_list, \
                                                          Failed = b2s_failed_list))
    b2s_figure.vbar_stack(uHelper.b2s_s2b_status, \
                          x='b2s_connection_phase', \
                          width = 0.2, \
                          color = uHelper.b2s_s2b_colors, \
                          source = uHelper.b2s_datasource)
    b2s_figure.title.align = 'center'
    b2s_figure.toolbar.active_drag = None
    b2s_figure.toolbar.logo = None
    b2s_figure.toolbar_location = None
    b2s_figure.y_range.start = 0
    b2s_figure.x_range.range_padding = 0.1
    b2s_figure.xaxis.major_label_orientation = 1
    b2s_figure.xgrid.grid_line_color = None
    b2s_figure.ygrid.grid_line_color = None

    s2b_figure = figure(x_range = uHelper.s2b_connection_phase, \
                        plot_width = 670, \
                        plot_height = 430, \
                        sizing_mode = uHelper.sizing_mode, \
                        title = "Slip to Bottom")
    uHelper.s2b_datasource = ColumnDataSource(data = dict(s2b_connection_phase = uHelper.s2b_connection_phase, \
                                                          Canceled = s2b_canceled_list, \
                                                          Completed = s2b_completed_list, \
                                                          Exception = s2b_exception_list, \
                                                          Failed = s2b_failed_list))
    s2b_figure.vbar_stack(uHelper.b2s_s2b_status, \
                          x = 's2b_connection_phase', \
                          width = 0.2, \
                          color = uHelper.b2s_s2b_colors, \
                          source = uHelper.s2b_datasource, \
                          legend= [value(x) for x in uHelper.b2s_s2b_status])
    s2b_figure.title.align = 'center'
    s2b_figure.toolbar.active_drag = None
    s2b_figure.toolbar.logo = None
    s2b_figure.toolbar_location = None
    s2b_figure.y_range.start = 0
    s2b_figure.x_range.range_padding = 0.1
    s2b_figure.xaxis.major_label_orientation = 1
    s2b_figure.xgrid.grid_line_color = None
    s2b_figure.ygrid.grid_line_color = None
    s2b_figure.legend.location = "top_right"
    s2b_figure.legend.orientation = "vertical"

    new_legend = s2b_figure.legend[0]
    s2b_figure.legend[0].plot = None
    s2b_figure.add_layout(new_legend, 'right')

    line_figure = figure(x_range=(0, 100), \
                         y_range=(0, 300),  \
                         plot_width = 120, \
                         plot_height = 430)
    line_figure.line(x=[50, 50], \
                     y= [0, 300], \
                     line_width = 3, \
                     line_color='black')
    line_figure.xaxis.visible = None
    line_figure.yaxis.visible = None
    line_figure.toolbar.logo = None
    line_figure.toolbar_location = None
    line_figure.toolbar.active_drag = None
    line_figure.min_border_left = 10
    line_figure.min_border_right = 10
    line_figure.min_border_top = 0
    line_figure.min_border_bottom = 0

    mTicker = uHelper.customize_ticker()    
    
    uHelper.novos_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    uHelper.novos_config_source = ColumnDataSource(data = dict(x = uHelper.novos_config_variables, \
                                                              hBarColors = uHelper.hBar_color_list, \
                                                              counts = uHelper.novos_counts, \
                                                              nclegends = uHelper.novos_config_legends))
    
    uHelper.novos_config_plot = figure(y_range = FactorRange(*uHelper.novos_config_variables), \
                                       plot_width = 800, \
                                       plot_height = 250, \
                                       title="NOVOS Config Details", \
                                       toolbar_location = None, \
                                       tools = "", \
                                       y_axis_location = 'right', \
                                       sizing_mode = uHelper.sizing_mode, \
                                       id = "novos_config_plot_id")

    uHelper.novos_config_plot.hbar(y = 'x', \
                                   right = 0, \
                                   left = 'counts', \
                                   height = 0.5, \
                                   color = 'hBarColors', \
                                   source = uHelper.novos_config_source, \
                                   legend = 'nclegends')
    max_counts = max(uHelper.novos_counts)
    max_counts = int(max_counts)
    if max_counts <= 5:
        uHelper.novos_config_plot.x_range.start = 5 
    else:
        uHelper.novos_config_plot.x_range.start = max_counts
    uHelper.novos_config_plot.x_range.end = 0
    
    uHelper.novos_config_plot.ygrid.grid_line_color = None
    uHelper.novos_config_plot.title.align = 'center'
    uHelper.novos_config_plot.title.text_font_size = '15pt'
    uHelper.novos_config_plot.legend.location = "top_left"
    uHelper.novos_config_plot.legend.orientation = "horizontal"
    uHelper.novos_config_plot.legend.border_line_width = 0 
    uHelper.novos_config_plot.legend.border_line_color = "white"
    uHelper.novos_config_plot.legend.border_line_alpha = 0
    new_legend = uHelper.novos_config_plot.legend[0]
    uHelper.novos_config_plot.legend[0].plot = None
    uHelper.novos_config_plot.add_layout(new_legend, 'above')

    novos_config_columns = [
        TableColumn(field="variable", title="variables"),
        TableColumn(field="hole_depth_ft", title="hole depth"),
        TableColumn(field="value", title="value"),
        TableColumn(field="unit", title="unit")
    ]
    
    uHelper.novos_config_value_and_units_source = ColumnDataSource(data = dict(variable = uHelper.novos_config_variables, \
                                                                               hole_depth_ft = uHelper.novos_config_hole_depth_ft_list, \
                                                                               value = uHelper.novos_value_list, \
                                                                               unit = uHelper.novos_unit_list))
    novos_config_data_table = DataTable(source = uHelper.novos_config_value_and_units_source, \
                                        columns = novos_config_columns, \
                                        width = 500, \
                                        height = 250,
                                        sizing_mode = uHelper.sizing_mode)
    novos_config_table_plot = widgetbox(novos_config_data_table)
    novos_config.update_novos_config_counts(uHelper.novos_config_source, \
                                            uHelper.novos_config_table, \
                                            uHelper.novos_config_variables, \
                                            job)
    novos_config.update_novos_config_value_and_units(uHelper.novos_config_table, \
                                                     rig, \
                                                     job)
    
    uHelper.main_plot = figure(x_range = FactorRange(), \
                       y_range = (0, 50), \
                       plot_width = uHelper.plot_width - uHelper.conn_type_comp_txtbx_offset, \
                       plot_height = 400, \
                       tools = "tap, hover, pan, box_zoom, reset", \
                       sizing_mode = uHelper.sizing_mode, \
                       title="Overall Connection Times", \
                       tooltips = [('Duration', '@Periods'),])

    uHelper.main_plot.xaxis.ticker = mTicker
    uHelper.main_plot.title.align = 'center'
    uHelper.main_plot.legend.click_policy="hide"
    uHelper.main_plot.title.text_font_size = '15pt'
    uHelper.main_plot.xaxis.major_label_orientation = 1
    uHelper.main_plot.x_range.factors = []   
    uHelper.main_plot.toolbar.logo = None 
    uHelper.main_plot.toolbar_location = "above"
    uHelper.main_plot.css_classes = ["mainplot"] 


    uHelper.mainplot_source = ColumnDataSource(data = dict(HoleDepthRef = [], \
                                                           HoleDepth = [], \
                                                           VBarTop = [], \
                                                           VBarBottom = [], \
                                                           VBarColors = [], \
                                                           VBarType = [], \
                                                           Periods = []))     
    
    main_plot_vbars = uHelper.main_plot.vbar(x = 'HoleDepth', \
                   width = 0.1, \
                   bottom = 'VBarBottom', \
                   top = 'VBarTop', \
                   color = 'VBarColors', \
                   source = uHelper.mainplot_source, \
                   legend = 'VBarType')

    uHelper.main_plot.legend.location = "top_left"
    uHelper.main_plot.legend.orientation = "horizontal"
    uHelper.main_plot.legend.border_line_width = 0 
    uHelper.main_plot.legend.border_line_color = "white"
    uHelper.main_plot.legend.border_line_alpha = 0
    new_legend = uHelper.main_plot.legend[0]
    uHelper.main_plot.legend[0].plot = None
    uHelper.main_plot.add_layout(new_legend, 'above')

    main_textbox_plot = figure(      plot_width = uHelper.conn_type_comp_txtbx_offset, \
                                     x_range =(0, 200), \
                                     y_range = (0, 250), \
                                     plot_height = 400, \
                                     sizing_mode = uHelper.sizing_mode, \
                                     id = "main_textbox_plot_id")

    main_textbox_plot.xaxis.visible = None
    main_textbox_plot.yaxis.visible = None
    main_textbox_plot.toolbar.logo = None
    main_textbox_plot.toolbar_location = None
    main_textbox_plot.toolbar.active_drag = None
    main_textbox_plot.xgrid.grid_line_color = None
    main_textbox_plot.ygrid.grid_line_color = None
    main_textbox_plot.x_range.start = 0
    main_textbox_plot.y_range.start = 0
    main_textbox_plot.min_border_left = 0
    main_textbox_plot.min_border_right = 10
    main_textbox_plot.min_border_top = 0
    main_textbox_plot.min_border_bottom = 0

    main_textbox_plot.rect(x = 80, \
                     y = 130, \
                     width = 140, \
                     height = 140, \
                     line_color = '#666666', \
                     line_width = 2, \
                     color = "white")

    uHelper.main_plot_ckbx_txtbx_source = ColumnDataSource(data = dict(x = [30, 30], \
                                                                       y = [230, 210],  \
                                                                       txt = uHelper.plot_ckbx_textbox_text))
    main_plot_ckbx_textbox = LabelSet(x = 'x', \
                                y = 'y', \
                                text = 'txt', \
                                source = uHelper.main_plot_ckbx_txtbx_source,\
                                text_font_size = "10pt", \
                                text_font_style = 'bold')
    main_textbox_plot.add_layout(main_plot_ckbx_textbox)

    uHelper.main_plot_textbox_source = ColumnDataSource(data = dict(x = [30, 30, 30, 30, 30, 30, 30, 30], \
                                                                    y = [180, 165, 145, 130, 110, 95, 75, 60],  \
                                                                    txt = uHelper.plot_textbox_text))
    uHelper.main_textbox = LabelSet(x = 'x', \
                                y = 'y', \
                                text = 'txt', \
                                source = uHelper.main_plot_textbox_source,\
                                text_font_size = "10pt", \
                                text_font_style = 'bold')
    main_textbox_plot.add_layout(uHelper.main_textbox)

    vs_plot_textbox = figure(x_range = (0, 200), \
                             y_range = (0, 800), \
                             plot_width = uHelper.conn_type_comp_txtbx_offset, \
                             plot_height = 800, \
                             sizing_mode = uHelper.sizing_mode)
    vs_plot_textbox.xaxis.visible = None
    vs_plot_textbox.yaxis.visible = None
    vs_plot_textbox.toolbar.logo = None
    vs_plot_textbox.toolbar_location = None
    vs_plot_textbox.toolbar.active_drag = None
    vs_plot_textbox.xgrid.grid_line_color = None
    vs_plot_textbox.ygrid.grid_line_color = None
    vs_plot_textbox.x_range.start = 0
    vs_plot_textbox.y_range.start = 0
    vs_plot_textbox.min_border_left = 0
    vs_plot_textbox.min_border_right = 10
    vs_plot_textbox.min_border_top = 0
    vs_plot_textbox.min_border_bottom = 0

    uHelper.vs_ckbx_textbox_source = ColumnDataSource(data = dict(x = [30, 30], \
                                                                  y = [775, 750],  \
                                                                  txt = uHelper.plot_ckbx_textbox_text))
    vs_ckbx_text = LabelSet(x = 'x', \
                                y = 'y', \
                                text = 'txt', \
                                source = uHelper.vs_ckbx_textbox_source,\
                                text_font_size = "10pt", \
                                text_font_style = 'bold')
    vs_plot_textbox.add_layout(vs_ckbx_text)

    uHelper.driller_vs_textbox_source = ColumnDataSource(data = dict(x = [35, 35, 35, 35, 35, 35, 35, 35], \
                                                             y = [708, 690, 665, 645, 620, 605, 580, 560],  \
                                                             txt = uHelper.plot_textbox_text))
    driller_vs_text = LabelSet(x = 'x', \
                                y = 'y', \
                                text = 'txt', \
                                source = uHelper.driller_vs_textbox_source,\
                                text_font_size = "10pt", \
                                text_font_style = 'bold')
    vs_plot_textbox.add_layout(driller_vs_text)

    uHelper.hybrid_vs_textbox_source = ColumnDataSource(data = dict(x = [35, 35, 35, 35, 35, 35, 35, 35], \
                                                             y = [468, 450, 425, 405, 380, 350, 335, 315],  \
                                                             txt = uHelper.plot_textbox_text))
    hybrid_vs_text = LabelSet(x = 'x', \
                                y = 'y', \
                                text = 'txt', \
                                source = uHelper.hybrid_vs_textbox_source,\
                                text_font_size = "10pt", \
                                text_font_style = 'bold')
    vs_plot_textbox.add_layout(hybrid_vs_text)

    uHelper.novos_vs_textbox_source = ColumnDataSource(data = dict(x = [35, 35, 35, 35, 35, 35, 35, 35], \
                                                             y = [218, 200, 175, 155, 130, 110, 85, 65],  \
                                                             txt = uHelper.plot_textbox_text))
    novos_vs_text = LabelSet(x = 'x', \
                                y = 'y', \
                                text = 'txt', \
                                source = uHelper.novos_vs_textbox_source,\
                                text_font_size = "10pt", \
                                text_font_style = 'bold')
    vs_plot_textbox.add_layout(novos_vs_text)




    vs_plot_textbox.rect(x = 100, \
                     y = 640, \
                     width = 150, \
                     height = 170, \
                     line_color = '#666666', \
                     line_width = 2, \
                     color = "white")
    
    vs_plot_textbox.rect(x = 100, \
                     y = 400, \
                     width = 150, \
                     height = 170, \
                     line_color = '#666666', \
                     line_width = 2, \
                     color = "white")

    vs_plot_textbox.rect(x = 100, \
                     y = 150, \
                     width = 150, \
                     height = 170, \
                     line_color = '#666666', \
                     line_width = 2, \
                     color = "white")

    uHelper.all_novosconfig_circle_source = uHelper.create_novosconfig_all_circle_source(uHelper.novos_config_variables)   
    uHelper.create_novosconfig_circles(uHelper.main_plot, uHelper.all_novosconfig_circle_source)
      
    
    
    # layout
    uHelper.m_well_selection = Div(text='Well Section:', height=1)
    uHelper.m_well_connection = Div(text='Connection Type:', height=1)
    uHelper.m_well_conn_phase = Div(text='Connection Phase:', height=1)
    
    uHelper.version = Div(text='Version: 1.4.0', width=200, height=30)
    uHelper.version.css_classes = ["version"]
    #sidebar menu
    uHelper.spacer_1 = Spacer(width = 200, height = 10)
    uHelper.spacer_2 = Spacer(width = 200, height = 30)
    uHelper.spacer_3 = Spacer(width = 200, height = 30)

    uHelper.menu_column_1_layout = column(uHelper.spacer_3, widgetbox(uHelper.rigs_combx), widgetbox(uHelper.jobs_combx))
    uHelper.menu_column_1_layout.css_classes = ["sidebarmenucombxlayout"] 
    uHelper.well_selection_layout = column(uHelper.m_well_selection, uHelper.checkbox_group_1)
    uHelper.well_connection_layout = column(uHelper.m_well_connection, uHelper.checkbox_group_2)
    uHelper.well_conn_phase_layout = column(uHelper.m_well_conn_phase, uHelper.checkbox_group_3)
    uHelper.menu_column_2_layout = column(uHelper.well_selection_layout, uHelper.well_connection_layout, uHelper.well_conn_phase_layout)
    uHelper.menu_column_2_layout.css_classes = ["sidebarmenucheckbxlayout"] 
    uHelper.menu_middle_layout = layout(column(uHelper.menu_column_1_layout, uHelper.menu_column_2_layout))
    uHelper.menu_middle_layout.css_classes = ["sidebarmenumiddlelayout"] 
    uHelper.menu_top_layout = layout(column(uHelper.spacer_1, uHelper.version))
    uHelper.menu_top_layout.css_classes = ["sidebarmenutoplayout"] 
    uHelper.menu_bottom_layout = layout(column(uHelper.spacer_2))
    uHelper.menu_bottom_layout.css_classes = ["sidebarmenubottomlayout"] 
    
    
    uHelper.menu_layout = layout(column(uHelper.menu_top_layout, uHelper.menu_middle_layout, uHelper.menu_bottom_layout))
    uHelper.menu_layout.css_classes = ["menulayout"]

    #sub_plot
    subplot_dict = {}
    subplot_dict['rectcolors'] = []
    subplot_dict['rectheights'] = []
    subplot_dict['rectwidths'] = []
    subplot_dict['text'] = []
    subplot_dict['text_x'] = []
    subplot_dict['text_y'] = []
    subplot_dict['x'] = []
    subplot_dict['y'] = []
    
    uHelper.sub_plot_rects_source = ColumnDataSource(data = subplot_dict)
    # 3. plot     
    uHelper.sub_plot = figure(x_range = [0, 60], \
                              y_range = [0, 30], \
                              plot_width = 1540, \
                              plot_height = 350, \
                              toolbar_location = None, \
                              sizing_mode = 'scale_both')

    uHelper.sub_plot.rect(x = 'x', \
                          y = 'y', \
                          width = 'rectwidths', \
                          height = 'rectheights', \
                          color = "rectcolors", \
                          width_units = "screen", \
                          height_units = "screen", \
                          source = uHelper.sub_plot_rects_source)
    rect_text = Text(x = 'text_x', \
                     y = 'text_y', \
                     text = "text", \
                     text_font_size = "10pt")
    uHelper.sub_plot.add_glyph(uHelper.sub_plot_rects_source, rect_text)

    uHelper.sub_plot_textbox_text = ['', '', '', ''] #leave them empty strings
    uHelper.sub_plot_textbox_source = ColumnDataSource(data = dict(x = [550, 550, 550, 550], \
                                                                   y = [280, 250, 220, 190],  \
                                                                   txt = uHelper.sub_plot_textbox_text))
    uHelper.sub_plot_textbox = LabelSet(x = 'x', \
                                y = 'y', \
                                x_units = 'screen', \
                                y_units = 'screen', \
                                text = 'txt', \
                                source = uHelper.sub_plot_textbox_source,\
                                text_font_size = "12pt", \
                                text_font_style = 'bold')
    uHelper.sub_plot.add_layout(uHelper.sub_plot_textbox)

    uHelper.sub_plot.xaxis.visible = None
    uHelper.sub_plot.yaxis.visible = None
    uHelper.sub_plot.background_fill_color = "white"
    uHelper.m_color_white = uHelper.sub_plot.background_fill_color
    uHelper.sub_plot.outline_line_color = None
    uHelper.sub_plot.title.align = 'center'
    uHelper.sub_plot.title.text_font_size = '15pt'
    
    drillingConnectionBreakdown_column = column(well_connection_chart)
    drillingConnectionBreakdown_column.sizing_mode = uHelper.sizing_mode
    drillingConnectionBreakdown_layout = layout(drillingConnectionBreakdown_column, sizing_mode = uHelper.sizing_mode)   
    activity_type_stats_top = row(b2s_figure, line_figure, s2b_figure)
    uHelper.novos_config_row = row(uHelper.novos_config_plot, novos_config_table_plot)
    uHelper.spacer_5 = Spacer(width = uHelper.plot_width - uHelper.conn_type_comp_txtbx_offset, height = 2)
    main_plot_column_1 = column(uHelper.main_plot, uHelper.spacer_5)
    main_plot_row = row(main_plot_column_1, main_textbox_plot)
    over_conn_analysis_column = column(uHelper.novos_config_row, main_plot_row, uHelper.sub_plot)
    over_conn_analysis_column.sizing_mode = uHelper.sizing_mode
    summary_layout = layout(column(activity_type_stats_top))
    right_layout = layout(over_conn_analysis_column, sizing_mode = uHelper.sizing_mode)
    
    tabMain = Panel(title='Main', child=drillingConnectionBreakdown_layout)
    tabMain.tags=["MainTag"]
    tabMain.name="MainName"

    tabOverConnectionAnalysis = Panel(child = right_layout, title = 'Over Connection Analysis')
    tabOverConnectionAnalysis.name="OverConnectionAnalysisName"
    tabOverConnectionAnalysis.tags=["OverConnectionAnalysisTag"]
    
    uHelper.driller_vs_plot = figure(x_range=FactorRange(), \
                                     y_range = (0, 50), \
                                     plot_width = uHelper.plot_width - uHelper.conn_type_comp_txtbx_offset, \
                                     plot_height = 250, \
                                     tools = "tap, pan, box_zoom, reset",\
                                     sizing_mode = uHelper.sizing_mode)
       
    uHelper.driller_vs_dataset, driller_vs_display_depth_list = all_main_plot.get_all_dataset(uHelper.all_connection_dict)
    driller_vs_display_depth_list = [str(x) for x in driller_vs_display_depth_list]
   
    uHelper.driller_vs_plot.toolbar.logo = None 
    uHelper.driller_vs_plot.toolbar_location = "above"
    uHelper.driller_vs_plot.css_classes = ["DrillerVSPlot"] 
    uHelper.driller_vs_plot.xaxis.ticker = mTicker
    uHelper.driller_vs_plot.title.align = 'center'
    uHelper.driller_vs_plot.legend.click_policy="hide"
    uHelper.driller_vs_plot.xaxis.major_label_orientation = 1
    uHelper.driller_vs_plot.x_range.factors = []
    uHelper.driller_vs_plot.yaxis.axis_label = "Driller"
    uHelper.driller_vs_plot.axis.axis_label_text_font_style = "bold"

    uHelper.driller_vs_plot_source = ColumnDataSource(data=dict(HoleDepthRef = [], \
                                                             HoleDepth = [],\
                                                             B2S = [], \
                                                             S2S = [], \
                                                             S2B = [], \
                                                             Survey = [], \
                                                             BackReam = [], \
                                                             FrictionTest = []))
    
    driller_vs_plot_vbars = uHelper.driller_vs_plot.vbar_stack(uHelper.connection_phase_list,\
                                                               x = 'HoleDepth', \
                                                               width = 0.1, \
                                                               color = uHelper.color_list, \
                                                               source = uHelper.driller_vs_plot_source, \
                                                               legend = [value(x) for x in uHelper.connection_phase_list])
    uHelper.driller_vs_plot.legend.location = "top_left"
    uHelper.driller_vs_plot.legend.orientation = "horizontal"
    uHelper.driller_vs_plot.legend.border_line_width = 0 
    uHelper.driller_vs_plot.legend.border_line_color = "white"
    uHelper.driller_vs_plot.legend.border_line_alpha = 0
    driller_vs_new_legend = uHelper.driller_vs_plot.legend[0]
    uHelper.driller_vs_plot.legend[0].plot = None
    uHelper.driller_vs_plot.add_layout(driller_vs_new_legend, 'above')

    uHelper.hybrid_vs_plot = figure(x_range = uHelper.driller_vs_plot.x_range, \
                                   y_range = uHelper.driller_vs_plot.y_range, \
                                   plot_width = uHelper.plot_width - uHelper.conn_type_comp_txtbx_offset, \
                                   plot_height = 250, \
                                   tools = "tap, pan, box_zoom, reset", \
                                   sizing_mode = uHelper.sizing_mode)    
    
    uHelper.hybrid_vs_plot.toolbar.logo = None 
    uHelper.hybrid_vs_plot.toolbar_location = "above"
    uHelper.hybrid_vs_plot.css_classes = ["HybridVSPlot"] 
    uHelper.hybrid_vs_plot.xaxis.ticker = mTicker
    uHelper.hybrid_vs_plot.title.align = 'center'
    uHelper.hybrid_vs_plot.xaxis.major_label_orientation = 1
    uHelper.hybrid_vs_plot.x_range.factors = []
    uHelper.hybrid_vs_plot.x_range.factors = driller_vs_display_depth_list
    uHelper.hybrid_vs_plot.yaxis.axis_label = "Hybrid"
    uHelper.hybrid_vs_plot.axis.axis_label_text_font_style = "bold"
    uHelper.hybrid_vs_plot_source = ColumnDataSource(data=dict(HoleDepthRef = [], \
                                                             HoleDepth = [],\
                                                             B2S = [], \
                                                             S2S = [], \
                                                             S2B = [], \
                                                             Survey = [], \
                                                             BackReam = [])) 
    hybrid_vs_plot_vbars = uHelper.hybrid_vs_plot.vbar_stack(uHelper.connection_phase_list,\
                                                               x = 'HoleDepth', \
                                                               width = 0.1, \
                                                               color = uHelper.color_list, \
                                                               source = uHelper.hybrid_vs_plot_source)
    
    uHelper.novos_vs_plot = figure(x_range = uHelper.driller_vs_plot.x_range, \
                                   y_range = uHelper.driller_vs_plot.y_range, \
                                   plot_width = uHelper.plot_width - uHelper.conn_type_comp_txtbx_offset, \
                                   plot_height = 250, \
                                   tools = "tap, pan, box_zoom, reset", \
                                   sizing_mode = uHelper.sizing_mode)   
    
    uHelper.novos_vs_plot.css_classes = ["NovosVSPlot"] 
    uHelper.novos_vs_plot.xaxis.ticker = mTicker
    uHelper.novos_vs_plot.title.align = 'center'
    uHelper.novos_vs_plot.xaxis.major_label_orientation = 1
    uHelper.novos_vs_plot.x_range.factors = []
    uHelper.novos_vs_plot.x_range.factors = driller_vs_display_depth_list   
    uHelper.novos_vs_plot.yaxis.axis_label = "NOVOS"
    uHelper.novos_vs_plot.axis.axis_label_text_font_style = "bold"

    uHelper.novos_vs_plot_source = ColumnDataSource(data=dict(HoleDepthRef = [], \
                                                             HoleDepth = [],\
                                                             B2S = [], \
                                                             S2S = [], \
                                                             S2B = [], \
                                                             Survey = [], \
                                                             BackReam = [])) 
    novos_vs_plot_vbars = uHelper.novos_vs_plot.vbar_stack(uHelper.connection_phase_list,\
                                                               x = 'HoleDepth', \
                                                               width = 0.1, \
                                                               color = uHelper.color_list, \
                                                               source = uHelper.novos_vs_plot_source)
       
    vs_driller_hybrid_novos_gridplot = gridplot([[uHelper.driller_vs_plot], [uHelper.hybrid_vs_plot], [uHelper.novos_vs_plot]], \
                                                toolbar_location = "above", \
                                                toolbar_options = dict(logo = None))    
    vs_driller_hybrid_novos_gridplot.sizing_mode = uHelper.sizing_mode    
    spacer_6 = Spacer(width = uHelper.plot_width - uHelper.conn_type_comp_txtbx_offset, height = 10)
    vs_plot_textbox_column = column(spacer_6, vs_plot_textbox)
    vs_plot_textbox_column.sizing_mode = uHelper.sizing_mode
    vs_driller_hybrid_novos_row = row(vs_driller_hybrid_novos_gridplot, vs_plot_textbox_column)
    vs_driller_hybrid_novos_layout = layout(vs_driller_hybrid_novos_row, sizing_mode = uHelper.sizing_mode) 
    vsDrillerHybridNOVOS = Panel(child = vs_driller_hybrid_novos_layout, title = "Driller vs Hybrid vs Novos")
    vsDrillerHybridNOVOS.name = "vsDrillerHybridNOVOSName"
    vsDrillerHybridNOVOS.tags = ["vsDrillerHybridNOVOSTag"]
   
    tabActivitytypeStats = Panel(child = summary_layout, title = "Activity type Stats")
    tabActivitytypeStats.name = "ActivitytypeStatsName"
    tabActivitytypeStats.tags = ["ActivitytypeStatsTag"]

    p6 = figure(plot_width=uHelper.plot_width, plot_height=900, toolbar_location=None)
    p6.text([65,65,65],[65,65,65], text=[ "Coming Soon"], alpha=0.5, text_font_size="50pt", text_baseline="middle", text_align="center")
    p6.xaxis.visible = None
    p6.yaxis.visible = None
    p6.background_fill_color = "white"
    p6.outline_line_color = None
    tabDistributioncharts = Panel(child=p6, title="Distribution charts")
    tabDistributioncharts.name="DistributionchartsName"
    tabDistributioncharts.tags=["DistributionchartsTag"]

    about_div = Div(text="""<p> Data Visualization <br> 
                            Copyright 2018 Precision Drilling Corporation. All rights reserved.<br> 
                            Version 1.3.0(Official Build)<br>
                            <br>
                            <h3>Technical Support</h3>
                            <h4>Email:</h4>
                            <ul style="list-style-type:square">
                                 <li>KFransisco@precisiondrilling.com</li>
                                 <li>peng.wang@precisiondrilling.com</li>
                            </ul>
                            <h4>Phone:</h4>
                            <ul style="list-style-type:square">
                              <li>403-716-4704</li>
                              <li>403-716-4631</li>
                            </ul>
                            <h4>Release Note:</h4>
                              <ul style="list-style-type:square">
                                <li>--- 1.4.0 ---</li>                              
                                <ul style="list-style-type:lower-alpha">
                                   <li>Added "Friction Test" feature <br></li>
                                   <li>Linked toolbar on "Driller vs Hybrid vs Novos"<br></li>
                                </ul>
                                <li>--- 1.3.0 ---</li>                              
                                <ul style="list-style-type:lower-alpha">
                                   <li>Added "connection statistics" textboxes and legends <br></li>
                                   <li>Made "connection statistics" dynamically update based options from those checkboxes on the left sidebar <br></li>
                                   <li>Modified B2S and S2B UI when user clicks stackedbar on "Over Connection Analysis" <br></li>
                                   <li>Added legends on "NOVOS Config Detail" <br></li>
                                   <li>Cut off extra "Hole Depth" on x-axis ("Over Connection Times") <br></li>
                                   <li>Displyed rects if "Connection Type" is "Driller"</li>
                                   <li>Added Tooltips on stackedbar ("Over Connection Times")</li>
                                   <li>Changed "Double click to "Single Click", if user wants to hide "NOVOS Activities" </li>
                                </ul>
                              </ul>
                              <ul style="list-style-type:square">
                                <li>--- 1.2.0 ---</li>
                                <ul style="list-style-type:lower-alpha">
                                    <li>Merged novos config feature <br></li>
                                </ul>
                              </ul>
                              <ul style="list-style-type:square">
                                <li>--- 1.1.0 ---</li>
                                <ul style="list-style-type:lower-alpha">
                                    <li>Added "Driller vs Hybrid vs Novos" tab <br></li>
                                    <li>Moved mainplot from "Main" tab to "Over Connection Analysis" Tab</li>
                                    <li>Deleted "Continuous in Depth" and "Driller vs Novos" tabs</li>
                                    <li>"Connection Type" Checklist is greyed out, when "Driller vs Hybrid vs Novos" tab is activated</li>
                                    <li>Colors are now consistent with what we have in "PowerBI"</li>
                                    <li>"Wheel zoom" is removed from  plot "tool bar"</li>
                                    <li>Display the latest dataset, whenever user clicks "Reload this page" from browser</li>
                                </ul>
                              </ul>
                            </p>""",
                     width=uHelper.plot_width, height=900)
    about_div.css_classes = ["aboutDiv"] 
    tabAboutPanel = Panel(child = about_div, title = "About", width = uHelper.plot_width, height = 900)
    tabAboutPanel.name="AboutPanelName"
    tabAboutPanel.tags=["AboutPanelTag"]


    uHelper.tabs = Tabs(tabs = [tabMain, \
                      tabOverConnectionAnalysis, \
                      vsDrillerHybridNOVOS, \
                      tabActivitytypeStats, \
                      tabDistributioncharts, \
                      tabAboutPanel], width= uHelper.plot_width, sizing_mode='scale_width')
    
    uHelper.tabs.css_classes = ["tabsbackgroundcolorblack"]

    uHelper.spacer_4 = Spacer(width = 120, height = 350)
    uHelper.sidebar_layout = layout(column(uHelper.menu_layout, uHelper.spacer_4))
    uHelper.sidebar_layout.css_classes = ["sidebarlayout"] 
    tabs_row = row(uHelper.tabs)
    tabs_row.sizing_mode = uHelper.sizing_mode
    main_row = row(uHelper.sidebar_layout, tabs_row)
    main_row.sizing_mode = uHelper.sizing_mode
    uHelper.main_row = main_row
    uHelper.main_row.css_classes = ["mainrowlayout"] 
    uHelper.main_layout = layout(uHelper.main_row, sizing_mode = 'scale_width')# uHelper.sizing_mode)
    uHelper.main_layout.css_classes = ["mainlayout"]
    
    main_plot_vbars.data_source.on_change('selected', uHelper.update_sub_plot)

def on_session_destroyed(session_context):
    ''' If present, this function is called when a session is closed. '''
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("on_session_destroyed")

