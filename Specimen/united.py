from sqlalchemy.orm import sessionmaker
from Specimen.necessary_for_the_user import *

Session = sessionmaker(engine)
session = Session()


