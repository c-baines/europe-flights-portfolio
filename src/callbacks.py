"""
src/callbacks.py

created: 19/5/25
updated: 2/6/25
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
    
    @app.callback(
        Output('emissions-choropleth', 'figure'),
        Input('choropleth-dropdown-year', 'value'),
        Input('choropleth-dropdown-month', 'value')
    )
    def update_choropleth_year(year, month):
        print('STARTING')
        print(year)
        print(month)
        df = STARTUP_QUERIES.COUNTRY_EMISSIONS_DF.copy()

        if year!='all':
            df = df[df['year']==year]
        print('after year filter')
        print(df)

        if month!='all':
            df = df[df['month_string']==month]
        print('after month filter')
        print(df)

        df = df.groupby(['iso_alpha3']).agg({
            'state_name': 'first',
            'co2_qty_tonnes': 'mean'
        }).reset_index()
        print('after aggregation')
        print(df)

        fig = px.choropleth(df,
                    locations='iso_alpha3',
                    color='co2_qty_tonnes',
                    hover_name='state_name',
                    projection='natural earth',
                    )
        return fig



