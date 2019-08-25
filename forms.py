from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField
from wtforms.validators import *


class ErrorSearchForm(FlaskForm):
	filename = StringField('Error Type', validators=[DataRequired()],render_kw={"placeholder": "Enter the error type you want to search"})
	date = StringField('Date', validators=[DataRequired()],render_kw={"placeholder": "Enter the date you want to search"})
	submit = SubmitField('Search this error')