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
    pass

# User Routes


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    pass


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template('./auth/login.html')


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

######################### Exercise Routes #########################

# Global variables for video recording
video_camera = None
global_frame = None

# Prevent caching for every request.
# used to avoid issues related to releasing video camera
@app.after_request
def prevent_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Defined decorator to exclude a function from the before_request hook
def exclude(func):
    func._exclude = True
    return func

# Utility function to release the camera resources before each request
@app.before_request
def release_camera(*args, **kwargs):
    is_excluded = False

    if request.endpoint in app.view_functions:
        view_func = app.view_functions[request.endpoint]
        is_excluded = hasattr(view_func, '_exclude')
    
    if is_excluded: return

    global video_camera
    if video_camera:
        video_camera.release()
        video_camera = None

# GET: Display the exercise selection page
@app.route('/exercises')
def exercises():
    return render_template('exercise_selection.html', exercises=utils.exercises)


# Utility function to evaluate the video
def evaluate_video(video_name: str, exercise_id: int):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.UPLOAD_FOLDER,
        secure_filename(video_name)
    )

    processed_video_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.PROCESSED_FOLDER,
        secure_filename(video_name)
    )

    evaluator = ExerciseEvaluator.Evaluator(path, processed_video_path, ExerciseEvaluator.ExerciseType(exercise_id))
    evaluator.evaluate()


# GET: Display the exercise options page based on the exercise id
# POST: Upload the video, process it and redirect to the feedback page
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

        evaluate_video(video.filename, exercise_id)

        return render_template(
            'feedback.html',
            exercise=utils.exercises[exercise_id],
            video_path=f'{Config.PROCESSED_FOLDER}/{secure_filename(video.filename)}'.removeprefix("static/")
        )

    return render_template('exercise_options.html', exercise=utils.exercises[exercise_id], form=form)


# GET: Evaluate the exercise and display the feedback page based on the exercise id
## NOTE: This route is accessed directly from the record page
@app.route('/exercises/<int:exercise_id>/evaluate')
def evaluate(exercise_id):
    evaluate_video(Config.DEFAULT_VIDEO_NAME, exercise_id)
    return render_template(
        'feedback.html',
        exercise=utils.exercises[exercise_id],
        video_path=f'{Config.PROCESSED_FOLDER}/{secure_filename(Config.DEFAULT_VIDEO_NAME)}'.removeprefix("static/")
    )


# GET: Display the record page to record the video and evaluate it

@app.route('/exercises/<int:exercise_id>/record')
@exclude
def record_video(exercise_id):
    return render_template('record.html', exercise=utils.exercises[exercise_id])

# Utility routes for recording video (start, stop)
@app.route('/record_status', methods=['POST'])
@exclude
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

# Utility route for streaming video
@app.route('/video')
@exclude
def video():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

# GET: Display the streaming page and evaluate the stream in real time while recording
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
