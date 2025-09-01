"""
setup/data_update.py

Downloads and ingests new data releases and updates PostgreSQL DB. 

created: 26/7/25
modified: 29/8/25
"""

from setup import data_ingestion as ingest, data_download as download
from setup.data_download import download_metadata 
from src.db import create_tables

# download data 
# download_metadata()

# ingest data
# create_tables() # create empty DB tables
# ingest.setup() # ingset all data


# update data 
# download.update() # download new data releases 
# ingest.update() # ingest new data releases 




