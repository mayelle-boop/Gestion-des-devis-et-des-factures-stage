from tempfile import template

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from DevisFact.models import db

db = SQLAlchemy()


def create_app():
    DevisFact = Flask(__name__, static_folder='static', template_folder='templates', instance_relative_config=True)
    DevisFact.config.from_object(Config)
    db.init_app(DevisFact)
    @DevisFact.route('/')
    def accueil():
        return render_template("landingPage2.html")
    return DevisFact





