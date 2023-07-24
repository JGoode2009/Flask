from flask import Flask, render_template, url_for, flash, redirect, request
app = Flask(__name__)
from forms import RegistrationForm, LoginForm

app.config['SECRET_KEY'] = 'd4187d9e3f9a16051f0f1b3002211882'

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




if __name__ == '__main__':
    app.run(debug=True)