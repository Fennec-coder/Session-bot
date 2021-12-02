from Specimen.set import *


class Timetable(base):
    __tablename__ = 'timetables'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, default='-')
    creator = db.Column(db.Integer, default=0)
    public = db.Column(db.Boolean, default=False)

    table_E = db.Column(db.ARRAY(db.String))
    table_NE = db.Column(db.ARRAY(db.String))

    id_of_schedule = db.Column(db.Integer, db.ForeignKey('schedules.id'))
