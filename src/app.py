"""
src/app.py

author: c-baines
created: 28/4/25
modified: 5/8/25
"""

from dash import Dash
from src.layout import layout
from src.callbacks import register_callbacks
import os
import dash_bootstrap_components as dbc

assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets')
app = Dash(__name__, assets_folder=assets_path, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = layout
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)


