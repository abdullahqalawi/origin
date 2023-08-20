from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta


class Coach(UserMixin, db.Model):
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
    

    


class Player(UserMixin, db.Model):
    PlayerID = db.Column(db.Integer, primary_key=True)
    PlayerName = db.Column(db.String(5000), nullable=False)
    PlayerEmail = db.Column(db.String(120), unique=True, nullable=False)
    CoachCode = db.Column(db.String(10), db.ForeignKey(
        'coach.CoachCode'), nullable=True)
    PlayerPasswordHash = db.Column(db.String(120), nullable=False)
    Position = db.Column(db.String(50), nullable=True)
    Finishing = db.Column(db.Integer, nullable=True)
    Shooting = db.Column(db.Integer, nullable=True)
    Rebounding = db.Column(db.Integer, nullable=True)
    Workout_code = db.Column(db.Integer, nullable=True)

    workouts = db.relationship('WorkoutRoutine', secondary='player_workout', lazy='subquery', backref=db.backref('players', lazy=True))

    personalized_workout = db.relationship('PersonalizedPlayerWorkout', backref='player', uselist=False)

    CoachCode = db.Column(db.String(10), db.ForeignKey('coach.CoachCode'), nullable=True)

    coach = db.relationship('Coach', back_populates='players')

    def get_id(self):
        return str(self.PlayerID)

    coach = db.relationship('Coach', back_populates='players')

    def set_password(self, password):
        self.PlayerPasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.PlayerPasswordHash, password)

    def get_upcoming_workouts(self):
        today = datetime.now().date()
        # Calculate days until next Monday
        days_ahead = (0 - today.weekday()) % 7

        if days_ahead == 0:
            upcoming_day = today + timedelta(days=2)  # Wednesday
        elif days_ahead == 1:
            upcoming_day = today + timedelta(days=1)  # Wednesday
        elif days_ahead == 2:
            upcoming_day = today + timedelta(days=2)  # Friday
        else:
            upcoming_day = today + timedelta(days=(4 - days_ahead))  # Monday

        day_name = upcoming_day.strftime('%A')

        # Assuming Workout_code corresponds to the workout group
        workout_group = self.Workout_code

        upcoming_workouts = WorkoutRoutine.query.filter_by(day=day_name).filter_by(
            day=day_name, workout_group=workout_group).all()

        return upcoming_workouts

class PersonalizedPlayerWorkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.CoachID'), nullable=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.PlayerID'), nullable=True)
    exercises = db.relationship('PersonalizedExercise', backref='personalized_workout', lazy=True)

class PersonalizedExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    sets = db.Column(db.String(50), nullable=True)
    reps = db.Column(db.String(50), nullable=True)
    personalized_workout_id = db.Column(db.Integer, db.ForeignKey('personalized_player_workout.id'), nullable=True)


class WorkoutRoutine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50), nullable=True)
    workout_group = db.Column(db.Integer, nullable=True)  # New field
    exercises = db.relationship(
        'Exercise', backref='workout_routine', lazy=True)


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    sets = db.Column(db.String(50), nullable=True)
    reps = db.Column(db.String(50), nullable=True)
    workout_routine_id = db.Column(
        db.Integer, db.ForeignKey('workout_routine.id'), nullable=True)


class PlayerWorkout(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey(
        'player.PlayerID'), primary_key=True)
    workout_routine_id = db.Column(db.Integer, db.ForeignKey(
        'workout_routine.id'), primary_key=True)


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
