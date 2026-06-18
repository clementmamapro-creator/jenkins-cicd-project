# Ce fichier contient les tests automatiques de calculator.py
# pytest va lire ce fichier et exécuter toutes les fonctions qui commencent par "test_"

import sys
import os

# On indique à Python où trouver calculator.py
# car il est dans src/ et non dans tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# On importe les fonctions qu'on veut tester
from calculator import add, subtract, multiply, average

def test_add():
    # On vérifie que add(2, 3) retourne bien 5
    # "assert" signifie : "je affirme que ... est vrai"
    # Si c'est faux, pytest marque le test comme FAILED
    assert add(2, 3) == 5

def test_subtract():
    # On vérifie que 10 - 4 = 6
    assert subtract(10, 4) == 6

def test_multiply():
    # On vérifie que 3 x 7 = 21
    assert multiply(3, 7) == 21

def test_average():
    # On vérifie que la moyenne de [10, 20, 30] = 20.0
    assert average([10, 20, 30]) == 20.0

def test_average_empty():
    # On vérifie que average() lève bien une erreur si la liste est vide
    # "pytest.raises" attrape l'erreur et vérifie qu'elle est du bon type
    import pytest
    with pytest.raises(ValueError):
        average([])