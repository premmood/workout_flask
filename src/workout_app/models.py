from flask_login import UserMixin
from sqlalchemy.orm import backref
from datetime import datetime
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    workout = db.relationship('Workout', backref='author', lazy=True)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    pushup = db.Column(db.Integer, nullable = False)
    comment = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)