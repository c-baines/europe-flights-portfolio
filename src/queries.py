"""
src/queries.py

created: 19/5/25
"""

# src/queries.py
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

class STARTUP_QUERIES():
    FL_COUNT_BY_DAY_DF = get_flight_counts_by_day()

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
    return df