""" 
data_download.py 

Downloads flight_list, flight_events, measurements data files from OPDI.

1. Download .parquet files from OPDI between specified date range
2. Convert to .csv 
3. Delete .parquet files

Author: Eurocontrol Open Performance Data Initiative
Source: https://www.opdi.aero/flight-event-data 
"""

import os
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path
import pandas as pd

# ADDED 24/4/5 c-baines: get parent directory
here = Path(__file__).resolve().parent 

def generate_urls(data_type: str, start_date: str, end_date: str) -> list:
    """
    Generate a list of URLs for flight lists, flight events, or measurements.

    Args:
        data_type (str): Type of data ("flight_list", "flight_events", "measurements").
        start_date (str): The start date in the format YYYYMM or YYYYMMDD.
        end_date (str): The end date in the format YYYYMM or YYYYMMDD.

    Returns:
        list: List of generated URLs.
    """
    base_url = f"https://www.eurocontrol.int/performance/data/download/OPDI/v002/{data_type}/{data_type}_"

    urls = []
    
    if data_type == "flight_list":  # Monthly intervals
        start_dt = datetime.strptime(start_date, "%Y%m")
        end_dt = datetime.strptime(end_date, "%Y%m")
        delta = relativedelta(months=1)
    else:  # Flight events & Measurements: 10-day intervals
        start_dt = datetime.strptime(start_date, "%Y%m%d")
        end_dt = datetime.strptime(end_date, "%Y%m%d")
        delta = timedelta(days=10)

    current_dt = start_dt
    while current_dt <= end_dt:
        if data_type == "flight_list":
            url = f"{base_url}{current_dt.strftime('%Y%m')}.parquet"
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
        file_name = url.split("/")[-1]
        save_path = os.path.join(save_folder, file_name)

        # ADDED 22/4/5 c-baines: skip .parquet if .csv already exists 
        if os.path.exists(save_path.replace('.parquet', '.csv')): 
            print(f"Skipping {file_name}, already exists.")
            continue

        print(f"Downloading {url}...")

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            print(f"Saved to {save_path}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

        # ADDED 22/4/25 c-baines: convert .parquet to .csv 
        df = pd.read_parquet(save_path) 
        df.to_csv(save_path.replace('.parquet', '.csv'), index=False) 

        # ADDED 22/4/25 c-baines: delete .parquet file after conversion
        os.remove(save_path) 

if __name__ == "__main__":
    datasets = {
        "flight_list": ("202501", "202502")#,
        #"flight_events": ("20220101", "20241231")#,
        #"measurements": ("20220101", "20241231")
    }

    for data_type, (start_date, end_date) in datasets.items():
        urls = generate_urls(data_type, start_date, end_date)
        download_files(urls, f"{here}/data/{data_type}")