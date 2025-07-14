"""
src/layout.py

App layout

created: 19/5/25
modified: 12/7/25
"""

from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from src.queries import get_flight_counts_by_day, get_months_unique, get_country_emissions, get_year_emissions, get_month_emissions, STARTUP_QUERIES
import plotly.graph_objects as go


manufacturer_df = STARTUP_QUERIES.MANUFACTURER_COUNTS_DF.copy()
manu_fig = go.Figure()

for manufacturer in manufacturer_df['manufacturer'].unique():
    df_subset = manufacturer_df[manufacturer_df['manufacturer'] == manufacturer]

    manu_fig.add_trace(go.Scatter(
        x=df_subset['year'],
        y=df_subset['count'],
        mode='lines',
        name=manufacturer
    ))

manu_fig.update_layout(
    xaxis=dict(
        showgrid=False,
        showline=True,   
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        tickmode='linear',
        dtick=1,              
        tickformat='d',
        ticklen=5,
        ticks='outside',
        tickwidth=2,
        tickcolor='rgb(204, 204, 204)'
    ),
    yaxis=dict(
        showgrid=True,
        showline=False,   
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        griddash='dot',
        gridcolor='rgb(204, 204, 204)'       
    ),
    legend=dict(
        orientation="h",     
        yanchor="bottom",
        y=-0.25,              
        xanchor="center",
        x=0.5
    ),
    title="Number of Recorded Flights by Manfactuerer",
    xaxis_title="Year",
    yaxis_title="Number of Aircraft",
    template="plotly_white",
    plot_bgcolor='white', 
    height=500
)

layout = html.Div([
    # number of flights line graph
    html.Div(children=[
        html.H1("European Flight Records Dashboard"),

        dcc.Dropdown(
            id='flight-count-dropdown', 
            options=[{"label": "All data", "value": "all"}] + [{"label": m, "value": m} for m in get_months_unique()],
            value="all",
            placeholder='Select a Month'
        ),

    # flight count decomposed cards
        dcc.Graph(id="card"),

        dcc.Graph(id='flight-count-graph')
    ]),

    # airlines bar graphs
    html.Div(children=[
        html.H2('Airlines and Aircraft'),

        dcc.Dropdown(
            id='airlines-dropdown',
            options=[{"label": "All years", "value": "all"}] + [{"label": y, "value": y} for y in STARTUP_QUERIES.TOP_AIRLINES_DF['year'].unique().tolist()],
            value='all',
            placeholder='Year' 
        ),

        dcc.Graph(id='airlines-bar-graph'),

        dcc.Graph(id='manufacturer-line-graph', figure=manu_fig)
    ]),

    # emissions heatmap
    html.Div(children=[
        html.H1('Choropleth Emissions Test'),
        
        dcc.Dropdown(
            id='choropleth-dropdown-year',
            options=[{"label": "All years", "value": "all"}] + [{"label": y, "value": y} for y in get_year_emissions()],
            value="all",
            placeholder='Year'
        ),

        dcc.Dropdown(
            id='choropleth-dropdown-month',
            options=[{"label": "All months", "value": "all"}] + [{"label": m, "value": m} for m in get_month_emissions()],
            value="all",
            placeholder='Month'
        ),

        dcc.Graph(id='emissions-choropleth')
    ])

])

