from flask_login import AnonymousUserMixin

# Créez une classe pour votre utilisateur anonyme
class Anonyme(AnonymousUserMixin):
    def __init__(self, id=None):
        self.id = id

    def is_authenticated(self):
        # L'utilisateur anonyme n'est pas actif
        return False # o

    def is_active(self):
        # L'utilisateur anonyme n'est pas actif
        return True

    def get_id(self):
        # Récupérer l'ID de l'utilisateur
        return str(self.id)