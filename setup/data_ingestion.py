""" 
data_ingestion.py 

Ingest data into postgreSQL database

author: c-baines
created: 23/4/25
last modified: 21/5/25
"""

import pandas as pd
from pathlib import Path
import os
from src.db import FlightList, Emissions, IcaoList, IsoCodes, IcaoIso, TableName, session
from loguru import logger

here = Path(__file__).resolve().parent 

def dict_to_db(row: dict, table: TableName):
    # make all keys lowercase and remove 'NaN' strings
    row = {k.lower(): v for k,v in row.items() if not str(v).lower()=='nan'}
    if table == TableName.flight_list:
        row.update({'ec_id': row['id']})
        row.pop('id')
        db_obj = FlightList(**row)
    if table == TableName.emissions:
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
        # db_obj = IcaoIso(
        #     icao=row['state code/icao'],
        #     iso_alpha3=row['iso alpha3']
        # )
        db_obj = IcaoIso(**new_row)

    return db_obj

def ingest_csv(filename: str, table: TableName, delimiter: str = ',' ):
    """
    - Reads .csv file
    - For each row: 
        - Changes id to ec_id 
        - Creates FlightList object 
    - Bulk saves to db every 100000 rows 

    Args:
        filename (str): .csv file

    """
    df = pd.read_csv(filename, delimiter=delimiter)
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
        str: full path to each file  
        
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.csv'):
                yield os.path.join(root, file)

def ingest_folder(folder: str, table: TableName, delimiter: str = ','):
    """ 
    - Iterates through folder
    - Calls ingest_csv on each file 
    """
    for filename in iterate_folder(str(here/'data'/folder)):
        # skip files already ingested
        # if "flight_list_2022" in filename or "flight_list_2025" in filename:
        #     logger.info(f"Skipping {filename}")
        #     continue
        logger.info(f"Processing {filename}")
        ingest_csv(filename, table)
        logger.info(f"Finished processing {filename}")

# ingest_folder('flight_list', TableName.flight_list)
# ingest_folder('co2_emissions_by_state', TableName.emissions)
# ingest_folder('iata-icao', TableName.icao_list)
# ingest_folder('iso_codes', TableName.iso_codes)
# ingest_folder('icao_iso', TableName.icao_iso, ';')