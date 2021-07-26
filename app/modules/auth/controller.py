# app/auth/controller.py

from flask import flash, redirect, render_template, url_for, abort, session, request
from flask_login import login_required, login_user, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from .forms import LoginForm, RegistrationForm
from app import db
from app.models import User



@auth.route('/login', methods=['GET'])
def login():
    try:
        if session['_user_id'] != None:
            if current_user.is_admin == False:
                return redirect(url_for('home.employee_dashboard'))
            return redirect(url_for('home.admin_dashboard'))
    except:
        return render_template('auth/login.html')


@auth.route('/login', methods=['POST'])
def login_post():


    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(mail=email).first()
    

    if user is not None and user.verify_password(password):
        # log employee in
        login_user(user)
        print(session)

        # redirect to the appropriate dashboard page
        if user.is_admin:
            return redirect(url_for('home.admin_dashboard'))
        else:
            return redirect(url_for('home.employee_dashboard'))
    else:
        flash('Invalid email or password.')
        return redirect(url_for('auth.login'))
        


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    current_user = None
    # flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))