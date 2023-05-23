import unittest

from application.models import db
from application.models.produit import Produit
from application.models.categorie import Categorie

class TestProduit(unittest.TestCase):

    def setUp(self):
        # Configuration initiale pour les tests
        self.app = create_app()  # Remplacez create_app() par votre fonction de création d'application
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Nettoyage après les tests
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_creer_produit():
        # Création d'une nouvelle catégorie.
        categorie = Categorie(nom="Categorie 1")
        db.session.add(categorie)
        db.session.commit()

        # Création d'un nouveau produit.
        produit = Produit(libelle="Produit 1", description="Nouveau produit", prix=9.99, chemin_image="image.jpg", categorie=categorie)
        db.session.add(produit)
        db.session.commit()

        # Récupération du produit et affiche ses caractéristiques.
        produit_recup = Produit.query.filter_by(libelle="Produit").first()
        print(produit_recup)


    def test_maj_produit():
        # Récupération d'un produit de la base de données.
        produit = Produit.query.filter_by(libelle="Produit 1").first()

        # Mise à jour de la description du produit.
        produit.description = "description mise à jour"
        produit.prix = 19.99

        # "Commit" le changement dans la basde de données.
        db.session.commit()

        # Récupération de la mise à jour de la description du produit et aqffichage.
        produit_recup = Produit.query.filter_by(libelle="Produit 1").first()
        print(produit_recup)


    def test_suppression_produit():
        # Récupération d'un produit de la base de données.
        produit = Produit.query.filter_by(libelle="Produit 1").first()

        #wTest : Suppression d'un produit :
        db.session.delete(produit)
        db.session.commit()

        # Tentative de récuypérer le produit effacé dans la bbase de données.(Il devrait retounrner : None).
        produit_recup = Produit.query.filter_by(libelle="Produit 1").first()
        print(produit_recup)


if __name__ == '__main__':
    unittest.main()