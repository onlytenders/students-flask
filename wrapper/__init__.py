from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'wrapper/static/uploads/'
app.config['CSRF_ENABLED'] = True

db = SQLAlchemy(app)
manager = LoginManager(app)

from wrapper import routes, models