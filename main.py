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
            new_blog_entry = Blog(title, blog_entry)
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
            return render_template('individual_post.html', new_blog_entry)
    else:
        #grabs all the blogs from the database
        display_blogs = Blog.query.all()
        return render_template('add_new_post.html')

if "__main__" == __name__:
    app.run()