from tempfile import template
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from DevisFact.models import Utilisateur
from werkzeug.security import check_password_hash




auth_bp = Blueprint('Auth_routes', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        mot_de_passe = request.form.get('password')

        utilisateur = Utilisateur.query.filter_by(email=email).first()

    
        if utilisateur and check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
        
            session['id_utilisateur'] = utilisateur.id_utilisateur
            session['nom'] = utilisateur.nom
            session['role'] = utilisateur.role

            flash(f"Bienvenue {utilisateur.nom} !", "success")
            return redirect(url_for('Main_routes.firstpage'))  # ta future page d'accueil connectée

        else:
            flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for('Auth_routes.login'))
    return render_template('login.html')




@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Vous avez été déconnecté(e).", "success")
    return redirect(url_for('Auth_routes.login'))

