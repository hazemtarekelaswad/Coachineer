# Routes for the app

from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt
# from app.forms import 
# from app.models import 

# Add any needed routes here

@app.route('/')
def home():
    pass