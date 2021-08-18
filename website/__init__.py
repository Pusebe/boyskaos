from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()

DB_NAME = "boyskaos.db"
UPLOAD_FOLDER = "website/static/uploads"
socketio = SocketIO()


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config["SECRET_KEY"] = os.environ.get('KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    socketio.init_app(app)

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .challenge_events import challenge_events
    from .battle_events import battle_events

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(challenge_events, url_prefix="/")
    app.register_blueprint(battle_events, url_prefix="/")

    from .models import User, Card, Connection

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = "Por favor inicia sesión para acceder a esta página."
    login_manager.login_message_category = "error"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
