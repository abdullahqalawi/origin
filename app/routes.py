from flask import Blueprint,render_template, request, redirect, flash, session,url_for
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from .models import Coach, Player ,Exercise,PlayerWorkout,WorkoutRoutine
import random
import string


def generate_coach_code():
    characters = string.ascii_uppercase + string.digits
    code_length = 6
    return ''.join(random.choice(characters) for _ in range(code_length))


def generate_player_code():
    characters = string.ascii_letters + string.digits
    code_length = 8
    return ''.join(random.choice(characters) for _ in range(code_length))


views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
@login_required 
def home():
    if 'user_id' in session:
        user_type = session.get('user_type')
        if user_type == 'coach':
            return render_template('coach_home.html')
        elif user_type == 'player':
            player_id = session['user_id']
            player = Player.query.get(player_id)
    
            
            if player.Position is None or player.Finishing is None or player.Shooting is None or player.Rebounding is None:
                return redirect('/player_form')  
            
            coach = Coach.query.filter_by(CoachCode=player.CoachCode).first()


            return render_template('player_home.html', player=player, coach=coach)
    return redirect('/login')


@views.route('/login/', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        coach = Coach.query.filter_by(CoachName=username).first()
        player = Player.query.filter_by(PlayerName=username).first()

        if coach and coach.check_password(password):
            session['user_id'] = coach.CoachID
            session['user_type'] = 'coach'  
            login_user(coach)
            return redirect('/')
        elif player and player.check_password(password):
            session['user_id'] = player.PlayerID
            session['user_type'] = 'player'  
            login_user(player) 
            return redirect('/')
        else:
            flash('Wrong username or password!')
            return redirect('/login')

    return render_template('login.html')


@views.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        new_email = request.form['new_email']
        role = request.form['role']

        existing_coach = Coach.query.filter_by(CoachEmail=new_email).first()
        existing_player = Player.query.filter_by(PlayerEmail=new_email).first()

        if existing_coach or existing_player:
            flash('Email already in use. Please choose another.')
        elif new_password != confirm_password:
            flash('Passwords do not match. Please re-enter.')
        else:
            hashed_password = generate_password_hash(new_password)
            if role == 'coach':
                coach_code = generate_coach_code()
                new_coach = Coach(CoachName=new_username, CoachEmail=new_email, CoachCode=coach_code, CoachPasswordHash=hashed_password)
                new_coach.set_password(new_password)
                db.session.add(new_coach)

            elif role == 'player':
                new_player = Player(PlayerName=new_username, PlayerEmail=new_email, CoachCode=None, PlayerPasswordHash=hashed_password)
                new_player.set_password(new_password)
                db.session.add(new_player)
                
            else:
                flash('Invalid role.')
                return redirect('/signup')

            
            db.session.commit()

            flash('Signup successful! You can now log in.')
            return redirect('/login')

    return render_template('signup.html')




@views.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    coach = Coach.query.get(user_id)
    player = Player.query.get(user_id)

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']

        if (coach and coach.check_password(current_password)) or (player and player.check_password(current_password)):
            if new_password == confirm_new_password:
                hashed_password = generate_password_hash(new_password)
                if coach:
                    coach.CoachPasswordHash = hashed_password
                elif player:
                    player.PlayerPasswordHash = hashed_password
                db.session.commit()
                flash('Password changed successfully!')
                return redirect('/')
            else:
                flash('New passwords do not match.')
        else:
            flash('Incorrect current password.')

    return render_template('change_password.html')




@views.route('/delete_account/', methods=['GET', 'POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    coach = Coach.query.get(user_id)
    player = Player.query.get(user_id)

    if request.method == 'POST':
        db.session.delete(coach or player)
        db.session.commit()
        session.pop('user_id', None)
        flash('Account deleted successfully!')
        return redirect('/')
    return render_template('delete_account.html', coach=coach, player=player)



@views.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['email']
        
        coach = Coach.query.filter_by(CoachEmail=email).first()
        player = Player.query.filter_by(PlayerEmail=email).first()
        
        if coach or player:
            session['reset_email'] = email
            return redirect('/reset_password')
        else:
            flash('Email not found. Please enter a valid email address.')
    
    return render_template('forget_password.html')


@views.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        
        if new_password == confirm_new_password:
            email = session.get('reset_email')  
            
            if email:
                coach = Coach.query.filter_by(CoachEmail=email).first()
                player = Player.query.filter_by(PlayerEmail=email).first()
                
                if coach:
                    hashed_password = generate_password_hash(new_password)
                    coach.CoachPasswordHash = hashed_password
                elif player:
                    hashed_password = generate_password_hash(new_password)
                    player.PlayerPasswordHash = hashed_password

                db.session.commit()
                flash('Password reset successfully. You can now log in with your new password.')
                return redirect('/login')
              
                session.pop('reset_email', None)
            else:
                flash('Email not found in the session.')
        else:
            flash('Passwords do not match.')
    
    return render_template('reset_password.html')


@views.route('/join_coach', methods=['GET', 'POST'])
def join_coach():
    if 'user_id' not in session:
        return redirect('/login')

    player_id = session['user_id']
    player = Player.query.get(player_id)

    if request.method == 'POST':
        coach_code = request.form['coach_code']
        coach = Coach.query.filter_by(CoachCode=coach_code).first()

        if coach:
            player.CoachCode = coach_code
            db.session.commit()
            flash('Joined coach successfully!')
            return redirect('/player_home')
        else:
            flash('Coach not found with the provided code.')

    return render_template('join_coach.html', player=player)
 

@views.route('/player_form', methods=['GET', 'POST'])
def player_form():
    if 'user_id' in session and session.get('user_type') == 'player':
        player_id = session['user_id']
        player = Player.query.get(player_id)

        existing_workouts = PlayerWorkout.query.filter_by(player_id=player.PlayerID).all()
        if existing_workouts:
            # Delete the existing personalized workout
            for existing_workout in existing_workouts:
                db.session.delete(existing_workout)   
                db.session.commit()

        if request.method == 'POST':
            position = request.form['position']
            finishing = int(request.form['finishing'])
            shooting = int(request.form['shooting'])
            rebounding = int(request.form['rebounding'])

           
            player.Position = position
            player.Finishing = finishing
            player.Shooting = shooting
            player.Rebounding = rebounding
            position = player.Position

            skills = {
                'Finishing': player.Finishing,
                'Shooting': player.Shooting,
                'Rebounding': player.Rebounding
            }
            
            def generate_workout(position, lowest_skills, equal_skills, rebounding_tied_with_highest, skills):
                workout_types = {
                    'Point Guard': ['1', '6', '11'],
                    'Shooting Guard': ['2', '7', '12'],
                    'Small Forward': ['3', '8', '13'],
                    'Power Forward': ['4', '9', '14'],
                    'Center': ['5', '10', '15']
                }
                finishing_skill = skills['Finishing']
                shooting_skill = skills['Shooting']
                
                workout_type = None
                if equal_skills or rebounding_tied_with_highest:
                    # Prioritize Finishing or Shooting for equal skills or tied with Rebounding
                    workout_type = workout_types[position][0]
                else:
                    # Determine the lowest-rated skill and select corresponding workout
                    if 'Finishing' in lowest_skills:
                        workout_type = workout_types[position][0]
                    elif 'Shooting' in lowest_skills:
                        workout_type = workout_types[position][0]
                    elif 'Rebounding' in lowest_skills:
                        if finishing_skill > shooting_skill:
                            workout_type = workout_types[position][2]
                        elif finishing_skill < shooting_skill:
                            workout_type = workout_types[position][1]
                        else:
                            workout_type = workout_types[position][1]###### We can change this based on what is more important shooting or finishing 
                return workout_type
                
            # Determine the highest-rated skill(s) and lowest-rated skill
            highest_rated_skills = [skill for skill, rating in skills.items() if rating == max(skills.values())]
            lowest_rated_skill = min(skills, key=skills.get)

            # Check if all skills are rated equally
            equal_skills = len(set(skills.values())) == 1

            # Check if Rebounding is tied with the highest-rated skill
            rebounding_tied_with_highest = 'Rebounding' in highest_rated_skills

            # Generate the workout using the generate_workout function
            workout = generate_workout(position, [lowest_rated_skill], equal_skills, rebounding_tied_with_highest, skills)

            player.Position = position
            player.Finishing = finishing
            player.Shooting = shooting
            player.Rebounding = rebounding
            player.Workout_code = workout

            db.session.commit()
            workout_routines = WorkoutRoutine.query.filter_by(workout_group=workout).all()

            # Create PlayerWorkout entries for each workout routine
            for workout_routine in workout_routines:
                for exercise in workout_routine.exercises:
                    player_workout = PlayerWorkout(
                        player_id=player.PlayerID,
                        workout_routine_id=workout_routine.id,
                        exercise_name=exercise.name,
                        sets=exercise.sets,
                        reps=exercise.reps
                    )
                    db.session.add(player_workout)

            db.session.commit()
            flash('Profile details updated successfully!')

            return redirect('/')

        return render_template('player_form.html', player=player) 
    else:
        flash('Please log in as a player.')
        return redirect('/login')





@views.route('/player_home')
def player_home():
    if 'user_id' in session and session.get('user_type') == 'player':
        player_id = session['user_id']
        player = Player.query.get(player_id)

        coach = None
        if player.CoachCode:
            coach = Coach.query.filter_by(CoachCode=player.CoachCode).first()

        return render_template('player_home.html', player=player, coach=coach,coach_name=coach.CoachName if coach else None,
                               coach_code=coach.CoachCode if coach else None)
    else:
        flash('Please log in as a player.')
        return redirect('/login')


@views.route('/workout/<day>')
def workouts_by_day(day):
    if 'user_id' in session and session.get('user_type') == 'player':
        player_id = session['user_id']
        player = Player.query.get(player_id)
        workouts = player.get_upcoming_workouts(day)
        return render_template('workout.html', workouts=workouts, day=day)
    else:
        return "Unauthorized", 401



@views.route('/coach_dashboard')
def coach_dashboard():
    if 'user_id' in session:
        coach_id = session.get('user_id')
        coach = Coach.query.get(coach_id)

        enrolled_players = Player.query.filter_by(CoachCode=coach.CoachCode).all()
        return render_template('coach_dashboard.html', coach=coach, enrolled_players=enrolled_players)
    else:
        flash('Please log in as a coach.')
        return redirect('/login')
    
@views.route('/edit_player_workouts/<int:player_id>', methods=['GET', 'POST'])
def edit_player_workouts(player_id):
    if 'user_id' in session:
        coach_id = session.get('user_id')
        coach = Coach.query.get(coach_id)
        player = Player.query.get(player_id)

        if request.method == 'POST':
            # Iterate through the form items and update the workouts
            for workout_id, value in request.form.items():
                if "_sets" in workout_id:
                    workout_id = workout_id.replace("_sets", "")  # Remove the "_sets" suffix
                    player_workout = PlayerWorkout.query.get(workout_id)
                    if player_workout:
                        player_workout.exercise_name = request.form.get(workout_id + '_name')  # Update name
                        player_workout.sets = request.form.get(workout_id + '_sets')  # Update sets
                        player_workout.reps = request.form.get(workout_id + '_reps')  # Update reps
                        db.session.commit()


            db.session.commit()
            flash('Player workouts updated successfully.')
            return redirect(url_for('views.coach_dashboard'))

        # Get the player's workouts for display
        days = ['Monday', 'Wednesday', 'Friday']
        player_workouts = {}
        for day in days:
            player_workouts[day] = player.get_upcoming_workouts(day)

        return render_template('edit_player_workouts.html', coach=coach, player=player, player_workouts=player_workouts)
    else:
        flash('Please log in as a coach.')
        return redirect('/login')


""" @views.route('/mark_completed/<int:exercise_id>', methods=['POST'])
@login_required
def mark_completed(exercise_id):
    player_id = session['user_id']
    player = Player.query.get(player_id)
    exercise = Exercise.query.get(exercise_id)

    if player and exercise:
        completion = ExerciseCompletion(player=player, exercise=exercise)
        db.session.add(completion)
        db.session.commit()
        flash('Exercise marked as completed!')
    else:
        flash('Exercise or player not found.')

    return redirect('/workout') """

@views.route('/player_dashboard')
def player_dashboard():
    if 'user_id' in session:
        player_id = session['user_id']
        player = Player.query.get(player_id)
        workout = player.Workout_code
       

        return render_template('player_dashboard.html', player=player, workout=workout)
    else:
        return redirect('/login')

@views.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('user_id', None)
    return redirect('/')