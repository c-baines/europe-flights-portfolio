""" 
data_download.py 

Downloads ``flight_list``, ``flight_events``, ``measurements``, ``co2_emmissions_by_state`` data files from OPDI.

This script is based on the download script available from Eurocontrol. 

Original functionality: Downloads ``flight_list``, ``flight_events`` and ``measurements`` data as parquet files.

Modifications:
    - Add ``co2_emissions_by_state`` data download 
    - Skip file for download if csv with filename already exists
    - Convert parquet to csv for ingestion into PostgreSQL
    - Added function to download new data releases and missing data 

Note: Eurocontrol filename ``co2_emmissions_by_state`` contains a typo for "emissions". 

Original author: Eurocontrol Open Performance Data Initiative
Source: https://www.opdi.aero/flight-list-data
Last modified: 26/8/25 c-baines
"""

import os
import requests
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from pathlib import Path
import pandas as pd
from loguru import logger


# ADDED: get parent directory
here = Path(__file__).resolve().parent 

def generate_urls(data_type: str, start_date: str, end_date: str) -> list:
    """
    Generate a list of URLs for ``flight_list``, ``flight_events``, ``measurements`` or ``co2_emmissions_by_state``.

    Note: Eurocontrol filename for ``co2_emmissions_by_state`` contains a typo for "emissions". 

    Args:
        data_type (str): Type of data ``flight_list``, ``flight_events``, ``measurements``, ``co2_emmissions_by_state``).
        start_date (str): The start date in the format YYYYMM, YYYYMMDD or YYYY.
        end_date (str): The end date in the format YYYYMM, YYYYMMDD or YYYY.

    Returns:
        list: List of generated URLs.
    """
    base_url = f"https://www.eurocontrol.int/performance/data/download/OPDI/v002/{data_type}/{data_type}_"
    emissions_url = f"https://www.eurocontrol.int/performance/data/download/csv/{data_type}_" 

    urls = []
    
    if data_type == "flight_list":  # Monthly intervals
        start_dt = datetime.strptime(start_date, "%Y%m") # crate datetime obj from start_date string
        end_dt = datetime.strptime(end_date, "%Y%m")
        delta = relativedelta(months=1)
    # ADDED: co2_emmissions_by_state data intervals 
    elif data_type == "co2_emmissions_by_state": # Yearly intervals
        start_dt = datetime.strptime(start_date, "%Y")
        end_dt = datetime.strptime(end_date, "%Y")
        delta = relativedelta(years=1)
    else:  # Flight events & Measurements: 10-day intervals
        start_dt = datetime.strptime(start_date, "%Y%m%d")
        end_dt = datetime.strptime(end_date, "%Y%m%d")
        delta = timedelta(days=10)

    current_dt = start_dt
    while current_dt <= end_dt:
        if data_type == "flight_list":
            url = f"{base_url}{current_dt.strftime('%Y%m')}.parquet"
        # ADDED: co2_emmissions-by_state url
        elif data_type == "co2_emmissions_by_state": 
            url = f"{emissions_url}{current_dt.strftime('%Y')}.csv"
        else:
            next_dt = current_dt + delta
            url = f"{base_url}{current_dt.strftime('%Y%m%d')}_{next_dt.strftime('%Y%m%d')}.parquet"
        
        urls.append(url)
        current_dt += delta

    return urls

def download_files(urls: list, save_folder: str):
    """
    Download files from the generated URLs and save them in the specified folder.

    Args:
        urls (list): List of URLs to download.
        save_folder (str): Folder to save downloaded files.
    """
    os.makedirs(save_folder, exist_ok=True)

    for url in urls:
        file_name = url.split("/")[-1] # file_name "flight_list_{YYYYmm}.parquet"
        save_path = os.path.join(save_folder, file_name)
        # ADDED: skip file if file_name.csv already exists 
        csv_path = save_path.split(".")[0] + '.csv'
        if os.path.exists(csv_path): 
            logger.info(f"SKIPPING: {csv_path} already exists.")
            continue

        # MODIFIED: changed from print() to logger.info()
        logger.info(f"DOWNLOADING: {url}")

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            # MODIFIED: changed from print() to logger.info()
            logger.info(f"SAVED TO {save_path}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download {url}: {e}. This month's data may not be released yet")
            continue

        # ADDED: convert .parquet to .csv and delete .parquet
        if save_path.split(".")[-1] == "parquet":
            df = pd.read_parquet(save_path) 
            df.to_csv(save_path.replace('.parquet', '.csv'), index=False)
            logger.info(f"CONVERTED {save_path} to csv")

            os.remove(save_path) 
            logger.info(f"REMOVED {save_path}")

def download_metadata():
    """
    Download metadata files from github. 

    Args:
        urls (list): List of URLs to download.
        save_folder (str):  Folder to save downloaded files.

    """
    urls = [
        "https://raw.githubusercontent.com/ip2location/ip2location-iata-icao/master/iata-icao.csv",
        "https://raw.githubusercontent.com/rikgale/ICAOList/main/Airlines.csv"
    ]

    for url in urls:
        file_name = url.split("/")[-1].lower() 
        save_folder = f"{here}/data/{file_name.split(".")[0]}"
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, file_name)

        if os.path.exists(save_path): 
            logger.info(f"SKIPPING: {file_name} already exists.")
            continue

        logger.info(f"DOWNLOADING: {url}")

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            logger.info(f"SAVED TO {save_path}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download {url}: {e}.")
            continue


# ADDED: update function  
def update(): 
    """
    Checks downloaded data and downloads all new and missing files.
    """
    datasets = {
        "co2_emmissions_by_state": ("2010", datetime.strftime(date.today(), "%Y")),
        "flight_list": ("202201", datetime.strftime(date.today(), "%Y%m"))
        #"flight_events": ("20220101", datetime.strftime(date.today(), "%Y%m"))#,
        #"measurements": ("20220101", datetime.strftime(date.today(), "%Y%m")),
    }
    
    for data_type, (start_date, end_date) in datasets.items():
        urls = generate_urls(data_type, start_date, end_date)
        download_files(urls, f"{here}/data/{data_type}")

# if __name__ == "__main__": 
#     update()
