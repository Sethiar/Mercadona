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
id = 1
nom = "john"
prenom = "Doe"
email = "johndoe@gmail.com"
date_naissance = "02/02/1958"
genre= "Homme"



# Si vous voulez changer votre identifiant et votre mot de passe, c'est ici'
identifiant = "client1"
password = "1234"
role = "SuperClient"

# On crée une valeur fictive pour l'id. Ce client n'existe pas.
client_id=1


# Génération d'un sel aléatoire
salt = bcrypt.gensalt()

# Encodage de la chaînes de caractère.
password_str = password.encode("utf-8")
# Hachage du mot de passe avec le sel
password_hash = bcrypt.hashpw(password_str, salt)

# Affichage du mot de passe haché
print("le processus de hachage a bien fonctionné.")

# Sélection d'un curseur pour action sur base de données.
cur = conn.cursor()

# Insertion de l'identifiant et du mot de passe hashé dans la base de données.
cur.execute(
"INSERT INTO client_promo (id, role, identifiant, password_hash, salt) VALUES (%s, %s, %s, %s, %s)", (client_id, role, identifiant, password_hash, salt))
print("L'identifiant, le mot de passe et le rôle du SuperClient ont bien été enregistrés dans la base de données.")
# Validation de la procédure et enregistremnt au sein de la base de données.
conn.commit()

# Génération d'un message affirmant que la procédure s'est bien passée.
print("Les identifiants du client ont bien été enregistrés et sont sécurisés.")