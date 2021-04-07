import numpy as np
from time import time

from matrix import *
from tools import *

def decode_LDPC_aux(H,S,weight_S,n,break_cpt):
    if break_cpt >= 25:
        #print(f'Error: LDPC code not found after {break_cpt} iterations')
        return []
    # On stocke dans L, les positions erronées
    L = []
    for i in range(n):
        if weightOfCol(mod2(S + getCol(H,i), n//2),n//2) <= weight_S:
            L.append(i)
    # S2 est la somme de toutes les colonnes de H qui sont erronées
    S2 = np.zeros(n//2)
    for i in L:
        S2 = S2 + getCol(H,i)
    S2 = mod2(S2, n//2)
    # S3 est notre nouveau syndrome
    S3 = np.zeros(n//2)
    S3 = mod2(S+S2, n//2)
    # si S3 est nul alors on a trouvé les positions erronées
    # sinon, on continue
    if weightOfCol(S3,n//2) == 0:
        #print(f'Error found in {break_cpt} times')
        return L
    else:
        return decode_LDPC_aux(H,S3,weightOfCol(S3,n//2),n,break_cpt+1)

def decode_LDPC(H,e,n):
    S = mod2(H@(e.T),n//2)
    weight_S = weightOfCol(S,n//2)
    ldpc = decode_LDPC_aux(H,S,weight_S,n,1)
    return ldpc

def test_decode_LDPC(H,weight_e,max_loop,n):
    cpt = 0
    errors = randomErrorVectorGenerator(weight_e,max_loop,n)
    for e in errors:
        if decode_LDPC(H,e,n) == getInd1inCol(e,n):
            cpt+=1
    return cpt/max_loop

def displayTestLoop(H,weight_e,max_loop,n):
    print(f"Test sur {max_loop} vecteurs erreurs de poids {weight_e}: {test_decode_LDPC(H,weight_e,max_loop,n)}")
    return None

def displayTestLoopWithTime(H,weight_e,max_loop,n):
    start = time()
    print(f"Test sur {max_loop} vecteurs erreurs de poids {weight_e}: {test_decode_LDPC(H,weight_e,max_loop,n)}")
    end = time()
    print("Time:",end - start)
    return None

if __name__ == "__main__":
    n = 1000
    H = matrixFromWeight(5,n)
    print(f"Soit H une matrice de taille {n}x{n//2}\n")
    for i in range(1,16):
        displayTestLoop(H,i,25,n)

    n*=2
    H = matrixFromWeight(5,n)
    print(f"\nNouvelle matrice de taille {n}x{n//2}\n")
    for i in range(1,16):
        displayTestLoop(H,i,25,n)