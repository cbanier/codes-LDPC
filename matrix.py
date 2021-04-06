import random
import numpy as np

def mod2(a,n):
    for i in range(n):
        a[i]%=2
    return a

# retourne la ind-ème colonne
# de la matrice a
def getCol(a,ind):
    a = a.T
    return a[ind]

# retourne une liste d'indice
# qui contiennent des 1
def getInd1inCol(a,n):
    res = []
    for i in range(n):
        if a[i] == 1:
            res.append(i)
    return res

# calcul le poids d'un vecteur colonne
def poidsOfCol(a,n):
    cpt = 0
    for i in range(n):
        if a[i] == 1:
            cpt+=1
    return cpt

# teste si deux colonnes sont égales
def colEquals(a,b,n):
    return np.array_equal(a,b)

"""
A MODIFIER
"""
def testIfColAreEquals(A,B,N):
    A = A.T
    B = B.T
    for i in range(N):
        for j in range(N):
            if np.array_equal(A[i],B[j]):
                return True
    return False

def createMatrix(N):
    A = np.zeros(N*N//6)
    A = np.reshape(A,(N//6,N))
    i , j = 0 , 0
    while j < N//6 and i < N:
        if (i+6)%6 == 0 and i>=5:
            j=j+1
        A[j,i] = 1
        i=i+1
    return A

# Permutation au hasard des colonnes d'une matrice a
def createRandFlipMatrix(A,N):
    B = np.random.permutation(A.T)
    return B.T

def createMatrixLDPC(N):
    A = createMatrix(N)
    B = createRandFlipMatrix(A,N)
    while not testIfColAreEquals(A,B,N//6):
        B = createRandFlipMatrix(A,N)
    C = createRandFlipMatrix(A,N)
    while not testIfColAreEquals(A,C,N//6) and not testIfColAreEquals(B,C,N//6):
        C = createRandFlipMatrix(B,N)
    return np.concatenate(((np.concatenate((A,B), axis=0)),C),axis=0)

def setRandomErrorVector(poids,max_loop,N):
    errors = []
    for _ in range(max_loop):
        tmp = np.zeros(N)
        for _ in range(poids):
            tmp[random.randint(0,N)] = 1
        errors.append(tmp)
    return errors