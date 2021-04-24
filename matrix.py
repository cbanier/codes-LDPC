import random
import numpy as np

from tools import *

# On créer une matrice de la forme suivante:
# 1 1 1 1 1 1 0 . . . . . . . 0 0 0 0
# 0 0 0 0 0 0 1 1 1 1 1 1 0 0 . . . .
# ...................................
def lowDensityMatrix(weight_row,n):
    a = np.zeros((n//weight_row,n))
    i , j = 0 , 0
    while j < n//weight_row and i < n:
        if (i+weight_row)%weight_row == 0 and i >= weight_row:
            j = j+1
        a[j,i] = 1
        i = i+1
    return a

# La fonction construit une matrice de Gallager ici, n doit
# être un multiple de 6 pour que la fonction marche
# Par exemple, on peut appeler la fonctions avec les couples suivants:
# (5,30) ; (6,54) ; (7;84) ; (8;120) ; ....
def createGallagerMatrix(weight_row,n):
    a = lowDensityMatrix(weight_row,n)
    b = createRandFlipMatrix(a)
    while not colsEquals(a,b,n//6):
        b = createRandFlipMatrix(a)
    c = createRandFlipMatrix(a)
    while not colsEquals(a,c,n//6) and not colsEquals(b,c,n//6):
        c = createRandFlipMatrix(a)
    return np.concatenate(((np.concatenate((a,b), axis=0)),c),axis=0)

# Retourne une liste de vecteur erreur d'un certain poids
def randomErrorVectorGenerator(poids,max_loop,n):
    errors = []
    for _ in range(max_loop):
        tmp = np.zeros(n)
        while weightOfCol(tmp,n) != poids:
            tmp[random.randint(0,n-1)] = 1
        errors.append(tmp)
    return errors

# Retourne une matrice de taille (n,n//2) tel que les colonnes est un
# poids prescrit. On ne produit pas de colonnes identiques.
def matrixFromWeight(poids,n):
    L = listOfRandomIndOne(poids,n)
    res = np.array(L[0])
    for col in L:
        if np.array_equal(col,L[0]) == False:
            res = np.concatenate((res,np.array(col)), axis=0)
    return np.reshape(res, (n,n//2)).T