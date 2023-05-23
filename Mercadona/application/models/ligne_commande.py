

from . import db

class LigneCommande(db.Model):

    # Nom de la table dans la base de données.
    __tablename__ = "ligne_commande"

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

    # Représentaiton en chaîne de caractères.
    def __repr__(self):
        return f"LigneCommande(id={self.id}, prix_ligne='{self.prix_ligne}')"
