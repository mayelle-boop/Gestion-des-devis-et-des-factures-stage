from tempfile import template
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config

dashboard_bp = Blueprint('Dashboard_routes', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'id_utilisateur' not in session:
        flash("Veuillez vous connecter.", "error")
        return redirect(url_for('Auth_routes.login'))

    nb_clients = 0          # on branchera le vrai calcul avec le modèle Client bientôt
    nb_devis_attente = 0    # idem avec Devis
    nb_factures_mois = 0    # idem avec Facture

    return render_template(
        'dashboard.html',
        active_page='dashboard',
        nb_clients=nb_clients,
        nb_devis_attente=nb_devis_attente,
        nb_factures_mois=nb_factures_mois
    )
