from . import db

from flask_login import UserMixin


# Modèle de la table client.
class Client(db.Model, UserMixin):

    # Nom de la table dans la base de données.
    __tablename__ = "client"

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

    # représentation en chaîne de caractères.
    def __repr__(self):
        return f"Client(nom='{self.nom}', prenom='{self.prenom}', email='{self.email}', date_naissance='{self.date_naissance}', genre='{self.genre}')"

