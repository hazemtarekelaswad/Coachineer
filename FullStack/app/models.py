# Database models for the application

from app import db
# from app import login_manager
from flask_login import UserMixin


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# Add Entities as classes here


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(20), nullable=False)
    lName = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    activityLevel = db.Column(db.String(20), nullable=False)
    goal = db.Column(db.String(20), nullable=False)
    dietType = db.Column(db.String(20), nullable=False)
    #allergies = db.Column(db.String(20), nullable=False)
    

    def __repr__(self):
        pass
