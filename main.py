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

########################################################
#                    Strict version                    #
########################################################

def decode_LDPC_aux_strict(H,S,weight_S,n,break_cpt):
    if break_cpt >= 25:
        return []
    L = []
    # On essaie de supprimer les positions parasites dès le début
    if break_cpt == 1:
        for i in range(n):
            if weightOfCol(mod2(S + getCol(H,i), n//2),n//2) <= weight_S - 5:
                L.append(i)
    else:
        for i in range(n):
            if weightOfCol(mod2(S + getCol(H,i), n//2),n//2) <= weight_S:
                L.append(i)
    S2 = np.zeros(n//2)
    for i in L:
        S2 = S2 + getCol(H,i)
    S2 = mod2(S2, n//2)
    S3 = np.zeros(n//2)
    S3 = mod2(S+S2, n//2)
    if weightOfCol(S3,n//2) == 0:
        return L
    else:
        return decode_LDPC_aux_strict(H,S3,weightOfCol(S3,n//2),n,break_cpt+1)

def decode_LDPC_strict(H,e,n):
    S = mod2(H@(e.T),n//2)
    weight_S = weightOfCol(S,n//2)
    ldpc = decode_LDPC_aux_strict(H,S,weight_S,n,1)
    return ldpc

def test_decode_LDPC_strict(H,weight_e,max_loop,n):
    cpt = 0
    errors = randomErrorVectorGenerator(weight_e,max_loop,n)
    for e in errors:
        if decode_LDPC_strict(H,e,n) == getInd1inCol(e,n):
            cpt+=1
    return cpt/max_loop

########################################################
#                  Display functions                   #
########################################################

def displayTestLoop(H,weight_e,max_loop,n):
    print(f"Test sur {max_loop} vecteurs erreurs de poids {weight_e}: {test_decode_LDPC(H,weight_e,max_loop,n)}")
    return None

def displayTestLoop_strict(H,weight_e,max_loop,n):
    print(f"Test sur {max_loop} vecteurs erreurs de poids {weight_e}: {test_decode_LDPC_strict(H,weight_e,max_loop,n)}")
    return None

def displayTestLoopWithTime(H,weight_e,max_loop,n):
    start = time()
    print(f"Test sur {max_loop} vecteurs erreurs de poids {weight_e}: {test_decode_LDPC(H,weight_e,max_loop,n)}")
    end = time()
    print("Time:",end - start)
    return None

def displayTest(res,weight_e,max_loop):
    print(f"Test sur {max_loop} vecteurs erreurs de poids {weight_e}: {res}")
    return None

########################################################
#                  Experimental tests                  #
########################################################

def opt_weight_search(max_loop,n):
    for j in range(5,25):
        start = time()
        H = matrixFromWeight(j,n)
        print(f"Soit H une matrice de taille {n//2}x{n}")
        print(f"Dont le poids des colonnes est {j}.\n")
        i = 1
        # Arrêt lorsque la proba est inférieur à 0.4
        # Ou si la proba est différente de 1 pour le poids 1
        # (on gagne du temps, puisque'on sait que c'est pas optimal)
        tmp = test_decode_LDPC(H,i,max_loop,n)
        if tmp == 1:
            while tmp >= 0.67:
                displayTest(tmp,i,max_loop)
                i += 1
                tmp = test_decode_LDPC(H,i,max_loop,n)
            displayTest(tmp,i,max_loop)
            print("Time:",time() - start, " secondes \n")
        else:
            displayTest(tmp,i,max_loop)
            print("Time:",time() - start, " secondes \n")
    return None

# Lorsqu'on a trouvé le poids optimal pour le décodage d'une matrice
# de taille (n//2,n) on regarde si on peut améliorer le décodage.

def opt_weight_search_strict(borne_inf,borne_sup,max_loop,n):
    print("Version optimal")
    for j in range(borne_inf,borne_sup):
        start = time()
        H = matrixFromWeight(j,n)
        print(f"Soit H une matrice de taille {n//2}x{n}")
        print(f"Dont le poids des colonnes est {j}.\n")
        i = 1
        tmp = test_decode_LDPC_strict(H,i,max_loop,n)
        while tmp >= 0.67:
            displayTest(tmp,i,max_loop)
            i += 1
            tmp = test_decode_LDPC_strict(H,i,max_loop,n)
        displayTest(tmp,i,max_loop)
        print("Time:",time() - start, " secondes \n")
    return None

if __name__ == "__main__":
    #opt_weight_search(27,2000)
    opt_weight_search_strict(13,21,50,2000)