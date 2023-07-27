from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt   
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required





example_posts = [
    {
        'author': 'JGoode',
        'title': 'Blog Post 1',
        'content': "My first blog post :)",
        'date_posted': 'July 21, 2023'
    },
      {
        'author': 'Eduardo',
        'title': 'Blog Post 2',
        'content': "My primera blog post",
        'date_posted': 'July 21, 2023'
    }
]



@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=example_posts)

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
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('login unsuccesful. Check email/password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/accout")
@login_required
def account():
    return render_template('account.html', title='acount')
