# Ce fichier contient les fonctions de calcul de l'application
# C'est le "coeur métier" — la logique que Jenkins va tester automatiquement

def add(a, b):
    # Addition de deux nombres et retourne le résultat
    return a + b

def subtract(a, b):
    # Soustrait b de a et retourne le résultat
    return a - b

def multiply(a, b):
    # Multiplie deux nombres et retourne le résultat
    return a * b

def average(values):
    # Calcule la moyenne d'une liste de nombres
    # "values" est une liste, par exemple : [10, 20, 30]
    if not values:
        # Si la liste est vide, on lève une erreur explicite
        # plutôt que de diviser par zéro
        raise ValueError("La liste ne peut pas être vide")
    return sum(values) / len(values)