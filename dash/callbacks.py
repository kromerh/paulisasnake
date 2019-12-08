import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash_daq import DarkThemeProvider as DarkThemeProvider
from dash.dependencies import Input, Output, State
import dash
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from pymongo import MongoClient

import time
from datetime import datetime
import pytz

from app import app



def convertUTCtoLocalTime(timestamp):

    utc = datetime.utcfromtimestamp(timestamp/1000)

    tz = pytz.timezone('Europe/Berlin')
    now_berlin = tz.fromutc(utc)

    return pd.to_datetime(now_berlin)

def read_mongo_db(hours_to_plot=1):
	if hours_to_plot > 0:
		# Choose the appropriate client
		client = MongoClient()

		# Connect to the db paulisasnake
		db = client.paulisasnake

		# Use the collection temp and humid
		coll = db.temp_and_humid

		# Bulk inserting documents. Each row in the DataFrame will be a document in Mongo
		# coll.insert_many(data.to_dict('records'))


		entries_to_read = int(hours_to_plot * 60 * 60 / 10) # readout frequency is 10 seconds
		# ====== Finding Documents ====== #
		documents = coll.find().sort([('utc_time', -1)]).limit(entries_to_read)

		data = pd.DataFrame(list(documents))
		data = data[['utc_time', 'temp', 'humid']]
		data['time'] = data['utc_time'].apply(lambda x: convertUTCtoLocalTime(x))
		# clean data
		data = data[(data['humid']>-0.5)&(data['humid']<110)]
		data = data[(data['temp']>-40)&(data['temp']<60)]

		# print(entries_to_read,data)

		return data
	else:
		print("none")



# callback to read the database and store in a json objective
@app.callback(
	Output('db_values', 'children'),
	[Input('button_plot', 'n_clicks')],
	[State("input_hours_to_plot", "value")]
	)
def cb_read_db(n, hours_to_plot):
	df = read_mongo_db(float(hours_to_plot))  # retrieve the past 60 seconds
	return df.to_json(date_format='iso', orient='split')


@app.callback(
	Output('display_date_plotted', 'children'),
	[Input('db_values', 'children')],
	[State("input_hours_to_plot", "value")])
def display_time(json_data, hours_to_plot):
	return u'Plot for the last : {} hours'.format(hours_to_plot)


# temperature
@app.callback(
	Output("plot_temp", "figure"),
	[Input("db_values", "children")]
)
# def plot_graph_data(df, figure, command, start, start_button, PID):
def cb_plot_graph(json_data):

	# print(state_dic)
	traces = []

	try:
		data = pd.read_json(json_data, orient='split')
		data = data[['time', 'temp']]
		data = data[ data['temp'] > -9000 ]
		data = data.dropna()
		print(data.head())
		traces.append(
			go.Scatter(
				x=data['time'],
				y=data['temp'],
				line=go.scatter.Line(
					color='#42C4F7',
					# width=2.0
				),
				text='Temperature [degC]',
				# mode='markers',
				mode='lines',
				opacity=1,

				name='FP [W]'
			)
		)


	except:
		traces.append(go.Scatter(
			x=[],
			y=[],
			line=go.scatter.Line(
				color='#42C4F7',
				width=1.0
			),
			text='dose [muSv/hr]',
			# mode='markers',
			opacity=1,
			marker={
				 'size': 15,
				 'line': {'width': 1, 'color': '#42C4F7'}
			},
			mode='lines',
			name='dose [muSv/hr]'
		))

	return {
		'data': traces,
		'layout': go.Layout(
			xaxis={'title': 'Time'},
			yaxis={'title': 'Temperature [degC]', 'range':[0,40]},
			margin={'l': 100, 'b': 100, 't': 10, 'r': 10},
			legend={'x': 0, 'y': 1},
			hovermode='closest'
		)
	}


# humidity graph
@app.callback(
	Output("plot_humid", "figure"),
	[Input("db_values", "children")]
)
# def plot_graph_data(df, figure, command, start, start_button, PID):
def cb_plot_graph(json_data):

	# print(state_dic)
	traces = []

	try:
		data = pd.read_json(json_data, orient='split')
		data = data[['time', 'humid']]
		data = data[ data['humid'] > -9000 ]


		data = data.dropna()

		# print(data.head())

		traces.append(
			go.Scatter(
				x=data['time'],
				y=data['humid'],
				line=go.scatter.Line(
					color='red',
					# width=2.0
				),
				text='Humidity [%]',
				# mode='markers',
				mode='lines',
				opacity=1,

				name='RP [W]'
			)
		)


	except:
		traces.append(go.Scatter(
			x=[],
			y=[],
			line=go.scatter.Line(
				color='#42C4F7',
				width=1.0
			),
			text='dose [muSv/hr]',
			# mode='markers',
			opacity=1,
			marker={
				 'size': 15,
				 'line': {'width': 1, 'color': '#42C4F7'}
			},
			mode='lines',
			name='dose [muSv/hr]'
		))

	return {
		'data': traces,
		'layout': go.Layout(
			xaxis={'title': 'Time'},
			yaxis={'title': 'Humidity [%]', 'range':[0,100]},
			margin={'l': 100, 'b': 100, 't': 10, 'r': 10},
			legend={'x': 0, 'y': 1},
			hovermode='closest'
		)
	}