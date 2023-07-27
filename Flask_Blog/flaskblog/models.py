from datetime import datetime
from flaskblog import app, db, login_manager
from flask_login import UserMixin


#creating a decorator using login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
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
    

############################################
#functions created to test database, used add_user, but add_post i used the python repl


def add_user_to_database(username, email, password):
    # created this function mostly to test if the db and its models were connected and working
    with app.app_context():
        #context has to be called or else there are errors about context
        new_user = User(username=username, email=email, password=password)
        # connecting User model to functions parameters
        db.session.add(new_user)  # add to db, then commit
        db.session.commit()
        whole_table = User.query.all() #for testing that db is successfully updated
        print(whole_table) # same note as above
# add_user_to_database('Mehcad Brooks', 'superman@place.net', 'iewiwo')

def add_post_to_database(title, content, user_id):
    # created this function mostly to test if the db and its models were connected and working
    with app.app_context():
        #context has to be called or else there are errors about context
        new_post = Post(title=title, content=content, user_id=user_id)
        # connecting Post model to functions parameters
        db.session.add(new_post)  # add to db, then commit
        db.session.commit()
        whole_table = Post.query.all() #for testing that db is successfully updated
        print(whole_table) # same note as above
#add_post_to_database('Mehcad Brooks', 'superman@place.net', 'iewiwo')