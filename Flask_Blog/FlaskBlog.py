from flask import Flask, render_template, url_for, flash, redirect, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm



app = Flask(__name__)
app.config['SECRET_KEY'] = 'd4187d9e3f9a16051f0f1b3002211882'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db= SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # post is sort of pseudo-column, will not be listed when we run the full user table, but connects query

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user.id is User.id, it is lowercase because it is referencing the tablename, which default to lowercase

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"



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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        # havent seen form.username obj/dict, but assume it binds e.target.value to a key called data in username
        return redirect(url_for('home'))
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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('login unsuccesful. Check username/password', 'danger')
    return render_template('login.html', title='Login', form=form)

def add_user_to_database(username, email, password):
    with app.app_context():
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        whole_table = User.query.all()
        print(whole_table)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # add_user_to_database('JasonTiya', 'jt@tyson.net', 'thugpon')

    app.run(debug=True)