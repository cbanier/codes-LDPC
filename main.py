import random
import numpy as np
from time import time

from matrix import *

def LDPC_aux(H,S,poids_S,N,break_cpt):
    if break_cpt >= 20:
        #print(f'Error: LDPC code not found after {break_cpt} iterations')
        return []
    # on stocke dans l, les positions erronées
    l = []
    for i in range(N):
        if poidsOfCol(mod2(S + getCol(H,i), N//2),N//2) <= poids_S:
            l.append(i)
    # S2 est la somme de toutes les colonnes
    # de H qui sont erronées
    S2 = np.zeros(N//2)
    for i in l:
        S2 = S2 + getCol(H,i)
    S2 = mod2(S2, N//2)
    #print("S2=",S2,'\n')
    # S3 est notre nouveau syndrome
    S3 = np.zeros(N//2)
    S3 = mod2(S+S2, N//2)
    #print("S3=",S3,'\n')
    # si S3 est nul alors on a trouvé les positions erronées
    # sinon, on continue
    if poidsOfCol(S3,N//2) == 0:
        #print(f'Error found in {break_cpt} times')
        return l
    else:
        return LDPC_aux(H,S3,poidsOfCol(S3,N//2),N,break_cpt+1)

def LDPC(H,e,N):
    # calcul du syndrome
    S = mod2(H@(e.T),N//2)
    #print("S=", S, "\n")
    poids_S = poidsOfCol(S,N//2)
    ldpc = LDPC_aux(H,S,poids_S,N,1)
    return ldpc

def testLDPC(H,poids_e,max_loop,N):
    cpt = 0
    errors = setRandomErrorVector(poids_e,max_loop,N)
    for e in errors:
        if LDPC(H,e,N) == getInd1inCol(e,N):
            cpt+=1
    return cpt/max_loop

def displayTestLoop(h,poids_e,max_loop,N):
    start = time()
    print(f"Test sur {max_loop} vct erreurs de poids {poids_e}:{testLDPC(h,1,max_loop,N)}")
    end = time()
    print("Time:",end - start)
    return None

if __name__ == "__main__":
    N = 54
    loop = 10
    h = createMatrixLDPC(N*10) #size 540
    #displayTestLoop(h,1,loop,N*10)
    #displayTestLoop(h,2,loop,N*10)
    #displayTestLoop(h,3,loop,N*10)
    #displayTestLoop(h,4,loop,N*10)
    #displayTestLoop(h,5,loop,N*10)
    displayTestLoop(h,200,loop,N*10)

    # another matrix
    #h1 = createMatrixLDPC(N*10) #size 540
    #displayTestLoop(h1,1,loop,N*10)
    #displayTestLoop(h1,2,loop,N*10)
    #displayTestLoop(h1,3,loop,N*10)
    #displayTestLoop(h1,4,loop,N*10)