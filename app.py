from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# configure path to sql alchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
'''
sqlite is used right now for simplicity.
/// means relative path to the working directory
//// means absolute path
Here, post.db file is created in the current working directory.
'''
db = SQLAlchemy(app)
# This class represents the table of our databse.


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post' + str(self.id)


@app.route('/')
def temp():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post) # adding post to database
        db.session.commit() # commit it to database
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted)
        return render_template('posts.html', posts=all_posts)

# Now we want to delete our post from the page itself.
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id) # Make sure that the app doesn't break if not found
    db.session.delete(post) # delete the post with given ID
    db.session.commit() # commit the change
    return redirect('/posts') # redirect to /posts

# Now we want to edit our post from the page itself.
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post) # adding post to database
        db.session.commit() # commit it to database
        return redirect('/posts')
    else:
        return render_template('new_post.html')

if __name__ == "__main__":
    app.run(debug=True)