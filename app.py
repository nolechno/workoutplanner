from flask import Flask, render_template, session, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Exercises.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class Exercises(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return '<Name %r>' % self.name

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
