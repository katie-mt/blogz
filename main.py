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
    blog_entry = db.Column(db.String(1000))

    #initializer (otherwise known as constructor) for the Blog class.  Blog posts should have both a title and blog_entry.  Add these as parameters to the constructor
    def __init__(self, title, blog_entry):
        self.title = title
        self.blog_entry = blog_entry

    def is_valid(self):
        if self.title and self.blog_entry and self.created:
            return TRUE
        else:
            return FALSE

@app.route('/', methods=['GET'])
def blog_home():
    new_post = request.args.get('title', 'blog_entry')
    if new_post:
        #handler method to display all blog posts from the database
        display_blogs = Blog.query.all()
        return render_template('blog_list.html')
    
    else:
        return render_template('blog_list.html')


#adding handler to display the registration template
@app.route('/addnewpost', methods=['POST', 'GET'])
def new_blog():
    #if the request method is POST then we request the title and blog_entry from the form.
    if request.method =='POST':
        #requests the title from the form
        title = request.form['title']
        #requests the blog_entry from the form
        blog_entry = request.form['blog_entry']
        #creates blog entry that is a blog entry object
        new_blog_entry = Blog(title, blog_entry)
        #put the new_blog_entry in the database
        db.session.add(new_blog_entry)
        db.session.commit()
        #if it is a POST then render the blog_list page at the '/' route
        return render_template('blog_list.html')

    #add new_entry to pass into the blog_list.html template
    return render_template('add_new_post.html')

#TODO:  If either the blog title or blog body is left empty in the new post form, the form is rendered again, with a helpful error message and any previously-entered content in the same form inputs.

if "__main__" == __name__:
    app.run()



#Routes
# "/" - GET:redirect to "/blog"
# "/blog" - GET:Display list of all entries with default sort order(oldest-first)
# "/blog?entry=ID" GET: display entry with id=ID
# "/new_entry" - GET display new entery form; POST; process entry 

#def index
#def display_blog_entries
#def 