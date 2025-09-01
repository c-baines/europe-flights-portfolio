""" 
data_ingestion.py 

Ingest data into PostgreSQL database

author: c-baines
created: 23/4/25
last modified: 29/8/25
"""

import pandas as pd
from pathlib import Path
import os
from src.db import FlightList, Emissions, IcaoList, IsoCodes, IcaoIso, TableName, session, Airlines
from loguru import logger
from src.db import engine 
from sqlalchemy import text 

here = Path(__file__).resolve().parent 

def is_ingested(filename: str, table: TableName, delimiter: str = ','):
    """
    Checks whether a CSV file has already been ingested into the PostgreSQL database
    by comparing a random sample of 3 rows against existing records.

    Args:
        filename (str): Path or name of the CSV file to check.
        table (TableName): Enum value representing the database table to check against.
        delimiter (str): Delimiter used in the CSV file (defaults to ',').

    Returns:
        bool: 
            - True if all sampled rows are already present in the database.  
            - False if none of the sampled rows are present in the database.

    Raises:
        Exception: If only some of the sampled rows are found in the database
                (indicating a partially ingested file).
    """

    logger.info(f'Checking if {filename} already ingested... ')

    df = pd.read_csv(filename, delimiter=delimiter)

    if table == TableName.flight_list:
        df = df.sample(n=3) # random sample
        rows = df.to_dict(orient='records') # convert df to list of dictionaries
        ids_to_check = [f"'{row.get('id')}'" for row in rows] # convert list of dictionaries to list of ids (=ec_id)
        query = text(f""" 
                    select ec_id
                    from {table.value}
                    where ec_id in ({','.join(ids_to_check)}) 
                    """) 
        sql_df = pd.read_sql(query, engine)

        if len(sql_df) == len(rows): # if n of rows found in query = n of sample then:
            return True
        elif sql_df.empty:
            return False
        else:
            raise Exception('File partially ingested')

    elif table==TableName.emissions:
        df = df.sample(n=3)
        rows = df.to_dict(orient='records')
        conditions = [f"(state_name='{row.get('STATE_NAME')}' and year={row.get('YEAR')} and month={row.get('MONTH')})" for row in rows]
        query = text(f"""
                Select * from emissions
                Where {" or ".join(conditions)}
                """)
        sql_df = pd.read_sql(query, engine)

        if len(sql_df) == len(rows):
            return True
        elif sql_df.empty:
            return False
        else:
            raise Exception('File partially ingested')

    else:
        query = text(f"""
                    select count(*)
                    from {table.value}
                         """)
        
        sql_df = pd.read_sql(query,engine)

        if sql_df['count'].to_list()[0] == len(df):
            return True
        elif sql_df['count'].to_list()[0] == 0:
            return False
        else:
            raise Exception('File partially ingested')

def dict_to_db(row: dict, table: TableName):
    """
     Normalises and converts a dictionary row into a SQLAlchemy databse object for insertion into PostgreSQL.

    Args:
        row (dict): A single row of data represented as a dictionary. Keys are column names (case-insensitive).
        table (TableName): Enum value indicating the target table. 

    Returns
        db_obj (SQLAlchemy model instance): A SQLAlchemy ORM object corresponding to the given table, ready to be added to a session and committed to the database.

    Raises:
        KeyError: If required fields are missing from the row dictionary.
    """
    # make all keys lowercase and remove 'NaN' strings
    row = {k.lower(): v for k,v in row.items() if not str(v).lower()=='nan'}

    if table == TableName.flight_list:
        row.update({'ec_id': row['id']}) # rename id column 
        row.pop('id')
        db_obj = FlightList(**row)

    if table == TableName.emissions:
        if "flight_month" in row: # 2019-2021 data files have extra date column 
            row.pop("flight_month") # remove extra date column 
        db_obj = Emissions(**row)

    if table == TableName.icao_list:
        db_obj = IcaoList(**row)

    if table == TableName.iso_codes:                
        new_row = {
            "region_name": row.get("region name") or None,
            "subregion_name": row.get("sub-region name") or None,
            "intermediate_region_name": row.get("intermediate region name") or None,
            "country": row.get("country or area") or None,
            "iso_alpha2": row.get("iso-alpha2 code") or None,
            "iso_alpha3": row.get("iso-alpha3 code") or None
        }
        db_obj = IsoCodes(**new_row)

    if table == TableName.icao_iso:
        new_row = {
            "emissions_state_name": row.get("emissions state name") or None,
            "icao_state_name": row.get("iso country name") or None,
            "icao": row.get("state code/icao") or None,
            "iso_alpha3": row.get("iso alpha3") or None
        }
        db_obj = IcaoIso(**new_row)

    if table == TableName.airlines:
        new_row = {
            "airline": row.get("company") or None,
            "country": row.get("country") or None,
            "telephony": row.get("telephony") or None,
            "icao_operator_code": row.get("3ltr") or None
        }
        db_obj = Airlines(**new_row)
      
    return db_obj

def ingest_csv(filename: str, table: TableName, delimiter: str = ',' ):
    """
    Ingests ORM objects into PostgreSQL table.

    Args:
        filename (str): Name of the csv file to ingest.
        table (TableName): Enum value indicating the target table. 
        delimiter (str): Delimiter in csv file. Defaults to ','.
    """
    df = pd.read_csv(filename, delimiter=delimiter)

    db_objects = []

    for row in df.to_dict(orient='records'): 
        db_obj = dict_to_db(row, table)
        db_objects.append(db_obj) # append each row to db_objects 
        
        if len(db_objects) == 100000: # commit every 100k rows 
            session.bulk_save_objects(db_objects)
            session.commit()

            logger.info(f"Inserted {len(db_objects)} records into the database")

            db_objects = []

    if db_objects: # if less than 100k left in db_objects, commit remainder 
        session.bulk_save_objects(db_objects)
        session.commit()

        logger.info(f"Inserted {len(db_objects)} records into the database")

def iterate_folder(folder: str):
    """
    Yields the paths to each file in a given folder.

    Args:
        folder (str): Directory of files to ingest.

    Yields:
        str: The path to each file in the folder. 
        
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.csv'):
                yield os.path.join(root, file)

def ingest_folder(folder: str, table: TableName, delimiter: str = ',',  engine='python', encoding='utf-8'):
    """ 
    Ingests each file in a folder into the provided PostgreSQL table.

    Args:
        folder (str): Directory of files to ingest.
        table (TableName): Enum value indicating the target table.
        delimiter (str): Delimiter in csv file. Defaults to ','.
    """
    for filename in iterate_folder(str(here/'data'/folder)):
        if is_ingested(filename, table, delimiter)==False: # check if file is already ingested or not
            logger.info(f"Processing {filename}")
            ingest_csv(filename, table, delimiter)
            logger.info(f"Finished processing {filename}")
        else:
            logger.info(f"{filename} is already ingested. Skipping file")

def setup():
    """
    Ingests each dataset into PostgreSQL DB.
    """
    ingest_folder('iata-icao', TableName.icao_list)
    ingest_folder('iso_codes', TableName.iso_codes, ';')
    ingest_folder('icao_iso', TableName.icao_iso)
    ingest_folder('airlines', TableName.airlines)
    ingest_folder('co2_emmissions_by_state', TableName.emissions)
    ingest_folder('flight_list', TableName.flight_list)

def update():
    """
    Ingests new data releases for ``flight_list`` and ``co2_emmissions_by_state`` datasets into PostgreSQL DB.
    """
    ingest_folder('co2_emmissions_by_state', TableName.emissions)
    ingest_folder('flight_list', TableName.flight_list)
