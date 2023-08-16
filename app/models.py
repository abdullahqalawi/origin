from . import db  
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False) 
    coach_code = db.Column(db.String(10), unique=True, nullable=True)
    def __repr__(self):
        return f'<User {self.username}>'

class Player(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    coach_code = db.Column(db.String(10), unique=True, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'player',
    }

