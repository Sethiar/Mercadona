import sys
import os
import bcrypt

project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)


from flask_wtf.csrf import CSRFProtect


from flask import Flask, render_template, request, flash, \
    redirect, url_for, session, abort

from flask_login import current_user


from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query
from werkzeug.utils import secure_filename

from decimal import Decimal
from datetime import datetime

from fonctions_admin.fonctions_mail import create_message, send_message

from models.user_session import User
from models.categorie import Categorie
from models.produit import Produit
from models.prix_promo import PrixPromo
from models.admin import Admin
from models.client import Client
from models.superclient import SuperClient
from models.anonyme import Anonyme

from models.forms import SouscriptionForm, ConnexionAdministrateur, NouvelleCategorieForm

import config

from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, Config

from fonctions_user.methodes_pour_image import allowed_file
from fonctions_admin.fonction_authentification import  moyenne



from create_app import create_app

# Configuration de la base de données Postgresql.

app, login_manager, db = create_app()

# Utilisez login_manager dans votre application Flask
login_manager.init_app(app)

# Configuration de l'application pour utiliser la protection CSRF.
csrf = CSRFProtect(app)



# Tests des fonctions.
@app.route('/Tests')
def calcul():
    resultat = moyenne()
    return str(resultat)


# Redirection vers la page 401.
@app.errorhandler(401)
def acces_non_authorise(error):
    return render_template("401.html"), 401


# Redirection vers la page 404.
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route("/")
def accueil():
    return render_template("accueil.html")


@app.route("/deconnexion",methods=["GET"])
def utilisateur_deconnexion():
    session.pop("logged_in", None)
    session.pop("identifiant", None)
    session.pop("user_id", None)
    return redirect(url_for('accueil'))


@app.route("/catalogue", methods=["GET"])
def catalogue():
    # Mise en place des règles de la pagination.
    page = request.args.get("page", 1, type=int)
    per_page = 30
    offset = (page - 1) * per_page

    # Calcul du nombre total de produits.
    total_produits = Produit.query.count()

    # Calcul du nombre total de pages.
    total_pages = (total_produits + per_page - 1) // per_page

    # Récupération dees données des produits et des catégories..
    produits = Produit.query.all()
    categories = Categorie.query.all()
    prix_promos = {promo.produit_id: promo for promo in PrixPromo.query.all()}

    for produit in produits:
        if produit.id in prix_promos:
            prix_promo = prix_promos[produit.id]

        # Supprimer les promotions expirées.
        promotions_expirees = PrixPromo.query.filter(PrixPromo.date_fin < datetime.now().date()).all()
        for promotion in promotions_expirees:
            db.session.delete(promotion)
        db.session.commit()

    # Récupération de la catégorie sélectionnée.
    categorie = request.args.get("categorie")
    # Filtrer les produits par la catégorie sélectionnée.
    if categorie:
        produits = Produit.query.filter(Produit.categorie.has(nom=categorie)).all()

    return render_template("catalogue_produit.html", produits=produits, categories=categories, prix_promos=prix_promos,
                           total_pages=total_pages)


# Route utilisée pour accéder au back-end.
@app.route("/admin", methods=["GET"])
#@login_required
def afficher_back_end():
    formcategories = NouvelleCategorieForm()
    # pour accéder à cet écran, l'utilisateur doit être enregistré dans la table de données en tant que "super administrateur".
    if current_user.is_active:

        # Permet l'affichage des enregistrements dans le back_end.
        categories = Categorie.query.all()
        produits = Produit.query.all()
        return render_template("admin/back_end.html", categories=categories, produits=produits, formcategories=formcategories)
    else:
         # Redirection vers une page d'erreur ou afficher un message d'interdiction d'accès.
        return "Accès refusé. Vous n'avez pas les autorisations nécessaires pour accéder au back-end."


# Route utilisée pour renvoyer vers le formulaire de la connexion administrateur.
@app.route("/formulaire_connexion_admin")
def admin_form():
    form = ConnexionAdministrateur()
    return render_template("admin/connexion_admin.html", form=form)


# Route permettant de se connecter en tant qu'administrateur afin d'accéder au back-end du site.
@app.route("/connexion_administrateur", methods=["GET", "POST"])
def login_administrateur():
    # Instanciation du formulaire LoginForm.
    form = ConnexionAdministrateur()

    if request.method == 'POST':
        if form.validate_on_submit():
            identifiant = form.identifiant.data
            password = form.password.data

            # Validation de identifiant et password.
            admin = Admin.query.filter_by(identifiant=identifiant).first()
            if admin is not None and bcrypt.checkpw(password.encode("utf-8"), admin.password_hash):
                # Authentification réussie.
                if admin.has_role("SuperAdmin"):
                    app.logger.info(f"L'administrateur {admin.identifiant} s'est bien connecté.")

                    # Connexion de l'utilisateur et stockage de ses informations dans la session.
                    session["logged_in"] = True
                    session["identifiant"] = admin.identifiant
                    session["user_id"] = admin.id

                    return redirect(url_for("afficher_back_end"))
                else:
                    app.logger.warning(f"L'administrateur {admin.identifiant} n'a pas le rôle de SuperAdmin.")
            else:
                app.logger.warning(f"Tentative de connexion échouée avec l'identifiant {identifiant}.")
                return redirect(url_for("admin_form"))

# Route utilisée pour renvoyer vers le formulaire de la connexion user.
@app.route("/formulaire_utilisateur")
def utilisateur_form():
    form = ConnexionAdministrateur()
    return render_template("user/connexion_utilisateur.html", form=form)



# Route utilisée pour renvoyer v
# ers le traitement des données reçues du formulaire.
@app.route("/formulaire_connexion_utilisateur", methods=["POST"])
def connexion_utilisateur():
    # Instanciation du formulaire LoginForm.
    form = ConnexionAdministrateur()

    if request.method == 'POST':
        if form.validate_on_submit():
            identifiant = form.identifiant.data
            password = form.password.data

    # Validation de identifiant et password.
    superclient = SuperClient.query.filter_by(identifiant=identifiant).first()
    if superclient is not None and bcrypt.checkpw(password.encode("utf-8"), superclient.password_hash):
        # Authentification réussie.
        if superClient.has_role("SuperClient"):
            app.logger.info(f"Le client {superClient.identifiant} s'est bien connecté.")

            # Connexion de l'utilisateur et stockage de ses informations dans la session.
            session["logged_in"] = True
            session["identifiant"] = superclient.identifiant
            session["user_id"] = superclient.id

            return redirect(url_for("catalogue"))
        else:
            app.logger.warning(f"Le client {superclient.identifiant} n'a pas le rôle de SuperClient.")
    else:
        app.logger.warning(f"Tentative de connexion échouée avec l'identifiant {identifiant}.")

    return render_template("user/connexion_utilisateur.html", error_message="L'identifiant du client et le mot de passe sont requis.")


# route permettant de créer une nouvelle catégorie.
@app.route("/admin/nouvelle_categorie", methods=["POST"])
@csrf.exempt
def creer_une_nouvelle_categorie():
    if request.method == "POST":
        # Saisie du nom de la catégorie.
        nom_categorie = escape(request.form.get("nom"))
        categorie = Categorie(nom=nom_categorie)

        # Enregistrement dans la base de données.
        db.session.add(categorie)
        db.session.commit()

        flash("La catégorie a bien été ajoutée" + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
    return redirect(url_for("afficher_back_end"))


# Route permettant de supprimer d'une catégorie.
@app.route("/admin/supprimer_catégorie/<int:id>", methods=["POST"])
@csrf.exempt
def supprimer_catégorie(id):
    categorie = Categorie.query.get(id)

    if categorie:
        # Suppression de la categorie.
        db.session.delete(categorie)
        # Validation de l'action.
        db.session.commit()
        flash("La catégorie a été supprimée avec succès."+ " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

        return redirect(url_for("afficher_back_end"))


# Route permettant de créer un nouveau produit.
@app.route("/admin/nouveau_produit", methods=["GET", "POST"])
@csrf.exempt
def creer_un_nouveau_produit():
    if request.method =="POST":
        # Saisie des caractéristiques du produit.
        libelle_produit = request.form.get("libelle")
        description_produit = request.form.get("description")
        prix_produit = request.form.get("prix")
        image_produit = request.files.get("image")
        categorie_id = request.form.get("categorie_id")
        categorie = Categorie.query.filter_by(id=categorie_id).first()

        # Code pour stocker l'image et l'utiliser.
        if "image" not in request.files:
            return redirect("creer_un_nouveau_produit")
        print("l'image n'est pas présente dans le fichier.")
        image = request.files['image']
        if image.filename == '':
            return redirect("creer_un_nouveau_produit")

        if image and allowed_file(image.filename):
            # Ajout d'une limite :10Mo sinon erreur 400.
            if len(image.read()) > 10 * 1024 * 1024:
                return redirect("creer_un_nouveau_produit")
            # Réinitialisation du curseur pour la sauvegarde du fichier.
            image.seek(0)
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            print('L\'image a bien été stockée dans le fichier "static/images/images_produits".')

        else:
            return redirect(url_for("afficher_back_end"))

        # Enregistrement du produit dans la base de données.
        produit = Produit(libelle=libelle_produit, description=description_produit, prix=prix_produit, chemin_image=filename,
                          categorie=categorie)
        db.session.add(produit)
        db.session.commit()

    flash("Le produit a bien été ajouté "+ " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
    return redirect(url_for("afficher_back_end"))


# Route permettant de supprimer un produit.
@app.route("/admin/supprimer_produit/<int:id>", methods=["POST"])
@csrf.exempt
def supprimer_produit(id):
    produit = Produit.query.get(id)
    if produit:
        # Suppression du produit.
        db.session.delete(produit)
        # Validation de l'action.
        db.session.commit()
        flash("Le produit a été supprimé avec succès."+ " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))

    return redirect(url_for("afficher_back_end"))


# Route permettant de saisir une promotion pour un produit.
@app.route("/admin/nouvelle_promotion/<produit_id>", methods=["POST"])
@csrf.exempt
def creer_promotion(produit_id):
    remise = Decimal(escape(request.form.get("remise")))
    date_debut = escape(request.form.get("date_debut"))
    date_fin = escape(request.form.get("date_fin"))
    print("remise:", remise)
    print("date_debut:", date_debut)
    print("date_fin:", date_fin)

    if datetime.strptime(date_fin, '%Y-%m-%d').date() <= datetime.strptime(date_debut, '%Y-%m-%d').date():
        flash("La date de fin doit être postérieure à la date de début." "error")
        return redirect(url_for("afficher_back_end"))

    prix = Decimal(Produit.query.filter_by(id=produit_id).first().prix)
    nouveau_prix = (prix * (Decimal(1)- remise / Decimal(100))).quantize(Decimal("0.01"))

    # Enregistrement dans la table prix_promo.
    prix_promo_produit = PrixPromo(remise=remise, date_debut=date_debut, date_fin=date_fin,
                      nouveau_prix=nouveau_prix, produit_id=produit_id)
    db.session.add(prix_promo_produit)
    db.session.commit()
    flash("Le nouveau prix a bien été ajouté et il est de : " + " " + str(nouveau_prix))
    return redirect(url_for("afficher_back_end"))


# Route utilisée pour renvoyer vers le formulaire de la souscription client.
@app.route("/souscription_utilisateur", methods=['GET', "POST"])
def souscription_utilisateur():
    form = SouscriptionForm()
    return render_template("user/souscription.html", form=form)


# Route utilisée pour enregistrer les informations du client qui demande une souscritpion pour accéder aux promotions.
@app.route("/enregistrer_client", methods=["GET", "POST"])
def soumettre_candidature():
    form = SouscriptionForm()
    if form.validate_on_submit():
        nom = form.nom.data
        prenom = form.prenom.data
        email = form.email.data
        date_naissance = form.date_naissance.data
        genre = form.genre.data

        # Conversion de la date qui est en chaîne de caractère en objet datetime.date.
        date_naissance =datetime.strptime(form.date_naissance.data, "%Y-%m-%d").date()

        # Enregistrement dans la table "client"
        client = Client(nom=nom, prenom=prenom, email=email, date_naissance=date_naissance, genre=genre)
        db.session.add(client)
        db.session.commit()

        flash("Un nouveau client a soumis son souhait de profiter des promotions " + datetime.now().strftime(
            "le %d-%m-%Y à %H:%M:%S"))
        return redirect(url_for("catalogue"))

    return render_template("user/souscription.html", form=form)


# Route permettant à l'utilisateur de consulter les conditions de souscription de Mercadona.
@app.route("/conditions")
def conditions():
    return render_template("user/conditions.html")


# Route permettant de paginer la page concernant les informations des clients souhaitant profiter des promotions.
@app.route("/admin/accepter_souscription", methods=["GET"])
def admin_validation():
    # Récupérer le numéro de page à partir des paramètres de requête
    page = request.args.get('page', 1, type=int)
    clients_par_page = 30

    # Récupérer les clients paginés à partir de la base de données
    pagination = Client.query.paginate(page=page, per_page=clients_par_page)

    return render_template("admin/liste_client.html", pagination=pagination)


@app.route("/admin/enregistrer_superclient/<client_id>", methods=["POST"])
@csrf.exempt
def enregistrer_superclient():
    # Récupératioon des informations du formulaire d'enregistrement d'un superclient.
    nom = escape(request.form.get("nom"))
    prenom = escape(request.form.get("prenom"))
    identifiant = escape(request.form.get("identifiant"))
    password = escape(request.form.get("password"))
    email = escape(request.form.get("email"))
    genre = escape(request.form.get("genre"))

    # Hachage du mot de passe de l'administrateur.
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iteration)
    # On vérifie que le mot de passe a bien été crypté.
    print("Le mot de passe a bien été crypté.")

    # Enregistrement dans la table client.
    super_client = SuperClient(nom=nom, prenom=prenom, identifiant=identifiant, password_hash=password_hash, email=email, genre=genre)
    db.session.add(super_client)
    db.session.commit()
    print("Un nouveau client est enregistrer dans la table Client_promo, il peut désormais s'authentifier et profiter des promotions "+" "+ datetime.now().strftime(
        " le %d-%m-%Y à %H:%M:%S"))
    return redirect(url_for("catalogue"))

    # Si le formulaire n'est pas valide, afficher les erreurs et revenir à la page du formulaire
    return redirect(url_for("catalogue"))


@app.route("/envoyer_email", methods=["POST"])
def envoyer_email():
    # Récupération de l'id du client.
    client_id =request.form.get("client_id")

    # Récupérer les informations du client à partir de la base de données ou d'une autre source
    client = Client.query.get(client_id)
    if client is None:
        return "Client introuvable"

    # Utilisation de l'adresse e-mail du client.
    recipient = client.email

    # Sujet de l'email.
    subject = "Inscription aux promotions"

    # Message envoyé.
    body = "Bonjour" f'{client.prenom}', "suite à votre demande d'adhésion, je vous incite à suivre ce lien afin de vous inscrire poiur profiter de nos promotions : {}".format(client.prenom, 'http://votre_formulaire_d_inscription')

    # Appel de la fonction create_message.
    message =Message(subject=subject, body=body, recipients=[recipient])

    # Envoi du message.
    mail.send(message)

    return "L'email a été envoyé avec  succès."





if (__name__) =='__main__':
        app.run()