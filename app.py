import os, datetime 
from datetime import datetime
datetime.utcnow()
from flask import Flask, render_template, session, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from sqlalchemy.sql.expression import func
from forms import LoginForm, RegistrationForm, AddExerciseUnit


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Unit.db'
app.config['SQLALCHEMY_BINDS'] = {
	'type':        'sqlite:///Type.db',
	'workout':      'sqlite:///Workout.db',
}

app.config['SECRET_KEY'] = 'secret string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


# class Users(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(50), nullable=False)


class Type(db.Model):
	__bind_key__='type'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return '<Name %r>' % self.name


class Unit(db.Model):
	# __bind_key__='unit'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
	type_id = db.Column(db.Integer, db.ForeignKey('type.id')) 
	weight = db.Column(db.Integer)
	reps = db.Column(db.Integer) 


class Workout(db.Model):
	__bind_key__ = 'workout'
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=True)
	# user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #natalie's User table 
	# exerciseunit_relationship = db.relationship('Unit', backref='workout', lazy='dynamic')





@app.route('/')
def home():
	title = "Home"
	return render_template("home.html")

@app.route('/history')
def history():
	title = "History"
	units = Unit.query.all()
	return render_template("history.html", units=units)


@app.route('/exercises', methods=['POST', 'GET'])
def exercises():
	title = "Exercises"
	if request.method == "POST": 
		ex_name = request.form['name']
		new_ex = Type(name=ex_name)
		try:
			db.session.add(new_ex)
			db.session.commit()
			return redirect(url_for('exercises'))
		except:
			return "there was an error"
	else:
		exercises = Type.query.all()
		return render_template("exercises.html", title=title, exercises=exercises)



@app.route('/createworkout', methods=['POST', 'GET'])
def createworkout():
	if request.method == "POST":
		current_workout = Workout(date=datetime.utcnow())

		try: 
			db.session.add(current_workout)
			db.session.commit()
			return redirect(url_for("addworkout"))
		except: 
			return "didnt work"
	else:
		# workouts.Workout.query.all()
		return render_template("home.html")



# @app.route('/addworkout', methods=['POST', 'GET'])
# def addworkout():  
# 	title = "Add Workout"

# 	workout_id = Workout.query.order_by(Workout.id.desc()).first() 
# 	get_workout_id = str(workout_id.id)

# 	if request.method == "POST":

# 		get_weight = request.form['weight1']
# 		get_reps = request.form['reps1']
# 		get_type = request.form['exercise1']

# 		exercise_unit = Unit(weight=get_weight, reps=get_reps, type_id=get_type, workout_id=get_workout_id)

# 		try:
# 			db.session.add(exercise_unit)
# 			db.session.commit()
# 			return redirect(url_for('addworkout'))
# 		except:
# 			return "fail"

# 	else:
# 		exercises = Type.query.all()
# 		units = Unit.query.all()
# 		workouts = Workout.query.all()
# 		return render_template("addworkout.html", exercises=exercises, units=units, workouts=workouts)
@app.route('/addworkout', methods=['POST', 'GET'])
def addworkout():
	title = "Add Workout"
	form = AddExerciseUnit()

	workout_id = Workout.query.order_by(Workout.id.desc()).first() 
	get_workout_id = str(workout_id.id)

	exercise_options = db.session.query(Type).all()
	exercise_name = [(i.name) for i in exercise_options]
	form.exercise_type.choices = exercise_name

	if form.validate_on_submit():
		exercise_unit = Unit(weight=form.weight.data, reps=form.reps.data, type_id=form.exercise_type.data, workout_id='1')
		db.session.add(exercise_unit)
		db.session.commit()
		return redirect(url_for('addworkout'))

	else:
		exercises = Type.query.all()
		units = Unit.query.all()
		workouts = Workout.query.all()
		return render_template("addworkout.html", exercises=exercises, units=units, workouts=workouts, form=form)





@app.route('/delete_ex/<int:id>')
def delete_ex(id):
    exercise_delete = Type.query.get_or_404(id)
    try:
        db.session.delete(exercise_delete)
        db.session.commit()
        return redirect(url_for('exercises'))
    except:
        return "there was a problem deleting"




