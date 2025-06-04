"""
src/app.py

author: c-baines
created: 28/4/25
modified: 21/5/25
"""

from dash import Dash
from src.layout import layout
import plotly.express as px
from src.callbacks import register_callbacks

app = Dash(__name__)
app.layout = layout
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)


