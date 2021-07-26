# app/__init__.py

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
#
socketio = SocketIO()
# local imports

# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    Bootstrap(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "app.modules.auth.login"
    # migrate = Migrate(app, db)

    from app import models

    # from .admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from app.modules.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.modules.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from app.modules.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    from app.modules.employee import employee as employee_blueprint
    app.register_blueprint(employee_blueprint)

    from app.modules.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from app.modules.chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)

    socketio.init_app(app)


    return app
