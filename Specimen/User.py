from Specimen.set import *


class User(base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, default="no name")
    date = db.Column(db.Date, default=datetime.today())  # date of the last message sent
    language = db.Column(db.String, default='us')
    utc = db.Column(db.Float, default=3)
