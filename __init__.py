from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from DevisFact.models import db

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(DevisFact)
    @app.route('/')
    def accueil():
        return "L'application fonctionne ! 🚀"
    return DevisFact





