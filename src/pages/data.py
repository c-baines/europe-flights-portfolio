"""
src/pages/data.py

Data page in app

created: 20/08/25
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/data', name='Data', order=2)


layout = (
    html.Div([
        html.Div([
            html.H5("Data"),
            html.P('Lorem Ipsum')
        ])
    ], className='my-container')
)