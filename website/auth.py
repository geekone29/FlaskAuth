from flask import Blueprint, flash, render_template, request, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint for authentication routes
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # Get the email from the form
        password = request.form.get('password')  # Get the password from the form

        # Look for the user in the database by email
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):  # Check if the provided password matches the stored hash
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))  # Redirect to the home page
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')  # Show an error message for non-existent email

    return render_template("login.html", user=current_user)  # Render the login template

@auth.route('/logout')
@login_required  # Ensure that the user is logged in to access this route
def logout():
    logout_user()  # Log out the current user
    return redirect(url_for('auth.login'))  # Redirect to the login page

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()  # Check if the user already exists in the database
         
        if user:
            flash('Email already used.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create a new user with the provided information and hashed password
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)  # Add the new user to the database session
            db.session.commit()  # Commit the session to save the new user
            login_user(new_user, remember=True)  # Log in the new user
            flash('Account created!', category='success')  # Show a success message
            return redirect(url_for('views.home'))  # Redirect to the home page

    return render_template("sign_up.html", user=current_user)  # Render the sign-up template
