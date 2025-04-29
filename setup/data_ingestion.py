""" 
data_ingestion.py 

Ingest data into postgreSQL database

c-baines
23/4/25
"""

import pandas as pd
from pathlib import Path
import os
from src.db import FlightList, Emissions, TableName, session
from loguru import logger

here = Path(__file__).resolve().parent 

def dict_to_db(row: dict, table: TableName):
    if table == TableName.flight_list:
        row.update({'ec_id': row['id']})
        row.pop('id')
        db_obj = FlightList(**row)
    if table == TableName.emissions:
        # make key name lower case 
        row = {k.lower(): v for k,v in row.items()}
        db_obj = Emissions(**row)
    return db_obj

def ingest_csv(filename: str, table: TableName):
    """
    - Reads .csv file
    - For each row: 
        - Changes id to ec_id 
        - Creates FlightList object 
    - Bulk saves to db every 100000 rows 

    Args:
        filename (str): .csv file

    """
    df = pd.read_csv(filename)
    db_objects = []
    for row in df.to_dict(orient='records'): 
        db_obj = dict_to_db(row, table)
        db_objects.append(db_obj)
        if len(db_objects) == 100000:
            session.bulk_save_objects(db_objects)
            session.commit()
            logger.info(f"Inserted {len(db_objects)} records into the database")
            db_objects = []
    
    if db_objects:
        session.bulk_save_objects(db_objects)
        session.commit()
        logger.info(f"Inserted {len(db_objects)} records into the database")

def iterate_folder(folder: str):
    """
    Yields list of .csv object paths 

    Args:
        folder (str): directory of files to ingest 

    Yields:
        str: full path to each file found 
        
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.csv'):
                yield os.path.join(root, file)

def ingest_folder(folder: str, table: TableName):
    """ 
    - Iterates through folder
    - Calls ingest_csv on each file 
    """
    for filename in iterate_folder(str(here/'data'/folder)):
        # skip files already ingested
        if "flight_list_2022" in filename or "flight_list_2025" in filename:
            logger.info(f"Skipping {filename}")
            continue
        logger.info(f"Processing {filename}")
        ingest_csv(filename, table)
        logger.info(f"Finished processing {filename}")

# ingest_folder('flight_list', TableName.flight_list)
# ingest_folder('co2_emissions_by_state', TableName.emissions)