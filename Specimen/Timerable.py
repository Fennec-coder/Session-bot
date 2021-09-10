import datetime

from Specimen.set import *


class Timetable(base):
    __tablename__ = 'timetables'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, default='-')
    creator = db.Column(db.Integer, default=0)
    public = db.Column(db.Boolean, default=False)

    table_E = db.Column(db.ARRAY(db.String))
    table_NE = db.Column(db.ARRAY(db.String))

    time_of_one_lesson = db.Column(db.Interval, default=timedelta(minutes=90))
    start_schedule = ['8:30', '10:10', '11:50', '14:00', '15:40', '17:20', '19:00']
