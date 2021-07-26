from flask import session, redirect, url_for, render_template, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from . import chat
from app.models import *



@chat.route('/chat_view', methods=['POST'])
@login_required
def chat_view():
    conver_id = request.form['conver_id']
    messages = Message.query.filter(Message.conversation_id == conver_id).order_by(Message.time_create.asc()).all()
    mess_arr = []
    for mess in messages:
        tmp = dict()
        tmp['sender_id'] = mess.sender_id
        tmp['conversation_id'] = mess.conversation_id
        tmp['content'] = mess.content
        tmp['time_create'] = mess.time_create.strftime('%H:%M , %d/%m')

        mess_arr.append(tmp)

    user = User.query.filter(User.id == conver_id).first()
    data = dict()
    data['id'] = user.id
    data['avatar'] = user.avatar
    data['name'] = user.name

    return jsonify(messages=mess_arr , current_user_id = current_user.id, status = 200, receiver=data)


@chat.route('/chat')
@login_required
def chat():
    if current_user.is_admin == True:
        messages = None
        users = User.query.filter(User.is_admin == False).all()
        if len(users) > 0:
            messages = Message.query.filter(Message.conversation_id == users[0].id).order_by(Message.time_create.asc()).all()
            return render_template('chat/chat.html', users=users, messages=messages, current_user_id=current_user.id,
                                   has_user = True)

        return render_template('chat/chat.html', has_user = False)
    else:
        messages = Message.query.filter(Message.conversation_id == current_user.id).order_by(Message.time_create.asc()).all()
        user = User.query.filter(User.is_admin == True).first()
        print(user)
        return render_template('chat/chat_emp.html', messages= messages, admin=user)







