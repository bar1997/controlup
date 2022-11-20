from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    # The reason I have this 2 fields is only because not to waste time, I wanted to show that ive a mechanism of
    # password hashing, and I also need to authenticate to yad2 with the real password, so that's why I have 2 fields
    # for the same thing.
    saved_password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    severity = db.Column(db.String(100), unique=False)
    message = db.Column(db.String(1000))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
