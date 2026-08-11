from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 


db = SQLAlchemy()


class Client (db.model):
    __tablename__ = 'CLIENT'
    id_client = db.column(db.Integer, primary_key = True)
    nom = db.column(db.String(50), nullable = False)
    email = db.column(db.String(100), nullable = False)
    adresse =db.column(db.String(200), nullable = False)

    devis = db.relationship('devis', backref = 'client', lazy = True)
    payments = db.relationship('payment', backref = 'client', lazy = True)

    def __repr__(self):
        return f'<Client {self.nom}>'


class Utlisateur (db.model):
    __tablename__ = 'UTILISATEUR'
    id_utilisateur = db.column(db.Integer, primary_key = True)
    nom = db.column(db.String(50), nullable = False)
    email = db.column(db.String(100), nullable = False)
    mot_de_passe = db.column(db.String(100), nullable = False)
    role = db.column(
        db.Emun ('admin', 'commercial', 'gestionnaire', 'comptable', name = 'role_enum'),
        nullable = False,
    ) 
    devis = db.relationship('devis', backref = 'Utilisateur', lazy = True)


    def __repr__(self):
        return f'<Utilisateur {self.nom} {self.email} {self.role}>'



class Devis (db.model):
    __tablename__ = 'DEVIS'
    numero_devis = db.column(db.Varchar(12), primary_key = True)
    id_client = db.column(db.Integer, db.Foreignkey('CLIENT.id_client'), nullable = False)
    id_utilisateur = db.column(db.Integer, db.Foreignkey('UTILISATEUR.id_utilisateur'), nullable = False)
    date_creation = db.column(db.DateTime, nullable = False, default = datetime.utcnow)   
    date_validation = db.column(db.Date, nullable = True)
    statut = db.column(
        db.Enum('brouillon', 'envoyé', 'accepté', 'refusé', name = 'statut_enum'),
        nullable = False,
        default = 'brouillon'
    )
    LigneDevis = db.relationship('LigneDevis', backref = 'devis', cascade = "all, delete-orphan", lazy = True)
    facture = db.relationship('Facture', backref = 'devis', uselist = False, lazy = True)


    @property
    def total(self):
        return sum(LigneDevis.prix_unitaire * LigneDevis.quantite * (1 + LigneDevis.tva / 100) for LigneDevis in self.LigneDevis)

    def __repr__(self):
        return f'<Devis {self.numero_devis}>'


class LigneDevis (db.model):
    __tablename__ = 'LIGNEDEVIS'
    id_ligne_devis = db.column(db.Integer, primary_key = True)
    numero_devis = db.column(db.Varchar(12), db.Foreignkey('DEVIS.numero_devis'), nullable = False)
    designation = db.column(db.String(200), nullable = False)
    quantite = db.column(db.Integer, nullable = False)
    prix_unitaire = db.column(db.Float(3, 2), nullable = False)
    tva = db.column(db.Float(3,2), nullable = False)

    def __repr__(self):
        return f'<LigneDevis {self.designation} {self.quantite} {self.prix_unitaire} {self.tva}>'


class Facture (db.model):
    __tablename__ = 'FACTURE'
    numero_facture = db.column(db.Varchar(12), primary_key = True)
    numero_devis = db.column(db.Varchar(12), db.Foreignkey('DEVIS.numero_devis'), nullable = False)
    date_creation = db.column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_echeance = db.column(db.Date, nullable = False)
    statut_facture = db.column(
        db.Enum('impayée', 'partiellement_payée', 'payée', name = 'statut_facture_enum'),
        nullable = False,
        default = 'impayée'
    )    




class paiement (db.model):
    __tablename__ = 'PAIEMENT'
    code_paiement = db.column(db.Integer, primary_key = True)
    numero_facture = db.column(db.Varchar(12), db.Foreignkey('FACTURE.numero_facture'), nullable = False)
    date_paiement = db.column(db.DateTime, nullable = False, default = datetime.utcnow)
    mode_paiement = db.column(
        db.Enum('virement_bancaire', 'carte_bancaire', 'chèque', 'espèces', 'Money_money', 'Orange_money', name = 'mode_paiement_enum'),
        nullable = False
    )
    montant = db.column(db.Float(10, 2), nullable = False)


    def __repr__(self):
        return f'<Paiement {self.code_paiement}, {self.numero_facture}, {self.date_paiement}, {self.mode_paiement}, {self.montant}>'

