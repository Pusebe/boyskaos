from flask import Blueprint, request
from flask_socketio import emit, send
from . import socketio, db
from .models import User, Card, Connection
from sqlalchemy import select, and_, text, String
from flask_login import login_user, login_required, logout_user, current_user
import random

battle_events = Blueprint("battle_events", __name__)

fighters = []
players_ready = []

@socketio.on('batalla')
def batalla(user):
    if user not in fighters:
       fighters.append(user)  
    if (len(fighters) == 2): 
        emit('batalla', fighters, broadcast=True)
        fighters.clear()

@socketio.on('confirm')
def confirm(player):
    chances = ['speed', 'attack', 'intelligence','defense']
    dice = random.choice(chances)

    if player not in players_ready:
        players_ready.append(player)
    
    if (len(players_ready) == 2):
        player1 = players_ready[0]
        player2 = players_ready[1]

        player1_value = eval(f"User.query.filter_by(name = '{player1}').first().cards[0].{dice}")
        player2_value = eval(f"User.query.filter_by(name = '{player2}').first().cards[0].{dice}")
        
        if player1_value > player2_value:      
            emit('winner', (player1, dice), broadcast=True)
        else:
            emit('winner', (player2, dice), broadcast=True)
        players_ready.clear()

  

# @socketio.on('challenge')
# def challenge (challenger, challenged):

#     emit('challenged', (challenger, challenged), broadcast=True)
#      # send('challenged')

# @socketio.on('redirect')
# def redirect(challenger, challenged, accepted):
#     if accepted:
#         emit('redirect', (challenger, challenged), broadcast=True)
#     else:
#         emit('denied', (challenger, challenged), broadcast=True)

# @socketio.on('users')
# def group_all_users(name):

#     if not name in users:
#         users.append(name)

#     emit('connected_users', users)

# @socketio.on('disconnect')
# def delete_user():
#     name = current_user.name 
#     users.remove(name)
#     emit('user_disconnected', name, broadcast = True)