"""
src/pages/about.py

About page in app

created: 20/08/25
modified: 1/9/25
"""

import dash
from dash import html

dash.register_page(__name__, path='/about', name='About', order=3)

layout = html.Div([
    html.Div([
        html.H5("About",
            style={'font-weight': 'bold'}
        ),
        html.P([
            "An interactive portfolio dashboard to track European flight, aircraft and CO",
            html.Sub("2"),
            " emissions data.",
            html.Br(),
            html.Br(),
            "This project was built as a learning exercise to increase familiarity with:",
            html.Ul([
                html.Li("Python data manipulation"),
                html.Li("SQL (PostgreSQL) and relational databases"),
                html.Li("Downloading data via APIs"),
                html.Li("Git and Github"),
                html.Li("End-to-end data pipelines"),
                html.Li("Database architecture"),
                html.Li("Data ingestion and integration"),
                html.Li("Dashboard design")
            ]),
        ]),

        html.H6("Roadmap",
            style={'font-weight': 'bold'}
        ),
        html.P([
            "☐ Host dashboard",
            html.Br(),
            "☐ Add charts tracking most common departures and destinations",
            html.Br(),
            "☐ Add update script",
            html.Br(),
            "☐ Add tooltips"
            ])
    ], className="my-container"
    )
])
