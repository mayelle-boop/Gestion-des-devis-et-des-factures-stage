from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = 'client'
    id_client = db.Column(db.String(15), primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50))
    adresse = db.Column(db.String(200))

    devis = db.relationship('Devis', backref='client', lazy=True)


class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    id_utilisateur = db.Column(db.String(20), primary_key=True)
    nom_utilisateur = db.Column(db.String(200), nullable=False)
    prenom_utilisateur = db.Column(db.String(200), nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin / gestionnaire / commercial / employe

    devis = db.relationship('Devis', backref='utilisateur', lazy=True)


class Service(db.Model):
    __tablename__ = 'service'
    id_service = db.Column(db.String(10), primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    prix_unitaire_ser = db.Column(db.Float, nullable=False)
    unite = db.Column(db.String(20))
    type = db.Column(db.String(30), nullable=False)

    lignes = db.relationship('LigneDevis', backref='service', lazy=True)


class Devis(db.Model):
    __tablename__ = 'devis'
    numero_devis = db.Column(db.String(12), primary_key=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_validation = db.Column(db.Date)
    statut = db.Column(db.String(20), default='brouillon')

    id_client = db.Column(db.String(15), db.ForeignKey('client.id_client'), nullable=False)
    id_utilisateur = db.Column(db.String(20), db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)

    lignes = db.relationship(
        'LigneDevis', backref='devis',
        cascade='all, delete-orphan', lazy=True
    )
    facture = db.relationship(
        'Facture', backref='devis',
        uselist=False, lazy=True          # relation 1-1 : 0,1 <-> 1,1
    )

    def montant_total(self):
        return sum(l.quantite * l.prix_unitaire for l in self.lignes)


class LigneDevis(db.Model):
    __tablename__ = 'ligne_devis'
    id_ligne = db.Column(db.String(16), primary_key=True)
    designation = db.Column(db.String(50))
    quantite = db.Column(db.Float, nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)

    numero_devis = db.Column(db.String(12), db.ForeignKey('devis.numero_devis'), nullable=False)
    id_service = db.Column(db.String(10), db.ForeignKey('service.id_service'), nullable=False)

    def sous_total(self):
        return self.quantite * self.prix_unitaire


class Facture(db.Model):
    __tablename__ = 'facture'
    numero_facture = db.Column(db.String(15), primary_key=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.DateTime)
    statut = db.Column(db.String(20), default='impayee')

    numero_devis = db.Column(
        db.String(12), db.ForeignKey('devis.numero_devis'),
        nullable=False, unique=True        # garantit le 1-1
    )

    paiements = db.relationship('Paiement', backref='facture', lazy=True)


class Paiement(db.Model):
    __tablename__ = 'paiement'
    code_paiement = db.Column(db.String(30), primary_key=True)
    date_paiement = db.Column(db.DateTime, default=datetime.utcnow)
    montant = db.Column(db.Float, nullable=False)
    mode_paiement = db.Column(db.String(20), nullable=False)

    numero_facture = db.Column(db.String(15), db.ForeignKey('facture.numero_facture'), nullable=False)