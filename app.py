import os
from flask import Flask, render_template, session, redirect, request, url_for
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Exercises.db'
app.config['SQLALCHEMY_BINDS'] = {
	'block':        'sqlite:///Block.db',
	'workout':      'sqlite:///Workout.db'
}

app.config['SECRET_KEY'] = 'secret string'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Exercises.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
# migrate = Migrate(app, db)


class Exercises(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return '<Name %r>' % self.name

class Block(db.Model):
	__bind_key__ = 'block'
	id = db.Column(db.Integer, primary_key=True)
	weight = db.Column(db.Integer)
	reps = db.Column(db.Integer)
	exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id')) # might want to change to name after


class Workout(db.Model): # should add user and date maybe?
	__bind_key__ = 'workout'
	id = db.Column(db.Integer, primary_key=True)
	exercise_block = db.Column(db.Integer, db.ForeignKey('block.id'))
	# exercise_set = db.relationship('Block', backref='workout', lazy='dynamic')


@app.route('/')
def home():
	title = "Home"
	return render_template("home.html")


@app.route('/exercises', methods=['POST', 'GET'])
def exercises():
	title = "Exercises"
	if request.method == "POST": 
		ex_name = request.form['name']
		new_ex = Exercises(name=ex_name)
		try:
			db.session.add(new_ex)
			db.session.commit()
			return redirect(url_for('exercises'))
		except:
			return "there was an error"
	else:
		exercises = Exercises.query.all()
		return render_template("exercises.html", title=title, exercises=exercises)



<<<<<<< Updated upstream
    else:
        exercises = Exercises.query.all()
        return render_template("exercises.html", title=title, exercises=exercises)
=======
@app.route('/addworkout', methods=['POST', 'GET'])
def addworkout(): # trying to shuffle info into Block database 
	title = "Add Workout"
	if request.method == "POST":

		get_weight = request.form['weight1']
		get_reps = request.form['reps1']
		get_exercise = request.form['exercise1']

		block_unit = Block(weight=get_weight, reps=get_reps, exercise_id=get_exercise)

		try:
			db.session.add(block_unit)
			db.session.commit() # not working !
			return "success"
		except:
			return "there was an error"


	else:
		exercises = Exercises.query.all()
		return render_template("addworkout.html", exercises=exercises)



>>>>>>> Stashed changes
