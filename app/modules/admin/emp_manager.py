import json
import shutil
import time
from datetime import datetime
from flask import render_template, abort, session, request, jsonify, flash, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sqlalchemy import extract, or_
from werkzeug.utils import redirect
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app import db
from app.models import *
from . import admin
from flask_paginate import Pagination, get_page_args
import os
from FACE_RECOGNITION.make_gallery import make_gallery
from run import PATH_TO_MODULE_RECOGNITION, PATH_IMAGE_RECOGNITION

cwd = os.getcwd()


# PATH_TO_MODULE_RECOGNITION = '../../FACE_RECOGNITION/'

@admin.route('/register', methods=['GET'])
@login_required
def register():
    return render_template('auth/register.html')



@admin.route('/register', methods=['POST'])
# @login_required
def register_post():
    try:

        datetime_object = datetime.strptime(request.form['date_of_birth'], '%d/%m/%Y')
        has_user = User.query.filter(User.mail == request.form['mail']).first()
        if has_user != None:
            time.sleep(1)
            return jsonify(message='Email đã tồn tại', status=400)

        user = User(name= request.form['name'],
                    mail= request.form['mail'],
                    phone= request.form['phone'],
                    date_of_birth=datetime_object,
                    salary = request.form['salary'],
                    avatar = 'img/avatar/user.jpg',
                    is_admin = False)
        user.set_password('1')

        db.session.add(user)
        db.session.commit()

        file1 = request.files['file1']
        file2 = request.files['file2']
        file3 = request.files['file3']
        # file1.save(os.path.join(cwd + path_match_img, str(user.id) + '_1.' +(file1.filename).split('.')[-1]))
        # file2.save(os.path.join(cwd + path_match_img, str(user.id) + '_2.' +(file2.filename).split('.')[-1]))
        # file3.save(os.path.join(cwd + path_match_img, str(user.id) + '_3.' +(file3.filename).split('.')[-1]))

        folder_to_saved = PATH_IMAGE_RECOGNITION + 'data_nvup/' + str(user.id)
        os.mkdir(folder_to_saved)
        # print('folder_to_saved: ', folder_to_saved)

        file1.save(os.path.join(folder_to_saved, str(user.id) + '_1.' +(file1.filename).split('.')[-1]))
        file2.save(os.path.join(folder_to_saved, str(user.id) + '_2.' +(file2.filename).split('.')[-1]))
        file3.save(os.path.join(folder_to_saved, str(user.id) + '_3.' +(file3.filename).split('.')[-1]))

        create_vector(user.id)


        return jsonify(message= 'Đăng ký thành công', status = 200)
    except:
        time.sleep(1)
        return jsonify(message= 'Đăng ký thất bại', status = 400)


def create_vector(id):
    path_detection= PATH_TO_MODULE_RECOGNITION + "model_detection_2021/face-detection-0204.xml"
    path_vectori= PATH_TO_MODULE_RECOGNITION + "model_vectori/face_v2_16.xml"
    folder_nhanvienup= PATH_IMAGE_RECOGNITION + "data_nvup/"
    folder_database= PATH_TO_MODULE_RECOGNITION + "database/"  # chua images va vectors
    name= str(id)
    make_gallery(name,path_vectori,path_detection,folder_nhanvienup,folder_database)

    

# api
@admin.route('/search', methods=["POST"])
@login_required
def search():
    if current_user.is_admin == True:
        q = '%' + request.form['name'] +'%'
        users = User.query.filter(or_(User.name.like(q), User.id.like(q)), User.is_admin == False).all()

        data = []
        for u in users:
            user = dict()
            user['id'] = u.id
            user['name'] = u.name
            user['avatar'] = u.avatar
            user['phone'] = u.phone
            user['mail'] = u.mail
            user['date_of_birth'] = u.date_of_birth.strftime('%Y-%m-%d')

            data.append(user)

        # return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4) , 200
        return jsonify(data= data), 200

    abort(401)





@admin.route('/get_all_emp')
@login_required
def get_all_emp():
    if current_user.is_admin == True:
        # page, per_page, offset = get_page_args()
        page = int(request.args.get('page', 1))
        per_page = 10
        offset = (page - 1) * per_page

        users = User.query.filter(User.is_admin == 0).all()
        total = len(users)
        # pagination_users = get_users(offset=offset, per_page=per_page)
        # pagination_users = users[offset: offset + per_page]
        # pagination = Pagination(page=page, per_page=per_page, total=total,
        #                         css_framework='bootstrap4')
        return render_template('admin/list_employee.html',
                               users=users,
                               page=page,
                               per_page=per_page,
                               # pagination=pagination,
                               name=current_user.name
                               )
    abort(401)


@admin.route('/get_emp')
@login_required
def get_emp():
    if current_user.is_admin == True:
        user_id = int(request.args.get('emp_id'))
        user = User.query.filter(User.id == user_id, User.is_admin == False).first()

        d_user = dict()

        d_user['id'] = user.id
        d_user['name'] = user.name
        d_user['mail'] = user.mail
        d_user['phone'] = user.phone
        d_user['date_of_birth'] = user.date_of_birth
        d_user['avatar'] = user.avatar


        return render_template('admin/edit-employee.html', user= d_user, admin=current_user.name)

    abort(401)


#api
@admin.route('/update_emp', methods=['GET'])
@login_required
def update_emp():
    if current_user.is_admin == True:
        id = int(request.args.get('id'))
        user = User.query.filter(User.id == id).first()
        return render_template('admin/edit-employee.html', user = user)

    abort(401)


@admin.route('/update_emp', methods=['PUT'])
@login_required
def update_emp_put():
    if current_user.is_admin == True:
        try:
            id = request.form['id']
            user = User.query.filter(User.id == id).first()
            user.name = request.form['name']
            user.phone = request.form['phone']
            user.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%d/%m/%Y')

            db.session.commit()

            return jsonify(message='Cập nhật thành công', status = 200), 200
        except Exception as e:
            print(e)
            return jsonify(message='Cập nhật thất bại', status = 400)

    abort(401)

#api
@admin.route('/delete_emp', methods=['DELETE'])
@login_required
def delete_emp_del():
    if current_user.is_admin == True:
        try:
            user_id = request.form['user_id']
            user = User.query.filter(User.id == user_id, User.is_admin == False).first()
            if user == None:
                return jsonify(message='Không tồn tại nhân viên này', status=400)

            # for log in Log.query.filter(Log.user_id == user_id).all():
            #     db.session.delete(log)
            #
            # for sal in Salary.query.filter(Salary.user_id == user_id).all():
            #     db.session.delete(sal)
            #
            # for mess in Message.query.filter(Message.conversation_id == user_id).all():
            #     db.session.delele(mess)
            #
            # db.session.delete(user)
            Log.query.filter(Log.user_id == user_id).delete()
            Salary.query.filter(Salary.user_id == user_id).delete()
            Message.query.filter(Message.conversation_id == user_id).delete()
            User.query.filter(User.id == user_id, User.is_admin == False).delete()

            db.session.commit()
            try:
                shutil.rmtree(PATH_IMAGE_RECOGNITION + 'data_nvup/' + str(user_id), ignore_errors=True)
                shutil.rmtree(PATH_TO_MODULE_RECOGNITION + 'database/images/' + str(user_id), ignore_errors=True)
                os.remove(PATH_TO_MODULE_RECOGNITION + 'database/vectors/' + str(user_id) + '.txt')
                # if os.path.exists(PATH_TO_MODULE_RECOGNITION + 'database/images/' + str(user_id)):
                #     os.remove(PATH_TO_MODULE_RECOGNITION + 'database/images/' + str(user_id))

                # if os.path.exists(PATH_TO_MODULE_RECOGNITION + 'database/vectors/' + str(user_id) + '.txt'):
                #     os.remove(PATH_TO_MODULE_RECOGNITION + 'database/vectors/' + str(user_id) + '.txt')

                # if os.path.exists(PATH_IMAGE_RECOGNITION + 'data_nvup/' + str(user_id)):
                #     os.remove(PATH_IMAGE_RECOGNITION + 'data_nvup/' + str(user_id))
                    
            except Exception as e:
                print(e)

            users = User.query.filter(User.id != user_id, User.is_admin ==False).all()
            data = []
            for u in users:
                user = dict()
                user['id'] = u.id
                user['name'] = u.name
                user['avatar'] = u.avatar
                user['phone'] = u.phone
                user['mail'] = u.mail
                user['date_of_birth'] = u.date_of_birth.strftime('%Y-%m-%d')

                data.append(user)


            return jsonify(message='Xóa thành công', data=data,status=200)
        except Exception as e:
            print(e)
            return jsonify(message='Xóa không thành công', status =400)

    abort(401)

@admin.route("/get_images", methods=['POST'])
def get_images():
    user_id = request.form['user_id']
    root = PATH_IMAGE_RECOGNITION + 'data_nvup/' + str(user_id)
    print(root)
    paths = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            print(os.path.join(path, name))
            paths.append(os.path.join(path, name)[3:])

    return jsonify(paths = paths)


@admin.route("/get_imagesss")
def get_imagesss():
    return render_template('admin/list-image.html')