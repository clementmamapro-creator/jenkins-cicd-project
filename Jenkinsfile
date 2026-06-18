// Ce fichier est le "chef d'orchestre" du projet
// Il dit à Jenkins quoi faire à chaque git push
// Groovy est le langage utilisé par Jenkins pour les pipelines

pipeline {
    // "agent any" = Jenkins peut utiliser n'importe quelle machine disponible
    // pour exécuter cette pipeline
    agent any

// "environment" définit des variables utilisables dans toute la pipeline
    // C'est comme des constantes — si on veut changer une valeur,
    // on la change ici une seule fois au lieu de la chercher partout (DRY : Don't Repeat Yourself)
    environment {
        IMAGE_NAME = "jenkins-cicd-project"   // nom de l'image Docker
        DAG_SOURCE = "dags/sales_pipeline.py" // chemin du DAG dans le projet
        DAG_DEST   = "/opt/airflow/dags/"     // dossier Airflow sur le serveur
        DAG_ID     = "sales_pipeline"         // identifiant du DAG dans Airflow
    }


stages {

        // Stage 1 : récupérer le code depuis GitHub
        // C'est le point de départ de toute pipeline CI/CD
        stage('Checkout') {
            steps {
                echo "==> Récupération du code depuis GitHub"
                git branch: 'main',
                    url: 'https://github.com/clementmamapro-creator/jenkins-cicd-project.git'
                echo "==> Code récupéré dans le workspace"
            }
        }   

// Stage 2 : installer les dépendances Python
        // pip lit requirements.txt et installe pytest + pymongo
        stage('Install Dependencies') {
            steps {
                echo "==> Installation des dépendances Python"
                sh 'pip install -r requirements.txt'
            }
        }

// Stage 3 : exécuter les tests automatiques
        // C'est le stage BLOQUANT : si un test échoue,
        // Jenkins arrête la pipeline et ne déploie pas
        stage('Run Tests') {
            steps {
                echo "==> Exécution des tests unitaires pytest"
                sh 'pytest tests/ -v'
            }
            // "post" définit ce qui se passe APRES le stage
            post {
                failure {
                    echo "ECHEC : les tests ont échoué — pipeline interrompue"
                }
                success {
                    echo "SUCCES : tous les tests sont passés"
                }
            }
        }

// Stage 4 : construire l'image Docker
        // On utilise la variable IMAGE_NAME définie dans environment
        // ${IMAGE_NAME} sera remplacé par "jenkins-cicd-project" automatiquement
        stage('Build Docker Image') {
            steps {
                echo "==> Construction de l'image Docker : ${IMAGE_NAME}"
                sh "docker build -t ${IMAGE_NAME} ."
                echo "==> Image Docker créée avec succès"
            }
        }

// Stage 5 : déployer le DAG dans Airflow
        // On copie le fichier DAG dans le dossier surveillé par Airflow
        // Airflow détecte automatiquement les nouveaux fichiers dans /opt/airflow/dags/
        stage('Deploy DAG') {
            steps {
                echo "==> Déploiement du DAG Airflow"
                sh "cp ${DAG_SOURCE} ${DAG_DEST}"
                echo "==> DAG copié dans ${DAG_DEST}"
            }
        }

// Stage 6 : déclencher le DAG Airflow
        // Jenkins envoie l'ordre à Airflow de lancer le DAG
        // C'est le lien entre Jenkins (CI/CD) et Airflow (orchestration données)
        stage('Trigger DAG') {
            steps {
                echo "==> Déclenchement du DAG : ${DAG_ID}"
                sh "airflow dags trigger ${DAG_ID}"
                echo "==> DAG ${DAG_ID} déclenché"
            }
        }

// Stage 7 : vérifier que les métriques sont bien dans MongoDB
        // On s'assure que le DAG a bien tourné et stocké ses résultats
        stage('Verify MongoDB') {
            steps {
                echo "==> Vérification des métriques dans MongoDB"
                sh '''
                    mongosh --quiet --eval "
                        db = db.getSiblingDB('airflow_project');
                        var count = db.ventes_metrics.countDocuments();
                        print('Documents trouvés : ' + count);
                    "
                '''
                echo "==> Vérification terminée"
            }
        }

    } // fin des stages      


// "post" global : s'exécute après TOUTE la pipeline
    // qu'elle soit en succès ou en échec
    post {
        success {
            echo "================================"
            echo "PIPELINE TERMINEE AVEC SUCCES"
            echo "Image : ${IMAGE_NAME}"
            echo "DAG   : ${DAG_ID}"
            echo "================================"
        }
        failure {
            echo "================================"
            echo "ECHEC DE LA PIPELINE"
            echo "Consultez les logs ci-dessus"
            echo "================================"
        }
    }

} // fin du pipeline