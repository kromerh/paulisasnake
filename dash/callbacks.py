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

from app import app


# Choose the appropriate client
client = MongoClient()

# Connect to the db
db = client.paulisasnake

def read_dates_from_db(db=db):
	"""
	Gets the list of dates available in the temperature storage table and returns the list.
	"""

	# Use the collection
	coll = db.temp_storage

	agg = coll.aggregate([
	    {"$group": {
	        "_id" : { "$concat": [
	            {"$substr": [{"$year": "$time"}, 0, 4 ]},
	            "-",
	            {"$substr": [{"$month": "$time"}, 0, 2 ]},
	            "-",
	            {"$substr": [{"$dayOfMonth": "$time"}, 0, 2 ]},
	        ]},
	        "count": {"$sum": 1 }
	     }},
	     {"$sort": { "_id": 1 }}
	])

	dates = {}
	# conver mongo object to dictionary
	for x in agg:
	    d  = x['_id'] # this date in the object
	    c = x['count']# how many counts for that day
	    dates[d] = c



	# convert to list
	lst_dates = dates.keys()
	print(lst_dates)
	return lst_dates


def read_temp_from_db(start_date, end_date, db=db):
	"""
	Reads the temperature collection from start_date to end_date and returns the temperature.
	"""


	# Use the collection
	coll = db.temp_storage

	# query the mongo database
	# select data

	data = data[['time', 'temp']]
	# return


def read_humid_from_db(db, start_date,end_date):
	"""
	Reads the humidity collection from start_date to end_date and returns the humidity.
	"""


	# Use the collection
	coll = db.temp_storage

	# query the mongo database
	# select data

	data = data[['time', 'humid']]
	# return




# callback to update date range start value
@app.callback(
	Output('values_date_start', 'children'),
	[Input('dropdown_date_start', 'value')])
def update_values_date_start(value):
	print(f'Start date: {value}')
	return value

# callback to update date range end value
@app.callback(
	Output('values_date_end', 'children'),
	[Input('dropdown_date_end', 'value')])
def update_values_date_end(value):
	print(f'End date: {value}')
	return value


# callback to get available dates from the database
# in this callback the dates of the start and end date range must be set


# callback to update end dates from the database to be larger than the start dates only
@app.callback(
	Output('dropdown_date_end', 'options'),
	[Input('values_date_start', 'children')],
	[State('dropdown_date_start', 'options')])
def update_values_date_end_based_on_start(value_date_start, date_start_options):
	lst_date_start_options = [d['value'] for d in date_start_options] # list of the options in the start date dropdown

	# get the index of the start date in the list
	idx = lst_date_start_options.index(value_date_start)

	# select only later start dates (by index)
	date_end_options = lst_date_start_options[idx:]


	# make it a dropdown object
	date_end_options = [{'label': i, 'value': i} for i in date_end_options]

	return date_end_options


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
		# print(data.head())
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