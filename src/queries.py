"""
src/queries.py

PostgreSQL queries

created: 19/5/25
modified: 9/7/25
"""

from sqlalchemy import text
from src.db import engine
import pandas as pd
from datetime import datetime

def get_flight_counts_by_day():
    query = text("""
                SELECT *
                FROM flight_counts;
            """)
    df = pd.read_sql(query, engine, dtype_backend="pyarrow")
    df['month_year'] = df['dof'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%B %Y'))
    return df

def get_months_unique():
    query = text("""
                 SELECT DISTINCT dof
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
            FROM card_counts 
            ORDER BY month;
        """)
    df = pd.read_sql(query, engine)
    df['month_string'] = df['month'].apply(lambda x: datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S%z").strftime('%B %Y'))
    return df 

def get_top_airlines():
    query = text("""
                SELECT COUNT(fl.icao_operator) AS count, a.airline as airline, DATE_PART('year', fl.dof) as year
                FROM flight_list fl
                LEFT JOIN airlines a ON fl.icao_operator = a.icao_operator_code
                GROUP BY airline, year;
                 """)
    df = pd.read_sql(query, engine)
    return df

def get_top_models():
    # get most popular aircrafts
    query = text("""
                select count(*), am.normalized_model, date_part('year', fl.dof) as year
                from aircraft_model am
                left join flight_list fl on fl.model = am.raw_model 
                group by 2, 3
                ;
                 """)
    df = pd.read_sql(query, engine)
    return df

def get_manufacturer_counts():
    query = text("""
                 SELECT *
                 FROM manufacturer_counts
                 WHERE manufacturer != 'Not recorded';
                 """)
    df = pd.read_sql(query, engine)
    return df

class STARTUP_QUERIES():
    FL_COUNT_BY_DAY_DF = get_flight_counts_by_day()
    COUNTRY_EMISSIONS_DF = get_country_emissions()
    TOP_AIRLINES_DF = get_top_airlines()
    TOP_MODEL_DF = get_top_models()
    MANUFACTURER_COUNTS_DF = get_manufacturer_counts()