import os
import secrets
from PIL import Image 
from flask import render_template, url_for, flash, redirect, request, Request
from flaskblog import app, db, bcrypt   
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required




# dummy data
# example_posts = [
#     {
#         'author': 'JGoode',
#         'title': 'Blog Post 1',
#         'content': "My first blog post :)",
#         'date_posted': 'July 21, 2023'
#     },
#       {
#         'author': 'Eduardo',
#         'title': 'Blog Post 2',
#         'content': "My primera blog post",
#         'date_posted': 'July 21, 2023'
#     }
# ]



@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit() # an error is occuring hear, resulting can't find user table
        flash(f'Your account has been created. You are now able to login', 'success')
        # havent seen form.username obj/dict, but assume it binds e.target.value to a key called data in username
        return redirect(url_for('login'))
        # note url for goes to home function
    if request.method == "POST":
        # Print form validation errors to the console
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field: {field}, Error: {error}")
    # else:
    #     print("the form isn't validating on submit properly. form.validate_on_submit= ", form.validate_on_submit())
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) #using get method instead of [key] in case it doesn't exist
            next_page = request.args.get('next')
            return redirect(next_page)if next_page else redirect(url_for('home'))
        else:
            flash('login unsuccesful. Check email/password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # to get the file extension
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    #adding this to resize the profile pics in case they are large
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            # this appears to be updating the username and email in the account essentially replacing the old account. 
            flash('Your account has been updated', 'success')
            return redirect(url_for('account')) # need to redirect for post get redirect pattern (warning about resubmitting data thing)
    elif request.method == 'GET': #? why just for get? maybe just the form we end up at first?
        form.username.data = current_user.username
        form.email.data = current_user.email
    print(" current user image file=", current_user.image_file)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', 
                        image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)