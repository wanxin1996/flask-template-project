from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
from .models import User    # import the User class from models.py to create new_user
from werkzeug.security import generate_password_hash, check_password_hash # lib to hash password
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # check if the user exists
        user = User.query.filter_by(email=email).first()
        if user:
            # check if the password is correct
            if check_password_hash(user.password, password):
                flash('You are now logged in', category='success')
                login_user(user, remember=True)
                #session['user_id'] = user.id
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('No account found for that email.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required # only logged in users can access this page
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
            return redirect(url_for('views.home'))
        elif len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters long.', category='error')
        elif password != password_confirm:
            flash('Passwords do not match.', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', category='error')
        else:
            # add user to database
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully signed up!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
