from application.create_app import db

from flask_login import UserMixin

# Classe factice d'utilisateur
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

        from flask import Flask, render_template, redirect, url_for, session

        app = Flask(__name__)

        # Route pour le formulaire de connexion
        @app.route('/login', methods=['GET', 'POST'])
        def login():
            # Traitement du formulaire de connexion
            if request.method == 'POST':
                # Validation des informations de connexion
                # Stockage des données de l'utilisateur dans la session
                session['identifiant'] = 'admin1'
                session['role'] = 'SuperAdmin'
                return redirect(url_for('bienvenue'))

            # Affichage du formulaire de connexion
            return render_template('login.html')

        # Route pour la page de bienvenue
        @app.route('/bienvenue')
        def bienvenue():
            # Vérification de la présence des données de l'utilisateur dans la session
            if 'identifiant' in session and 'role' in session:
                identifiant = session['identifiant']
                role = session['role']
                return render_template('bienvenue.html', identifiant=identifiant, role=role)

            # Redirection vers la page de connexion si les données de l'utilisateur ne sont pas présentes
            return redirect(url_for('login'))

        if __name__ == '__main__':
            app.run()

            prix_promos = PrixPromo.query.all()

            nouveaux_prix = []
            dates_debut = []
            dates_fin = []

            for prix_promo in prix_promos:
                nouveaux_prix.append(prix_promo.nouveau_prix)
                dates_debut.append(prix_promo.date_debut)
                dates_fin.append(prix_promo.date_fin)