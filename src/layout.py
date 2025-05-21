"""
src/layout.py

created: 19/5/25
"""

from dash import html, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from src.queries import get_flight_counts_by_day, get_months_unique

layout = html.Div([
    html.H1("Europe Flights Portfolio"),
    dcc.Dropdown(
        id='flight-count-dropdown', 
        options=[{"label": "All data", "value": "all"}] + [{"label": m, "value": m} for m in get_months_unique()],
        value="all",
        placeholder='Select a Month'
    ),
    dcc.Graph(id='flight-count-graph')

])

