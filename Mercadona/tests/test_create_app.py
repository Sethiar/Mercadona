import unittest
from application.create_app import create_app
from application.config import ProductConfig, StagingConfig, DevelopmentConfig
from application.models import db
from sqlalchemy import text
import secrets

class CreateAppTest(unittest.TestCase):

    def setUp(self):
        # Configuration initiale pour les tests
        self.app, self.login_manager = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Nettoyage après les tests
        db.session.execute(text('DROP TABLE IF EXISTS commande CASCADE'))

        # Suppression de la table "client"
        db.session.execute(text('DROP TABLE IF EXISTS client'))
        db.session.commit()
        db.session.remove()
        self.app_context.pop()

    def test_creer_app(self):
        # Générer une clé secrète pour l'application
        secret_key = secrets.token_hex(16)

        # Appel de la fonction create_app pour créer l'application Flask
        app, login_manager = create_app(secret_key=secret_key)


        # Vérification que l'application Flask est créée avec succès
        self.assertIsNotNone(self.app)
        self.assertEqual(self.app.name, 'Mercadona')  # Vérifier le nom de l'application Flask

        # Vérification de la configuration de l'application
        self.assertEqual(self.app.config['SECRET_KEY'], '852ff1e8083d6a66305ed710fc57f9f6')
        self.assertIsInstance(self.app.config['SQLALCHEMY_DATABASE_URI'], str)
        self.assertIsInstance(self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], bool)

        # Vérification de l'initialisation de l'extension Flask-Login
        self.assertIsNotNone(self.login_manager)

    def test_config(self):
        # Vérification de la configuration en fonction de l'environnement
        self.assertEqual(self.app.config['ENV'], 'development')
        self.assertEqual(self.app.config['DEBUG'], True)

        # Vérification des valeurs spécifiques de la configuration
        self.assertEqual(self.app.config['SOME_CONFIG_OPTION'], 'some-value')

    # Ajoutez d'autres méthodes de test pour vérifier différents aspects de votre application create_app


if __name__ == '__main__':
    unittest.main()