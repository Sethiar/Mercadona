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

# Création d'un curseur pour exécuter des requêtes SQL
cur = conn.cursor()

# Exécution de la requête pour ajouter une colonne
cur.execute("ALTER TABLE produit ADD COLUMN categorie_id INT")

print("La nouvelle colonne a bien été ajoutée.")
# Validation des modifications et fermeture de la connexion
conn.commit()
cur.close()
conn.close()
