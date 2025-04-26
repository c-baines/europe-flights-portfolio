""" 
data_ingestion.py 

Ingest data into postgreSQL database

c-baines
23/4/25
"""

import pandas as pd
from pathlib import Path
import os
from src.db import FlightList, session
from loguru import logger

here = Path(__file__).resolve().parent 

def ingest_flight_list_csv(filename: str):
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
        row.update({'ec_id': row['id']})
        row.pop('id')
        db_obj = FlightList(**row)
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


def ingest_flight_list_folder():
    """ 
    - Iterates through flight_list folder
    - Calls ingest_flight_list_csv on each file 
    """
    for filename in iterate_folder(str(here/'data'/'flight_list')):
        # skip files already ingested
        if "flight_list_2022" in filename:
            logger.info(f"Skipping {filename}")
            continue
        logger.info(f"Processing {filename}")
        ingest_flight_list_csv(filename)
        logger.info(f"Finished processing {filename}")


ingest_flight_list_folder()