from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', 
							validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	#creating custeom validation for form 
	def validate_username(self, username):
		#this query returns the username if same username is entered by user otherwise return the none
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('This username is taken. Please choose different one.')

	def validate_email(self, email):
		#this query returns the email if same email is entered by user otherwise return the none
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email is taken. Please choose different one.')

class LoginForm(FlaskForm):
	email = StringField('Email', 
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')