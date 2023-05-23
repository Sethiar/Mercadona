
from . import db
from .client import Client

# Modèle de la classe Client_promo.
class SuperClient(Client):

    # Nom de la table dans la base de données.
    __tablename__ = "superclient"

    # Identifiant unique du client_promo.
    id = db.Column(db.Integer, db.ForeignKey("client.id"), primary_key=True)

    # Définition d'un rôle pour le client_promo.
    role = db.Column(db.String(20), nullable=False)

    # Identifiant du client_promo.
    identifiant = db.Column(db.String(30), unique=True, nullable=False)

    # Le mot de passe qui a subi un hachage.
    password_hash = db.Column(db.String(255), nullable=False)

    # Salage du mot de passe.
    salt = db.Column(db.String(254), nullable=False)

    # Relation avec la table des clients.
    client = db.relationship("Client", backref="superclient", uselist=False)

    # Représentaiton en chaîne de caractères.
    def __repr__(self):
        return f"SuperClient(role={self.role}, identifiant={self.identifiant}, password_hash{self.password_hash}, salt={self.salt}"

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