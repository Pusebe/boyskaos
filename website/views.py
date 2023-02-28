import os
import re
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import redirect, secure_filename
from .models import User, Card, Connection
from . import *
from .num_generator import id_generator
import json

views = Blueprint('views', __name__)


@views.route('/')
def home():
    ip = request.environ['REMOTE_ADDR']
    if Connection.query.filter_by(ip=ip).first():
        pass
    else:
        new_connection = Connection(ip=ip)
        db.session.add(new_connection)
        db.session.commit()

    cards = db.session.query(Card)

    return render_template('home.html', user=current_user, cards=cards)


@views.route('create-card', methods=["GET", "POST"])
@login_required
def create_card():
    if request.method == "POST":
        name = request.form.get('name')

        card = Card.query.filter_by(name=name).first()

        if card:
            flash('Ya existe una carta con ese nombre', category='error')
            return redirect('create-card')

        attack = request.form.get('attack')
        defense = request.form.get('defense')
        intelligence = request.form.get('intelligence')
        speed = request.form.get('speed')

        try:
            total = abs(int(attack)) + abs(int(defense)) + \
                abs(int(intelligence)) + abs(int(speed))
        except ValueError as e:
            print(
                f'Algún campo está vacío, si está vacío tiene que poner al menos 0, {e}')
            flash("Dejaste algún campo vacío, recuerda que la puntuación mínima de una habilidad es 0", category='error')
            return redirect('create-card')

        if total > 400:
            flash(
                'Recuerda... máximo 400 puntos en total. No se permiten números negativos', category='error')
            return redirect('create-card')

        img = request.files['img']

        imgname = (id_generator() + img.filename).replace(' ', '')

        imgsecure = secure_filename(imgname)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        img.save(os.path.join(UPLOAD_FOLDER, imgsecure))

        new_card = Card(name=name, attack=attack, img=imgname,
                        defense=defense, intelligence=intelligence, speed=speed, user_id=current_user.id)
        try:
            db.session.add(new_card)
            db.session.commit()
        except:
            flash('Vaya... algo ha salido mal, asegurate de rellenar todos los campos y subir una foto.', category='error')
            return redirect('create-card')
        flash('Carta creada con éxito', category='succes')
        return redirect('/')

    return render_template('create_card.html', user=current_user)


@views.route('my-cards')
@login_required
def my_cards():
    return render_template('my_cards.html', user=current_user)


@views.route('delete-card', methods=["POST"])
@login_required
def delete_card():
    card = json.loads(request.data)
    cardId = card["card"]
    card = Card.query.get(cardId)

    if card.user.id == current_user.id or current_user.name == "Tenal":
        db.session.delete(card)
        db.session.commit()
        os.remove(f'{UPLOAD_FOLDER}/{card.img}')
        flash("Tu carta ha sido eliminada del servidor", category='sucess')
    else:
        flash("O no eres admin o esta carta no te pertenece", category='error')

    return jsonify({})


@views.route('challenges')
@login_required
def challenges():
    return render_template('challenges.html', user=current_user)


@views.route('admin')
@login_required
def control_panel():
    return render_template('admin.html', user=current_user)


@views.route('battle/<challenger>/<challenged>')
@login_required
def battle(challenger, challenged):

    player1 = User.query.filter_by(name=challenger).first()
    player2 = User.query.filter_by(name=challenged).first()

    print(player1, player2)
    if len(player1.cards) == 0 or len(player2.cards) == 0:
        flash('Vaya! parece que alguno de los dos no tiene cartas', category='error')
        return redirect('/')

    return render_template('battle.html', user=current_user, player1=player1, player2=player2)


@views.route('admin-delete-cards/', methods=['POST', 'GET'])
@views.route('admin-delete-cards/<user>', methods=['POST', 'GET'])
@login_required
def admin_delete_cards(user=None):
    if current_user.admin or current_user.name == 'Tenal':
        if request.method == 'GET' and user == None:
            cards = Card.query.all()
            users = User.query.all()
            return render_template('admin_delete_cards.html', user=current_user, users=users, cards=cards)
        else:
            print("entra aki")
            user = user
            new_admin = User.query.filter_by(name=user).first()
            if new_admin.admin:
                new_admin.admin = False
            else:
                new_admin.admin = True
            db.session.commit()
            return redirect('/admin-delete-cards')
            # new_admin = request.form.get('')

    flash("No eres admin, no puedes acceder aquí", category='error')
    return redirect('/')
