"""
src/app.py

author: c-baines
created: 28/4/25
modified: 20/8/25
"""

from dash import Dash, html, page_container, page_registry
# from src.pages.home import layout
from src.callbacks import register_callbacks
import os
import dash_bootstrap_components as dbc

assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets')
app = Dash(__name__, use_pages=True, assets_folder=assets_path, external_stylesheets=[dbc.themes.BOOTSTRAP])

nav_links = dbc.Nav(
    [
        dbc.NavLink(
            page["name"],       # Display name
            href=page["path"],  # URL path
            active="exact"      # highlight only when exact match
        )
        for page in page_registry.values()
    ],
    pills=True
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            # Left-aligned row with brand + nav
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Europe Flights Portfolio", className="me-4")),
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
                className="g-0",  # remove gutter spacing
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
    app.run(debug=True)


