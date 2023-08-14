from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Change to your preferred database URI
app.secret_key = 'asdasd'  # Change this to a secure secret key
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('hello_boss.html')
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/signup', methods=['GET', 'POST'])
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

            flash('Signup successful! You can now log in.')
            return redirect('/')

    return render_template('signup.html')


@app.route('/change_password', methods=['GET', 'POST'])
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


@app.route('/delete_account', methods=['GET', 'POST'])
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







@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
 