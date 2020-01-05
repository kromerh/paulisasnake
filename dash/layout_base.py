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

from callbacks import *

################################################################################################################################################
# layout_base
################################################################################################################################################

# make the dates a callback
lst_dates = read_dates_from_db()

layout_base = html.Div([

	html.Div(
        html.Img(
            src='/assets/paul.jpg',
            height=150,
            style={'paddingLeft': '30px'}
        ),
		className="two columns"
	),
	html.Div([
		html.Div(
			id="header",
			children=[

				html.H2("Paul is a snake - temperature and humidity monitor"),
				],
			className="banner",
		),
		html.H5('Select date range to query:'),
		html.Div([
			html.Div(
				[
					html.Div('Start:'),
					dcc.Dropdown(
						id='dropdown_date_start',
						options=[{'label': i, 'value': i} for i in lst_dates],
						value=lst_dates[0]
						),
				],

				className="two colums"

			),

			html.Div(
				[
					html.Div('End:'),
					dcc.Dropdown(
						id='dropdown_date_end',
						options=[{'label': i, 'value': i} for i in lst_dates],
						value=lst_dates[-1]
						),
				],

				className="two colums"
			),

			],
			className="two colums"
		),
		html.Div(
			html.Button(id='button_plot', n_clicks=0, children='Plot'),
			style={
				"marginTop": "2%",
				},
		),
		html.Hr(),

		dcc.Graph(id='plot_temp'),  # displays the data,plot_humid
		dcc.Graph(id='plot_humid'),  # displays the data,plot_humid
		# Placeholder Divs
		html.Div(
			[
				html.Div(id="values_date_start"), # date selector start date
				html.Div(id="values_date_end"), # date selector end date
				html.Div(id="values_dates"), # dates queried from the database
				html.Div(id="values_temp"), # temperature data
				html.Div(id="values_humid"), # humidity data
			],
			style={"visibility": "hidden"},
		)
	],
	className="eight columns"
	)

])

