from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from application import config

import logging
import os
import secrets


from application.models.anonyme import Anonyme
from application.models.admin import Admin
from application.models.superclient import SuperClient
from models import db


def create_app():
    # Créationde l'instance Flask.
    app = Flask("Mercadona", template_folder="templates")

    # Charger la configuration en fonction de l'environnement.
    if os.environ.get("FLASK_ENV") == "development":
        app.config.from_object(config.DevelopmentConfig)
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.ProductConfig)


    # Configuration de l'environnement de l'application.
    app.config.from_envvar("FLASK_APP_SETTINGS")
    app.config["SESSION_COOKIE_SECURE"] = False

    # Initialiser le gestionnaire de connexion en créant une instance de LoginManager.
    login_manager = LoginManager()

    @login_manager.user_loader
    def load_user(user_id):
        # Charger l'utilisateur à partir de la base de données en utilisant l'ID
        client = Client.query.get(user_id)
        admin = Admin.query.get(user_id)
        superclient = SuperClient.query.get(user_id)

        if client:
            return client
        elif admin:
            return admin
        elif superclient:
            return superclient

        # Aucun utilisateur correspondant à l'ID ou type d'utilisateur non pris en charge
        # ou le type d'utilisaterus pris en charge.
        return None

    login_manager.init_app(app)
    # Définissez la classe à utiliser pour les utilisateurs anonymes.
    login_manager.anonymous_user = Anonyme

    # Définition de la clé secrète.
    app.secret_key = secrets.token_hex(16)

    # Configuration de la journalisation.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    app.logger.setLevel(logging.DEBUG)
    app.logger.debug("Message de débogage")
    app.logger.info("Message informatif")
    app.logger.warning("Message d'avertissement")
    app.logger.error("Message d'erreur")
    handler = logging.FileHandler("fichier.log")
    app.logger.addHandler(handler)

    # Charger la configuration en fonction de l'environnement.
    if os.environ.get("FLASK_ENV") == "development":
        app.config.from_object(config.DevelopmentConfig)
    else:
        app.config.from_object(config.ProductConfig)

    # Création de l'objet Migrate afin de mettre à jour les tables( !!! Attention !!! ).
    migrate = Migrate(app, db)

    # Configuration de la base de données Postgresql.
    app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://postgres:Monolithe8@localhost:5432/db_appliStudi"

    # Initialisez la base de données
    with app.app_context():
        db.init_app(app)


    # Configuration de  l'envoi de mail avce Flask-Mail.
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'applistudi@gmail.com'
    app.config['MAIL_PASSWORD'] = 'applibloc3Studi'
    app.config['MAIL_DEFAULT_SENDER'] = 'applistudi@gmail.com'

    mail = Mail(app)

    return app, login_manager, db