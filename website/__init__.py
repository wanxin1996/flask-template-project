# make the "website" folder a python package
# whenever import this package, all the things in the folder will run automatically

from sys import prefix
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '90557568pP!'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # register the views
    from .views import views
    from .auth import auth
    app.register_blueprint(views, prefix='/')
    app.register_blueprint(auth, prefix='/')

    from .models import User, Note

    # where user will be directed if they are not logged in
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)

    return app

# check if data base is already exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database created.')