from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#creates the app
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive3@localhost:8889/blogz'
#connection string used to connect the database.  Connecting to mysql database using a pysysql driver, username, password, hosting is local, port number, name of database.
app.config['SQLALCHEMY_ECHO'] = True
#provides additional details on object relational mapping by using SQLAlcchemy to echo the SQL commands in the terminal when app is running.
db = SQLAlchemy(app)
#sets variable equal to the results of the SQLAlchemy object.  Calls the SQLAlchemy constructor and passes in the flask application in order to bind the two together.  This creates a database object that can be used within the application to interface with the database via Python code.
app.secret_key = 'y337kGcys&zP3B'

#Creates a persistent class to help add data to the database.  The class will represent the application specific data that we want to store in the database.
#extends the db.model class.  Allows task objects to be translated to a class settign by SQLAlchemy.
class Blog(db.Model):
    #specifies the datafields that should go into columns. Every persistent class (stored in a database) will have a primary key and the id field will represent the primary key for this class and for the database table.  Primary keys uniquely identify rows in a given table.  The data that is associated with the id field will be an integer.
    id = db.Column(db.Integer, primary_key=True)
    #represents the blog title field, represented as a string with a limit of 120 characters.
    title = db.Column(db.String(120))
    #represents the blog post content, represented as a string with a limit of 1000 characters.
    blog_entry = db.Column(db.String(1000))
    #foreign key linking the user's id to the blog past (adds new column)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #initializer (otherwise known as constructor) for the Blog class.  Blog posts should have a title, blog_entry and owner.  Add these as parameters to the constructor
    def __init__(self, title, blog_entry, owner):
        self.title = title
        self.blog_entry = blog_entry
        self.owner = owner


#add user class model.  Declare new class called user that extends db.Model.  
class User(db.Model):

    #specify the datafields that should go into columns.  Set primary key
    id = db.Column(db.Integer, primary_key=True)
    #our users will have email and password properties
    #we shouldn't have two different accounts associated with an email.  unique=True ensures that SQLAlchemy will not allow the creation of two separate users with the same email. 
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    #specify that a user can have many blogs.  This isn't going to be a column because there won't be a column in the database for this.  But we want to establish that there is a relationship here that we want the relational database manager SQLAlchemy to manage for us.  
    #SQLAlchemy should populate this blogs list with things from the class task such that their owner property is equal to the specific user that is in consideration. 
    blogs = db.relationship('Blog', backref='owner')

    #initializer (constructor) for the user class
    #users should always have emails and passwords so we'll add those as parameters to our constructor
    def __init__(self, email, password):
        self.email = email
        self.password = password
        #we then went into python shell to create the user table and at least one user object for us to work with.  See video 5 for details.


#adding handler to display the login template
#add methods argument to ensure that login can process requests
@app.route('/login', methods=['POST', 'GET'])
def login():
    #check for the request type.  On a GET request I just want to render the login form and on a POST request I want to get data out of the request and try to log the user in.
    if request.method == 'POST':
        #remember that there are two inputs on the login form, one that is name=email and one that is name=password.  Get this data out of the request
        ##request.form is the python dictionary that contains Post data or data sent in a post request
        email = request.form['email']
        password = request.form['password']
        #try to verify the user's password.  Need to retrieve the user and the associated email from the database. 
        #.first.  If we expect that our result set will only contain one thing or we want to get the first thing. This will retrieve that one item
        #this will return a user with the given email with the given email if the user exists.  If the user doesn't exist then the user variable will be equal to the special value none. 
        user = User.query.filter_by(email=email).first()
        #to verify that not only do i have the correct password but do I have a user in the system with the given email
        #this will check first, does the user exist.  If this is none (query did not return a user with the given email address from the database) then this will be none and the conditional will short circuit.
        #if the user does exist then we will go ahead and compare the password.  At which point we would want to login
        if user and user.password == password:
            #a session is an object that you can use to store data that is associated with a specific user from one request to another. 
            #when a user logs in, put in session (session is a dictionary) a piece of data.  Under email input the email.  Add this both here and under register.
            session['email'] = email
            #here we want to give the user a message that says they are logged in.  This puts the message in a queue for us to access within our base template
            flash("Logged in")
            #when a user logs in, we are going to redirect them to the homepage
            return redirect('/newpost')   
        else:
            #when the login fails, let user know why.  We also add a category to add styling on the front, this is the second parameter.  For this one, we named the category error.  To make a category, must also edit the loop in the base template.
            flash('User password incorrect, or user does not exist', 'error')
    
    return render_template('login.html')
    #if the user doesn't login, we will return them back to the login form

#adding handler to display the registration template
@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
    #if we are dealing with a request method of post then create a new user
    #in the registration template we have an email, password and verify.  Retrieve those parameters from the database
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        #if we validate the data and everything is good, then go ahead and create a new user
        #check that the user does not exist
        existing_user = User.query.filter_by(email=email).first()
        #if there is not an existing user then create a new user from the input information
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            #we put this above under login as well.  Once a user registers and we put them in the database, we'll log them in by putting their email in the session.
            #cookies will track who is logging in so server knows who to automatically log in.
            session['email'] = email
            #if there is not an existing user, redirect the user back to the root
            return redirect('/blog')
        else:
            #TODO - return a message that tells the user that they alreaday exist in the database
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')


@app.route('/blog', methods=['GET'])
def blog_home():
    #GET request to receive the individual id that the user is reqeusting
    individual_id = request.args.get('id')
    if not individual_id:
        #handler method to display all blog posts from the database
        display_blogs = Blog.query.all()
        #display_blogs_display_blogs.  Keyword argument.   
        return render_template('blog_list.html', display_blogs=display_blogs)
    
    else:
        #retrieve the id field from the database
        requested_blog_post = Blog.query.get(individual_id)
        return render_template('individual_post.html', display_blog=requested_blog_post)       

#new function.  Special type of function to run for every request (therefore no handler).  For every request, we want it to run and see if the user has logged in.
#special decorator - run this function before you call the request handler for the incoming request.  
@app.before_request
def require_login():
    #create a whitelist or list of pages that you don't need to be logged in to view
    #list called allowed routes.  List of routes that users don't have to be logged in to see.  Don't need to login to see the login route or the register route
    allowed_routes = ['login', 'signup']
    #if I say that the endpoint is not login and not register (request.endpoint is not in the allowed routes) then this means that i'm wanting to force the user to login meaning i should also check if the email is in session.  If the request.endpoint is in the allowed routes then skip over the redirect and process requests as previously
    if request.endpoint not in allowed_routes and 'email' not in session:
    #if the user has not logged in yet
        #redirect to the login page
        return redirect('/login')

#adding handler to display the registration template
@app.route('/newpost', methods=['POST', 'GET'])
def new_blog():
    #if the request method is POST then we request the title and blog_entry from the form.
    if request.method =='POST':
        #requests the title from the form
        title = request.form['title']
        #requests the blog_entry from the form
        blog_entry = request.form['blog_entry']
        #empty string for title error message
        title_error = ''
        #empty string for blog entry (body) error message
        blog_entry_error = ''

        #evaluating that the title and blog_entry fields are not left empty
        if not title:
            title_error = 'Please enter a valid title'
        
        if not blog_entry:
            blog_entry_error = 'Please enter a valid blog post'
        
        #if there is a title_error or blog_entry_error then re-render the template and keep the title and blog_entry entries
        if title_error or blog_entry_error:
            return render_template('add_new_post.html', title=title, blog_entry=blog_entry, title_error=title_error, blog_entry_error=blog_entry_error)
        
        else:
            #creates blog entry that is a blog entry object
            email = session['email']
            owner = User.query.filter_by(email=email).first()
            
            new_blog_entry = Blog(title, blog_entry, owner)
            #put the new_blog_entry in the database
            db.session.add(new_blog_entry)
            db.session.commit()
            #redirect to the blog_list page at the '/blog' route with the ?= appended with the id number of the blog post
            #id = new_blog_entry.id
            #redirect to the blog_list page at the '/blog' route with the ?= appended with the id number of the blog post
            #return redirect ('/blog?=' + str(new_blog_entry.id))
            #if new_blog_entry:
            #display_blog = Blog.query.get(new_blog_entry)
            #return render_template('individual_post.html', display_blog)
            url = "/blog?id=" + str(new_blog_entry.id)
            return redirect(url)
            #return render_template('individual_post.html', new_blog_entry)
    else:
        #grabs all the blogs from the database
        display_blogs = Blog.query.all()
        return render_template('add_new_post.html')

if "__main__" == __name__:
    app.run()