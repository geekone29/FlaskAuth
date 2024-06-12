from flask import Flask  # Import Flask to create the Flask app
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database interactions
from os import path  # Import path to handle file paths
from flask_login import LoginManager  # Import LoginManager for user session management

# Initialize the SQLAlchemy instance
db = SQLAlchemy()
DB_NAME = "database.db"  # Name of the SQLite database file

def create_app():
    app = Flask(__name__)  # Create a Flask app instance
    app.config['SECRET_KEY'] = 'test'  # Set a secret key for securely signing the session cookie
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Configure the app to use SQLite database
    db.init_app(app)  # Bind SQLAlchemy to this Flask app instance

    # Import Blueprints for views and authentication
    from .views import views
    from .auth import auth

    # Register the blueprints with the Flask app
    app.register_blueprint(views, url_prefix='/')  # Main routes
    app.register_blueprint(auth, url_prefix='/')  # Authentication routes

    # Import the User model to ensure it's available when creating the database
    from .models import User

    # Ensure the database is created within the app context
    with app.app_context():
        db.create_all()  # Create database tables for all models

    # Set up the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Specify the login view to redirect to when login is required
    login_manager.init_app(app)  # Bind the login manager to the app

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Define a user loader function for Flask-Login

    return app  # Return the configured Flask app instance

def create_database(app):
    if not path.exists('website/' + DB_NAME):  # Check if the database file does not exist
        db.create_all(app=app)  # Create the database and all tables
        print('Created Database!')  # Print a message indicating that the database was created
