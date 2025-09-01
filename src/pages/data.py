"""
src/pages/data.py

Data page in app

created: 20/08/25
"""

import dash
from dash import html

dash.register_page(__name__, path='/data', name='Data', order=2)

layout = html.Div([
    html.Div([
        html.H5("Data", style={"font-weight": "bold"}),
        html.P([
            "This project uses data made available by the ",
            html.A(
                "Eurocontrol Open Data Performance Initiative",
                href="https://www.opdi.aero/",
                target="_blank",
                style={"textDecoration": "none", "color": "blue"}
            ),
            ". ",
            html.Br(),
            html.Br(),
            "The Eurocontrol data used in this project include the ",
            html.A(
                "Flight List",
                href="https://ansperformance.eu/data/#img-idopdi-srcimagesprcq_opdipng-width50-height50-altopen-performance-data-initiative-open-performance-data-initiative-opdi",
                target="_blank",
                style={"textDecoration": "none", "color": "blue"}
            ),
            " dataset and the ",
            html.A(
                ["CO", html.Sub("2"), " Emissions"],
                href="https://ansperformance.eu/data/#cosub2sub-emissions-smallsmall-small-emitters-toolhttpswwweurocontrolinttoolsmall-emitters-toolsmallsmall",
                target="_blank",
                style={"textDecoration": "none", "color": "blue"}
            ),
            " dataset.",
            html.Br(),
            html.Br(),
            "Other data used includes a list of ",
            html.A(
                "airlines and associated ICAO codes",
                href="https://github.com/rikgale/ICAOList/blob/main/Airlines.csv",
                target="_blank",
                style={"textDecoration": "none", "color": "blue"}
                   ),
            ", countries with associated two- and three-letter ISO codes from the ",
            html.A(
                "United Nations Statistics Division",
                href="https://unstats.un.org/unsd/methodology/m49/overview/",
                target="_blank",
                style={"textDecoration": "none", "color": "blue"}
                ),
            " and a list of ",
            html.A(
                "IATA and ICAO codes",
                href="https://github.com/ip2location/ip2location-iata-icao",
                target="_blank",
                style={"textDecoration": "none", "color": "blue"}
            ),
            " for airports and countries."
        ]),

        html.H6("Licences", style={"font-weight": "bold"}),
        html.P([
            "The IATA/ICAO list data is licensed under ",
            html.A(
                "Creative Commons Attribution-ShareAlike 4.0 International License",
                href="https://creativecommons.org/licenses/by-sa/4.0/",
                target="_blank",
                style={"textDecoration": "none", "color": "blue"}
            ),
            ". It is free for personal or commercial use with attribution required by mentioning the use of this data as follows: ",
            html.Span("This site or product includes IATA/ICAO List data available from ", style={"fontWeight": "bold"}),
            html.A(
                "ip2location.com",
                href="https://www.ip2location.com",
                target="_blank",
                style={"textDecoration": "none", "color": "blue"}
                ),
            ". ",
            html.Br(),
            "IATA is a registered trademark of International Air Transport Association.",
            html.Br(),
            "ICAO is a registered trademark of International Civil Aviation Organization."
        ])
    ])
], className="my-container")
