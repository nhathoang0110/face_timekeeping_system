from flask import render_template, abort, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from datetime import datetime

from . import profile
from ...models import User


@profile.route('/update_password', methods=['GET'])
@login_required
def update_password():
    return render_template('profile/update_password.html')


@profile.route('/update_password', methods=['POST'])
@login_required
def update_password_post():
    try:
        curr_pass = request.form['current_password']
        new_pass = request.form['new_password']
        re_new_pass = request.form['re_enter_new_password']

        user = User.query.filter_by(id=current_user.id).first()

        if not current_user.verify_password(curr_pass):
            return jsonify(message = 'Mật khẩu không đúng', status = 400)
        elif new_pass != re_new_pass:
            return jsonify(message = 'Mật khẩu mới không trùng khớp' ,status = 400)

        current_user.set_password(new_pass)
        db.session.commit()

        return jsonify(message =  'Cập nhật mật khẩu thành công' ,status = 200) , 200
    except Exception as e:
        print(e)
        return jsonify(message = 'Cập nhật không thành công', status = 400)



@profile.route('/update_profile', methods=['GET'])
@login_required
def update_profile():
    return render_template('profile/update_profile.html')

@profile.route('/update_profile', methods=['POST'])
@login_required
def update_profile_post():
    try:
        current_user.name = request.form['name']
        current_user.phone = request.form['phone']
        current_user.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%d/%m/%Y')

        db.session.commit()

        return jsonify(message = 'Cập nhật thành công', status = 200), 200
    except Exception as e:
        print(e)
        return jsonify(message = 'Cập nhật thất bại', status = 400)


@profile.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile/profile.html')