"""
src/pages/about.py

About page in app

created: 20/08/25
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/about', name='About', order=3)

layout = (
    html.Div([
        html.Div([
            html.H5("About"),
            html.P('Lorem Ipsum')
        ])
    ], className='my-container')
)