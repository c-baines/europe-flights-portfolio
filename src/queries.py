"""
src/queries.py

PostgreSQL queries

created: 19/5/25
modified: 
"""

from sqlalchemy import text
from src.db import engine
import pandas as pd
from datetime import datetime

def get_flight_counts_by_day():
    query = text("""
                SELECT dof, COUNT(*) AS count
                FROM flight_list
                GROUP BY dof
                ORDER BY dof;
            """)
    df = pd.read_sql(query, engine, dtype_backend="pyarrow")
    df['month_year'] = df['dof'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%B %Y'))
    return df

def get_months_unique():
    query = text("""
                 SELECT DISTINCT dof
                 FROM flight_list             
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
                JOIN icao_iso i ON e.state_name = i.emissions_state_name
             """)
    df = pd.read_sql(query, engine, dtype_backend="pyarrow")
    df['month_string'] = df['month'].apply(lambda x: datetime.strptime(str(x), '%m').strftime('%B'))
    return df

def get_year_emissions():
    query = text("""
                SELECT 
                    DISTINCT year
                FROM emissions
                ORDER BY year ASC
                 """)
    df = pd.read_sql(query, engine, dtype_backend="pyarrow")
    return df['year'].to_list()

def get_month_emissions():
    query = text("""
                SELECT
                    DISTINCT month
                FROM emissions
                ORDER BY month ASC
                 """)
    df = pd.read_sql(query, engine, dtype_backend="pyarrow") 
    df['month'] = df['month'].apply(lambda x: datetime.strptime(str(x), '%m').strftime('%B'))
    return df['month'].to_list()
   

class STARTUP_QUERIES():
    FL_COUNT_BY_DAY_DF = get_flight_counts_by_day()
    COUNTRY_EMISSIONS_DF = get_country_emissions()