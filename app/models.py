from . import db  
from werkzeug.security import generate_password_hash, check_password_hash

class Coach(db.Model):
    CoachID = db.Column(db.Integer, primary_key=True)
    CoachName = db.Column(db.String(100), nullable=False)
    CoachEmail = db.Column(db.String(120), unique=True, nullable=False)
    CoachCode = db.Column(db.String(10), unique=True, nullable=False)
    CoachPasswordHash = db.Column(db.String(120), nullable=False)

    players = db.relationship('Player', back_populates='coach')

   

class Player(db.Model):
    PlayerID = db.Column(db.Integer, primary_key=True)
    PlayerName = db.Column(db.String(100), nullable=False)
    PlayerEmail = db.Column(db.String(120), unique=True, nullable=False)
    CoachCode = db.Column(db.String(10), db.ForeignKey('coach.CoachCode'), nullable=False)
    PlayerPasswordHash = db.Column(db.String(120), nullable=False)

    coach = db.relationship('Coach', back_populates='players')

