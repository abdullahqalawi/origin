from flask import Flask
from app import db
from app.routes import views as views_blueprint
from flask_login import LoginManager
from app.models import Coach, Player 

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
