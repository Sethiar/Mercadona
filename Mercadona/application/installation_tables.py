from app import app
from models import db
from flask_login import UserMixin
from models.client import Client

with app.app_context():

    # Modèle pour la table administrateur.
    class Admin(db.Model, UserMixin):

        # Nom de la table dans la base de données.
        __tablename__ = "admin"

        # Cette ligne permet de recréer la table si désinstallation complète sans message d'erreur de SQLalchemy.
        __table_args__ = {"extend_existing": True}

        # Identifiant unique de l'admin.
        id = db.Column(db.Integer, primary_key=True)

        # Définition d'un rôle pour l'administrateur.
        role = db.Column(db.String(20), nullable=False)

        # Identifiant de l'admin.
        identifiant = db.Column(db.String(30), unique=True, nullable=False)

        # Le mot de passe qui a subi un hachage.
        password_hash = db.Column(db.LargeBinary(255), nullable=False)

        # Salage du mot de passe.
        salt = db.Column(db.LargeBinary(254), nullable=False)


    # Modèle de la table client.
    class Client(db.Model, UserMixin):
        # Nom de la table dans la base de données.
        __tablename__ = "client"

        # Cette ligne permet de recréer la table si désinstallation complète sans message d'erreur de SQLalchemy.
        __table_args__ = {"extend_existing": True}

        # Identifiant unique du client.
        id = db.Column(db.Integer, primary_key=True)

        # Nom du client.
        nom = db.Column(db.String(30), nullable=False)

        # Prénom du client.
        prenom = db.Column(db.String(30), nullable=False)

        # Email du client.
        email = db.Column(db.String(255), nullable=False)

        # Date de naissance.
        date_naissance = db.Column(db.Date, nullable=False)

        # Genre du client.
        genre = db.Column(db.String(10), nullable=False)


    # Modèle de la classe ClientPromo.
    class SuperClient(Client):
        # Nom de la table dans la base de données.
        __tablename__ = "superclient"

        # Cette ligne permet de recréer la table si désinstallation complète sans message d'erreur de SQLalchemy.
        __table_args__ = {"extend_existing": True}

        # Identifiant unique du client_promo.
        id = db.Column(db.Integer, db.ForeignKey("client.id"), primary_key=True)

        # Définition d'un rôle pour le client_promo.
        role = db.Column(db.String(20), nullable=False)

        # Identifiant du client_promo.
        identifiant = db.Column(db.String(30), unique=True, nullable=False)

        # Le mot de passe qui a subi un hachage.
        password_hash = db.Column(db.LargeBinary(255), nullable=False)

        # Salage du mot de passe.
        salt = db.Column(db.String(254), nullable=False)

        # Relation avec la table des clients.
        client = db.relationship("Client", backref="superclient", uselist=False)


    # Modèle de la classe catégorie
    class Categorie(db.Model):
        # Nom de la table dans la base de données.
        __tablename__ = "categorie"

        # Cette ligne permet de recréer la table si désinstallation complète sans message d'erreur de SQLalchemy.
        __table_args__ = {"extend_existing": True}

        # Identifiant unique de la catégorie.
        id = db.Column(db.Integer, primary_key=True)

        # Nom de la catégorie.
        nom = db.Column(db.String(50), unique=True, nullable=False)


    # Modèle pour la table prix_promo.
    class PrixPromo(db.Model):
        # Nom de la table dans la base de données.
        __tablename__ = "prix_promo"

        # Cette ligne permet de recréer la table si désinstallation complète sans message d'erreur de SQLAlchemy
        __table_args__ = {"extend_existing": True}

        # Identifiant unique de l'admin.
        id = db.Column(db.Integer, primary_key=True)

        # Identifiant du produit associé au prix promotionnel.
        produit_id = db.Column(db.Integer, db.ForeignKey("produit.id"), nullable=False)

        # Relation avec la table des produits.
        produit = db.relationship("Produit", backref=db.backref("prix_promo", uselist=False))

        # Pourcentage de remise accordée à un produit.
        remise = db.Column(db.DECIMAL(8, 2), nullable=False)

        # Date de début de la promotion.
        date_debut = db.Column(db.DateTime, nullable=False)

        # Date de fin de la promotion.
        date_fin = db.Column(db.DateTime, nullable=False)

        # Nouveau prix.
        nouveau_prix = db.Column(db.DECIMAL(8,2), nullable=False)


    # Modèle de la table produit.
    class Produit(db.Model):
        # Nom de la table dans la base de données.
        __tablename__ = "produit"

        # Cette ligne permet de recréer la table si désinstallation complète sans message d'erreur de SQLAlchemy.
        __table_args__ = {"extend_existing": True}

        # Identifiant unique du produit.
        id = db.Column(db.Integer, primary_key=True)

        # Libellé du produit.
        libelle = db.Column(db.String(30), nullable=False)

        # Description du produit.
        description = db.Column(db.Text(), nullable=False)

        # Prix du produit.
        prix = db.Column(db.DECIMAL(8, 2), nullable=False)

        # Chemin de l'image associée au produit.
        chemin_image = db.Column(db.String(100), nullable=False)

        # Identifiant de la catégorie associé au produit.
        categorie_id = db.Column(db.Integer, db.ForeignKey("categorie.id"), nullable=False)

        # Relation avec la table des catégories.
        categorie = db.relationship("Categorie", backref=db.backref("produits", lazy="dynamic"))


    # Modèle de la table commande.
    class Commande(db.Model):
        # Nom de la table dans la base de données.
        __tablename__ = "commande"

        # Cette ligne permet de recréer la table si désinstallation complète sans message d'erreur de SQLalchemy.
        __table_args__ = {"extend_existing": True}

        # Identifiant unique de la commande.
        id = db.Column(db.Integer, primary_key=True)

        # Montant total de la commande.
        montant_total = db.Column(db.DECIMAL(8, 2), nullable=False)

        # Date à laquelle la commande a été faîte.
        date_commande = db.Column(db.Date)

        # Identifiant de la classe Client.
        client_id = db.Column(db.Integer, db.ForeignKey("client.id"))

        # Relation avec la table client.
        client = db.relationship("Client", backref="commande")


    class LigneCommande(db.Model):
        # Nom de la table dans la base de données.
        __tablename__ = "ligne_commande"

        # Cette ligne permet de recréer la table si désinstallation complète sans message d'erreur de SQLalchemy.
        __table_args__ = {"extend_existing": True}

        # Identifiant unique de la ligne de la commande.
        id = db.Column(db.Integer, primary_key=True)

        # Quantité du produit sélectionné.
        quantite = db.Column(db.Integer)

        # Prix de la ligne de commande.
        prix_ligne = db.Column(db.DECIMAL(8, 2), nullable=False)

        # Identifiant de la commande associée à la ligne de commande.
        commande_id = db.Column(db.Integer, db.ForeignKey("commande.id"))

        # Relation avec la table de la commande.
        commande = db.relationship("Commande", backref=db.backref("ligne_commande"))

        # Identifiant du produit associé à la ligne de commande.
        produit_id = db.Column(db.Integer, db.ForeignKey("produit.id"))

        # Relation avec la table du produit.
        produit = db.relationship("Produit", backref=db.backref("ligne_commande", uselist=False))


    # Création de toutes les tables à partir de leur classe.
    db.create_all()

    print("Vos tables ont bien été installées.")