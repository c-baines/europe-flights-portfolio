"""
src/callbacks.py

created: 19/5/25
"""
from dash import Input, Output, callback
from src.queries import STARTUP_QUERIES
import plotly.express as px

def register_callbacks(app): 

    @app.callback(
            Output('flight-count-graph', 'figure'),
            Input('flight-count-dropdown', 'value')
    )
    def update_month_dropdown(month_string):

        df = STARTUP_QUERIES.FL_COUNT_BY_DAY_DF.copy()

        # filter df for only records where df['month_string']=month_string
        if month_string!='all':
            df = df[df['month_year']==month_string] 

        # redefine the figure
        fig = px.line(df, x='dof', y='count', title='Flights over time')
        return fig