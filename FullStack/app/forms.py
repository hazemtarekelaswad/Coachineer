# Forms used in the application

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired


class UploadVideoForm(FlaskForm):
    video = FileField("video", validators=[InputRequired()])
    
    
class loginForm(FlaskForm):
    
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
