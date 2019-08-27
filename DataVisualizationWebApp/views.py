"""
Routes and views for the flask application.
"""

from datetime import datetime
from DataVisualizationWebApp  import bk_plotter as bk_plter
from flask import Flask, render_template, request
from DataVisualizationWebApp import app
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop
import timeit
from bokeh.application.handlers import Handler
from DataVisualizationWebApp import server_lifecycle

#paramater
@app.route('/', methods=['GET'])
def bkapp_page():
    """Renders the home page.""" 
    url="http://10.1.8.9:5006/bk_plotter"
    script = server_document(url=url)
    return render_template("embed.html", script=script, template="Flask")

@app.route('/contact')
def contact():
    return bk_plter.plot_html()
    
@app.route('/about')
def about():
    return bk_bar__stacked_plter.plot_bar_stacked()

def bk_worker():
    server = Server({'/bk_plotter': bk_plter.plot_doc}, io_loop=IOLoop(), allow_websocket_origin=["10.1.8.9:80"], websocket_max_message_size = 9999999999 * 1024 * 1024)
    server.start()
    Handler.on_server_loaded = server_lifecycle.on_server_loaded(server)	
    server.io_loop.start()

       