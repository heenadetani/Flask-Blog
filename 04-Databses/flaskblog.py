from datetime import datetime
from flask import Flask,render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '421a3db5f7fad994c82505c4ec4c1d42'
#Specifying URI for database i.e where the DB is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#In SQLAlchemy we can represent DB structure as classes and those classes are called models
#creating SQlAlchemy DB instance
db = SQLAlchemy(app)

#Models
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	#user and post models are going to have a one-to-many relationship as users are the authors who can write as many posts as they want
	posts = db.relationship('Post', backref='author', lazy=True)

	#this is a magic method which is used to return object representation(i.e to display object)
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	#user.id i.e id of the user who authored the post
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"


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
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html',title='Register',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('you have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful.Please check username and password', 'danger')
	return render_template('login.html',title='Login',form=form)

if __name__ == '__main__':
	app.run(debug=True)