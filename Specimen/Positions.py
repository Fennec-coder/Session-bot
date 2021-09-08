from Specimen.set import *


class Positions(base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    last_message = Column(String)
    week_even = Column(Boolean, default=False)  # поменять местами неделю
    day = Column(Integer, default=0)
    week = Column(Integer, default=1)
    last_message_id = Column(Integer)
    last_message_type = Column(String)
    lesson = Column(Integer, default=0)
