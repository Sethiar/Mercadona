import psycopg2

# On teste la connexion à la base de données.
try:
    conn = psycopg2.connect(
        user="postgres",
        password="Monolithe8",
        host="localhost",
        port="5432",
        database="db_appliStudi"
    )
    # Créer un curseur pour pouvoir faire des actions sur la base de données.
    cur = conn.cursor()

    #Afficher la version de PostgreSQL.
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Version : ", version, "\n")

    #fermeture de la connexion à la base de données.
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")
# Renvoyer une erreuir psycopg si problème.
except (Exception, psycopg2.Error) as error:
    print("Erreur lors de la connexion à PostgreSQL", error)