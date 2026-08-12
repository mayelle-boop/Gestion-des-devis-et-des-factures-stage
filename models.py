from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 


db = SQLAlchemy()


class Client (db.Model):
    __tablename__ = 'CLIENT'
    id_client = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    adresse =db.Column(db.String(200), nullable = False)

    devis = db.relationship('devis', backref = 'client', lazy = True)
    payments = db.relationship('payment', backref = 'client', lazy = True)

    def __repr__(self):
        return f'<Client {self.nom}>'


class Utlisateur (db.Model):
    __tablename__ = 'UTILISATEUR'
    id_utilisateur = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    mot_de_passe = db.Column(db.String(100), nullable = False)
    role = db.Column(
        db.Enum('admin', 'commercial', 'gestionnaire', 'comptable', name = 'role_enum'),
        nullable = False,
    ) 
    devis = db.relationship('devis', backref = 'Utilisateur', lazy = True)


    def __repr__(self):
        return f'<Utilisateur {self.nom} {self.email} {self.role}>'



class Devis (db.Model):
    __tablename__ = 'DEVIS'
    numero_devis = db.Column(db.String(12), primary_key = True)
    id_client = db.Column(db.Integer, db.ForeignKey('CLIENT.id_client'), nullable = False)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('UTILISATEUR.id_utilisateur'), nullable = False)
    date_creation = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)   
    date_validation = db.Column(db.Date, nullable = True)
    statut = db.Column(
        db.Enum('brouillon', 'envoyé', 'accepté', 'refusé', name = 'statut_enum'),
        nullable = False,
        default = 'brouillon'
    )
    LigneDevis = db.relationship('LigneDevis', backref = 'devis', cascade = "all, delete-orphan", lazy = True)
    facture = db.relationship('Facture', backref = 'devis', uselist = False, lazy = True)



    def __repr__(self):
        return f'<Devis {self.numero_devis}>'


class LigneDevis (db.Model):
    __tablename__ = 'LIGNEDEVIS'
    id_ligne_devis = db.Column(db.Integer, primary_key = True)
    numero_devis = db.Column(db.String(12), db.ForeignKey('DEVIS.numero_devis'), nullable = False)
    designation = db.Column(db.String(200), nullable = False)
    quantite = db.Column(db.Integer, nullable = False)
    prix_unitaire = db.Column(db.Float(3, 2), nullable = False)
    taux_tva = db.Column(db.Float(3,2), nullable = True, default = 20.0)



    @property
    def total_HT(self):
        return self.prix_unitaire * self.quantite

    @property
    def montant_TVA(self):
        if self.taux_tva is None:
            return 0.0
        return self.total_HT * (self.taux_tva / 100)

    @property
    def total_TTC(self):
        return self.total_HT + self.montant_TVA

    def __repr__(self):

        return f'<LigneDevis {self.designation} {self.quantite} {self.prix_unitaire} {self.taux_tva}>'

class Facture (db.Model):
    __tablename__ = 'FACTURE'
    numero_facture = db.Column(db.String(12), primary_key = True)
    numero_devis = db.Column(db.String(12), db.ForeignKey('DEVIS.numero_devis'), nullable = False)
    date_creation = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_echeance = db.Column(db.Date, nullable = False)
    statut_facture = db.Column(
        db.Enum('impayée', 'partiellement_payée', 'payée', name = 'statut_facture_enum'),
        nullable = False,
        default = 'impayée'
    )    




class paiement (db.Model):
    __tablename__ = 'PAIEMENT'
    code_paiement = db.Column(db.Integer, primary_key = True)
    numero_facture = db.Column(db.String(12), db.ForeignKey('FACTURE.numero_facture'), nullable = False)
    date_paiement = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    mode_paiement = db.Column(
        db.Enum('virement_bancaire', 'carte_bancaire', 'chèque', 'espèces', 'Money_money', 'Orange_money', name = 'mode_paiement_enum'),
        nullable = False
    )
    montant = db.Column(db.Float(10, 2), nullable = False)


    def __repr__(self):
        return f'<Paiement {self.code_paiement}, {self.numero_facture}, {self.date_paiement}, {self.mode_paiement}, {self.montant}>'

