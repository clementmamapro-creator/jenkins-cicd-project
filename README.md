# Jenkins CI/CD — Sales Pipeline Project

> Pipeline d'intégration et de déploiement continu intégrant
> Jenkins, Docker, Apache Airflow et MongoDB.
> Master Informatique / Data Engineering

---

## Description

Ce projet automatise le cycle de vie complet d'un pipeline de données :
- Le développeur pousse son code sur GitHub
- Jenkins détecte le push et lance automatiquement la pipeline
- Les tests sont exécutés — si un test échoue, tout s'arrête
- L'image Docker est construite
- Le DAG Airflow est déployé et déclenché
- Les métriques sont stockées dans MongoDB

## Technologies utilisées

| Outil | Rôle |
|-------|------|
| Jenkins | Orchestration CI/CD — exécute le Jenkinsfile |
| Docker | Containerisation de l'application |
| Git / GitHub | Versionning et déclencheur de la pipeline |
| Apache Airflow | Orchestration des traitements de données |
| MongoDB | Stockage des métriques d'exécution |
| pytest | Tests unitaires automatiques |

---

## Prérequis

- Docker
- Git
- Python 3.11
- Apache Airflow
- MongoDB

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/clementmamapro-creator/jenkins-cicd-project.git
cd jenkins-cicd-project
```

### 2. Créer le réseau Docker

```bash
docker network create devops-network
```

### 3. Lancer Jenkins sur le port 8181

```bash
docker run -d \
  --name jenkins \
  --network devops-network \
  -p 8181:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

### 4. Récupérer le mot de passe initial

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Accéder à Jenkins : http://localhost:8181

---

## Structure du projet

jenkins-cicd-project/

│

├── Jenkinsfile                   # Pipeline CI/CD complète (7 stages)

├── Dockerfile                    # Image Python 3.11

├── requirements.txt              # Dépendances (pytest, pymongo)

├── .gitignore                    # Fichiers exclus de Git

│

├── src/

│   ├── app.py                    # Point d'entrée de l'application

│   └── calculator.py             # Module de calcul

│

├── tests/

│   └── test_calculator.py        # Tests unitaires pytest (5 tests)

│

├── dags/

│   └── sales_pipeline.py         # DAG Airflow — ventes + MongoDB

│

└── docs/                         # Captures d'écran de validation

---

## Pipeline Jenkins — 7 stages

| Stage | Description |
|-------|-------------|
| Checkout | Clone le dépôt GitHub |
| Install Dependencies | pip install -r requirements.txt |
| Run Tests | pytest — bloque si échec |
| Build Docker Image | docker build |
| Deploy DAG | Copie le DAG dans Airflow |
| Trigger DAG | Déclenche le DAG |
| Verify MongoDB | Vérifie les métriques en base |


---

## Lancer les tests localement

```bash
pip install -r requirements.txt
pytest tests/ -v
```

---

## Vérifier les métriques MongoDB

```bash
mongosh
use airflow_project
db.ventes_metrics.find().pretty()
```

---

## Auteur

Clément Ferry MAMA, Etudiant en Data Engineering  
Dépôt : [github.com/clementmamapro-creator](https://github.com/clementmamapro-creator)

---

*Projet réalisé dans le cadre de mon apprentissage — 2025/2026*