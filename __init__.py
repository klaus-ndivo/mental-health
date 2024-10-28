from flask import Flask, request, session
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_login import LoginManager
import requests

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
    app.config['SESSION_PERMANENT'] = True 
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    Session(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User, Doctor
        role = session.get('role')
        if role == 'doctor':
            return Doctor.query.get(int(user_id))
        elif role == 'user':
            return User.query.get(int(user_id))
        return None
    
    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    # blueprint for non-auth 
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # blueprint for client routes
    from .client import client as client_blueprint
    app.register_blueprint(client_blueprint)

    # blueprint for doctor routes
    from .doctor import doctor as doctor_blueprint
    app.register_blueprint(doctor_blueprint)
    
    return app
