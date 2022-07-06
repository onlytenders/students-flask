from flask_login import UserMixin

from sqlalchemy.ext.mutable import MutableList

from wrapper import db, manager

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    father_name = db.Column(db.String(50), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    workplace = db.Column(db.String(128), nullable=True)
    work_experience = db.Column(db.Integer, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(), nullable=True)
    date_started = db.Column(db.Date, nullable=True)
    date_ended = db.Column(db.Date, nullable=True)

    best = db.Column(MutableList.as_mutable(db.PickleType), nullable=True)
    worst = db.Column(MutableList.as_mutable(db.PickleType), nullable=True)
    grades = db.Column(MutableList.as_mutable(db.PickleType), nullable=True)
    tests = db.Column(MutableList.as_mutable(db.PickleType), nullable=True)

    problem_points = db.Column(db.String(), nullable=True)
    overall_evaluation = db.Column(db.String(), nullable=True)
    recommendations = db.Column(db.String(), nullable=True)

    hash = db.Column(db.String(), nullable=False)
    profile_pic = db.Column(db.String(), nullable=True)
    course_id = db.Column(db.String(), nullable=True)

class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(123), nullable=False)

class Course (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    date_started = db.Column(db.Date, nullable=True)
    date_ended = db.Column(db.Date, nullable=True)
    price = db.Column(db.String(), nullable=True)

    specification = db.Column(MutableList.as_mutable(db.PickleType), nullable=True)
    tests = db.Column(MutableList.as_mutable(db.PickleType), nullable=True)
    testing_min = db.Column(db.Integer, nullable=True)

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)