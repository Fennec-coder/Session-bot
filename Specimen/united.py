from sqlalchemy.orm import sessionmaker
from Specimen.User import *
from Specimen.Settings import *
from Specimen.Positions import *
from Specimen.Timerable import *
from Specimen.set import *

if not database_exists(url):
    create_database(url)

base.metadata.create_all(engine)

Session = sessionmaker(engine)
session = Session()
