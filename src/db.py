"""
src/db.py 

Initialise postgreSQL database with variables for flight_list, emissions, icao_list, iso_codes

1. Connect to local postgreSQL 
2. Define table class with variables 
3. Create table in postgreSQL

author: c-baines
created: 23/4/25
last modified: 12/5/25 
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL
from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Boolean
from dotenv import load_dotenv, find_dotenv
import os
from enum import Enum

load_dotenv(find_dotenv())

# create dialect+driver://username:password@host:port/database to connect to postgresql
# postgresql://postgres:DB_PADSSWORD@localhost:5432/postgres
url = URL.create(
    drivername="postgresql",
    username="postgres",
    password=os.getenv('DB_PASSWORD'),
    host="localhost",
    database="postgres",
    port="5432",
)

# create the db session for querying and add entries in tables
engine = create_engine(url=url) 
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = session()

Base = declarative_base()

# create class of objects that inherts from Base class (SQL class)
class FlightList(Base):
    """
    Represents table flight_list in the db

    Attributes:
    __tablename__ (str): PostgreSQL table name 
    __table_args__ (dict): Additional table arguments
    id (int): Primary key of the table
    ec_id (str): Eurocontrol hash id 
    icao24 (str): International Civil Avation Organization aircraft identifier
    flt_id (str): Flight number
    dof (date): Date of flight
    adep (str): Aerodrome of departure
    ades (str): Aerodrome of destination 
    adep_p (str): Planned aerodrome of departure
    ades_p (str): Planned aerodrome of destination 
    registration (str): Aircraft registration number
    model (str): Aircraft model name
    typecode (str): Aircraft model code
    icao_aircraft_class (str): Aircraft type class
    icao_operator (str): Airline code
    first_seen (datetime): Time aircraft first seen
    last_seen (datetime): Time aircraft last seen
    version (str): Algorithm version used to detect flight events
    unix_time (int): first_seen in unix time  

    """
    
    __tablename__ = "flight_list"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    ec_id = Column(String, nullable=True)
    icao24 = Column(String, nullable=True)
    flt_id = Column(String, nullable=True)
    dof = Column(Date, nullable=True)
    adep = Column(String, nullable=True)
    ades = Column(String, nullable=True)
    adep_p = Column(String, nullable=True)
    ades_p = Column(String, nullable=True)
    registration = Column(String, nullable=True)
    model = Column(String, nullable=True)
    typecode = Column(String, nullable=True)
    icao_aircraft_class = Column(String, nullable=True)
    icao_operator = Column(String, nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    version = Column(String, nullable=True)
    unix_time = Column(Integer, nullable=True)

class Emissions(Base):
    """
    Represents emissions table in the db
    
    Attributes:
        __tablename__ (str): PostgreSQL table name 
        __table_args__ (dict): Additional table arguments
        year (int): year of record
        month (int): number of month of record
        state_name (str): name of state
        state_code (str): 2 letter state abbreviation
        co2_qty_tonnes (flt): quantitity of CO2 emissions in tonnes (kg)
        tf (int): traffic for the state 
        note (bool): special aggregation for state
    """

    __tablename__ = "emissions"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer)
    month = Column(Integer)
    state_name = Column(String)
    state_code = Column(String)
    co2_qty_tonnes = Column(Float)
    tf = Column(Integer)
    note = Column(Boolean)

class IcaoList(Base):
    """
    Represents table icao_list in db

    Attributes:
        __tablename__ (str): 
        __table_args__ (str):
        country_code (str):
        region_name (str):
        iata (str):
        icao (str):
        airport (str):
        latitude (flt):
        longitude (flt):

    """

    __tablename__ = "icao_list"
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_code = Column(String)
    region_name = Column(String)
    iata = Column(String)
    icao = Column(String)
    airport = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

class IsoCodes(Base):
    """
    Represents table iso_codes in db

    Attributes:
        __tablename__ (str):
        __table_args__ (str):
        id (int):
        region_name (str):
        subregion_name (str):
        intermediate_region_name (str):
        country (str):
        iso_alpha2 (str):
        iso_alpha3 (str): 

    """

    __tablename__ = "iso_codes"
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    region_name = Column(String)
    subregion_name = Column(String)
    intermediate_region_name = Column(String)
    country = Column(String)
    iso_alpha2 = Column(String)
    iso_alpha3 = Column(String)

class IcaoIso(Base):
    
    __tablename__ = 'icao_iso'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    emissions_state_name = Column(String)
    icao_state_name = Column(String)
    icao = Column(String)
    iso_alpha3 = Column(String)

class Airlines(Base):

    __tablename__ = 'airlines'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    airline = Column(String)
    country = Column(String)
    telephony = Column(String)
    icao_operator_code = Column(String)

class TableName(Enum):
    emissions = 'emissions'
    flight_list = 'flight_list'
    icao_list = 'icao_list' 
    iso_codes = 'iso_codes'
    icao_iso = "icao_iso"
    airlines = "airlines" 


# Create just the "flight_list"/"co2_emissions"/"icao_list/iso_codes" table, run this the first time
# Comment out when running data_ingestion.py
# Base.metadata.tables['public.flight_list'].create(engine)
# Base.metadata.tables['public.emissions'].create(engine)
# Base.metadata.tables['public.icao_list'].create(engine)
# Base.metadata.tables['public.iso_codes'].create(engine)
# Base.metadata.tables['public.icao_iso'].create(engine)
# Base.metadata.tables['public.airlines'].create(engine)

