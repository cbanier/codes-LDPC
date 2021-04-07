import random
import numpy as np

def mod2(a,n):
    for i in range(n):
        a[i]%=2
    return a

# retourne la ind-ème colonne de la matrice a
def getCol(a,ind):
    a = a.T
    return a[ind]

# Retourne une liste d'indices qui contiennent des 1
def getInd1inCol(a,n):
    res = []
    for i in range(n):
        if a[i] == 1:
            res.append(i)
    return res

# Calcul le poids d'un vecteur colonne
def weightOfCol(a,n):
    cpt = 0
    for i in range(n):
        if a[i] == 1:
            cpt+=1
    return cpt

# Teste si deux colonnes sont égales
def colEquals(a,b):
    return np.array_equal(a,b)

# Teste si deux matrices ont une colonne en commun
def colsEquals(a,b,n):
    a = a.T
    b = b.T
    for i in range(n):
        for j in range(n):
            if colEquals(a[i],b[j]):
                return True
    return False

# Permutation au hasard des colonnes d'une matrice a
def createRandFlipMatrix(a):
    return np.random.permutation(a.T).T

# Calcule le nombre de 1 dans une liste L
def nbOfOneFromList(L,n):
    cpt = 0
    for i in range(n):
        if L[i] == 1:
            cpt+=1
    return cpt

# Retourne une liste contenant "poids" 1 aléatoirement.
def randomIndOne(weight,n):
    L = [0 for i in range(n)]
    while nbOfOneFromList(L,n) != weight:
        L[random.randint(0,n-1)] = 1
    return L

# Retourne une liste contenant toutes les listes de randomIndOne.
# On fait attention de ne pas produire de doublon.
def listOfRandomIndOne(weight,n):
    L = []
    while len(L) != n:
        tmp = randomIndOne(weight,n//2)
        if tmp not in L:
            L.append(tmp)
    return L