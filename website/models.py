from enum import unique
from sqlalchemy.orm import relationship
from werkzeug.wrappers import request
from . import db 
from flask_login import UserMixin
from datetime import datetime

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    img = db.Column(db.String(250), unique=True, nullable=False)
    attack = db.Column(db.Integer, nullable=False )
    intelligence = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    wins = db.Column(db.Integer)
    defeats = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # user = db.relationship('User', foreign_keys='Card.user_id')

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    cards = db.relationship('Card', backref='user')

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(20))