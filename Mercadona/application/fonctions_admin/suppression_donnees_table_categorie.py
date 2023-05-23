import sys
import os

# Chemin absolu du répertoire courant
current_dir = os.path.abspath(os.path.dirname(__file__))

# Chemin absolu du répertoire parent
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Ajouter le répertoire parent au sys.path
sys.path.append(parent_dir)

# Importer la fonction conn() depuis db_appliStudi.py
from fonctions_base_de_donnees.db_appliStudi import conn


# Création d'un curseur
cur = conn.cursor()

#Exécution d'une requête de suppression
#cur.execute("DELETE FROM produit where id = %s", (0,))
cur.execute("DELETE FROM categorie")
# Validation de la transaction
conn.commit()
print('Toutes les données de la table categorie ont bien été supprimées.')

# Fermeture de la connexion
cur.close()
conn.close()