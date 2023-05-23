
from . import db

# Modèle de la table commande.
class Commande(db.Model):

    # Nom de la table dans la base de données.
    __tablename__ = "commande"

    # Identifiant unique de la commande.
    id = db.Column(db.Integer, primary_key=True)

    # Montant total de la commande.
    montant_total = db.Column(db.DECIMAL(8,2), nullable=False)

    # Date à laquelle la commande a été faîte.
    date_commande = db.Column(db.Date)

    # Identifiant de la classe Client.
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))

    # Relation avec la table client.
    client = db.relationship("Client", backref="commande")
