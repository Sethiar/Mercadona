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
identifiant = "SuperAdmin1"
password = "#12345six"
role = "SuperAdmin"

# Génération d'un sel aléatoire pour le hachage du mot de passe.
salt = bcrypt.gensalt()

# Hachage du mot de passe avec le sel généré.
password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

print("Le processus de hachage a bien fonctionné.")

# Sélection d'un curseur pour action sur la base de données.
cur = conn.cursor()

# Insertion de l'identifiant et du mot de passe hashé dans la base de données.
cur.execute(
    "INSERT INTO admin (role, identifiant, password_hash, salt) VALUES (%s, %s, %s, %s)",
    (role, identifiant, password_hash, salt)
)
print("Les identifiants et le rôle de l'administrateur ont bien été enregistrés dans la base de données.")

# Validation de la procédure et enregistrement au sein de la base de données.
conn.commit()

# Génération d'un message affirmant que la procédure s'est bien passée.
print("Les identifiants de l'administrateur ont bien été enregistrés et sont sécurisés.")