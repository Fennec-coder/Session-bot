from Specimen.set import *


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    username = Column(String, default="no name")
    date = Column(Date, default=datetime.today())  # date of the last message sent
    language = Column(String, default='us')
    utc = Column(Float, default=3)
