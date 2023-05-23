
from . import db

# Modèle de la classe catégorie
class Categorie(db.Model):

    # Nom de la table dans la base de données.
    __tablename__ = "categorie"

    # Identifiant unique de la catégorie.
    id = db.Column(db.Integer, primary_key=True)

    #Nom de la catégorie.
    nom = db.Column(db.String(50), unique=True, nullable=False)

    # Représentaiton en chaîne de caractères.
    def __repr__(self):
        return f"Categorie(nom='{self.nom}')"