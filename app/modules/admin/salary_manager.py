import json
from datetime import datetime , timedelta
from flask import render_template, abort, session, request, jsonify, flash, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sqlalchemy import extract, or_
from werkzeug.utils import redirect
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app import db
from app.models import User, Log, Salary
from . import admin
from flask_paginate import Pagination, get_page_args


@admin.route('/get_salaries')
@login_required
def get_salaries():
    if current_user.is_admin == True:
        try:
            year = request.args.get('year')
            month = request.args.get('month')

            if month == None:
                month = datetime.now().month - 1
                year = datetime.now().year

            data = []
            for element in db.session.query(User, Salary).filter(User.id == Salary.user_id,
                                                                   Salary.year == year,
                                                                   Salary.month == month,
                                                                   ).order_by(User.id.asc()).all():
                obj = dict()
                obj['user_id'] = element[0].id
                obj['username'] = element[0].name
                obj['avatar'] = element[0].avatar
                obj['salary'] = "{:,}".format(element[1].salary)

                obj['num_log'] = element[1].num_log
                obj['in_late'] = element[1].in_late
                obj['out_early'] = element[1].out_early


                data.append(obj)


            # return json.dumps(data, ensure_ascii=False), 200
            return  render_template('admin/salary-view.html', data=data, time=str(month) +"/" + str(year))
        except Exception as e:
            print(e)
            return json.dumps(dict()), 400



@admin.route('/get_salaries', methods=['POST'])
@login_required
def get_salaries_post():
    if current_user.is_admin == True:
        try:
            year = request.form('year')
            month = request.form('month')

            if month == None:
                month = datetime.now().month - 1
                year = datetime.now().year

            data = []
            for element in db.session.query(User, Salary).filter(User.id == Salary.user_id,
                                                                   Salary.year == year,
                                                                   Salary.month == month,
                                                                   ).order_by(User.id.asc()).all():
                obj = dict()
                obj['user_id'] = element[0].id
                obj['username'] = element[0].name
                obj['avatar'] = element[0].avatar
                obj['salary'] = "{:,}".format(element[1].salary)

                obj['num_log'] = element[1].num_log
                obj['in_late'] = element[1].in_late
                obj['out_early'] = element[1].out_early


                data.append(obj)


            # return json.dumps(data, ensure_ascii=False), 200
            # return  render_template('admin/salary-view.html', data=data, time=str(month) +"/" + str(year))
            return jsonify(data=data, status = 200)
        except Exception as e:
            print(e)
            return jsonify(data=[], status = 400)


@admin.route('/get_salary')
@login_required
def get_salary():
    year = request.args.get('year')
    month = request.args.get('month')
    user_id = request.args.get('emp_id')

    salary = Salary.query.filter(Salary.year == year,
                            Salary.month == month,
                            Salary.user_id == user_id).first()
    if salary is None:
        return jsonify(message="Don't have log salary in time query"), 400

    logs = Log.query.filter(extract('year', Log.date) == year,
                            extract('month', Log.date) == month,
                            Log.user_id == user_id).all()
    num_in_late = 0
    num_out_early = 0
    for log in logs:
        if log.tag_in == 2:
            num_in_late += 1
        if log.tag_out == 2:
            num_out_early += 1

    return jsonify(salary= salary.salary, num_log = len(logs), num_in_late = num_in_late, num_out_early = num_out_early), 200

@admin.route('/get_hard_salaries')
@login_required
def get_hard_salaries():
    if current_user.is_admin == True:
        users = User.query.filter(User.is_admin == False).all()
        return render_template('admin/hard-salary.html', data= users)
    abort(401)


@admin.route('/search_hard_salary', methods=['POST'])
@login_required
def search_hard_salary():
    q = '%' + request.form['name'] + '%'
    users = User.query.filter(or_(User.name.like(q), User.id.like(q)), User.is_admin == False).all()

    data = []
    for u in users:
        user = dict()
        user['id'] = u.id
        user['name'] = u.name
        user['avatar'] = u.avatar
        user['mail'] = u.mail
        user['salary'] = "{:,}".format(u.salary)

        data.append(user)

    return jsonify(data=data, status = 200)


@admin.route('/get_hard_salary', methods=['POST'])
@login_required
def get_hard_salary():
    try:
        id = request.form['user_id']
        new_salary = request.form['new_salary']

        user = User.query.filter(User.id == id).first()
        user.salary = new_salary
        db.session.commit()

        users = User.query.filter(User.is_admin == False).all()
        data = []
        for u in users:
            user = dict()
            user['id'] = u.id
            user['name'] = u.name
            user['avatar'] = u.avatar
            user['mail'] = u.mail
            user['salary'] = "{:,}".format(u.salary)

            data.append(user)

        return jsonify(data=data,message="Cập nhật lương thành công", status=200)
    except Exception as e:
        print(e)
        return jsonify(message="Cập nhật lương không thành công", status=400)



@admin.route('/cal_salary')
@login_required
def cal_salary():
    if current_user.is_admin == True:
        today = datetime.today()
        first = today.replace(day=1)
        lastMonth = first - timedelta(days=1)

        month = int(lastMonth.strftime("%m"))
        year = int(lastMonth.strftime("%Y"))

        sal = Salary.query.filter(Salary.year == year, Salary.month == month).first()
        if sal != None:
            # return jsonify(message= "calculated salary") , 400
            return redirect(url_for('admin.get_salaries', month=month, year=year))
        data = dict()
        for user, log in db.session.query(User, Log).filter(User.id == Log.user_id,
                                                               extract('year', Log.date) == year,
                                                               extract('month', Log.date) == month,
                                                               ).order_by(User.id.asc()).all():
            if user.id not in data:
                data[user.id] = {'num_log' : 0, 'in_late' : 0, 'out_early': 0, 'hard_sal' : user.salary, 'sal' : 0}


            if log.tag_in == 2:
                data[user.id]['in_late'] += 1
                data[user.id]['num_log'] += 0.5
            elif log.tag_in == 1:
                data[user.id]['num_log'] += 0.5
            # else:
            #     data[user.id]['num_log'] += 0.5

            if log.tag_out == 2:
                data[user.id]['out_early'] += 1
                data[user.id]['num_log'] += 0.5
            elif log.tag_out == 1:
                data[user.id]['num_log'] += 0.5
            # else:
            #     data[user.id]['num_log'] += 0.5

        # phat 50k di muon ve som, khong co log nua ngay tru nua ngay cong
        for user in data:
            data[user]['sal'] = ((data[user]['hard_sal']//22 * data[user]['num_log']- 50000 *  (data[user]['in_late']  + data[user]['out_early'])) // 1000 * 1000)
            db.session.add(Salary(user_id=user, salary=data[user]['sal'], year=year,
                                  month=month, num_log=data[user]['num_log'],
                                  in_late=data[user]['in_late'],
                                  out_early = data[user]['out_early']))

        db.session.commit()

        # return jsonify(message= 'success'), 200
        return redirect(url_for('admin.get_salaries', month=month, year=year))
    abort(401)



