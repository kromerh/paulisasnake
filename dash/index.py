# -*- coding: utf-8 -*-
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


from app import app # calls the app
from apps import app_plot_temp_and_humid

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])

index_page = html.Div([
	dcc.Link('Go to temperature and humidity readout', href='/apps/app_plot_temp_and_humid'),
	html.Br()
])

# Update the index
@app.callback(Output('page-content', 'children'),
			  [Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/apps/app_plot_temp_and_humid':
		return app_plot_temp_and_humid.layout_base
	else:
		return index_page
	# You could also return a 404 "URL not found" page here

if __name__ == '__main__':
	app.run_server(debug=True, port=5000, host='0.0.0.0')
	# app.run_server(debug=True)
