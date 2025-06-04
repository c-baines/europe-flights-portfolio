"""
src/callbacks.py

created: 19/5/25
modified: 2/6/25
"""
from dash import Input, Output, callback
from src.queries import STARTUP_QUERIES
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def register_callbacks(app): 

    @app.callback(
            Output('flight-count-graph', 'figure'),
            Input('flight-count-dropdown', 'value')
    )
    def update_month_dropdown(month_string):
        """
        Number of flights line graph with date dropdown
        """
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
        """
        Emissions heatmap and bar graph with date dropdown
        """
    
        df = STARTUP_QUERIES.COUNTRY_EMISSIONS_DF.copy()

        if year!='all':
            df = df[df['year']==year]

        if month!='all':
            df = df[df['month_string']==month]

        df = df.groupby(['iso_alpha3']).agg({
            'state_name': 'first',
            'co2_qty_tonnes': 'mean'
        }).reset_index()

        df = df.sort_values(by='co2_qty_tonnes',ascending=False)
        x = df['co2_qty_tonnes'].to_list()[:5]
        y = df['state_name'].to_list()[:5]
        x.reverse()
        y.reverse()

        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'choropleth'}, {'type': 'xy'}]],
            column_widths=[0.6, 0.4]
        )

        fig.add_trace(
            px.choropleth(df,
                    locations='iso_alpha3',
                    color='co2_qty_tonnes',
                    hover_name='state_name',
                    projection='natural earth',
                    ).data[0],
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x = x,
                y = y,
                marker=dict(
                    color='rgba(50, 171, 96, 0.6)',
                    line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1)
                ),
            name='CO2 quantity (tonnes)',
            orientation='h'
            ),
            row=1, col=2
        )

        fig.update_geos(
        projection_type="natural earth",
        showcoastlines=True,
        showframe=False,
        row=1, col=1
        )

        fig.update_layout(
        title='CO₂ Emissions and Top Emitters',
        height=600
        )
    
        return fig



