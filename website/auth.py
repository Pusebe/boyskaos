from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)


@auth.route('login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f'¡Bienvenido de nuevo {user.name}!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrecto', category='error')
        else:
            flash('Comprueba tu usuario.', category='error')        
        
    return render_template('login.html', user=current_user)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(name=name).first()

        if user:
            flash('Usuario ya registrado', category='error')
        elif len(name) < 3:
            flash('El nombre tiene que tener al menos 3 caracteres', category='error')
        elif (password1 != password2):
            flash('El password no coincide', category='error')
        elif len(password1) < 4:
            flash('El password tiene que tener al menos 3 caracteres', category='error')

        else:
            new_user = User(name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(f'¡Bienvenido {name}, tu cuenta ha sido creada con éxito!', category='succes')
            return redirect(url_for('views.home'))
        
    return render_template('sign_up.html', user=current_user)
