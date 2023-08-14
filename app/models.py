from . import db  # Import db from the current package

# Define the User class after initializing the db object
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class CoachPlayerConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coach_code = db.Column(db.String(10), unique=True, nullable=False)
    player_code = db.Column(db.String(10), unique=True, nullable=False)

    coach = db.relationship('User', foreign_keys=[coach_id])
    player = db.relationship('User', foreign_keys=[player_id])
