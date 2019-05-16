from app import app,db
from models import Blog, User
from flask import render_template, request, redirect, flash, url_for, session
from datetime import datetime,timedelta

 # ==================== R A N D O M    F U N C T I O N S =========================   
def get_active_posts(user=None):
    if user is None:
        return Blog.query.filter_by(active=True).order_by(-Blog.id).all()
    else:
        return Blog.query.filter_by(user_id=user.id, active=True).order_by(-Blog.id).all()

def get_inactive_posts():
    return Blog.query.filter_by(active=False).order_by(-Blog.id).all()

 # ================================================================================   

# Filter requests when user tries to make a "NEW POST" i.e. /newpost
@app.before_request
def logincheck():
    protected_path = ['/newpost']
    if 'username' not in session and request.path in protected_path:
        return redirect('/login')

 # ================================================================================   
@ app.route('/')
def index():
    all_users = User.query.all()
    return render_template('index.html', users = all_users)

@ app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        login_username = request.form['username']
        login_password = request.form['password']

        possible_user = User.query.filter_by(username = login_username).first()
        if possible_user and possible_user.check_password(login_password):
            session['username'] = login_username
            return redirect('/blog?user={}'.format(login_username))
        else:
            flash('Invalid username and/or password.','info')
            return redirect('')
    else:
        return render_template('login.html')

 # ================================================================================   

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify']

        check_username_length = (3<= len(username) <=20)
        check_pass_length = (3<= len(password) <=20)
        check_pass_match = (verify_password == password)

        if not check_username_length:
            flash('Invalid username','username')
        if not check_pass_length:
            flash('Invalid password','password')
        if not check_pass_match:
            flash('Passwords do not match','verify')
            
        if all([check_pass_length,check_username_length,check_pass_match]):
            # add the user to the database
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            # add the username to the session
            session['username']= username
            # send the new_user to /new_post

            return render_template('newpost.html')
        
        # this will probably not run at all!
        return render_template('signup.html',username=username)
    # for GET request, just render the page
    return render_template('signup.html')

 # ================================================================================   

@app.route('/blog',methods=['GET'])
# This needs to be able to handle

#   /blog                   will show all the posts
#   /blog?user=user_x       will show all user's posts
#   /blog?id=000000         will show a certain blog with that id

def blog():
    # Handling different GET requests
    blog_id = request.args.get('id')
    user_name = request.args.get('user')
    the_user = User.query.filter_by(username = user_name).first()
    
    # if no query variables, just open the /blog
    if (blog_id is None) and (user_name is None):
        return render_template('blog.html',posts=get_active_posts())

    # if blog_id is a number, try to find it, otherwise do nothing
    elif not blog_id is None:
        try:
            the_post = Blog.query.filter_by(id=int(blog_id)).first()
            if the_post:
                return render_template('blog.html',posts=[the_post])
            else:
                flash('The requested blog does not exist.','info')
                return redirect('')
        except TypeError:
            flash('Invalid blog id.','info')
            return redirect('')

    # if user_id is given in the url, try to find the user and display posts.
    if not user_name is None:
        if not the_user:
            # if no user with that user_name, then redirect to same spot and flash error
            flash('The specified user not found.','info')
            return redirect('')
        else:
            # if user found, list all the blogs for that user
            return render_template('blog.html',posts=get_active_posts(the_user))
        
 # ================================================================================   

@app.route('/newpost', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner_user_name = session['username']
        owner = User.query.filter_by(username = owner_user_name).first()
        if title and body:
            new_post = Blog(title,body,owner)
            new_post.post_date = datetime.now()
            db.session.add(new_post)
            db.session.commit()
            flash('Your new blog is published.','info')
            return render_template('blog.html',posts=[new_post])
        else:
            flash('Your blog needs both "title" and some "text"','info')
            return render_template('newpost.html', title=title, body=body)
    else:
        return render_template('newpost.html')

 # ================================================================================   
 # === Commenting this part out for now, perhaps make it work in the future! ======  
 # ================================================================================    
"""
@app.route('/archive',methods=['POST','GET'])
def archive():
    if request.method == 'POST':
        post_id = request.form['post-id']
        the_post = Blog.query.filter_by(id=post_id).first()
        the_post.active = True
        db.session.add(the_post)
        db.session.commit()
        flash('The post is unarchived.','info')
        return redirect('/blog')

    else:
        return render_template('blog.html',posts=get_inactive_posts())
"""
 # ================================================================================    

if __name__ == '__main__':
    app.run()