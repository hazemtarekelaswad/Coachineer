# Database models for the application

from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Add Entities as classes here

class User(db.Model, UserMixin):
    pass

    def __repr__(self):
        pass
