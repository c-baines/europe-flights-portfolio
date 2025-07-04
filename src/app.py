"""
src/app.py

author: c-baines
created: 28/4/25
modified: 4/7/25
"""

from dash import Dash
from src.layout import layout
from src.callbacks import register_callbacks
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(current_dir, '..', 'assets')

app = Dash(__name__, assets_folder=assets_path)
app.layout = layout
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)


