"""
src/queries.py

PostgreSQL queries

created: 19/5/25
modified: 19/8/25
"""

from sqlalchemy import text
from src.db import engine
import pandas as pd
from datetime import datetime

def get_flight_counts_by_day():
    query = text("""
        SELECT *
        FROM flight_count_summary
        order by dof;
    """)
    df = pd.read_sql(query, engine, dtype_backend="pyarrow")
    df['month_year'] = df['dof'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%B %Y'))
    return df

def get_months_unique():
    query = text("""
        SELECT 
            DISTINCT dof
        FROM flight_list;             
    """)
    df = pd.read_sql(query, engine, dtype_backend="pyarrow")
    df['month_year'] = df['dof'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%B %Y'))
    return df['month_year'].unique()

def get_country_emissions():
    query = text("""
        SELECT 
            e.id, 
            e.year, 
            e.month, 
            e.state_name, 
            e.state_code, 
            e.co2_qty_tonnes, 
            i.iso_alpha3
        FROM emissions e
        JOIN icao_iso i ON e.state_name = i.emissions_state_name;
    """)
    df = pd.read_sql(query, engine, dtype_backend="pyarrow")
    df['month_string'] = df['month'].apply(lambda x: datetime.strptime(str(x), '%m').strftime('%B'))
    return df

def get_year_emissions():
    query = text("""
        SELECT 
            DISTINCT year
        FROM emissions
        ORDER BY year ASC;
    """)
    df = pd.read_sql(query, engine, dtype_backend="pyarrow")
    return df['year'].to_list()

def get_month_emissions():
    query = text("""
        SELECT
            DISTINCT month
        FROM emissions
        ORDER BY month ASC;
    """)
    df = pd.read_sql(query, engine, dtype_backend="pyarrow") 
    df['month'] = df['month'].apply(lambda x: datetime.strptime(str(x), '%m').strftime('%B'))
    return df['month'].to_list()
   
def get_counts_cards():
    query = text("""
        SELECT * 
        FROM card_count_summary 
        ORDER BY month;
    """)
    df = pd.read_sql(query, engine)
    df['month_string'] = df['month'].apply(lambda x: datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S%z").strftime('%B %Y')) # convert month column into string
    return df 

def get_top_airlines():
    query = text("""
        SELECT 
            COUNT(fl.icao_operator) AS count, 
            a.airline as airline, 
            DATE_PART('year', fl.dof) as year
        FROM flight_list fl
        LEFT JOIN airlines a ON fl.icao_operator = a.icao_operator_code
        GROUP BY airline, year;
    """)
    df = pd.read_sql(query, engine)
    return df

def get_top_models():
    # get most popular aircrafts
    query = text("""
        SELECT 
            COUNT(*), 
            am.normalized_model, 
            date_part('year', fl.dof) as year
        FROM aircraft_model am
        LEFT JOIN flight_list fl on fl.model = am.raw_model 
        GROUP BY 2, 3;
    """)
    df = pd.read_sql(query, engine)
    return df

def get_manufacturer_percent():
    query = text("""
       SELECT *, 
        (count::numeric / SUM(count) OVER (PARTITION BY year, month)) * 100 AS percentage
        FROM manufacturer_count_summary
    """)
    df = pd.read_sql(query, engine)
    df['date'] = pd.to_datetime(
        df['year'].astype(int).astype(str) +
        df['month'].astype(int).astype(str).str.zfill(2),
        format='%Y%m'
    )   
    return df

def get_manufacturer_counts():
    query = text("""
        SELECT *
        FROM manufacturer_count_summary
        WHERE manufacturer != 'Not recorded' 
        AND manufacturer != 'Ground Support Equipment (GSE)'
        ORDER BY year, month;
                 """)
    df = pd.read_sql(query, engine)
    df['date'] = pd.to_datetime(
        df['year'].astype(int).astype(str) +
        df['month'].astype(int).astype(str).str.zfill(2),
        format='%Y%m'
    ).dt.strftime('%B %Y')    
    return df

def get_top_departures():
    query = text("""
        WITH monthly_counts AS (
            SELECT 
                f.adep,
                DATE_TRUNC('month', f.dof)::date AS month,
                COUNT(*) AS departures
            FROM flight_list f
            WHERE f.adep IS NOT NULL
            GROUP BY f.adep, DATE_TRUNC('month', f.dof)
        ),
        airport_totals AS (
            SELECT adep, SUM(departures) AS total_departures
            FROM monthly_counts
            GROUP BY adep
        ),
        top_airports AS (
            SELECT adep
            FROM airport_totals
            ORDER BY total_departures DESC
            LIMIT 10
        )
        SELECT 
            mc.adep,
            i.airport,
            mc.month,
            mc.departures
        FROM monthly_counts mc
        JOIN top_airports ta ON mc.adep = ta.adep
        LEFT JOIN icao_list i ON mc.adep = i.icao
        ORDER BY mc.month, mc.departures DESC;
    """)
    df = pd.read_sql(query, engine)
    return df
    

def get_top_destinations():
    query = text("""
        WITH monthly_counts AS (
            SELECT 
                f.ades,
                DATE_TRUNC('month', f.dof)::date AS month,
                COUNT(*) AS destinations
            FROM flight_list f
            WHERE f.ades IS NOT NULL
            GROUP BY f.ades, DATE_TRUNC('month', f.dof)
        ),
        airport_totals AS (
            SELECT ades, SUM(destinations) AS total_destinations
            FROM monthly_counts
            GROUP BY ades
        ),
        top_airports AS (
            SELECT ades
            FROM airport_totals
            ORDER BY total_destinations DESC
            LIMIT 10
        )
        SELECT 
            mc.ades,
            i.airport,
            mc.month,
            mc.destinations
        FROM monthly_counts mc
        JOIN top_airports ta ON mc.ades = ta.ades
        LEFT JOIN icao_list i ON mc.ades = i.icao
        ORDER BY mc.month, mc.destinations DESC;
    """)
    df = pd.read_sql(query, engine)
    return df

class STARTUP_QUERIES():
    FL_COUNT_BY_DAY_DF = get_flight_counts_by_day()
    COUNTRY_EMISSIONS_DF = get_country_emissions()
    TOP_AIRLINES_DF = get_top_airlines()
    TOP_MODEL_DF = get_top_models()
    MANUFACTURER_COUNTS_DF = get_manufacturer_counts()
    MANUFACTURER_PERCENT_DF = get_manufacturer_percent()


