

from . import db


# Modèle de la table produit.
class Produit(db.Model):

    # Nom de la table dans la base de données.
    __tablename__ = "produit"

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

    # Représentation en chaîne de caractères.
    def __repr__(self):
        return f"Produit('{self.libelle}', '{self.description}', {self.prix:.2f}€, '{self.chemin_image}', {self.categorie_id})"

