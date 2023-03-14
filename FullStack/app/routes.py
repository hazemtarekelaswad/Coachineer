# Routes for the app
import os
import cv2
from flask import render_template, url_for, flash, redirect, request, jsonify, Response
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt, utils
from app.forms import UploadVideoForm
from app.config import Config
from werkzeug.utils import secure_filename
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
    form = UploadVideoForm()

    if form.validate_on_submit():
        video = form.video.data
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(video.filename))
        video.save(path)
        print("Uploaded successfully")
        return "Uploaded successfully"
    
    return render_template('exercise_options.html', exercise=utils.exercises[exercise_id], form=form)


@app.route('/exercises/<int:exercise_id>/upload', methods=['GET', 'POST'])
def upload_video(exercise_id):
    pass

@app.route('/exercises/<int:exercise_id>/record', methods=['GET', 'POST'])
def record_video(exercise_id):
    pass

@app.route('/exercises/<int:exercise_id>/realtime', methods=['GET', 'POST'])
def realtime_video(exercise_id):
    pass


camera = cv2.VideoCapture(0)
def generate_frames():
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame, 1)
        if not success: break

        _, buffer = cv2.imencode('.jpg',frame)
        frame = buffer.tobytes()

        yield(b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype = 'multipart/x-mixed-replace; boundary=frame')

