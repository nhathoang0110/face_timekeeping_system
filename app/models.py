# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from json import JSONEncoder
from app import db, login_manager


class User(UserMixin, db.Model):


    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(128))
    avatar = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    phone = db.Column(db.String(12))
    date_of_birth = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)

    # def __init__(self, mail, name, salary):
    #     self.mail = mail
    #     self.salary = salary
    #     self.name = name

    # @property
    def get_password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')
        # return self.password
    # @password.setter
    def set_password(self, password):
        """
        Set password to a hashed password
        """
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.name)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Salary(db.Model):
    __tablename__ = 'salary'
    user_id = db.Column(db.Integer, primary_key=True)
    salary = db.Column(db.Integer)
    year = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, primary_key=True)
    num_log = db.Column(db.Integer)
    in_late = db.Column(db.Integer)
    out_early = db.Column(db.Integer)


class Message(db.Model):
    __tablename__ = 'message'
    mess_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(640))
    time_create = db.Column(db.DateTime)



class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    start_time_in = db.Column(db.Time)
    end_time_in = db.Column(db.Time)
    correct_time_in = db.Column(db.Time)
    start_time_out = db.Column(db.Time)
    end_time_out = db.Column(db.Time)
    correct_time_out = db.Column(db.Time)


class Log(db.Model, JSONEncoder):
    __tablename__ = 'log'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    date = db.Column(db.Date)
    time_in = db.Column(db.Time)
    time_out = db.Column(db.Time)
    tag_in = db.Column(db.Integer)
    tag_out = db.Column(db.Integer)