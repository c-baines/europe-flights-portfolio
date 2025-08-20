"""
src/pages/home.py

App home page with html layout

created: 19/5/25
modified: 20/8/25
"""

import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from src.queries import get_flight_counts_by_day, get_months_unique, get_country_emissions, get_year_emissions, get_month_emissions, STARTUP_QUERIES
import plotly.graph_objects as go
from statistics import mean
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Home', order=1)

layout = html.Div([
       # Flights overview container
    html.Div([
        html.H5("Flight History",
                style={'font-weight': 'bold'}
        ),

        dcc.Dropdown(
            id='flight-count-dropdown',
            options=[{"label": "All data", "value": "all"}] + [{"label": m, "value": m} for m in get_months_unique()],
            value="all",
            clearable=False,
            className='my-dropdown'
        ),

        dcc.Graph(id="card"),
        dcc.Graph(id='flight-count-graph')
    ], className="my-container"),

    # Airlines + manufacturers container
    html.Div([
        html.H5('Airlines and Aircraft',
                style={'font-weight': 'bold'}
        ),

        dcc.Dropdown(
            id='airlines-dropdown',
            options=[{"label": "All years", "value": "all"}] + [{"label": y, "value": y} for y in sorted(STARTUP_QUERIES.TOP_AIRLINES_DF['year'].unique())],
            value='all',
            clearable=False,
            className='my-dropdown'
        ),

        dcc.Graph(id='airlines-bar-graph'),
        dcc.Graph(id='manufacturer-percent-graph')
    ], className="my-container"),

    # Emissions container
    html.Div([
        html.H5('Flight Emissions',
                style={'font-weight': 'bold'}
        ),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='choropleth-dropdown-year',
                    options=[{"label": "All years", "value": "all"}] + [{"label": y, "value": y} for y in get_year_emissions()],
                    value="all",
                    clearable=False,
                    className='my-dropdown'
                )
            ], className="dropdown-container"),

            html.Div([
                dcc.Dropdown(
                    id='choropleth-dropdown-month',
                    options=[{"label": "All months", "value": "all"}] + [{"label": m, "value": m} for m in get_month_emissions()],
                    value="all",
                    clearable=False,
                    className='my-dropdown'
                )
            ], className="dropdown-container")
        ]),

        dcc.Graph(id='emissions-choropleth')
    ], className="my-container")
])
