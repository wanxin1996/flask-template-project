# store the views and URLs for the endpoints

# Blueprint allow separation of the views so that to be organised
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")