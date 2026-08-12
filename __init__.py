from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from DevisFact.models import db

db = SQLAlchemy()

def create_app():
    DevisFact = Flask(__name__)
    DevisFact.config.from_object(Config)
    db.init_app(DevisFact)
    @DevisFact.route('/')
    def accueil():
        return "L'application fonctionne ! 🚀"
    return DevisFact





