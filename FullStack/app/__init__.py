from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.config import Config


app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# Redirects to login page if user is not logged in
# for all routes that require login with @login_required decorator
# login_manager.login_view = 'login' # Name of the function that handles login
# login_manager.login_message_category = 'info' # Bootstrap class for the message

from app import routes