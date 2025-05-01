from flask import Blueprint, url_for, render_template, request, redirect, flash
from . import db
from .models import User, Workout
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    print(f'name: {name}, email: {email}, password: {password}')
    user = User.query.filter_by(email = email).first()
    if user and check_password_hash(user.password, password):
        print(f"User already exists.")
        return redirect(url_for('auth.signup'))  # Send them back to try again or sign in

    else:
        print(f"User does not exists.")
        new_user = User(email=email, password = generate_password_hash(password, method='pbkdf2:sha256'), name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.signin'))

@auth.route('/signin')
def signin():
    return  render_template('signin.html')

@auth.route('/signin', methods=['POST'])
def signin_post():
    password = request.form.get('password')
    email = request.form.get('email')
    remember = True if request.form.get('remember') else False
    print(f'name: {password}, email: {email}, remember: {remember}')
    user = User.query.filter_by(email = email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('auth.signin'))
    else:
        login_user(user, remember = remember)
        flash("You are successfully logged in!!")
        return redirect(url_for('main.profile'))

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    return render_template('signout.html')