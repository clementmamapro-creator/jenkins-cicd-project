# Ce fichier est le point d'entrée de l'application
# C'est lui que Docker va exécuter au démarrage du conteneur
# Via la commande : python app.py

# On importe notre module de calcul
from calculator import add, subtract, multiply, average

# On affiche un message de démarrage
print("=== Sales Pipeline App ===")

# On teste rapidement les fonctions pour vérifier que tout fonctionne
print(f"Test add      : 2 + 3 = {add(2, 3)}")
print(f"Test subtract : 10 - 4 = {subtract(10, 4)}")
print(f"Test multiply : 3 x 7 = {multiply(3, 7)}")
print(f"Test average  : moyenne de [10,20,30] = {average([10, 20, 30])}")

print("=== Application démarrée avec succès ===")