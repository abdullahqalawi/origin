from flask import Flask
from app import db
from app.routes import views as views_blueprint
from flask_login import LoginManager
from app.models import Coach, Player ,Exercise, WorkoutRoutine
 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'asdasd'

app.register_blueprint(views_blueprint)


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
        
    """      
        
     # Monday workout (Workout Group 1)
        monday_workout_group1 = WorkoutRoutine(day='Monday', workout_group=1)
        db.session.add(monday_workout_group1)

        monday_exercises_group1 = [
            Exercise(name='Squats', sets=3, reps=12, tutorial_link='https://www.youtube.com/watch?v=nFAscG0XUNY', workout_routine=monday_workout_group1),
            Exercise(name='Leg Extensions', sets=3, tutorial_link='https://www.youtube.com/watch?v=YyvSfVjQeL0',reps=12, workout_routine=monday_workout_group1),
            Exercise(name='Leg Curls', sets=3, reps=12, tutorial_link='https://www.youtube.com/watch?v=1Tq3QdYUuHs',workout_routine=monday_workout_group1),
            Exercise(name='Bulgarian Split Squats', sets=3, reps=10,tutorial_link='https://www.youtube.com/shorts/uODWo4YqbT8', workout_routine=monday_workout_group1),
            Exercise(name='Calf Raises', sets=3, reps=20, tutorial_link='https://www.youtube.com/watch?v=3UWi44yN-wM',workout_routine=monday_workout_group1)
        ]
        db.session.add_all(monday_exercises_group1)

        # Wednesday workout (Workout Group 1)
        wednesday_workout_group1 = WorkoutRoutine(day='Wednesday', workout_group=1)
        db.session.add(wednesday_workout_group1)

        wednesday_exercises_group1 = [
            Exercise(name='Tricep Pushdown', sets=3, reps=12, workout_routine=wednesday_workout_group1),
            Exercise(name='Lateral Raises', sets=3, reps=12, workout_routine=wednesday_workout_group1),
            Exercise(name='Shoulder Press', sets=3, reps=12, workout_routine=wednesday_workout_group1),
            Exercise(name='Dumbbell Row', sets=3, reps=12, workout_routine=wednesday_workout_group1),
            Exercise(name='Bench Press', sets=3, reps=12, workout_routine=wednesday_workout_group1)
        ]
        db.session.add_all(wednesday_exercises_group1)

        # Friday workout (Workout Group 1)
        friday_workout_group1 = WorkoutRoutine(day='Friday', workout_group=1)
        db.session.add(friday_workout_group1)

        friday_exercises_group1 = [
            Exercise(name='Squats', sets=3, reps=12, workout_routine=friday_workout_group1),
            Exercise(name='Leg Extensions', sets=3, reps=12, workout_routine=friday_workout_group1),
            Exercise(name='Leg Curls', sets=3, reps=12, workout_routine=friday_workout_group1),
            Exercise(name='Bulgarian Split Squats', sets=3, reps=10, workout_routine=friday_workout_group1),
            Exercise(name='Calf Raises', sets=3, reps=20, workout_routine=friday_workout_group1)
        ]
        db.session.add_all(friday_exercises_group1)

        db.session.commit()
        
        # Monday workout (Workout Group 2)
        monday_workout_group2 = WorkoutRoutine(day='Monday', workout_group=2)
        db.session.add(monday_workout_group2)

        monday_exercises_group2 = [
            Exercise(name='Squats', sets=3, reps=12, workout_routine=monday_workout_group2),
            Exercise(name='Leg Extensions', sets=3, reps=12, workout_routine=monday_workout_group2),
            Exercise(name='Leg Curls', sets=3, reps=12, workout_routine=monday_workout_group2),
            Exercise(name='Bulgarian Split Squats', sets=3, reps=10, workout_routine=monday_workout_group2),
            Exercise(name='Calf Raises', sets=3, reps=20, workout_routine=monday_workout_group2)
        ]
        db.session.add_all(monday_exercises_group2)

        # Wednesday workout (Workout Group 2)
        wednesday_workout_group2 = WorkoutRoutine(day='Wednesday', workout_group=2)
        db.session.add(wednesday_workout_group2)

        wednesday_exercises_group2 = [
            Exercise(name='Tricep Pushdown', sets=3, reps=12, workout_routine=wednesday_workout_group2),
            Exercise(name='Lateral Raises', sets=3, reps=12, workout_routine=wednesday_workout_group2),
            Exercise(name='Shoulder Press', sets=3, reps=12, workout_routine=wednesday_workout_group2),
            Exercise(name='Dumbbell Row', sets=3, reps=12, workout_routine=wednesday_workout_group2),
            Exercise(name='Bench Press', sets=3, reps=12, workout_routine=wednesday_workout_group2)
        ]
        db.session.add_all(wednesday_exercises_group2)

        # Friday workout (Workout Group 2)
        friday_workout_group2 = WorkoutRoutine(day='Friday', workout_group=2)
        db.session.add(friday_workout_group2)

        friday_exercises_group2 = [
            Exercise(name='Squats', sets=3, reps=12, workout_routine=friday_workout_group2),
            Exercise(name='Leg Extensions', sets=3, reps=12, workout_routine=friday_workout_group2),
            Exercise(name='Leg Curls', sets=3, reps=12, workout_routine=friday_workout_group2),
            Exercise(name='Bulgarian Split Squats', sets=3, reps=10, workout_routine=friday_workout_group2),
            Exercise(name='Calf Raises', sets=3, reps=20, workout_routine=friday_workout_group2)
        ]
        db.session.add_all(friday_exercises_group2)

        db.session.commit() 


        # Monday workout (Workout Group 3)
        monday_workout_group3 = WorkoutRoutine(day='Monday', workout_group=3)
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

        # Monday workout (Workout Group 8)
        monday_workout_group8 = WorkoutRoutine(day='Monday', workout_group=8)
        db.session.add(monday_workout_group8)

        monday_exercises_group8 = [
            Exercise(name='Squats', sets=3, reps=12, workout_routine=monday_workout_group8),
            Exercise(name='Broad Jumps', sets=3, reps=12, workout_routine=monday_workout_group8),
            Exercise(name='Box Jumps', sets=3, reps=12, workout_routine=monday_workout_group8),
            Exercise(name='Deadlift', sets=3, reps=12, workout_routine=monday_workout_group8),
            Exercise(name='Calf Raises', sets=3, reps=30, workout_routine=monday_workout_group8)
        ]
        db.session.add_all(monday_exercises_group8)

        # Wednesday workout (Workout Group 8)
        wednesday_workout_group8 = WorkoutRoutine(day='Wednesday', workout_group=8)
        db.session.add(wednesday_workout_group8)

        wednesday_exercises_group8 = [
            Exercise(name='Front Raises', sets=3, reps=12, workout_routine=wednesday_workout_group8),
            Exercise(name='Shoulder Press', sets=3, reps=12, workout_routine=wednesday_workout_group8),
            Exercise(name='Seated Cable Rows', sets=3, reps=12, workout_routine=wednesday_workout_group8),
            Exercise(name='Lat Pulldown', sets=3, reps=12, workout_routine=wednesday_workout_group8),
            Exercise(name='Incline Bench Press', sets=3, reps=12, workout_routine=wednesday_workout_group8)
        ]
        db.session.add_all(wednesday_exercises_group8)

        # Friday workout (Workout Group 8)
        friday_workout_group8 = WorkoutRoutine(day='Friday', workout_group=8)
        db.session.add(friday_workout_group8)

        friday_exercises_group8 = [
            Exercise(name='Squats', sets=3, reps=12, workout_routine=friday_workout_group8),
            Exercise(name='Broad Jumps', sets=3, reps=12, workout_routine=friday_workout_group8),
            Exercise(name='Box Jumps', sets=3, reps=12, workout_routine=friday_workout_group8),
            Exercise(name='Deadlift', sets=3, reps=12, workout_routine=friday_workout_group8),
            Exercise(name='Calf Raises', sets=3, reps=30, workout_routine=friday_workout_group8)
        ]
        db.session.add_all(friday_exercises_group8)

        db.session.commit()
 """