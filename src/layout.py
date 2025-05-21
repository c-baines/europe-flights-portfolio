"""
src/layout.py

App layout

created: 19/5/25
"""

from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from src.queries import get_flight_counts_by_day, get_months_unique, get_country_emissions

choro_fig = px.choropleth(get_country_emissions(),
                    locations='iso_alpha3',
                    color='co2_qty_tonnes',
                    hover_name='state_name',
                    projection='natural earth')

layout = html.Div([
    html.Div(children=[
    html.H1("Europe Flights Portfolio"),

    dcc.Dropdown(
        id='flight-count-dropdown', 
        options=[{"label": "All data", "value": "all"}] + [{"label": m, "value": m} for m in get_months_unique()],
        value="all",
        placeholder='Select a Month'
    ),
    dcc.Graph(id='flight-count-graph')]),

    html.Div(children=[
        html.H1('Choropleth Emissions Test'),
    dcc.Graph(figure=choro_fig)
    ])

])

