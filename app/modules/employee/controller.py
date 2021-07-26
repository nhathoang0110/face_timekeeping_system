import json
from datetime import datetime
from flask import render_template, abort, session, request, jsonify, url_for
from flask_login import login_required, current_user
from flask_wtf import Form
from sqlalchemy import extract
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from app.models import User, Log, Salary, Schedule
from . import employee
# from run import PATH_IMAGE_RECOGNITION
import os


@employee.route('/home')
@login_required
def home():
    # get month
    # logs = Log.query.filter(extract('year', Log.date) == datetime.today().year,
    #                         extract('month', Log.date) == datetime.today().month,
    #                         Log.user_id == session['_user_id']
    #                         ).all()

    # get year
    logs = Log.query.filter(extract('year', Log.date) == datetime.today().year,
                            Log.user_id == session['_user_id']
                            ).all()

    data = []
    for log in logs:
        data.append({'tag_in': log.tag_in, 'tag_out': log.tag_out, 'date': str(log.date), 'time_in': str(log.time_in), 'time_out': str(log.time_out)})
    # print(json.dumps(logs, default=lambda o: o.__dict__))
    return json.dumps(data)
    


@employee.route('/get_detail_log')
@login_required
def get_detail_log():
    date = request.args.get('date')

    try:
        log = Log.query.filter(Log.date == date, Log.user_id == session['_user_id']).first()
        schedule = Schedule.query.filter(Schedule.id == log.schedule_id).first()

        return jsonify(date = str(log.date), time_in = str(log.time_in), tag_in = log.tag_in,
                       time_out = str(log.time_out), tag_out = log.tag_out,
                       correct_time_in = str(schedule.correct_time_in),
                       correct_time_out=str(schedule.correct_time_out))
    except:

        return jsonify(date = '', time_in = '', tag_in = '',
                   time_out = '', tag_out = '',
                   correct_time_in = '',
                   correct_time_out= '')





# @employee.route('/get_salary')
# @login_required
# def get_salary():
#     year = request.args.get('year')
#     month = request.args.get('month')
#
#     salary = Salary.query.filter(Salary.year == year,
#                             Salary.month == month,
#                             Salary.user_id == session['_user_id']).first()
#     if salary is None:
#         return jsonify(message="Don't have log salary in time query"), 400
#
#     logs = Log.query.filter(extract('year', Log.date) == year,
#                             extract('month', Log.date) == month,
#                             Log.user_id == session['_user_id']).all()
#     num_in_late = 0
#     num_out_early = 0
#     for log in logs:
#         if log.tag_in == 2:
#             num_in_late += 1
#         if log.tag_out == 2:
#             num_out_early += 1
#
#     return jsonify(salary= salary.salary, num_log = len(logs), num_in_late = num_in_late, num_out_early = num_out_early), 200


@employee.route('/get_stranger')
@login_required
def get_stranger():
    day = request.args.get('d')
    month = request.args.get('m')
    year = request.args.get('y')

    if day == None:
        now = datetime.now()
        day = now.day
        month = now.month
        year = now.year

    root = 'app/static/image_to_debug/' + str(day) +'_'+ str(month) +'_'+ str(year)

    paths = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            paths.append(os.path.join(path, name)[3:])

    i = 0
    results = []
    while i < len(paths):
        results.append(paths[i:i+6])
        i +=6
    return render_template('employee/image_stranger.html', paths=results, date = str(day) +'-' + str(month) +'-' +str(year))

@employee.route('/get_salaríes')
@login_required
def get_salaries():
    salaries = Salary.query.filter(Salary.user_id == current_user.id).order_by(Salary.year.desc(), Salary.month.desc()).all()
    return render_template('employee/salary-view.html', data=salaries)
#

