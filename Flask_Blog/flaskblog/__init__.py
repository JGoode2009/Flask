from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

#configurations and initializations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd4187d9e3f9a16051f0f1b3002211882'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# print(app.config['SQLALCHEMY_DATABASE_URI'], 'this is the db config')
##!!! in order to create the database, have to enter python repl, import needed items
# then use app.app_context.push() to avoid have to with...context for every command which created issues

db= SQLAlchemy()
db.init_app(app)
bcrypt = Bcrypt(app)

from flaskblog import routes