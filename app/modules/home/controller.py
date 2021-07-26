# app/home/controller.py
from datetime import datetime

from flask import render_template, abort, session, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy import extract

from app.models import User, Log, Salary
from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return redirect(url_for('auth.login'))


@home.route('/employee/dashboard')
@login_required
def employee_dashboard():

    if current_user != None:
        logs = Log.query.filter(extract('year', Log.date) == datetime.today().year,
                                extract('month', Log.date) == datetime.today().month,
                                Log.user_id == session['_user_id']
                                ).all()
        print(len(logs))
        return render_template('home/index_emp.html', logs = logs)

    else:
        abort(403)

# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/index.html')