from Specimen.set import *


class Settings(base):
    __tablename__ = 'settings'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    notification = db.Column(db.Date)
    notification_switch = db.Column(db.Boolean, default=False)

    time_in_schedule_switch = db.Column(db.Boolean, default=False)

    days_of_the_week_for_notifications = db.Column(db.ARRAY(db.Boolean),
                                                   default=[False, False, False, False, False, False, False])
    id_of_the_selected_schedule = db.Column(db.Integer, db.ForeignKey('timetables.id'))
