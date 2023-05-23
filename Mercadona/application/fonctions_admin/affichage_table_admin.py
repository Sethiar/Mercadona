import sys
import os

# Chemin absolu du répertoire courant.
current_dir = os.path.abspath(os.path.dirname(__file__))

# Chemin absolu du répertoire parent.
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Ajouter le répertoire parent au sys.path.
sys.path.append(parent_dir)

# Ces fonctions sont utilisées pour déterminer le
# répertoire parent du répertoire courant du fichier en cours d'exécution.


# Importer la fonction conn() depuis db_appliStudi.py.
from fonctions_base_de_donnees.db_appliStudi import conn

# Création d'un curseur.
cur = conn.cursor()

# Exécution d'une requête de sélection.
cur.execute("SELECT identifiant,role, password_hash, salt FROM admin")

# Récupération des résultats de la requête.
rows = cur.fetchall()

# Affichage des résultats.
for row in rows:
    print("Nom d'utilisateur :", row[0])
    print("role : ", row[1])
    print("Mot de passe hash:", row[2])
    print("salt : ", row[3])


# Fermeture de la connexion.
cur.close()
conn.close()