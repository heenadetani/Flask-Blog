from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

#user_loader i.e for reloading the user from the user_id stored in session
@login_manager.user_loader
def load_user(user_id):
	#returns user which belongs to this user_id
	return User.query.get(int(user_id))
#UserMixing is class which already contains methods likd                                                                                           is_authenticated,is_active,is_annonymous,get_id
class User(db.Model,UserMixin):
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
