"""
src/layout.py

App html layout

created: 19/5/25
modified: 19/8/25
"""

from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from src.queries import get_flight_counts_by_day, get_months_unique, get_country_emissions, get_year_emissions, get_month_emissions, STARTUP_QUERIES
import plotly.graph_objects as go
from statistics import mean
import dash_bootstrap_components as dbc


navbar = dbc.NavbarSimple(
    brand="Europe Flights Portfolio Project",
    color="#12436D",
    dark=True,
    fluid=True,    
    style={"padding-top": "20px", "padding-bottom": "20px"}  

)

layout = html.Div([
    navbar,

    # Flights overview container
    html.Div([
        html.H3("Flight History"),

        dcc.Dropdown(
            id='flight-count-dropdown',
            options=[{"label": "All data", "value": "all"}] + [{"label": m, "value": m} for m in get_months_unique()],
            value="all",
            clearable=False,
            className='my-dropdown'
        ),

        dcc.Graph(id="card"),
        dcc.Graph(id='flight-count-graph')
    ], style={
        "backgroundColor": "white",
        "borderRadius": "12px",
        "padding": "20px",
        "margin": "20px",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.15)"
    }),

    # Airlines + manufacturers container
    html.Div([
        html.H3('Airlines and Aircraft'),

        dcc.Dropdown(
            id='airlines-dropdown',
            options=[{"label": "All years", "value": "all"}] + [{"label": y, "value": y} for y in sorted(STARTUP_QUERIES.TOP_AIRLINES_DF['year'].unique())],
            value='all',
            clearable=False,
            className='my-dropdown'
        ),

        dcc.Graph(id='airlines-bar-graph'),
        dcc.Graph(id='manufacturer-percent-graph')
    ], style={
        "backgroundColor": "white",
        "borderRadius": "12px",
        "padding": "20px",
        "margin": "20px",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.15)"
    }),

    # Emissions container
    html.Div([
        html.H3('Flight Emissions'),

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
    ], style={
        "backgroundColor": "white",
        "borderRadius": "12px",
        "padding": "20px",
        "margin": "40px",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.15)"
    })
])
