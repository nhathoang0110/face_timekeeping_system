import json

from flask import session
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from ... import socketio
from app.models import *
from datetime import datetime


@socketio.on('joined', namespace='/chat1')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    # room = session.get('room')
    # join_room(room)
    # emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
    if current_user.is_admin == True:
        for user in User.query.filter(User.is_admin == False):
            join_room(user.id)
    else:
        join_room(current_user.id)
    print("Joined!!!!!!!!!")

@socketio.on('text', namespace='/chat1')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""

    print(message)
    if current_user.is_admin == True:
        room = message['conver_id']
    else:
        room = current_user.id

    print(room)
    emit('message', {'msg' : message['msg'], 'sender_name': current_user.name, 'conver_id' : room,
                     'sender_avatar' : current_user.avatar, 'time': datetime.now().strftime("%H:%M , %d/%m")}, include_self = False, room=room)

    try:
        mess = Message(sender_id = current_user.id, content=message['msg'], time_create=datetime.now(), conversation_id=room)
        db.session.add(mess)
        db.session.commit()
    except:
        pass


@socketio.on('left', namespace='/chat1')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

