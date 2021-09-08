from datetime import datetime
import sqlalchemy as db

from sqlalchemy import Column, String, Integer, Float, Boolean, ARRAY, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_utils import create_database, database_exists

import configparser

config = configparser.ConfigParser()  # parser object
config.read("config/settings.ini")  # read the configuration from the ini file

url = config["postgresql"]["url"]

engine = db.create_engine(url)
base = declarative_base()
