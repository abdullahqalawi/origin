from . import db  
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta



class Coach( UserMixin,db.Model):
    CoachID = db.Column(db.Integer, primary_key=True)
    CoachName = db.Column(db.String(100), nullable=False)
    CoachEmail = db.Column(db.String(120), unique=True, nullable=False)
    CoachCode = db.Column(db.String(10), unique=True, nullable=False)
    CoachPasswordHash = db.Column(db.String(120), nullable=False)

    def get_id(self):
        return str(self.CoachID)
    players = db.relationship('Player', back_populates='coach')
    def set_password(self, password):
        self.CoachPasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.CoachPasswordHash, password)


    
class Player(UserMixin,db.Model):
    PlayerID = db.Column(db.Integer, primary_key=True)
    PlayerName = db.Column(db.String(5000), nullable=False)
    PlayerEmail = db.Column(db.String(120), unique=True, nullable=False)
    CoachCode = db.Column(db.String(10), db.ForeignKey('coach.CoachCode'), nullable=True)
    PlayerPasswordHash = db.Column(db.String(120), nullable=False)
    Position = db.Column(db.String(50), nullable=True)
    Finishing = db.Column(db.Integer, nullable=True)
    Shooting = db.Column(db.Integer, nullable=True)
    Rebounding = db.Column(db.Integer, nullable=True)
    Workout_code = db.Column(db.Integer, nullable=True)
    CoachFeedback = db.Column(db.Text, nullable=True)


    workouts = db.relationship('WorkoutRoutine', secondary='player_workout', lazy='subquery',backref=db.backref('players', lazy=True))

    player_workouts = db.relationship('PlayerWorkout', back_populates='player', lazy=True, foreign_keys='PlayerWorkout.player_id')
    CoachCode = db.Column(db.String(10), db.ForeignKey('coach.CoachCode'), nullable=True)
    coach = db.relationship('Coach', back_populates='players')


    matches = db.relationship('Match', backref='player', lazy=True)

    def get_id(self):
        return str(self.PlayerID)

    
    
    coach = db.relationship('Coach', back_populates='players')

    def set_password(self, password):
        self.PlayerPasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.PlayerPasswordHash, password)

    def get_upcoming_workouts(self, day):
        workout_group = self.Workout_code
        upcoming_workouts = PlayerWorkout.query.join(WorkoutRoutine).filter(
            PlayerWorkout.player_id == self.PlayerID,
            WorkoutRoutine.day == day,
            WorkoutRoutine.workout_group == workout_group
        ).all()
        return upcoming_workouts
    
    @property
    def average_assists(self):
        total_assists = sum(match.assists for match in self.matches)
        return total_assists / len(self.matches) if len(self.matches) > 0 else 0

    @property
    def average_points(self):
        total_points = sum(match.points for match in self.matches)
        return total_points / len(self.matches) if len(self.matches) > 0 else 0

    @property
    def average_rebounds(self):
        total_rebounds = sum(match.rebounds for match in self.matches)
        return total_rebounds / len(self.matches) if len(self.matches) > 0 else 0

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_number = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    rebounds = db.Column(db.Integer, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.PlayerID'), nullable=False)

class WorkoutRoutine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50), nullable=True)
    workout_group = db.Column(db.Integer, nullable=True)  
    exercises = db.relationship('Exercise', backref='workout_routine', lazy=True)


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    sets = db.Column(db.String(50), nullable=True)
    reps = db.Column(db.String(50), nullable=True)
    workout_routine_id = db.Column(db.Integer, db.ForeignKey('workout_routine.id'), nullable=True)


class PlayerWorkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.PlayerID'))
    workout_routine_id = db.Column(db.Integer, db.ForeignKey('workout_routine.id'))
    exercise_name = db.Column(db.Integer, db.ForeignKey('exercise.name'))
    sets = db.Column(db.String(50), nullable=True)
    reps = db.Column(db.String(50), nullable=True)

    player = db.relationship('Player', back_populates='player_workouts', foreign_keys=[player_id])


""" def get_upcoming_workouts(self):
        workout_days = ['Monday', 'Wednesday', 'Friday']
        today = datetime.now().date()

        # Find the next workout day
        next_workout_day = None
        for day in workout_days:
            if day == 'Monday' and today.weekday() <= 3:
                next_workout_day = day
                break
            elif day == 'Wednesday' and today.weekday() <= 2:
                next_workout_day = day
                break
            elif day == 'Friday' and today.weekday() <= 4:
                next_workout_day = day
                break

        if next_workout_day:
            upcoming_workouts = WorkoutRoutine.query.filter_by(day=next_workout_day).all()
            return next_workout_day, upcoming_workouts
        else:
            return None, [] """