import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash_daq import DarkThemeProvider as DarkThemeProvider
from dash.dependencies import Input, Output, State
import dash
import plotly.graph_objs as go
import numpy as np
import pandas as pd

import time
from datetime import datetime

from app import app


################################################################################################################################################
# layout_base
################################################################################################################################################

layout_base = html.Div([
	html.Div(
		id="header",
		children=[
			html.H2("Paul is a snake - temperature and humidity monitor"),
			# html.A(
				# html.Img(
				# 	src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/excel/dash-daq/dash-daq-logo-by-plotly-stripe+copy.png"
				# ),
				# href="http://www.dashdaq.io",
			# ),
		],
		className="banner",
	),
	html.H4('Select past hours to plot:'),
	html.Div(
		dcc.Input(id='input_hours_to_plot',value='1', type='number')
			# options=[{'label': i, 'value': i} for i in lst_dates],
			# value=lst_dates[-1])
		),
	html.Div(
		html.Button(id='button_plot', n_clicks=0, children='Plot'),
		style={
			# "textAlign": "Center",
			# "paddingTop": "2.5%",
			"marginTop": "1%",
			},
		),
	html.Hr(),

	html.Div(id='display_date_plotted', children='Plotted past ... hours'),

	dcc.Graph(id='plot_temp'),  # displays the data,plot_humid
	dcc.Graph(id='plot_humid'),  # displays the data,plot_humid
	# Placeholder Divs
	html.Div(
		[
			html.Div(id="db_values"), # values stored in the database
		],
		style={"visibility": "hidden"},
	)


])

