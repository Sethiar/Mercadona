import os
from flask_sqlalchemy import SQLAlchemy


# Modèle de la classe Config.
class Config:
    DEBUG = False
    TESTING = True
    CSRF_ENABLED =True

    # Configuration de la base de données Postgresql.
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Monolithe8@localhost:5432/db_appliStudi"

    # Désactivation du suivi automatique des modifications apportées aux objets SQLalchemy.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuraiton des fichiers uploadés.
    UPLOADS_FOLDER = "static/images/images_produits"

UPLOAD_FOLDER = 'static/images/images_produits'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Configuration de l'environnement de production.
class ProductConfig(Config):
    DEBUG = False


# Configuration de l'environnement de staging.
class StagingConfig(Config):
    DEVELOPMENT =True
    DEBUG =True


# Configueration de l'environnement de développement.
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


# Configuration de l'environnement de test.
class TestingConfig(Config):
    TESTING = True


