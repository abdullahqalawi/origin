from . import db  
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Coach( UserMixin,db.Model):
    CoachID = db.Column(db.Integer, primary_key=True)
    CoachName = db.Column(db.String(100), nullable=False)
    CoachEmail = db.Column(db.String(120), unique=True, nullable=False)
    CoachCode = db.Column(db.String(10), unique=True, nullable=False)
    CoachPasswordHash = db.Column(db.String(120), nullable=False)

    players = db.relationship('Player', back_populates='coach')
    def set_password(self, password):
        self.CoachPasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.CoachPasswordHash, password)
   

class Player(UserMixin,db.Model):
    PlayerID = db.Column(db.Integer, primary_key=True)
    PlayerName = db.Column(db.String(100), nullable=False)
    PlayerEmail = db.Column(db.String(120), unique=True, nullable=False)
    CoachCode = db.Column(db.String(10), db.ForeignKey('coach.CoachCode'), nullable=True)
    PlayerPasswordHash = db.Column(db.String(120), nullable=False)

    Position = db.Column(db.String(50))
    Finishing = db.Column(db.Integer)
    Shooting = db.Column(db.Integer)
    Rebounding = db.Column(db.Integer)

    
    coach = db.relationship('Coach', back_populates='players')

    def set_password(self, password):
        self.PlayerPasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.PlayerPasswordHash, password)