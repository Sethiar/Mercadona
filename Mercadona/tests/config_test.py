from application.config import Config


# Configuration de l'environnement de test.
class TestingConfig(Config):
    TESTING = True



class TestConfig:
    # Configuration de la base de données Postgresql.
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Monolithe8@localhost:5432/db_appliStudi"
    TESTING = True
    # Autres configurations de test