from sqlalchemy.orm import sessionmaker
from Specimen.User import *
from Specimen.Settings import *
from Specimen.Positions import *
from Specimen.Timerable import *
from Specimen.Schedule import *
from Specimen.set import *

if not database_exists(url):
    create_database(url)

base.metadata.create_all(engine)

Session = sessionmaker(engine)
session = Session()


def user_validation(user_id, database_check=False, give_user=False, show_info=False):
    restoration_carried_out = False
    if database_check:
        base.metadata.create_all(engine)

    if session.get(User, user_id) is None:
        session.add(User(id=user_id))
        session.commit()
        restoration_carried_out = True

    if session.get(Positions, user_id) is None:
        session.add(Positions(user_id=user_id))
        session.commit()
        restoration_carried_out = True

    if session.get(Settings, user_id) is None:
        session.add(Settings(user_id=user_id))
        session.commit()
        restoration_carried_out = True

    if show_info:
        print(f"{user_id}: {'Restored' if restoration_carried_out else 'OK'}")

    return session.get(User, user_id) if give_user else None


def validation_all_users():
    print('!checking the correctness of user data has been started:')
    for user_id in session.query(User.id).distinct():
        user_validation(int(user_id[0]), database_check=True, show_info=True)


validation_all_users()
