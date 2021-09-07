from datetime import datetime
import sqlalchemy as db

from sqlalchemy import Column, String, Integer, Float, Boolean, ARRAY, Date
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_utils import create_database, database_exists

import configparser

config = configparser.ConfigParser()  # parser object
config.read("config/settings.ini")  # read the configuration from the ini file

url = config["postgresql"]["url"]

engine = db.create_engine(url)
base = declarative_base()


class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, default=0)
    username = Column(String, default="no name")
    date = Column(Date, default=datetime.today())  # date of the last message sent
    language = Column(String, default='us')
    utc = Column(Float, default=3)


class Settings(base):
    __tablename__ = 'settings'

    user_id = Column(Integer, primary_key=True)
    eoo = Column(Boolean)
    notification = Column(Date)
    notification_switch = Column(Boolean)
    time_board_instead_of_numbering = Column(Boolean)
    # days_of_the_week_for_notifications = [False, False, False, False, False, False, False]
    days_of_the_week_for_notifications = Column(ARRAY(Boolean))


class Positions(base):
    __tablename__ = 'positions'

    user_id = Column(Integer, primary_key=True)
    last_message = Column(String)
    week_even = Column(Boolean)  # поменять местами неделю
    day = Column(Integer)
    week = Column(Integer)
    last_message_id = Column(Integer)
    last_message_type = Column(String)
    lesson = Column(Integer)


if not database_exists(url):
    create_database(url)

base.metadata.create_all(engine)
