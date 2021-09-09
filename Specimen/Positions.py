from Specimen.set import *


class Positions(base):
    __tablename__ = 'positions'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    last_message = Column(String)
    week_even = Column(Boolean, default=False)  # поменять местами неделю
    day = Column(Integer, default=0)
    week = Column(Integer, default=1)
    last_message_id = Column(Integer)
    last_message_type = Column(String)
    lesson = Column(Integer, default=0)
