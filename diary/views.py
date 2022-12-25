# Allows to store views (routes) without needing to now the complete final scope of the app
from flask import Blueprint, render_template
from diary.db import get_db

views = Blueprint('views', __name__)

@views.route("/", methods=['POST','GET'])
def index():
    # TODO: show calendar and allow to the user to click on individual days
    return render_template("home.html")

@views.route("/settings", methods=['POST','GET'])
def settings():
    # TODO: Allow user to create a list of emotion-color pairs
    return render_template("settings.html")