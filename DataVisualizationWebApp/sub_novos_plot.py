import flask
from bokeh.models import FactorRange, Spacer
from bokeh.embed import components
from bokeh.plotting import figure, curdoc
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import pandas as pd
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models import ColumnDataSource, TapTool, VBar, Rect
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
from DataVisualizationWebApp import utility as uHelper
from bokeh.document import without_document_lock

subplot = None
subplot_source  = None
subplot_dict = None
depth_ft_str = "edr_depth_ft"

@without_document_lock
def create_sub_plot(doc):
    global subplot
    global subplot_source
    global subplot_dict 

    subplot_dict = {}
    subplot_dict['B2SText'] = ['Cleanhole - Active', 'Cleanhole - Completed', 'Setboxheight - Active', 'Setboxheight - Completed', 'Setweight - Active', 'Setweight - Completed', 'Offbottom-Active', 'Unweightbit - Active', 'Unweightbit - Completed', 'Clearbit - Active', 'Clearbit - Completed', 'Offbottom - Completed']
    subplot_dict['text_x'] = [2, 12, 22, 32, 42, 52, 2, 12, 22, 32, 42, 52]
    subplot_dict['B2SColors'] = ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']
    subplot_dict['B2STextColors'] = ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black']
    subplot_dict['B2SHideColors'] = ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']
    subplot_dict['subplot_x'] = [5, 15, 25, 35, 45, 55, 5, 15, 25, 35, 45, 55]
    subplot_dict['subplot_y'] = [10, 10, 10, 10, 10, 10, 25, 25, 25, 25, 25, 25]
    subplot_dict['B2SArrowColors'] = ['#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0']
    subplot_dict['ArrowStartX'] = [10, 18, 26, 34, 42, 42, 10, 18, 26, 34, 42, 42]
    subplot_dict['ArrowEndX'] = [12, 20, 28, 36, 44, 44, 12, 20, 28, 36, 44, 44]
    subplot_dict['ArrowY'] = [20, 20, 20, 20, 20, 20, 25, 25, 25, 25, 25, 25]
    subplot_dict['arrow_end_y'] = [20, 20, 20, 20, 20, 20, 25, 25, 25, 25, 25, 25]
    subplot_dict['Text'] = ['', '', '', '','', '', '', '','', '', '', '']
    
    
    uHelper.sub_plot_rects_source = ColumnDataSource(data=subplot_dict)
    doc.add_root(uHelper.sub_plot_rects_source)
    # 3. plot     
    uHelper.subplot = figure(x_range = [0, 60], y_range = [0, 30], \
                     plot_width=1540, plot_height= 350, \
                     toolbar_location=None, \
                     sizing_mode='scale_both')
    subplot_height = 40
    subplot_weight = 175

    subplot.rect(x='subplot_x', y='subplot_y', width=subplot_weight, height=subplot_height, color="B2SColors",
          width_units="screen", height_units="screen", source = uHelper.sub_plot_rects_source)
    b2s_text = Text(x='text_x', y='subplot_y', text_color="B2STextColors", text="Text", text_font_size="10pt")
    subplot.add_glyph(uHelper.sub_plot_rects_source, b2s_text)
    
    subplot.xaxis.visible = None
    subplot.yaxis.visible = None
    subplot.background_fill_color = "white"
    m_color_white = subplot.background_fill_color
    subplot.outline_line_color = None
    doc.add_root(subplot)
    return subplot, uHelper.sub_plot_rects_source, subplot_dict

m_selected_index_code = """
    selection = require("core/util/selection")
    indices = selection.get_indices(allSource)
    
    console.log('------------- javascript ----------------------')
    console.log(indices.length)

    for (i = 0; i < indices.length; i++) 
    {
        console.log('------------- enter 1st loop ----------------------')

        ind = indices[i]
        console.log(ind)
        console.log(' +++++++++++++++++++++++++++++++++++++++++ ')
        selectedVbarIndexSource.data['index'][0] = ind
        console.log(ind)
        console.log('-------------     ----------------------')
        console.log(selectedVbarIndexSource.data['index'][0])
        index2[0] = ind
        selectedVbarIndexSource.change.emit()
        break   
     }
"""
