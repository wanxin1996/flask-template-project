# make the "website" folder a python package
# whenever import this package, all the things in the folder will run automatically

from sys import prefix
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '90557568pP!'

    # register the views
    from .views import views
    from .auth import auth
    app.register_blueprint(views, prefix='/')
    app.register_blueprint(auth, prefix='/')

    return app