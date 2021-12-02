from Specimen.set import *


class Schedule(base):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)

    time_of_one_lesson = db.Column(db.Interval, default=timedelta(minutes=90))

    table_E = db.Column(db.ARRAY(db.Time))
    table_NE = db.Column(db.ARRAY(db.Time))

