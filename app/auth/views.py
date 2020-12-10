from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, \
    current_user
from sqlalchemy.sql import func
from . import auth
from .. import db
from ..models import User, Type, Unit, Workout
from .forms import LoginForm, RegistrationForm, AddExerciseUnit, AddExercise
from datetime import datetime
datetime.utcnow()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/exercises', methods=['POST', 'GET'])
def exercises():
	title = "Exercises"
	form = AddExercise()

	if form.validate_on_submit():
		ex_name = form.exercise_name.data
		new_ex = Type(name=ex_name)
		db.session.add(new_ex)
		db.session.commit()
		return redirect(url_for('auth.exercises'))

	else:
		exercises = Type.query.all()
		return render_template("auth/exercises.html", title=title, exercises=exercises, form=form)
@auth.route('/delete_ex/<int:id>')
def delete_ex(id):
    exercise_delete = Type.query.get_or_404(id)
    try:
        db.session.delete(exercise_delete)
        db.session.commit()
        return redirect(url_for('auth.exercises'))
    except:
        return "there was a problem deleting"



@auth.route('/createworkout', methods=['POST', 'GET'])
def createworkout():
	if request.method == "POST":
		user_id=current_user.id
		current_workout = Workout(date=datetime.utcnow(), user_id=user_id)

		try: 
			db.session.add(current_workout)
			db.session.commit()
			return redirect(url_for("auth.addworkout"))
		except: 
			return "there was an error"
	else:
		return render_template("main/index.html")


@auth.route('/addworkout', methods=['POST', 'GET'])
def addworkout():
	title = "Add Workout"
	form = AddExerciseUnit()

	workout_id = Workout.query.order_by(Workout.id.desc()).first()
	get_workout_id = str(workout_id)

	exercise_options = db.session.query(Type).all()
	exercise_name = [(i.name) for i in exercise_options]
	form.exercise_type.choices = exercise_name
	user_id = current_user.id


	if form.validate_on_submit():
		exercise_unit = Unit(weight=form.weight.data, reps=form.reps.data, type_id=form.exercise_type.data, workout_id=get_workout_id, user_id=user_id)
		db.session.add(exercise_unit)
		db.session.commit()
		return redirect(url_for('auth.addworkout'))

	else:
		exercises = Type.query.all()
		units = Unit.query.all()
		workouts = Workout.query.all()
		return render_template("auth/addworkout.html", exercises=exercises, units=units, workouts=workouts, form=form)

@auth.route('/delete_unit/<int:id>')
def delete_unit(id):
    unit_delete = Unit.query.get_or_404(id)
    try:
        db.session.delete(unit_delete)
        db.session.commit()
        return redirect(url_for('auth.addworkout'))
    except:
        return "there was a problem deleting"

@auth.route('/history')
def history():
	title = "History"
	units = Unit.query.all()
	workouts = Workout.query.all()
	user_id = User.query.all()
	users = User.query.all()
	return render_template("auth/history.html", units=units, workouts=workouts, user_id=user_id, users=users)

