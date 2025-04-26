"""
db.py 

Initialise postgreSQL database with flight_list variables

1. Connect to local postgreSQL 
2. Define table class with variables 
3. Create table in postgreSQL

c-baines
23/4/25 
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy import Column, Integer, String, DateTime
from dotenv import load_dotenv, find_dotenv
import os

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

# creating the db session for querying and add entries in tables
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
    dof (str): Date of flight
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
    dof = Column(String, nullable=True)
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

# Create just the "flight_list" table, run this the first time 
# Base.metadata.tables['public.flight_list'].create(engine)
