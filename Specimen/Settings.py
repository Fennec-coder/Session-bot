from Specimen.set import *


class Settings(base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    eoo = Column(Boolean, default=False)
    notification = Column(Date)
    notification_switch = Column(Boolean, default=False)
    time_board_instead_of_numbering = Column(Boolean, default=False)

    days_of_the_week_for_notifications = Column(ARRAY(Boolean),
                                                default=[False, False, False, False, False, False, False])
    id_of_the_selected_schedule = Column(Integer, ForeignKey('timetables.id'))
