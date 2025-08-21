"""
src/callbacks.py

Callbacks used to update figures in app.

created: 19/5/25
modified: 21/8/25
"""
from dash import Input, Output, callback
from src.queries import STARTUP_QUERIES, get_counts_cards, get_top_airlines, get_top_models
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from dateutil.relativedelta import relativedelta
# import pandas as pd

def register_callbacks(app): 
    """
    Registers all Dash callbacks with the passed app instance. This function prevents circular imports by centralizing callback registration.

    Args:
        app (dash.Dash): The Dash app instance to which the callbacks will be registered.
    """

    # Flight count cards
    @app.callback(
        Output('card', 'figure'),
        Input('flight-count-dropdown', 'value')
    )
    def update_indicator_cards(month_string):
        """
        Update the indicator card figures based on selected month.

        Args:
            month_string (str): Valye from 'flight-count-dropdown'.
                Either 'all' (full dataset) or a month value matching 
                'month_string' column in the df.

        Returns:
            plotly.graph_objects.Figure: Updated indicator cards figure.
        """
        df = STARTUP_QUERIES.CARD_COUNTS_DF().copy()
        columns = ['intra_eu', 'departures_to_outside', 'arrivals_from_outside', 'overflights']
        vals = {}
        # tuple of value and previous month value
        if not month_string or month_string=='all': # if no previous month then delta value = None
            vals = {col:(df[col].sum(), None) for col in columns}

        else:
            curr_df = df[df['month_string']==month_string].copy()
            prev_month_str = (datetime.strptime(month_string,'%B %Y') + relativedelta(months=-1)).strftime('%B %Y')
            prev_df = df[df['month_string']==prev_month_str].copy()

            # if there is no previous month data 
            if prev_df.empty:
                vals = {col:(curr_df[col].to_list()[0], None) for col in columns}
            else:
                vals = {col:(curr_df[col].to_list()[0], prev_df[col].to_list()[0]) for col in columns} 

        fig = make_subplots(
                rows=1, cols=len(columns),
                specs=[[{'type': 'domain'}]*len(columns)]
            )
        
        count=1 # count is for tracking column position [0, 1, 2, 3, ...]
        for col, val in vals.items(): # add each category as trace 
            fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=val[0],
                    delta={
                        'reference': val[1], 
                        'relative': True, 
                        'valueformat': '.1%'
                    } 
                    if val[1] else None, 
                    title={'text': col.replace('_', ' ').title()},
                    number={"font": {"size": 60}},
                    domain={
                        'x': [0.5, 0.95], 
                        'y': [0.5, 0.95]
                    }
                ),
                row=1, col=count
            )
            count+=1

        fig.update_layout(
            height=200,
            margin=dict(t=30, b=10, l=10, r=10)  
        )

        return fig

    # Flight count line graph
    @app.callback(
            Output('flight-count-graph', 'figure'),
            Input('flight-count-dropdown', 'value')
    )
    def update_flight_count_line(month_string):
        """
        Updates flight_list line graph based on selected month. 

        Args:
            month_string (str): Value from 'flight-count-dropdown'.
                Either 'all' (full dataset) or a month value matching 
                'month_string' column in the df.

        Returns:
            plotly.graph_objects.Figure: Updated line graph figure.
        """
        df = STARTUP_QUERIES.FL_COUNT_BY_DAY_DF.copy()

        if month_string!='all':
            df = df[df['month_year']==month_string] 

        color_map = {
            'total': '#000000',   
            'intra-eu': '#12436D',
            'arrivals_from_outside': '#28A197', 
            'departures_to_outside': '#801650', 
            'overflights': '#F46A25'
        }

        label_map = {
            'total': 'Total',
            'intra-eu': 'Intra Europe',
            'arrivals_from_outside': 'Arrivals',
            'departures_to_outside': 'Departures',
            'overflights': 'Overflights'
        }

        fig = go.Figure()

        for category in df['category'].unique(): # iterates through unique category labels
            category_df = df[df['category'] == category] # get category subset df
            
            fig.add_trace(
                go.Scatter(
                    x=category_df['dof'],
                    y=category_df['count'],
                    mode='lines',
                    name=label_map.get(category, category), # gets category key value from dict, or default category label 
                    line=dict(color=color_map[category]),
                    showlegend=True
                )
            )

        fig.update_layout(
            xaxis=dict(
                showgrid=False,  
                showline=True,   
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticklen=5,
                ticks='outside',
                tickwidth=2,
                tickcolor='rgb(204, 204, 204)'
            ),
            yaxis=dict(
                showgrid=True, 
                griddash='dot',
                showline=False,   
                linecolor='rgb(204, 204, 204)',
                linewidth=2
            ),
            legend=dict(
                orientation="h",     
                yanchor="bottom",
                y=-0.3,              
                xanchor="center",
                x=0.5
            ),
            plot_bgcolor='white', 
            height=500,
            template="plotly_white",
            margin=dict(t=40)
        )

        fig.update_layout(
            title="Number of flights Over Time",
            xaxis_title="Time",
            yaxis_title="Number of flights"
        )

        return fig 

    # Airlines and aircraft pie and bar graphs
    @app.callback(
        Output('airlines-bar-graph', 'figure'),
        Input('airlines-dropdown', 'value')
    )    
    def update_aircraft_pie_bar(year):
        """
        Update aircraft and airline pie and bar charts. 

        Args:
            year (float): Value from airlines-dropdown. 
                Either 'all' (full dataset) or a year value matching 
                'year' column in the df.

        Returns:
            plotly.graph_objects.Figure: Updated pie and bar chart figure.
        """
        airlines_df = STARTUP_QUERIES.TOP_AIRLINES_DF.copy()
        model_df = STARTUP_QUERIES.TOP_MODEL_DF.copy()
        manufacturer_df = STARTUP_QUERIES.MANUFACTURER_COUNTS_DF.copy()

        airlines_df['airline'] = airlines_df['airline'].replace({
            "TURK HAVA YOLLARI (TURKISH AIRLINES CO.)": "TURKISH<br>AIRLINES",
            "DEUTSCHE LUFTHANSA, AG, KOELN": "LUFTHANSA",
            "EASYJET UK LTD": "EASYJET",
            "BRITISH AIRWAYS": "BRITISH<br>AIRWAYS"
        }) 

        if year!='all':
            airlines_df = airlines_df[airlines_df['year']==year]
            airlines_df.sort_values('count', ascending=False, inplace=True)
            airlines_df = airlines_df.head(10) 

            model_df = model_df[model_df['year']==year]
            model_df.sort_values('count', ascending=False, inplace=True)
            model_df = model_df.head(10)

            manufacturer_df = manufacturer_df[manufacturer_df['year']==year]
            manufacturer_df.sort_values('year', ascending=False, inplace=True)

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

            manufacturer_df = manufacturer_df.groupby(['manufacturer']).agg({
                'count': 'sum'
            }).reset_index()

        airline_count = airlines_df['count'].to_list()[:5]
        airline = airlines_df['airline'].to_list()[:5]
        airline_count.reverse()
        airline.reverse()

        model_count = model_df['count'].to_list()[:5]
        models = model_df['normalized_model'].to_list()[1:6]
        model_count.reverse()
        models.reverse()

        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=(
                'Manufacturer Share', 
                'Top Aircraft Models', 
                'Top Airlines'
            ),
            specs=[[
                {'type':'domain'}, 
                {'type':'bar'}, 
                {'type': 'bar'}
            ]],
            shared_xaxes=True,
            column_widths=[0.3, 0.35, 0.35] # must add to 1
        )

        total = manufacturer_df['count'].sum()
        percentages = manufacturer_df['count'] / total * 100

        color_map = {
            'Airbus': '#12436D', 
            'Bombardier': '#FFC000', 
            'Cessna': '#3D3D3D',
            'ATR': '#A285D1',
            'Embraer': '#801650',
            'Boeing': '#28A197',
            'Other':'#F46A25',
            'Piper': '#2073BC'
        }
        
        fig.add_trace(
            go.Pie(
            labels=manufacturer_df['manufacturer'],
            values=manufacturer_df['count'],
            textinfo='label+percent',
            # textposition=['inside' if pct >= 3.5 else 'outside' for pct in percentages],
            textposition='auto',
            name='',
            marker=dict(colors=[color_map[m] for m in manufacturer_df['manufacturer']]),
            domain=dict(x=[0, 1], y=[0, 0.85])  # shrink vertically
            ),            
            row=1, col=1
        )

        # for category in df['category'].unique():
        #     category_df = df[df['category'] == category]
            
        #     fig.add_trace(
        #         go.Scatter(
        #             x=category_df['dof'],
        #             y=category_df['count'],
        #             mode='lines',
        #             name=label_map.get(category, category), # gets category key value from dict or default category label 
        #             line=dict(color=color_map[category]),
        #             showlegend=True
        #         )
        #     )


        fig.add_trace(
            go.Bar(
                x=model_count,
                y=models,
                name='',
                orientation='h',
                width=0.5,
                marker_color='#2073BC'
            ),
            row=1, col=2
        )

        fig.add_trace(
            go.Bar(
                x=airline_count,
                y=airline,
                name='',
                orientation='h',
                width=0.5,
                marker_color='#6BACE6'
            ),
            row=1, col=3
        )

        # update layout for (1,2)
        fig.update_layout(
            xaxis=dict(
                showgrid=True,
                showline=False,
                gridcolor='rgb(204, 204, 204)',  
                griddash='dot'
            ),
            yaxis=dict(
                showgrid=True, 
                showline=False,   
                linecolor='rgb(204, 204, 204)',
                linewidth=2
            )
        )

        # update layout for plot (1,3)
        fig.update_layout(
            xaxis2=dict(
                showgrid=True,
                showline=False,
                gridcolor='rgb(204, 204, 204)',  
                griddash='dot'
            ),
            yaxis2=dict(
                showgrid=True, 
                showline=False,   
                linecolor='rgb(204, 204, 204)',
                linewidth=2
            )
        )

        fig.update_layout(
            plot_bgcolor='white',
            showlegend=False,
            height=450,
            yaxis2=dict(domain=[0.0, 1.0]),  # bar chart 1
            yaxis3=dict(domain=[0.0, 1.0]),
            margin=dict(t=50),
            # autosize=False 
        )
    
        return fig     

    # Manufacturers line graph
    @app.callback(
        Output('manufacturer-percent-graph', 'figure'),
        Input('airlines-dropdown', 'value')
    )    
    def update_manufacturer_percent_line(year):
        """
        Update manufacturer line graph. 

        Args:
            year (float): Value from airlines-dropdown. 
                Either 'all' (full dataset) or a year value matching 
                'year' column in the df.

        Returns:
            plotly.graph_objects.Figure: Updated manufacturer line graph figure. 
        """
        df = STARTUP_QUERIES.MANUFACTURER_PERCENT_DF.copy()

        if year!='all':
            df = df[df['year']==year]

        fig = go.Figure()

        color_map = {
            'Airbus': '#12436D', 
            'Bombardier': '#FFC000',
            'Cessna': '#3D3D3D',
            'ATR': '#A285D1',
            'Embraer': '#801650',
            'Boeing': '#28A197',
            'Other':'#F46A25',
            'Piper': '#2073BC'
        }

        for manufacturer in df['manufacturer'].unique():
            df_subset = df[df['manufacturer'] == manufacturer]

            fig.add_trace(go.Scatter(
                x=df_subset['date'], 
                y=df_subset['percentage'],
                mode='lines',
                name=manufacturer,
                marker=dict(color=color_map.get(manufacturer, 'rgb(204, 204, 204)'))
            ))

        fig.update_layout(
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
            title="Percentage Share",
            xaxis_title="Year",
            yaxis_title="Percent",
            template="plotly_white",
            plot_bgcolor='white', 
            height=500
        )

        fig.update_xaxes(
            dtick="M6",  # show every 6 months 
            tickformat="%b %Y"  # abbreviated month name + year (Jan 2021, Feb 2021...)
        )

        return fig
  
    # Emissions heatmap 
    @app.callback(
        Output('emissions-choropleth', 'figure'),
        Input('choropleth-dropdown-year', 'value'),
        Input('choropleth-dropdown-month', 'value')
    )
    def update_choropleth_year(year, month):
        """
        Update emissions choropleth.

        Args:
            year (int): Value from choropleth-dropdown-year. 
                Either 'all' (full dataset) or a year value matching 
                'month_string' column in the df.
            month (str): Value from choropleth-dropdown-month. 
                Either 'all' (full dataset) or a month value matching 
                'year' column in the df.

        Returns:
            plotly.graph_objects.Figure: Updated emissions choropleth figure.
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

        fig = go.Figure(go.Choropleth(
            locations=df['iso_alpha3'],           
            z=df['co2_qty_tonnes'],              
            text=df['state_name'],                
            colorscale='Blues',
            marker_line_color='white',           
            marker_line_width=1.5,                
            colorbar_title='CO₂ (tonnes)'
        ))

        fig.update_layout(
            title='CO₂ Emissions by Country',
            geo=dict(
                showframe=False,
                showcoastlines=True,
                showcountries=True,
                projection_type='natural earth',
                bgcolor='white',  
                center=dict(lat=52, lon=10),
                projection_scale=2.5
            ),
            height=600,
            margin=dict(l=0, r=0, t=50, b=0),
            font=dict(
                family='Open Sans, sans-serif',
                size=14,
                color='#2a3f5f'
            )
        )

        # fig = make_subplots(
        #     rows=1, cols=2,
        #     # specify type of figure. px.choropleth not automatically compatible with make_subplots()
        #     specs=[[{'type': 'choropleth'}, {'type': 'xy'}]],
        #     column_widths=[0.7, 0.3]
        # )
        # # bar graph
        # fig.add_trace(
        #     go.Bar(
        #         x = x,
        #         y = y,
        #         marker=dict(
        #             color='rgba(50, 171, 96, 0.6)',
        #             line=dict(
        #             color='rgba(50, 171, 96, 1.0)',
        #             width=1)
        #         ),
        #         name='CO2 quantity (tonnes)',
        #         orientation='h'
        #     ),
        #     row=1, col=2
        # )

        # fig.update_geos(
        #     projection_type="natural earth",
        #     showcoastlines=True,
        #     showframe=False,
        #     row=1, col=1
        # )

        # fig.update_layout(
        #     title='CO₂ Emissions and Top Emitters',
        #     height=600
        # )
        
        return fig
    

    # @app.callback(
    #     Output(), 
    #     Input()
    # )
    # def update_emissions_bar():
    #     """
        
    #     """
        # emissions_df = STARTUP_QUERIES.COUNTRY_EMISSIONS_DF
        # emissions_df['date'] = pd.to_datetime(emissions_df[['year', 'month']].assign(day=1))

        # line_fig = go.Figure()

        # for state in emissions_df['state_name'].unique():
        #     state_df = emissions_df[emissions_df['state_name'] == state]
            
        #     line_fig.add_trace(
        #         go.Scatter(
        #             x=state_df['date'], # x should be date 
        #             y=state_df['co2_qty_tonnes'],
        #             mode='lines',
        #             name=state,
        #             line=dict(color='rgb(192, 192, 192)')
        #         )
        #     )

        # line_fig.update_layout(
        #     xaxis=dict(
        #         showgrid=False,  
        #         showline=True,   
        #         linecolor='rgb(204, 204, 204)',
        #         linewidth=2,
        #         ticklen=5,
        #         ticks='outside',
        #         tickwidth=2,
        #         tickcolor='rgb(204, 204, 204)'
        #     ),
        #     yaxis=dict(
        #         showgrid=True, 
        #         griddash='dot',
        #         showline=False,   
        #         linecolor='rgb(204, 204, 204)',
        #         linewidth=2
        #     ),
        #     plot_bgcolor='white', 
        #     height=500,
        #     template="plotly_white",
        #     showlegend=False
        # )

        # avg_emissions_df = emissions_df.groupby('date')['co2_qty_tonnes'].mean().reset_index()
        # avg_emissions_df.rename(columns={'co2_qty_tonnes': 'avg_co2_qty_tonnes'}, inplace=True)

        # line_fig.add_trace(
        #     go.Scatter(
        #         x=avg_emissions_df['date'],
        #         y=avg_emissions_df['avg_co2_qty_tonnes'],
        #         mode='lines',
        #         line=dict(color='red', width=4) 
        #     )
        # )
