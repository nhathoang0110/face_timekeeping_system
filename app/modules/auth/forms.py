# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, EqualTo

from app.models import User


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    mail = StringField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(mail=field.data).first():
            raise ValidationError('Email is already in use.')

    # def validate_username(self, field):
    #     if Employee.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    mail = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')