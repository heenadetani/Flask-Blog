from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, bcrypt, db
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
	{
	'author' : 'heena',
	'title' :  'blog_post_1',
	'content' : 'first post content',
	'date_posted' : 'october 10, 2020',
	},
	{
	'author' : 'harsha',
	'title' :  'blog_post_2',
	'content' : '2nd post content',
	'date_posted' : 'october 11, 2020',
	}
]
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		#now creating new instance of user using the hashed_password
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created! You can now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html',title='Register',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		#querying db to make sure user exist in db of that email which is entered in the form 
		user = User.query.filter_by(email=form.email.data).first()
		#checking if user exist and password entered in form is equal to password in db
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			#for login we can use the inbuit login_user() fuction of flask_login which also takes remeber_me as a arguement
			login_user(user, remember=form.remember.data)
			#we are checking if in url next parameter exist if it exists than redirect to next page otherwise redirect to home
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful.Please check email and password', 'danger')
	return render_template('login.html',title='Login',form=form)

@app.route('/logout')
def logout():
	#for logout we can use inbuilt logout_user() function of flask_login
	logout_user()
	return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
	return render_template('account.html',title='Account')