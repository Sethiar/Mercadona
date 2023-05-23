
from . import db

# Modèle pour la table prix_promo.
class PrixPromo(db.Model):

    # Nom de la table dans la base de données.
    __tablename__ = "prix_promo"

    # Identifiant unique de l'admin.
    id = db.Column(db.Integer, primary_key=True)

    # Identifiant du produit associé au prix promotionnel.
    produit_id = db.Column(db.Integer, db.ForeignKey("produit.id"), nullable=True)

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


    # Représentation en chaîne de caractères.
    def __repr__(self):
        return f"PrixPromo(id={self.id}, remise='{self.remise}', date_debut='{self.date_debut}', date_fin='{self.date_fin}', nouveau_prix='{self.nouveau_prix}')"
