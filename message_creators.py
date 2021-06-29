from Specimen import User
import database


def language(user=User.User, user_language='us'):
    if user.id == 0:
        return "Sorry sweetheart, but I have no data about you, try to write /start.\n<3"
    user.language = user_language
    return f"Your preferred language => {user.language}"
