from Specimen.set import *


class Positions(base):
    __tablename__ = 'positions'

    """info message"""
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    last_message_id = db.Column(db.Integer)
    last_message_text = db.Column(db.String)
    last_message_type = db.Column(db.String)

    """WEEK"""
    week_even = db.Column(db.Boolean, default=False)
    day = db.Column(db.Integer, default=0)
    lesson = db.Column(db.Integer, default=0)
