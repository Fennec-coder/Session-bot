from Specimen.set import *


class Settings(base):
    __tablename__ = 'settings'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    notification = Column(Date)
    notification_switch = Column(Boolean, default=False)

    days_of_the_week_for_notifications = Column(ARRAY(Boolean),
                                                default=[False, False, False, False, False, False, False])
    id_of_the_selected_schedule = Column(Integer, ForeignKey('timetables.id'))
