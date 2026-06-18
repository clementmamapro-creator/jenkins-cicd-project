# On part d'une image Python 3.11 officielle (version légère)
# "slim" = image minimale, moins lourde que la version complète
FROM python:3.11-slim
# On définit le dossier de travail À L'INTÉRIEUR du conteneur
# Toutes les commandes suivantes s'exécuteront depuis ce dossier
WORKDIR /app

# On copie requirements.txt EN PREMIER (avant le reste du code)
# Pourquoi en premier ? Pour profiter du cache Docker :
# si requirements.txt n'a pas changé, Docker réutilise
# cette couche sans la reconstruire → build plus rapide
COPY requirements.txt .

# On installe les dépendances Python à l'intérieur du conteneur
# --no-cache-dir = ne pas stocker le cache pip → image plus légère
RUN pip install --no-cache-dir -r requirements.txt

# On copie tout le code source dans le conteneur
# "." à gauche = tout ce qui est sur ma machine (dans le dossier du projet)
# "." à droite = dans /app/ du conteneur
COPY . .

# CMD définit la commande exécutée quand le conteneur démarre
# C'est le point d'entrée : Docker va lancer "python src/app.py"
CMD ["python", "src/app.py"]