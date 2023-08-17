from flask import Blueprint,render_template, request, redirect, flash, session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from .models import Coach, Player
import random
import string

# Define a function to generate a random coach code
def generate_coach_code():
    characters = string.ascii_uppercase + string.digits
    code_length = 6
    return ''.join(random.choice(characters) for _ in range(code_length))

# Define a function to generate a random player code
def generate_player_code():
    characters = string.ascii_letters + string.digits
    code_length = 8
    return ''.join(random.choice(characters) for _ in range(code_length))

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' in session:
        user_type = session.get('user_type')  # Add this line to get user type
        if user_type == 'coach':
            return render_template('coach_home.html')
        elif user_type == 'player':
            return render_template('player_home.html')
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
            session['user_type'] = 'coach'  # Add this line
            return redirect('/')
        elif player and player.check_password(password):
            session['user_id'] = player.PlayerID
            session['user_type'] = 'player'  # Add this line
            return redirect('/')
        else:
            flash('Wrong username or password!')
            return redirect('/login')

    return render_template('login.html')

# ... (other route imports and code)
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
                new_player = Player(PlayerName=new_username, PlayerEmail=new_email, CoachCode="Null", PlayerPasswordHash=hashed_password)
                new_player.set_password(new_password)
                db.session.add(new_player)
                
            else:
                flash('Invalid role.')
                return redirect('/signup')

            
            db.session.commit()

            flash('Signup successful! You can now log in.')
            return redirect('/login')

    return render_template('signup.html')


# ... (other routes and code)

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
            email = session.get('reset_email')  # Retrieve the email from the session
            
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
                # Clear the reset_email from the session
                session.pop('reset_email', None)
            else:
                flash('Email not found in the session.')
        else:
            flash('Passwords do not match.')
    
    return render_template('reset_password.html')


""" @views.route('/join_coach', methods=['GET', 'POST'])
def join_coach():
    if 'user_id' not in session:
        return redirect('/login')

    player = User.query.get(session['user_id'])

    if request.method == 'POST':
        coach_code = request.form['coach_code']
        coach = Coach.query.filter_by(coach_code=coach_code).first()

        if coach:
            connection = CoachPlayerConnection(coach_id=coach.id, player_id=player.id)
            db.session.add(connection)
            db.session.commit()
            flash('Joined coach successfully!')
            return redirect('/')

        flash('Coach not found with the provided code.')

    return render_template('join_coach.html', player=player)

 """


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

    
@views.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect('/')
