"""
src/callbacks.py

created: 19/5/25
modified: 30/6/25
"""
from dash import Input, Output, callback
from src.queries import STARTUP_QUERIES, get_counts_cards, get_top_airlines, get_top_models
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from dateutil.relativedelta import relativedelta



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

        line_styles = {
            'total': 'solid',
            'intra_eu': 'dash',
            'arrivals_from_outside': 'dash',
            'departures_to_outside': 'dash',
            'overflights': 'dash'
        }

        color_map = {
            'total': '#000000',   
            'intra_eu': '#12436D',
            'arrivals_from_outside': '#28A197', 
            'departures_to_outside': '#801650', 
            'overflights': '#F46A25'
        }

        # redefine the figure
        fig = px.line(
            df, 
            x='dof', 
            y='count', 
            color='category',
            line_dash='category',         # Controls which dash style to use
            line_dash_map=line_styles,
            color_discrete_map=color_map
        )
        
        return fig

    @app.callback(
        Output('card', 'figure'),
        Input('flight-count-dropdown', 'value')
    )
    def update_card_counts(month_string):
        """
        """
        df = get_counts_cards().copy()
        columns = ['intra_eu', 'departures_to_outside', 'arrivals_from_outside', 'overflights']
        vals = {}
        if not month_string or month_string=='all':
            vals = {col:(df[col].sum(), None) for col in columns}

        else:
            curr_df = df[df['month_string']==month_string].copy()
            prev_month_str = (datetime.strptime(month_string,'%B %Y') + relativedelta(months=-1)).strftime('%B %Y')
            prev_df = df[df['month_string']==prev_month_str].copy()

            if prev_df.empty:
                vals = {col:(curr_df[col].to_list()[0], None) for col in columns}
            else:
                vals = {col:(curr_df[col].to_list()[0], prev_df[col].to_list()[0]) for col in columns}

        fig = make_subplots(
                rows=1, cols=len(columns),
                specs=[[{'type': 'domain'}]*len(columns)]
            )
        
        count=1
        for col, val in vals.items():
            fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=val[0],
                    delta={'reference': val[1], 'relative': True, 'valueformat': '.2%'} if val[1] else None, 
                    title={'text': col.replace('_', ' ').title()}),
                    row=1, col=count
            )
            count+=1
    
        fig.update_layout(
            paper_bgcolor = "lightgray",
            height=250)

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

        # get top 5 emitters for date range
        df = df.sort_values(by='co2_qty_tonnes',ascending=False)
        x = df['co2_qty_tonnes'].to_list()[:5]
        y = df['state_name'].to_list()[:5]
        x.reverse()
        y.reverse()

        fig = make_subplots(
            rows=1, cols=2,
            # specify type of figure. px.choropleth not automatically compatible with make_subplots()
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

    @app.callback(
        Output('airlines-bar-graph', 'figure'),
        Input('airlines-dropdown', 'value')
    )    
    def update_aircraft_graphs(year):
        airlines_df = STARTUP_QUERIES.TOP_AIRLINES_DF.copy()
        model_df = STARTUP_QUERIES.TOP_MODEL_DF.copy()

        if year!='all':
            airlines_df = airlines_df[airlines_df['year']==year]
            airlines_df.sort_values('count', ascending=False, inplace=True)
            airlines_df = airlines_df.head(10) 

            model_df = model_df[model_df['year']==year]
            model_df.sort_values('count', ascending=False, inplace=True)
            model_df = model_df.head(10)

        else:
            airlines_df = airlines_df.groupby(['airline']).agg({
            'count': 'sum'
            }).reset_index()
            airlines_df.sort_values('count', ascending=False, inplace=True)
            airlines_df = airlines_df.head(10)

            model_df = model_df.groupby(['normalized_model']).agg({
            'count': 'sum'
            }).reset_index()
            model_df.sort_values('count', ascending=False, inplace=True)
            model_df = model_df.head(10)

        airline_count = airlines_df['count'].to_list()[:5]
        airline = airlines_df['airline'].to_list()[:5]
        airline_count.reverse()
        airline.reverse()

        model_count = model_df['count'].to_list()[:5]
        models = model_df['normalized_model'].to_list()[1:6]
        model_count.reverse()
        models.reverse()


        fig = make_subplots(
            rows=1, cols=2
        )

        fig.add_trace(
            go.Bar(
                x=airline_count,
                y=airline,
                name='top-airlines',
                orientation='h'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=model_count,
                y=models,
                name='top-aircraft',
                orientation='h'
            ),
            row=1, col=2
        )

        return fig

