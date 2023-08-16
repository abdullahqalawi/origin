from flask import Blueprint,render_template, request, redirect, flash, session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  
from .models import User, CoachPlayerConnection  

print("getting her222e")
print("getting here22")
views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
def home():
    
    if 'user_id' in session:
        return render_template('hello_boss.html')
    return render_template('login.html')

@views.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect('/')
        else:
            flash('Wrong username or password!')
            return redirect('/')

    return render_template('login.html')

@views.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        new_email = request.form['new_email']

        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            flash('Username already exists. Please choose another.')
        elif new_password != confirm_password:
            flash('Passwords do not match. Please re-enter.')
        else:
            hashed_password = generate_password_hash(new_password)
            new_user = User(username=new_username, password_hash=hashed_password, email=new_email)
            db.session.add(new_user)
            db.session.commit()

            flash('Signup successful! You can now log i.')
            return redirect('/')

    return render_template('signup.html')


@views.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']

        if check_password_hash(user.password_hash, current_password):
            if new_password == confirm_new_password:
                hashed_password = generate_password_hash(new_password)
                user.password_hash = hashed_password
                db.session.commit()
                flash('Password changed successfully!')
                return redirect('/')
            else:
                flash('New passwords do not match.')
        else:
            flash('Incorrect current password.')

    return render_template('change_password.html', user=user)


@views.route('/delete_account/', methods=['GET', 'POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id', None)
        flash('Account deleted successfully!')
        return redirect('/')
    return render_template('delete_account.html', user=user)


@views.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['email']
        
        user = User.query.filter_by(email=email).first()
        
        if user:
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
                user = User.query.filter_by(email=email).first()
                if user:
                    hashed_password = generate_password_hash(new_password)
                    user.password_hash = hashed_password
                    db.session.commit()
                    flash('Password reset successfully. You can now log in with your new password.')
                    return redirect('/login')
                else:
                    flash('User not found with the provided email.')
            else:
                flash('Email not found in the session.')
        else:
            flash('Passwords do not match.')
    
    return render_template('reset_password.html')


@views.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect('/')
