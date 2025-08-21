"""
setup/data_update.py

Downloads and ingests new data releases and updates PostgreSQL DB. 

created: 26/7/25
modified: 4/8/25
"""

from setup import data_ingestion as ingest, data_download as download

# download data 
download.update()

# ingest data
ingest.update() # want to speed this up - far too slow

# update materialized views 

