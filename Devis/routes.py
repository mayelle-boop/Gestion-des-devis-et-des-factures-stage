from flask import Blueprint, render_template, request, redirect, url_for, flash
from DevisFact.models import db, Devis, LigneDevis, Client
from datetime import datetime
import uuid

devis_bp = Blueprint('routes', __name__)


def generer_numero_devis():
    annee = datetime.now().year
    suffixe = uuid.uuid4().hex[:6].upper()
    return f"DEV-{annee}-{suffixe}"


@devis_bp.route('/devis/nouveau', methods=['GET', 'POST'])
def creer_devis():

    # --- GET : afficher le formulaire ---
    if request.method == 'GET':
        clients = Client.query.all()
        return render_template('devis.html', clients=clients)

    # --- POST : traiter la soumission ---

    # Étape 2 : le client est obligatoire
    id_client = request.form.get('id_client')
    if not id_client:
        flash("Impossible de créer le devis : veuillez sélectionner un client.", "error")
        return redirect(url_for('routes.creer_devis'))

    # Étape 3 : récupération des lignes
    designations = request.form.getlist('designation[]')
    quantites = request.form.getlist('quantite[]')
    prix_unitaires = request.form.getlist('prixUnitaire[]')

    if not designations:
        flash("Le devis doit contenir au moins une ligne.", "error")
        return redirect(url_for('routes.creer_devis'))

    # Récupération des autres champs du formulaire
    duree = request.form.get('duree')
    taux_tva = request.form.get('taux_tva')  # peut être vide
    conditions_reglement = request.form.get('conditions_reglement')
    pied_de_page = request.form.get('pied_de_page')

    # Étape 4 : génération du numéro de devis
    numero_devis = generer_numero_devis()

    # Étape 5 : création du Devis
    nouveau_devis = Devis(
        numero_devis=numero_devis,
        id_client=id_client,
        date_devis=datetime.now(),
        statut='brouillon',
        duree=int(duree) if duree else None,
        taux_tva=float(taux_tva) if taux_tva else None,  # vide = pas de TVA
        conditions_reglement=conditions_reglement,
        pied_de_page=pied_de_page
    )

    # Étape 6 : création des lignes liées
    for i in range(len(designations)):
        ligne = LigneDevis(
            id_ligne=str(uuid.uuid4())[:8],
            designation=designations[i],
            quantite=int(quantites[i]),
            prixUnitaire=float(prix_unitaires[i])
        )
        nouveau_devis.lignes.append(ligne)

    # Étape 7 : enregistrement
    db.session.add(nouveau_devis)
    db.session.commit()

    flash(f"Devis {numero_devis} créé avec succès.", "success")
    return redirect(url_for('routes.voir_devis', numero=numero_devis))



@devis_bp.route('/devis/afficher')
def afficher_devis(numero_devis):
    devis = Devis.query.get_or_404(numero_devis)
    client = Client.query.get(devis.id_client)
    lignes = LigneDevis.query.filter_by(id_devis=numero_devis).all()
    
    # Infos de ton entreprise - tu peux les mettre en dur ou en BDD
    entreprise = {
        "nom": "DevisFact SARL",
        "adresse": "Yaoundé, Bastos",
        "telephone": "+237 6 90 00 00 00",
        "email": "contact@devisfact.cm",
        "logo": "logo.png",  # le nom du fichier dans static/img/
        "nif": "P0123456789"
    }

    return render_template('display_devis.html', devis=devis, client=client, lignes=lignes, entreprise=entreprise)

@devis_bp.route('/devis/list')
def liste_devis():
    # 1. Récupère tous les devis de la BDD, du plus récent au plus ancien
    tous_les_devis = Devis.query.order_by(Devis.date_creation.desc()).all()
    
    # 2. Pour chaque devis, on récupère aussi le nom du client
    liste = []
    for devis in tous_les_devis:
        client = Client.query.get(devis.id_client)
        liste.append({
            'devis': devis,
            'client_nom': client.nom if client else "Client supprimé"
        })

    return render_template('list_devis.html', liste_devis=liste)