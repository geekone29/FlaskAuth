from . import db
from flask_login import UserMixin # Import UserMixin to add user session methods to the User model
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    # Column to store the date and time the note was created, defaulting to the current time
    date = db.Column(db.DateTime(timezone=True), default=func.now()) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(200))
    first_name = db.Column(db.String(200))
    notes = db.relationship('Note')