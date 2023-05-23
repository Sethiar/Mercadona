import sys
import os
import bcrypt

# Chemin absolu du répertoire courant
current_dir = os.path.abspath(os.path.dirname(__file__))

# Chemin absolu du répertoire parent
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Ajouter le répertoire parent au sys.path
sys.path.append(parent_dir)

# Importer la fonction conn() depuis db_appliStudi.py
from fonctions_base_de_donnees.db_appliStudi import conn


# Si vous voulez changer votre identifiant et votre mot de passe, c'est ici'
id = 999999
nom = "john"
prenom = "Doe"
email = "johndoe@gmail.com"
date_naissance = "02/02/1958"
genre= "Homme"


# Sélection d'un curseur pour action sur la base de données.
cur = conn.cursor()

# Insertion de l'identifiant et du mot de passe hashé dans la base de données.
cur.execute(
    "INSERT INTO client (nom, prenom, email, date_naissance, genre) VALUES (%s, %s, %s, %s, %s)",
    (nom, prenom, email, date_naissance, genre)
)

# Validation de la procédure et enregistrement au sein de la base de données.
conn.commit()

# Génération d'un message affirmant que la procédure s'est bien passée.
print("Le client a bien été enregistré.")