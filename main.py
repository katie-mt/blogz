from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#creates the app
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive2@localhost:8889/build-a-blog'
#connection string used to connect the database.  Connecting to mysql database using a pysysql driver, username, password, hosting is local, port number, name of database.
app.config['SQLALCHEMY_ECHO'] = True
#provides additional details on object relational mapping by using SQLAlcchemy to echo the SQL commands in the terminal when app is running.
db = SQLAlchemy(app)
#sets variable equal to the results of the SQLAlchemy object.  Calls the SQLAlchemy constructor and passes in the flask application in order to bind the two together.  This creates a database object that can be used within the application to interface with the database via Python code.

#Creates a persistent class to help add data to the database.  The class will represent the application specific data that we want to store in the database.
#extends the db.model class.  Allows task objects to be translated to a class settign by SQLAlchemy.
class Blog(db.Model):
    #specifies the datafields that should go into columns. Every persistent class (stored in a database) will have a primary key and the id field will represent the primary key for this class and for the database table.  Primary keys uniquely identify rows in a given table.  The data that is associated with the id field will be an integer.
    id = db.Column(db.Integer, primary_key=True)
    #represents the blog title field, represented as a string with a limit of 120 characters.
    title = db.Column(db.String(120))
    #represents the blog post content, represented as a string with a limit of 1000 characters.
    blog_post = db.Column(db.String(1000))
    #TODO:  Does the variable name 'blog_post' need to match any objects or variables in the add_new_post.html file?

