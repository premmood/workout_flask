from flask import Blueprint, render_template, url_for,request,redirect
from flask_login import login_required, current_user
from datetime import datetime
from src.workout_app.auth import signup
from .models import Workout, User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name= current_user.name)

@main.route('/all')
@login_required
def all_workout():
    page = request.args.get('page', 1, type=int)
    #workoutlist = current_user.workout
    workoutlist = Workout.query.filter_by(author=current_user).paginate(page=page, per_page=3)
    print(workoutlist.items)
    print(dir(workoutlist))
    return render_template('all_workouts.html', workouts = workoutlist)

@main.route('/new')
@login_required
def create_workout():
    return render_template('create_workout.html')

@main.route('/delete/<int:workoutid>')
@login_required
def delete(workoutid):
    workout = Workout.query.get_or_404(workoutid)
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('main.all_workout'))

@main.route('/workout/<int:workout_id>/update', methods=['GET','POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method == 'POST':
        pushups = request.form.get('pushups')
        comment = request.form.get('comment')
        workout.pushup=pushups
        workout.comment=comment
        db.session.commit()
        return redirect(url_for('main.all_workout'))
    return render_template('update_workout.html', workout= workout)

@main.route('/new', methods = ['POST'])
@login_required
def create_workout_post():
    pushups= request.form.get('pushups')
    comments= request.form.get('comment')
    new_workout = Workout(pushup= pushups, comment = comments, author = current_user)
    db.session.add(new_workout)
    db.session.commit()
    # flash('Your workout has been added!!')
    return redirect(url_for('main.all_workout'))