from Specimen.set import *
from sqlalchemy.dialects import postgresql


class Timetable(base):
    __tablename__ = 'timetables'
    id = Column(Integer, primary_key=True)

    name = Column(String, default='-')
    creator = Column(Integer, default=0)
    public = Column(Boolean, default=False)

    table = Column(postgresql.ARRAY(String))
