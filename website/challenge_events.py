from flask import Blueprint, request
from flask_socketio import emit, send
from . import socketio
from flask_login import login_user, login_required, logout_user, current_user

challenge_events = Blueprint("challenge_events", __name__)
users = []

@socketio.on('connect')
@login_required
def new_user(data):
    try:
        name = current_user.name
        emit('user_connected', name, broadcast=True)
    except AttributeError:
        print("se conectó un usuario anónimo")

@socketio.on('challenge')
def challenge (challenger, challenged):
    print(f'{challenger} está retando a {challenged}')
    emit('challenged', (challenger, challenged), broadcast=True)
     # send('challenged')

@socketio.on('redirect')
def redirect(challenger, challenged, accepted):
    if accepted:
        emit('redirect', (challenger, challenged), broadcast=True)
    else:
        emit('denied', (challenger, challenged), broadcast=True)

@socketio.on('users')
def group_all_users(name):
    if not name in users:
        try:
            users.append(current_user.name)
        except:
            print("no se pudo añadir usuario actual a usuarios")    

    emit('connected_users', users)

@socketio.on('disconnect')
def delete_user():
    try:
        name = current_user.name 
        users.remove(name)
        emit('user_disconnected', name, broadcast = True)
    except:
        print("se desconectó un usuario no registrado...")