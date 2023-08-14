from flask import Flask
from app import db
from app.routes import views as views_blueprint  # Import the Blueprint



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'asdasd'

app.register_blueprint(views_blueprint)

if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        
        db.create_all()
        app.run(host='0.0.0.0', port=5000)
        