from flask import Flask
from app import db
from app.routes import views as views_blueprint
from flask_login import LoginManager
from app.models import Coach, Player ,Exercise, WorkoutRoutine
 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'asdasd'

app.register_blueprint(views_blueprint)

# Initialize and configure Flask-Login outside the app context
login_manager = LoginManager(app)
login_manager.login_view = 'views.login'

@login_manager.user_loader
def load_user(user_id):
    return Coach.query.get(int(user_id)) or Player.query.get(int(user_id))

if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.create_all()
        app.run(host='0.0.0.0', port=5000)
        
           # Monday workout (Workout Group 3)
        """ monday_workout_group3 = WorkoutRoutine(day='Monday', workout_group=3)
        db.session.add(monday_workout_group3)

        monday_exercises_group3 = [
            Exercise(name='Squats', sets=3, reps=12, workout_routine=monday_workout_group3),
            Exercise(name='Leg Extensions', sets=3, reps=12, workout_routine=monday_workout_group3),
            Exercise(name='Leg Curls', sets=3, reps=12, workout_routine=monday_workout_group3),
            Exercise(name='Weighted Step Ups', sets=3, reps=12, workout_routine=monday_workout_group3),
            Exercise(name='Calf Raises', sets=3, reps=20, workout_routine=monday_workout_group3)
        ]
        db.session.add_all(monday_exercises_group3)

        # Wednesday workout (Workout Group 3)
        wednesday_workout_group3 = WorkoutRoutine(day='Wednesday', workout_group=3)
        db.session.add(wednesday_workout_group3)

        wednesday_exercises_group3 = [
            Exercise(name='Tricep Pushdown', sets=3, reps=12, workout_routine=wednesday_workout_group3),
            Exercise(name='Lateral Raises', sets=3, reps=12, workout_routine=wednesday_workout_group3),
            Exercise(name='Shoulder Press', sets=3, reps=12, workout_routine=wednesday_workout_group3),
            Exercise(name='Lat Pulldown', sets=3, reps=12, workout_routine=wednesday_workout_group3),
            Exercise(name='Bench Press', sets=3, reps=12, workout_routine=wednesday_workout_group3)
        ]
        db.session.add_all(wednesday_exercises_group3)

        # Friday workout (Workout Group 3)
        friday_workout_group3 = WorkoutRoutine(day='Friday', workout_group=3)
        db.session.add(friday_workout_group3)

        friday_exercises_group3 = [
            Exercise(name='Squats', sets=3, reps=12, workout_routine=friday_workout_group3),
            Exercise(name='Leg Extensions', sets=3, reps=12, workout_routine=friday_workout_group3),
            Exercise(name='Leg Curls', sets=3, reps=12, workout_routine=friday_workout_group3),
            Exercise(name='Weighted Step Ups', sets=3, reps=12, workout_routine=friday_workout_group3),
            Exercise(name='Calf Raises', sets=3, reps=20, workout_routine=friday_workout_group3)
        ]
        db.session.add_all(friday_exercises_group3)

        db.session.commit() 
         """
    
       