#this file in our package is the file where we initialize our application and bring together different components
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = '421a3db5f7fad994c82505c4ec4c1d42'
#Specifying URI for database i.e where the DB is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#In SQLAlchemy we can represent DB structure as classes and those classes are called models
#creating SQlAlchemy DB instance
db = SQLAlchemy(app)

#to prevent from creating a condition of circular-imports we are importing  
from flaskblog import routes