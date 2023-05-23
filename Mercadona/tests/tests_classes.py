
import unittest
import datetime
from flask_login import UserMixin
from datetime import date
from flask import Flask, current_app

from application.create_app import create_app
from application.models.admin import Admin
from application.models.categorie import Categorie
from application.models.client import Client
from application.models.forms import SouscriptionForm


class AdminTest(unittest.TestCase):
    def setUp(self):
        # Création d'une instance de Admin pour les tests.
        self.admin = Admin()


    def test_is_authorized(self):
        self.admin.role = "admin"
        self.assertTrue(self.admin.is_authorized("admin"))
        self.assertFalse(self.admin.is_authorized("user"))


    def test_is_active(self):
        self.assertTrue(self.admin.is_active())


    def test_is_anonymous(self):
        self.assertFalse(self.admin.is_anonymous())


    def test_get_id(self):
        self.admin.id = 1
        self.assertEqual(self.admin.get_id(), "1")


    def test_has_role(self):
        self.admin.role = "admin"
        self.assertTrue(self.admin.has_role("admin"))
        self.assertFalse(self.admin.has_role("user"))



class CategorieTest(unittest.TestCase):
    def setUp(self):
        # Création d'une instance de Categorie pour les tests.
        self.categorie = Categorie()


    def test_representation(self):
        self.categorie.nom = "Fruits"
        self.assertEqual(repr(self.categorie), "Fruits")



class ClientTests(unittest.TestCase):
    def setUp(self):
        app_tuple = create_app()
        self.app = app_tuple[0]
        self.login_manager = app_tuple[1]
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # Désactiver la protection CSRF pour les tests
        self.app.config['WTF_CSRF_ENABLED'] = False


    def tearDown(self):
        self.app_context.pop()


    def test_creation_client(self):
        # Test de création d'une instance de Client avec des données valides.
        client = Client(nom="Gros", prenom="Edgar", email="edgargros@example.com", date_naissance=date(1990, 1, 1), genre="Masculin")
        self.assertIsInstance(client, Client)
        self.assertIsInstance(client, UserMixin)
        self.assertEqual(client.nom, "Gros")
        self.assertEqual(client.prenom, "Edgar")
        self.assertEqual(client.email, "edgargros@example.com")
        self.assertEqual(client.date_naissance, datetime.date(1990,1,1))
        self.assertEqual(client.genre, "Masculin")

    def test_validation_champs_obligatoires(self):
        with self.app.app_context():
            # Test de validation des champs obligatoires
            form = SouscriptionForm()
            form.prenom.data = "Edgar"
            form.email.data = "edgargros@example.com"
            form.date_naissance.data = date(1990, 1, 1)
            form.genre.data = "Masculin"

            try:
                form.validate()
            except ValueError as e:
                print("Erreur de validation du formulaire:", str(e))

            # Créer une instance du formulaire sans fournir la valeur obligatoire pour le champ 'nom'.
            form = SouscriptionForm(prenom="Edgar", email="edgargros@example.com", date_naissance=date(1990, 1, 1),
                                    genre="Masculin")

            try:
                form.validate()
            except ValueError as e:
                print("Erreur de validation du formulaire sans champ 'nom':", str(e))

            # Le champ 'date_naissance' doit être de type date, donc une exception TypeError devrait être levée si le type est incorrect.
            with self.assertRaises(TypeError):
                client = Client(nom="Gros", prenom="Edgar", email="edgargros@example.com", date_naissance="1990-01-01",
                                genre="Masculin")

    def test_validation_champs_obligatoires(self):
        with self.app.app_context():
            # Test de validation des champs obligatoires
            form = SouscriptionForm()
            form.prenom.data = "Edgar"
            form.email.data = "edgargros@example.com"
            form.date_naissance.data = date(1990, 1, 1)
            form.genre.data = "Masculin"

            print("Avant validation - Form values:", form.data)

            try:
                form.validate()
            except ValueError as e:
                print("Erreur de validation du formulaire:", str(e))

            # Créer une instance du formulaire sans fournir la valeur obligatoire pour le champ 'nom'.
            form = SouscriptionForm(prenom="Edgar", email="edgargros@example.com", date_naissance=date(1990, 1, 1),
                                    genre="Masculin")

            print("Avant validation sans champ 'nom' - Form values:", form.data)

            try:
                form.validate()
            except ValueError as e:
                print("Erreur de validation du formulaire sans champ 'nom':", str(e))

            # Le champ 'date_naissance' doit être de type date, donc une exception TypeError devrait être levée si le type est incorrect.
            with self.assertRaises(TypeError):
                client = Client(nom="Gros", prenom="Edgar", email="edgargros@example.com", date_naissance="1990-01-01",
                                genre="Masculin")


    def test_representation_string(self):
        # Test de la méthode __repr__().
        client = Client(nom="Gros", prenom="Edgar", email="edgargros@example.com", date_naissance=date(1990, 1, 1), genre="Masculin")
        expected_repr = "Client(nom='Gros', prenom='Edgar', email='edgargros@example.com', date_naissance='1990-01-01', genre='Masculin')"
        self.assertEqual(repr(client), expected_repr)

if __name__ == '__main__':
    unittest.main()