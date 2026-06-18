# Ce fichier est un DAG Airflow
# DAG = Directed Acyclic Graph = un enchaînement de tâches dans un ordre précis
# Jenkins va déposer ce fichier dans Airflow et le déclencher automatiquement

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# "pymongo" est la bibliothèque Python pour parler à MongoDB
from pymongo import MongoClient

# Configuration par défaut appliquée à toutes les tâches du DAG
default_args = {
    "owner": "airflow",         # propriétaire du DAG
    "retries": 1,               # nombre de tentatives en cas d'échec
    "retry_delay": timedelta(minutes=2),  # attendre 2 min avant de réessayer
}

# Tâche 1 : générer des données de ventes simulées
# Dans un vrai projet, on lirait un fichier CSV ou une API
def generer_ventes():
    # On importe random pour générer des nombres aléatoires
    import random

    # On génère un nombre de ventes aléatoire entre 3 et 10
    nb_ventes = random.randint(3, 10)

    # On génère une liste de montants aléatoires entre 50€ et 800€
    ventes = [round(random.uniform(50, 800), 2) for _ in range(nb_ventes)]

    print(f"[sales_pipeline] {nb_ventes} ventes générées : {ventes}")

    # On retourne les données pour la tâche suivante via XCom
    return {"nb_ventes": nb_ventes, "ventes": ventes}

# Tâche 2 : calculer les métriques à partir des ventes générées
# **context permet de récupérer les données de la tâche précédente
def calculer_metriques(**context):
    # XCom = Cross Communication : mécanisme Airflow pour passer
    # des données d'une tâche à une autre
    data = context["ti"].xcom_pull(task_ids="generer_ventes")

    ventes = data["ventes"]

    # On calcule le chiffre d'affaires total
    chiffre_affaires = round(sum(ventes), 2)

    # On calcule le montant moyen par vente
    montant_moyen = round(chiffre_affaires / len(ventes), 2)

    print(f"[sales_pipeline] CA={chiffre_affaires}€ | Moyenne={montant_moyen}€")

    return {
        "nb_ventes": data["nb_ventes"],
        "chiffre_affaires": chiffre_affaires,
        "montant_moyen": montant_moyen,
    }

# Tâche 3 : stocker les métriques dans MongoDB
# C'est la dernière tâche du DAG
def stocker_mongodb(**context):
    # On récupère les métriques calculées par la tâche précédente
    metriques = context["ti"].xcom_pull(task_ids="calculer_metriques")

    # On se connecte à MongoDB sur le port par défaut 27017
    client = MongoClient("mongodb://localhost:27017/")

    # On sélectionne la base de données "airflow_project"
    db = client["airflow_project"]

    # On sélectionne la collection "ventes_metrics" (équivalent d'une table)
    collection = db["ventes_metrics"]

    # On crée le document à insérer (équivalent d'une ligne en SQL)
    document = {
        "dag_id": "sales_pipeline",
        "execution_date": datetime.now().isoformat(),
        "nb_ventes": metriques["nb_ventes"],
        "chiffre_affaires": metriques["chiffre_affaires"],
        "montant_moyen": metriques["montant_moyen"],
        "status": "success",
    }

    # On insère le document dans MongoDB
    result = collection.insert_one(document)
    print(f"[sales_pipeline] Document inséré — id: {result.inserted_id}")

    # On ferme la connexion proprement
    client.close()

# On définit le DAG — c'est ici qu'Airflow enregistre le pipeline
with DAG(
    dag_id="sales_pipeline",        # identifiant unique du DAG dans Airflow
    default_args=default_args,       # on applique la config définie plus haut
    description="Pipeline de traitement des ventes avec stockage MongoDB",
    schedule_interval=None,          # None = déclenché manuellement par Jenkins
    start_date=datetime(2025, 1, 1), # date de début (obligatoire dans Airflow)
    catchup=False,                   # ne pas rattraper les exécutions passées
    tags=["sales", "jenkins", "mongodb"],  # tags visibles dans l'interface Airflow
) as dag:

    # On définit les 3 tâches du DAG
    t1 = PythonOperator(
        task_id="generer_ventes",        # identifiant de la tâche
        python_callable=generer_ventes,  # fonction à exécuter
    )

    t2 = PythonOperator(
        task_id="calculer_metriques",
        python_callable=calculer_metriques,
        provide_context=True,  # permet d'utiliser **context pour xcom_pull
    )

    t3 = PythonOperator(
        task_id="stocker_mongodb",
        python_callable=stocker_mongodb,
        provide_context=True,
    )

    # On définit l'ordre d'exécution des tâches
    # >> signifie "puis" : t1 puis t2 puis t3
    t1 >> t2 >> t3