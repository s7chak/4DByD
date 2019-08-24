from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField
from wtforms.validators import *

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()],render_kw={"placeholder": "Enter your username"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Enter your password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class SignUpForm(FlaskForm):
	firstname = StringField('First Name',render_kw={"placeholder": "Enter first name"})
	lastname = StringField('Last Name',render_kw={"placeholder": "Enter last name"})
	zipcode = IntegerField('Zip Code',render_kw={"placeholder": "Enter zip code"})
	gender = StringField('Gender',render_kw={"placeholder": "Enter gender"})
	username = StringField('UserName', validators=[DataRequired(), Length(min=2, max=20)],render_kw={"placeholder": "Select a username"})
	email = StringField('Email', validators=[DataRequired()],render_kw={"placeholder": "Enter email ID"})
	password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Select a strong password"})
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired()],render_kw={"placeholder": "Re-enter the password"})
	submit = SubmitField('Sign Up')

class ZipSearchForm(FlaskForm):
	zipcode = IntegerField('Zip Code', validators=[DataRequired()],render_kw={"placeholder": "Enter the zip code to search"})
	submit = SubmitField('Search this area')

class DateSearchForm(FlaskForm):
	starttime = IntegerField('Start Time(24-hr clock)', validators=[DataRequired()],render_kw={"placeholder": "Enter start time hour"})
	endtime = IntegerField('End Time(24-hr clock)', validators=[DataRequired()],render_kw={"placeholder": "Enter end time hour"})
	eventdate = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()],render_kw={"placeholder": ""})
	submit = SubmitField('Search Events')

class VenueDateForm(FlaskForm):
	zipcode = IntegerField('Zip Code', validators=[DataRequired()],render_kw={"placeholder": "Enter zipcode"})
	eventdate = StringField('Date', validators=[DataRequired()],render_kw={"placeholder": "Enter date"})
	submit = SubmitField('Search Events')


class StartEventForm(FlaskForm):
	venueid = IntegerField()
	eventname = StringField('Event Name', validators=[DataRequired()])
	eventdesc = StringField('Event Description')
	eventdate = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
	genderoption = StringField('Specify a Gender?(optional)')
	starttime = IntegerField('Start Time(24-Hr)', validators=[DataRequired()])
	endtime = IntegerField('End Time(24-Hr)', validators=[DataRequired()])
	eventcapacity = IntegerField('Number of players', validators=[DataRequired()])
	submit = SubmitField('Start Event')


	# c=common()
	# venuelist=c.get_all_venues()
	# venues=forms.ChoiceField(choices=venuelist)
	# class Meta:
	# 	model = Events
	# 	fields={
	# 		'eventname','eventdesc','eventdate','starttime','endtime','eventcapacity','genderoption'
	# 	}

	# 	labels = {
	# 			'genderoption': "Gender (Optional)",
	# 			'eventname': "Event Name",
	# 			'eventdesc': "Event Description",
	# 			'starttime': "Start Time(in 24-hour format)",
	# 			'endtime': "End Time(in 24-hour format)",
	# 			'eventcapacity': "Event Capacity",
	# 			'venues': "Choose Venue"
	# 	  }