# Routes for the app
import os
import sys
import cv2
from flask import render_template, url_for, flash, redirect, request, jsonify, Response
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
from app import app, db, bcrypt, utils
from app.forms import UploadVideoForm, loginForm
from app.models import User
from app.config import Config
from werkzeug.utils import secure_filename
from app.camera import VideoCamera
import time
# from app.models import

import ExerciseEvaluator
import MealRecommendation as mr

# Home Route


@app.route('/')
def home():
    pass

# User Routes


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('./auth/signup.html')




@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            print('User logged in!')
            flash('You have been logged in!', 'success')
            return redirect(url_for('exercises'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('./auth/login.html', form=form)

def init_meal_service():
    
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.MEAL_RECOMMENDER_FOLDER
    )

    
    recommender_service = mr.MealRecommenderService()

    ##################### SHOULD BE IN SIGNUP (FROM DB) #####################
    
    dummy_user = mr.User(
        uid = 94,
        first_name='John',
        last_name='Doe',
        email='john@gmai.com',
        password='password',
        gender=mr.Gender.MALE,
        age=20,
        weight=170,
        height=70,
        goal=mr.Goal.BUILD_MUSCLE,
        activity_level=mr.ActivityLevel.SEDENTARY,
        diet_type=mr.DietType.KETO,
        allergies=[mr.Allergy.GLUTEN],
    )
    recommender_service.init_user(dummy_user)
    recommender_service.preprocess(path)
    recommender_service.fill_user_interactions(recommender_service.pp_interactions)

    app.meal_recommender = recommender_service

    ######################################################

@app.route('/signout')
def signout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('exercises'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
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

#! should be called after the video evaluation is done
@app.route('/postprocessing')
def postprocess():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.ANALYSIS_FOLDER
    )
    graphs_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.GRAPHS_FOLDER
    )
    ExerciseEvaluator.PostProcessor.run_with_merge(path, graphs_path)
    return redirect(url_for('analyze_evaluated_exercise'))


@app.route('/analysis')
def analyze_evaluated_exercise():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.ANALYSIS_FOLDER
    )
    graphs_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.GRAPHS_FOLDER
    )
    feedback = ExerciseEvaluator.PostProcessor.run_without_merge(path, graphs_path)
    if feedback is None: return render_template('empty_analysis.html')
    return render_template('analysis.html', graphs=utils.joints, feedback=feedback)

######################### Meal Routes #########################

# TODO: should be in user's login
@app.route('/meals/init')
def init_meals():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.MEAL_RECOMMENDER_FOLDER
    )
    app.recommender_service = mr.MealRecommenderService()

    dummy_user = mr.User(
        uid = 94,
        first_name='John',
        last_name='Doe',
        email='john@gmai.com',
        password='password',
        gender=mr.Gender.MALE,
        age=20,
        weight=170,
        height=70,
        goal=mr.Goal.BUILD_MUSCLE,
        activity_level=mr.ActivityLevel.SEDENTARY,
        diet_type=mr.DietType.KETO,
        allergies=[mr.Allergy.GLUTEN],
    )
    app.recommender_service.init_user(dummy_user)
    app.recommender_service.preprocess(path)
    return redirect(url_for('meals'))


@app.route('/meals')
def meals():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.MEAL_RECOMMENDER_FOLDER
    )

    #! will be removed 
    dummy_user = mr.User(
        uid = 94,
        first_name='John',
        last_name='Doe',
        email='john@gmai.com',
        password='password',
        gender=mr.Gender.MALE,
        age=20,
        weight=170,
        height=70,
        goal=mr.Goal.BUILD_MUSCLE,
        activity_level=mr.ActivityLevel.SEDENTARY,
        diet_type=mr.DietType.KETO,
        allergies=[mr.Allergy.GLUTEN],
    )
    
    #TODO: pp_interactions should be retrieved from db and passed to this function in the same format
    app.recommender_service.fill_user_interactions(app.recommender_service.pp_interactions)

    if not hasattr(app, 'recommended_meals'):
        app.recommended_meals = app.recommender_service.recommend_meals(path, 100)
        app.meal_pointer = 2
        app.recommended_meals_indexes = app.recommended_meals.index[0:3].tolist()
        # app.recommended_meals = pd.DataFrame(
        #     index=[5, 898, 2132],
        #     columns=['id', 'calorie_level', 'replaced_ingredients', 'name', 'minutes', 'nutrition', 'steps', 'ingredients'],
        #     data={
        #         'id': [72621, 4325, 52300],
        #         'calorie_level': [25498, 472459, 203360],
        #         'replaced_ingredients': [1, 2, 1],
        #         'name': ['raspberry coconut and blueberry sundae', 'creamy cajun chicken pasta with bacon', 'barefoot contessa s rosemary polenta'],
        #         'minutes': [40, 40, 40],
        #         'nutrition': [[326.6, 13.0, 222.0, 3.0, 7.0, 26.0, 20.0], [1123.2, 89.0, 30.0, 23.0, 92.0, 157.0, 34.0], [300.8, 32.0, 4.0, 11.0, 14.0, 51.0, 7.0]],
        #         'steps': [['vanilla ice cream', 'fresh blueberries', 'fresh raspberries', 'coconut sauce', 'toasted coconut', 'toasted almonds'], ['cajun seasoning', 'extra virgin olive oil', 'chicken breasts', 'bacon', 'penne pasta', 'heavy cream', 'parmesan cheese'], ['unsalted butter', 'olive oil', 'garlic', 'crushed red pepper flakes', 'chicken stock', 'cornmeal', 'kosher salt', 'fresh ground black pepper', 'fresh rosemary', 'parmesan cheese']],
        #         'ingredients': [['vanilla ice cream', 'fresh blueberries', 'fresh raspberries', 'coconut sauce', 'toasted coconut', 'toasted almonds'], ['cajun seasoning', 'extra virgin olive oil', 'chicken breasts', 'bacon', 'penne pasta', 'heavy cream', 'parmesan cheese'], ['unsalted butter', 'olive oil', 'garlic', 'crushed red pepper flakes', 'chicken stock', 'cornmeal', 'kosher salt', 'fresh ground black pepper', 'fresh rosemary', 'parmesan cheese']]
        #     }
        # )
   
    return render_template('meals.html', meals=app.recommended_meals.loc[app.recommended_meals_indexes], user=dummy_user)

@app.route('/cached-meals')
def cached_meals():

    dummy_user = mr.User(
        uid = 94,
        first_name='John',
        last_name='Doe',
        email='john@gmai.com',
        password='password',
        gender=mr.Gender.MALE,
        age=20,
        weight=170,
        height=70,
        goal=mr.Goal.BUILD_MUSCLE,
        activity_level=mr.ActivityLevel.SEDENTARY,
        diet_type=mr.DietType.KETO,
        allergies=[mr.Allergy.GLUTEN],
    )
   
    return render_template('meals.html', meals=app.recommended_meals.loc[app.recommended_meals_indexes], user=dummy_user)


# Now you have the meal index, and the rating value
@app.route('/meals/submit-rating', methods=['POST'])
def submit_rating():
    meal_index = request.form.get(f'meal-index')
    rating = request.form.get(f'rating-value-{meal_index}')
    if rating is None or rating == '':
        return redirect(url_for('cached_meals'))
    
    print(f'rating: {rating}')
    print(f'meal index: {meal_index}')
    
    # TODO: save rating and meal_index to db for the current user

    # Partial fit the model with the new rating
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        Config.MEAL_RECOMMENDER_FOLDER
    )
    app.recommender_service.partial_fit(int(meal_index), int(rating), path)
    

    return redirect(url_for('cached_meals'))

@app.route('/meals/regenerate', methods=['POST'])
def regenerate_meal():
    meal_index = request.form.get('meal_index')
    index = request.form.get('index')
    print(f'meal index: {meal_index}')
    print(f'counter: {index}')

    app.meal_pointer += 1
    # replace the meal index with the new one
    for i, meal in enumerate(app.recommended_meals_indexes):
        if meal == int(meal_index):
            app.recommended_meals_indexes[i] = app.recommended_meals.index[app.meal_pointer]
            break

    print(f'INDEXES: {app.recommended_meals_indexes}')
    
    return redirect(url_for('meals'))