# Eurocontrol Flights Portfolio Project 

https://ansperformance.eu/data/  data from Eurocontrol 

https://www.opdi.aero/flight-event-data download script

## Flight List Data 
| Variable Name | Type | Description | Example |
|-|-|-|-|
| id | integer | Unique identification number (primary key) | 11365 |
| ec_id | character varying | unique hash Eurocontrol identifier for row | 9e4e05b14498109613cf2069f5de308471f9311ccd6120419cdcdbbf71fccbe0_0_2022_1 |
| icao24 | character varying | Unique 24-bit aircraft identifier | 394c04 |
| flt_id | character varying | Unique code for flight route by airline | AFR94RP |
| dof | character varying | Date of flight | 2022-01-01 |
| adep | character varying | Aerodrome of Departure code | LFPG |
| ades | character varying | Aerodrome of Destination code | LPPT |
| adep_p | character varying | Planned Aerodrome of Departure | LFPB |
| ades_p | character varying | Planned Aerodrome of Destination | LPAR |
| registration | character varying | Unique aircraft registration number | F-GTAE |
| model | character varying | Aircraft model name | A321 212 |
| typecode | character varying | Aircraft model code | A321 |
| icao_aircraft_class | character varying | Aircraft type class | L2J |
| icao_operator | character varying | Airline code | AFR |
| first_seen | timestamp without time zone | Time aircraft first seen | 2022-01-01 12:31:45 |
| last_seen | timestamp without time zone | Time aircraft last seen | 2022-01-01 14:56:25 |
| version |  character varying | Algorithm version used to detect flight events | v2.0.0 |
| unix_time | integer | fist_seen in unix time | 1641040305 |



ICAO - International Civil Avation Organization 

https://www.opdi.aero/concepts concept explainer 

https://virtualradarserver.co.uk/Documentation/Glossary/Icao24.aspx icao24 explainer

https://www.opdi.aero/methodology version explainer 

## Emissions Data
| Variable Name | Type | Description | Example |
|-|-|-|-|
| year | integer | Year of record | 2019 |
| month | integer | Month of record | 1 | 
| state_name | character varying | State name | ALBANIA | 
| state_code | character varying |2 character state abbreviation | LA |
| co2_qty_tonnes | double precision | CO2 quantity for that state in tonnes (kg) | 8318.42 |
| tf* | integer | Traffic for that state | 821 |
| note* | boolean | Special data aggregation True/False | TRUE | 

https://ansperformance.eu/reference/dataset/emissions/ explainer 

## ICAO Airports List 
| Variable Name | Type | Description | Example |
|-|-|-|-|
| country_code | string | Two-character country code based on ISO 3166 | AE |
| region_name | string | Region or state name | Abu Zaby |
| iata | string | Three-character IATA airport code  |AAN |
| icao | string | Four-character ICAO airport code | OMAL |
| airport | string | Name of airport | Al Ain International Airport |
| latitude | double precision | Airport latitude | 24.2617 |
| longitude | double precision | Airport longitude  | 55.6092 |

https://github.com/ip2location/ip2location-iata-icao source


## Country Codes 
| Variable Name | Type | Description | Example |
|-|-|-|-|

https://unstats.un.org/unsd/methodology/m49/overview/


callbacks function pattern 
https://community.plotly.com/t/dash-callback-in-a-separate-file/14122/16


Accessibility colour scheme references: https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-colours-in-charts/

Airlines source: https://github.com/rikgale/ICAOList/blob/main/Airlines.csv