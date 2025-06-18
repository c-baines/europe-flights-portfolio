"""
src/layout.py

App layout

created: 19/5/25
modified: 16/6/25
"""

from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from src.queries import get_flight_counts_by_day, get_months_unique, get_country_emissions, get_year_emissions, get_month_emissions, STARTUP_QUERIES

layout = html.Div([
    # number of flights line graph
    html.Div(children=[
    html.H1("Flight Counts"),
    dcc.Dropdown(
        id='flight-count-dropdown', 
        options=[{"label": "All data", "value": "all"}] + [{"label": m, "value": m} for m in get_months_unique()],
        value="all",
        placeholder='Select a Month'
    ),
    # flight count decomposed cards
    dcc.Graph(
        id="card"
    ),
    dcc.Graph(id='flight-count-graph')]),

    # emissions heatmap
    html.Div(children=[
    html.H1('Choropleth Emissions Test'),
    dcc.Dropdown(
        id='choropleth-dropdown-year',
        options=[{"label": "All years", "value": "all"}] + [{"label": y, "value": y} for y in get_year_emissions()],
        value="all",
        placeholder='Year'
    ),
    dcc.Dropdown(
        id='choropleth-dropdown-month',
        options=[{"label": "All months", "value": "all"}] + [{"label": m, "value": m} for m in get_month_emissions()],
        value="all",
        placeholder='Month'
    ),
    dcc.Graph(id='emissions-choropleth')
    ]),

    # airlines bar graphs
    html.Div(children=[
        html.H1('Airlines'),
        dcc.Dropdown(
            id='bar-dropdown',
            options=[{"label": "All years", "value": "all"}] + [{"label": y, "value": y} for y in STARTUP_QUERIES.TOP_AIRLINES_DF['year'].unique().tolist()],
            value='all',
            placeholder='Year' 
        ),
        dcc.Graph(id='airlines-bar-graph')
    ])

])

