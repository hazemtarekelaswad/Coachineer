# Configurations and constants for the project

class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///coachineer.db'
    PORT = 5000
    UPLOAD_FOLDER = 'static/videos/original'
    PROCESSED_FOLDER = 'static/videos/processed'
    ANALYSIS_FOLDER = 'static/analysis'
    GRAPHS_FOLDER = 'static/images/graphs'
    MEAL_RECOMMENDER_FOLDER = 'static/meal_recommender'
    DEFAULT_VIDEO_NAME = 'video.mp4'
