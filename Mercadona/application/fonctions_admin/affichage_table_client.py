import sys
import os

# Chemin absolu du répertoire courant.
current_dir = os.path.abspath(os.path.dirname(__file__))

# Chemin absolu du répertoire parent.
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Ajouter le répertoire parent au sys.path.
sys.path.append(parent_dir)

# Importer la fonction conn() depuis db_appliStudi.py.
from fonctions_base_de_donnees.db_appliStudi import conn


# Création d'un curseur.
cur = conn.cursor()

# Exécution d'une requête de sélection.
cur.execute("SELECT nom, prenom,date_naissance, email, genre FROM client")

# Récupération des résultats de la requête.
rows = cur.fetchall()

# Affichage des résultats.
for row in rows:
    print("nom : ", row[0])
    print("prenom :", row[1])
    print("date_naissance", row[2])
    print("email:", row[3])

# Fermeture de la connexion.
cur.close()
conn.close()