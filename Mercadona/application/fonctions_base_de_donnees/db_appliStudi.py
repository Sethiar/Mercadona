import psycopg2

# Paramètres de  la base de données db_appliStudi.
conn = psycopg2.connect(
        user="postgres",
        password="Monolithe8",
        host="localhost",
        port="5432",
        database="db_appliStudi"
    )
# Créer un curseur pour pouvoir faire des actions sur la base de données
cur = conn.cursor()


# Afficher la version de PostgreSQL
cur.execute("SELECT version();")
version = cur.fetchone()
print("Version : ", version, "\n")