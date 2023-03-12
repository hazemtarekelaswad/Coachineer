# Routes for the app

from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt, utils
# from app.forms import 
# from app.models import 


## Home Route
@app.route('/')
def home():
    return render_template('index.html')

## User Routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    pass

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    pass

@app.route('/signout')
def signout():
    pass

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    pass

## Meal Routes
@app.route('/meals')
def meals():
    pass

@app.route('/meals/<int:meal_id>', methods=['GET', 'POST'])
def meal(meal_id):
    pass

@app.route('/recommended-meals')
@login_required
def recommended_meals():
    pass

@app.route('/recommended-meals/<int:meal_id>', methods=['GET', 'POST'])
@login_required
def recommended_meal(meal_id):
    pass

## Exercise Routes
@app.route('/exercises')
def exercises():
    return render_template('exercise_selection.html', exercises=utils.exercises)

@app.route('/exercises/<int:exercise_id>', methods=['GET', 'POST'])
def exercise(exercise_id):
    return render_template('exercise.html', exercise=utils.exercises[exercise_id])


