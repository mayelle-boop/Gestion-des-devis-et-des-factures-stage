from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from config import Config



db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
   
    DevisFacts = Flask(__name__, static_folder='static', template_folder='templates', instance_relative_config=True)
    DevisFacts.config.from_object(Config)
    db.init_app(DevisFacts)
    bcrypt.init_app(DevisFacts)

    from .Auth.Auth_routes import auth_bp
    from .Dashboard.Dashboard_routes import dashboard_bp
    from .main.Main_routes import main_bp
    from .Devis.routes import devis_bp
    DevisFacts.register_blueprint(auth_bp)
    DevisFacts.register_blueprint(dashboard_bp)
    DevisFacts.register_blueprint(main_bp)
    DevisFacts.register_blueprint(devis_bp)
    
    

    return DevisFacts






