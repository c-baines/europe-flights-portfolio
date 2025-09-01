"""
src/app.py

author: c-baines
created: 28/4/25
modified: 20/8/25
"""

from dash import Dash, html, page_container, page_registry
from src.callbacks import register_callbacks
import os
import dash_bootstrap_components as dbc

assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets')
app = Dash(__name__, use_pages=True, assets_folder=assets_path, external_stylesheets=[dbc.themes.BOOTSTRAP])

nav_links = dbc.Nav(
    [
        dbc.NavLink(
            page["name"],       
            href=page["path"],  
            active="exact"      
        )
        for page in page_registry.values()
    ],
    pills=True
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("European Flight Data Dashboard", className="me-4")),
                    dbc.Col(
                        dbc.Nav(
                            [
                                dbc.NavLink("Home", href="/", active="exact"),
                                dbc.NavLink("Data", href="/data", active="exact"),
                                dbc.NavLink("About", href="/about", active="exact"),
                            ],
                            navbar=True
                        )
                    ),
                ],
                align="center",
                className="g-0", 
            ),
        ],
        fluid=True,
    ),
    color="#12436D",
    dark=True,
    className="my-navbar",
)

app.layout = html.Div([
    navbar,
    html.Div(page_container)
])

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=False)


