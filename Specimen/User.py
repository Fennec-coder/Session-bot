from datetime import datetime
import database

class User:
    id = 0
    name = 'unknown'
    date = datetime.now().date()  # date of the last message sent
    language = 'us'
    utc = 0

    def fill_information_with_an_array(self, array):
        if array is not None:
            self.id = array[0]
            self.name = array[1]
            self.date = array[2]
            self.language = array[3]
            self.utc = array[4]

    def __init__(self, id):
        information = database.get_user_array(id)
        self.fill_information_with_an_array(information)



class Settings:
    eoo = False
    notification = datetime.now().time()
    notification_switch = False
    time_board_instead_of_numbering = False
    days_of_the_week_for_notifications = [False, False, False, False, False, False, False]

    def fill_information_with_an_array(self, array):
        if array is not None:
            self.eoo = array[0]
            self.notification = array[1]
            self.notification_switch = array[2]
            self.time_board_instead_of_numbering = array[3]
            self.days_of_the_week_for_notifications = array[4]


class Position:
    user_id = 0
    last_message = 'null'
    week_even = False,  # поменять местами неделю
    day = 1
    week = 0
    last_message_id = 0,
    last_message_type = 'null'
    lesson = 0

    def fill_information_with_an_array(self, array):
        if array is not None:
            self.user_id = array[0]
            self.last_message = array[1]
            self.week_even = array[2]
            self.day = array[3]
            self.week = array[4]
            self.last_message_id = array[5]
            self.last_message_type = array[6]
            self.lesson = array[7]