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

@app.callback(
	Output('display_date_plotted', 'children'),
	[Input('button-plot-historical', 'n_clicks')])
def set_date_to_be_plotted(n_clicks):
	return u'Plotted past hours'