"""
src/db.py 

Initialise postgreSQL database with variables for flight_list, emissions, icao_list, iso_codes

1. Connects to local postgreSQL 
2. Defines table class with variables 
3. Creates table in postgreSQL

author: c-baines
created: 23/4/25
last modified: 15/7/25 
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
    SQLAlchemy ORM model for the ``flight_list`` table.

    This table stores metadata about individual flights, including aircraft
    identifiers, flight numbers, aerodromes, and timestamps. The data is 
    sourced from Eurocontrol.

    Attributes:
        __tablename__ (str): Database table name (``flight_list``).
        __table_args__ (dict): Additional table configuration (schema = "public").

        id (int): Primary key.
        ec_id (str, optional): Eurocontrol hash identifier for the flight.
        icao24 (str, optional): ICAO 24-bit aircraft identifier.
        flt_id (str, optional): Flight number.
        dof (date, optional): Date of flight.
        adep (str, optional): Actual aerodrome of departure.
        ades (str, optional): Actual aerodrome of destination.
        adep_p (str, optional): Planned aerodrome of departure.
        ades_p (str, optional): Planned aerodrome of destination.
        registration (str, optional): Aircraft registration number.
        model (str, optional): Aircraft model name.
        typecode (str, optional): Aircraft model ICAO type designator.
        icao_aircraft_class (str, optional): ICAO aircraft type class.
        icao_operator (str, optional): ICAO airline/operator code.
        first_seen (datetime, optional): Timestamp when the aircraft was first observed.
        last_seen (datetime, optional): Timestamp when the aircraft was last observed.
        version (str, optional): Algorithm version used to detect flight events.
        unix_time (int, optional): First seen time in Unix epoch seconds.
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
    SQLAlchemy ORM model for the ``co2_emmissions_by_state`` table.

    This table stores data on the CO2 emissions of flights by state. The data is 
    sourced from Eurocontrol.
    
    Attributes:
        __tablename__ (str): Database table name (``co2_emmissions_by_state``).
        __table_args__ (dict): Additional table configuration (schema = "public").

        id (int): Primary key.
        year (int): Year of record.
        month (int): Number of month of record.
        state_name (str): Name of state.
        state_code (str): 2 letter state abbreviation.
        co2_qty_tonnes (flt): Quantitity of CO2 emissions in tonnes (kg).
        tf (int): Traffic for the state. 
        note (bool): Special aggregation for state.
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
    SQLAlchemy ORM model for the ``icao_list`` table.

    This table stores a list of airports with country and region codes, 
    corresponding IATA and ICAO airport codes and the latitude and longitude of the airport.
    
    Attributes:
        __tablename__ (str): Database table name (``icao_list``).
        __table_args__ (dict): Additional table configuration (schema = "public").

        id (int): Primary key.
        country_code (str): Country the airport is located in.
        region_name (str): Region the airport is located in.
        iata (str): IATA code for the airport. 
        icao (str): ICAO code for the airport.
        airport (str): Airport name.
        latitude (flt): Latitude of the airport.
        longitude (flt): Longitude of the airport. 
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
    SQLAlchemy ORM model for the ``iso_codes`` table.

    This table contains a list of countries with region and subregion and intermediate regions, 
    with corresponsing 2 and 3 character ISO codes. 
    
    Attributes:
        __tablename__ (str): Database table name (``iso_codes``).
        __table_args__ (dict): Additional table configuration (schema = "public").

        id (int): Primary key.
        region_name (str): Region name e.g. 'Africa'.
        subregion_name (str): Subregion name e.g. 'Sub-Saharan Africa'.
        intermediate_region_name (str): Intermediate region name e.g. 'Eastern Africa'.
        country (str): Country name.
        iso_alpha2 (str): 2 character ISO country code.
        iso_alpha3 (str): 3 character ISO country code.

    """

    __tablename__ = "iso_codes"
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String)
    region_name = Column(String)
    intermediate_region_name = Column(String)
    subregion_name = Column(String)
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

def create_tables():
    """
    Creates empty tables ``flight_list``, ``co2_emissions``, ``icao_list``, ``iso_codes``, ``icao_iso``, ``airlines`` in PostgreSQL.
    """
    Base.metadata.tables['public.flight_list'].create(engine)
    Base.metadata.tables['public.emissions'].create(engine)
    Base.metadata.tables['public.icao_list'].create(engine)
    Base.metadata.tables['public.iso_codes'].create(engine)
    Base.metadata.tables['public.icao_iso'].create(engine)
    Base.metadata.tables['public.airlines'].create(engine)

