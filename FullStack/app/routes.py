# Routes for the app
import os
import sys
import cv2
from flask import render_template, url_for, flash, redirect, request, jsonify, Response
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt, utils
from app.forms import UploadVideoForm
from app.config import Config
from werkzeug.utils import secure_filename
from app.camera import VideoCamera
# from app.models import

import ExerciseEvaluator

# Home Route


@app.route('/')
def home():
    return render_template('index.html')

# User Routes


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

# Meal Routes


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

# Exercise Routes


@app.route('/exercises')
def exercises():
    return render_template('exercise_selection.html', exercises=utils.exercises)


@app.route('/exercises/<int:exercise_id>', methods=['GET', 'POST'])
def exercise(exercise_id):
    form = UploadVideoForm()

    if form.validate_on_submit():
        video = form.video.data
        path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            Config.UPLOAD_FOLDER,
            secure_filename(video.filename)
        )
        video.save(path)
        print('Uploaded successfully')

        # TODO: Display success message

        # process the video
        processed_video_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            Config.PROCESSED_FOLDER,
            secure_filename(video.filename)
        )

        evaluator = ExerciseEvaluator.Evaluator(path, processed_video_path)
        evaluator.evaluate()

        return render_template(
            'feedback.html',
            exercise=utils.exercises[exercise_id],
            video_path=f'{Config.PROCESSED_FOLDER}/{secure_filename(video.filename)}'.removeprefix(
                "static/")
        )

    return render_template('exercise_options.html', exercise=utils.exercises[exercise_id], form=form)


@app.route('/exercises/<int:exercise_id>/evaluate')
def evaluate(exercise_id):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.UPLOAD_FOLDER,
        secure_filename(Config.DEFAULT_VIDEO_NAME)
    )

    processed_video_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.PROCESSED_FOLDER,
        secure_filename(Config.DEFAULT_VIDEO_NAME)
    )

    evaluator = ExerciseEvaluator.Evaluator(path, processed_video_path)
    evaluator.evaluate()

    return render_template(
        'feedback.html',
        exercise=utils.exercises[exercise_id],
        video_path=f'{Config.PROCESSED_FOLDER}/{secure_filename(Config.DEFAULT_VIDEO_NAME)}'.removeprefix("static/")
    )


video_camera = None
global_frame = None


@app.route('/exercises/<int:exercise_id>/record')
def record_video(exercise_id):
    return render_template('record.html', exercise=utils.exercises[exercise_id])


@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera
    if video_camera == None:
        video_camera = VideoCamera()

    status = request.get_json()['status']

    if status == 'true':
        video_camera.start_record()
        return jsonify(result="started")
    video_camera.stop_record()
    return jsonify(result="stopped")


def video_stream():
    global video_camera
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()
        if frame:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


@app.route('/video')
def video():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/exercises/<int:exercise_id>/realtime', methods=['GET', 'POST'])
def realtime_video(exercise_id):
    pass

# camera = cv2.VideoCapture(0)
# def generate_frames(path):
#     writer = cv2.VideoWriter(path, -1, 20.0, (camera.get(3), camera.get(4)))

#     while True:
#         success, frame = camera.read()
#         frame = cv2.flip(frame, 1)
#         if not success or stop:
#             break

#         if start:
#             writer.write(frame)
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         yield(b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')
#     writer.release()

# @app.route('/video')
# def video():
#     path = os.path.join(
#             os.path.abspath(os.path.dirname(__file__)),
#             Config.UPLOAD_FOLDER,
#             secure_filename(video.filename)
#         )
#     return Response(generate_frames(path), mimetype='multipart/x-mixed-replace; boundary=frame')
