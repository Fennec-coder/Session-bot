from Specimen.set import *


class ExternalSchedules(base):
    __tablename__ = 'external_schedules'

    """info"""
    user_id = db.Column(db.String, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    university_name = db.Column(db.String)
    description = db.Column(db.String)
