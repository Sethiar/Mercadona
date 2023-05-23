
from . import db
import logging
from flask_login import UserMixin


# Modèle pour la table administrateur.
class Admin(db.Model, UserMixin):

    # Nom de la table dans la base de données.
    __tablename__ = "admin"

    # Identifiant unique de l'admin.
    id = db.Column(db.Integer, primary_key=True)

    # Définition d'un rôle pour l'administrateur.
    role = db.Column(db.String(20), nullable=False)

    # Identifiant de l'admin.
    identifiant = db.Column(db.String(30), unique=True, nullable=False)

    # Le mot de passe qui a subi un hachage.
    password_hash = db.Column(db.LargeBinary(120), nullable=False)

    # Salage du mot de passe.
    salt = db.Column(db.LargeBinary(254), nullable=False)


    # Représentation en chaîne de caractères.
    def __repr__(self):
        return f"Admin(id='{self.id}', role='{self.role}', identifiant='{self.identifiant}', salt='{self.salt}', password_hash='{self.password_hash}')"


    # Méthode pour que Flask-login authentifie correctement l'administrateur.
    def is_authorized(self, role):
        print("is_authenticated method called")
        logging.debug("is_authenticated method called")
        return self.role == role

    def is_active(self):
        print("is_active method called")
        logging.debug("is_active method called")
        return True

    def is_anonymous(self):
        print("is_anonymous method called")
        logging.debug("is_anonymous method called")
        return False

    def get_id(self):
        print("get_id method called")
        logging.debug("get_id method called")
        return str(self.id)

    def has_role(self, role):
        print("has_role method called")
        logging.debug("has_role method called")
        return self.role == role