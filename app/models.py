from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

import os, datetime 
from datetime import datetime
datetime.utcnow()
from flask import Flask, render_template, session, redirect, request, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from sqlalchemy.sql.expression import func
#from app.auth.forms import User, AddExerciseUnit, AddExercise


# class Role(db.Model):
# 	__tablename__ = 'roles'
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(64), unique=True)
# 	users = db.relationship('User', backref='role', lazy='dynamic')

# 	def __repr__(self):
# 		return '<Role %r>' % self.name

class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	# role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class Type(db.Model):
	__tablename__ ='type'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return '<Name %r>' % self.name


class Unit(db.Model):
	__tablename__='unit'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
	type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	weight = db.Column(db.Integer)
	reps = db.Column(db.Integer)


class Workout(db.Model):
	__tablename__ = 'workout'
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	

	

