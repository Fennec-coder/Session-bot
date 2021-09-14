from Specimen.set import *


class Positions(base):
    __tablename__ = 'positions'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    last_message = db.Column(db.String)
    week_even = db.Column(db.Boolean, default=False)
    day = db.Column(db.Integer, default=0)
    week = db.Column(db.Integer, default=1)
    last_message_id = db.Column(db.Integer)
    last_message_type = db.Column(db.String)
    lesson = db.Column(db.Integer, default=0)
