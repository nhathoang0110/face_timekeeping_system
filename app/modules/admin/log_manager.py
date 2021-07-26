import json
from datetime import datetime
from flask import render_template, abort, session, request, jsonify, flash, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sqlalchemy import extract, or_, func
from werkzeug.utils import redirect
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
import calendar
from app import db
from app.models import *
from . import admin
from run import PATH_IMAGE_RECOGNITION
import os

@admin.route('/get_logs')
@login_required
def get_logs():
    if current_user.is_admin == True:
        try:
            month = request.args.get('month')
            year = request.args.get('year')
            if month == None or year == None:
                month = datetime.today().month
                year = datetime.today().year
            else:
                month = int(month)
                year = int(year)
            arrs =  db.session.query(User, Log).filter(User.id == Log.user_id,
                                                            extract('year', Log.date) == year,
                                                            extract('month', Log.date) == month,
                                                            ).all()

            data = {} # {user_id: {date: {obj} } }
            users = {} # {user_id: username}

            for user, log in arrs:
                if user.id not in data:
                    data[user.id] = {}

                obj = dict()
                obj['username'] = user.name
                obj['log_id'] = log.log_id
                obj['tag_in'] = log.tag_in
                obj['tag_out'] = log.tag_out

                data[user.id][log.date.day] = obj

                users[user.id] = user.name

            data = dict(sorted(data.items(), key=lambda x: x[0]))
            for k, v in data.items():
                data[k] = dict(sorted(v.items(), key=lambda x: x[0]))


            num_day= calendar.monthrange(year, month)[1]

            time = str(month) + '/' + str(year)
            return render_template('admin/attendance.html', data=data, user=users, num_day= num_day, time=time)
        except Exception as e:
            print(e)
            return  render_template('admin/attendance.html')

    else:
        abort(401)



@admin.route('/get_log_search', methods=['POST'])
@login_required
def get_log_search():
    if current_user.is_admin == True:
        try:
            username = request.form.get('username')
            print(username)

            month = datetime.today().month
            year = datetime.today().year
            arrs =  db.session.query(User, Log).filter(User.id == Log.user_id, User.name==username,
                                                            extract('year', Log.date) == year,
                                                            extract('month', Log.date) == month,
                                                            ).all()
            print(arrs)
            data = {} # {user_id: {date: {obj} } }
            users = {} # {user_id: username}

            for user, log in arrs:
                if user.id not in data:
                    data[user.id] = {}

                obj = dict()
                obj['username'] = user.name
                obj['log_id'] = log.log_id
                obj['tag_in'] = log.tag_in
                obj['tag_out'] = log.tag_out

                data[user.id][log.date.day] = obj

                users[user.id] = user.name

            data = dict(sorted(data.items(), key=lambda x: x[0]))
            for k, v in data.items():
                data[k] = dict(sorted(v.items(), key=lambda x: x[0]))


            print(data)
            print(users)

            return render_template('admin/attendance.html', data=data, user=users)
        except Exception as e:
            print(e)
            return  render_template('admin/attendance.html')

    abort(401)


@admin.route('/get_log_post', methods=['POST'])
@login_required
def get_log_post():
    if current_user.is_admin == True:
        data = dict()
        try:
            user_id = request.form['user_id']
            day = datetime.strptime(request.form['time'], '%d/%m/%Y')
            user  = User.query.filter(User.id == user_id).first()
            if user == None:
                return jsonify(message="Không tồn tại nhân viên", status=400)


            log = Log.query.filter(Log.user_id == user_id, Log.date == day).first()
            if log:
                data['user_id'] = log.user_id
                data['log_id'] = log.log_id
                data['tag_in'] = log.tag_in
                data['tag_out'] = log.tag_out
                data['date'] = log.date.strftime('%d/%m/%Y')
                if log.time_in:
                    data['time_in'] = log.time_in.strftime('%H:%M:%S')
                else:
                    data['time_in'] = None

                if log.time_out:
                    data['time_out'] = log.time_out.strftime('%H:%M:%S')
                else:
                    data['time_out'] = None
            else:
                data['user_id'] = user.id
                data['time_in'] = None
                data['time_out'] = None
                data['tag_in'] = None
                data['time_out'] = None
                data['date'] = day.strftime('%d/%m/%Y')
                data['log_id'] = None


            return jsonify(data= data, status = 200)
        except Exception as e:
            print(e)
            return jsonify(message="Loi", status = 400)

    abort(401)



@admin.route('/get_log')
@login_required
def get_log():
    return render_template('admin/search_log.html')

@admin.route('update_log', methods=['PUT'])
@login_required
def update_log():
    if current_user.is_admin == True:
        try:

            user_id = int(request.form['user_id'])
            date = datetime.strptime(request.form['date'], '%d/%m/%Y')
            time_in = request.form['time_in']
            time_out = request.form['time_out']


            log = Log.query.filter(Log.user_id == user_id, Log.date == date).first()
            schedule = Schedule.query.filter().order_by(Schedule.id.desc()).limit(1).first()

            if log:
                if time_in != '' and time_in != 'undefined':
                    log.time_in = datetime.strptime(time_in, '%H:%M').time()
                    if schedule.correct_time_in >= log.time_in:
                        log.tag_in =1
                    else:
                        log.tag_in = 2
                if time_out != '' and time_out != 'undefined':
                    log.time_out = datetime.strptime(time_out, '%H:%M').time()
                    if schedule.correct_time_out <= log.time_out:
                        log.tag_out =1
                    else:
                        log.tag_out = 2

                db.session.commit()

            else:
                log = Log(user_id = user_id, date=date,schedule_id = schedule.id)
                if time_in != '' and time_in != 'undefined':
                    log.time_in = datetime.strptime(time_in, '%H:%M').time()
                    if schedule.correct_time_in >= log.time_in:
                        log.tag_in = 1
                    else:
                        log.tag_in = 2
                if time_out != '' and time_out != 'undefined':
                    log.time_out = datetime.strptime(time_out, '%H:%M').time()
                    if schedule.correct_time_out <= log.time_out:
                        log.tag_out = 1
                    else:
                        log.tag_out = 2

                db.session.add(log)
                db.session.commit()



            data = dict()
            data['user_id'] = log.user_id
            data['log_id'] = log.log_id
            data['tag_in'] = log.tag_in
            data['tag_out'] = log.tag_out
            data['date'] = log.date.strftime('%d/%m/%Y')
            if log.time_in:
                data['time_in'] = log.time_in.strftime('%H:%M:%S')
            else:
                data['time_in'] = None

            if log.time_out:
                data['time_out'] = log.time_out.strftime('%H:%M:%S')
            else:
                data['time_out'] = None



            return jsonify(message='Cập nhật thành công',data=data, status=200)

        except Exception as e:
            print(e)
            return jsonify(message='Cập nhật không thành công' ,status= 400)

    abort(401)


@admin.route('/get_stranger')
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

    root = PATH_IMAGE_RECOGNITION + 'image_to_debug/' + str(day) +'_'+ str(month) +'_'+ str(year)

    paths = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            paths.append(os.path.join(path, name)[3:])

    i = 0
    results = []
    while i < len(paths):
        results.append(paths[i:i+6])
        i +=6
    return render_template('admin/image_stranger.html', paths=results, date = str(day) +'-' + str(month) +'-' +str(year) )