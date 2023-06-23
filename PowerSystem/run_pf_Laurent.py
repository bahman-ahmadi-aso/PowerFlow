from numpy import ones, r_, conj
from scipy.sparse import csr_matrix, coo_matrix, bmat, csc_matrix, vstack
from scipy.sparse.linalg import spsolve

import pandas as pd
import numpy as np

def run_pf_Laurent(System_Data_Nodes,PP,QQ, Sbase, Yds, Ydd, V_0):
    nb = System_Data_Nodes.shape[0]  ## number of buses


    P = PP / Sbase
    Q = QQ/ Sbase

    S_nom = (P + 1j * Q).reshape(-1, ).tolist()
    alpha_P = System_Data_Nodes[System_Data_Nodes.Tb != 1].Pct.values.reshape(-1, ).tolist()
    alpha_I = System_Data_Nodes[System_Data_Nodes.Tb != 1].Ict.values.reshape(-1, ).tolist()
    alpha_Z = System_Data_Nodes[System_Data_Nodes.Tb != 1].Zct.values.reshape(-1, ).tolist()


    A = csr_matrix(np.diag(np.multiply(alpha_P, 1. / np.conj(V_0) ** (2)) * np.conj(S_nom)))  # Needs update
    D = csr_matrix((np.multiply(np.multiply(2, alpha_P), 1. / np.conj(V_0)) * np.conj(S_nom)).reshape(-1, 1))  # Needs update

    B = csr_matrix(np.diag(np.multiply(alpha_Z, np.conj(S_nom))) + Ydd)             # Constant
    C = csr_matrix(Yds + (np.multiply(alpha_I, np.conj(S_nom))).reshape(nb-1, 1))   # Constant

    M11 = np.real(A) - np.real(B)
    M12 = np.imag(A) + np.imag(B)
    M21 = np.imag(A) - np.imag(B)
    M22 = -np.real(A) - np.real(B)
    N1 = np.real(C) + np.real(D)
    N2 = np.imag(C) + np.imag(D)
    M = csr_matrix(bmat([[M11, M12], [M21, M22]]))
    N = vstack([N1,N2])
    V = spsolve(M, N)

    return np.add(V[0:nb-1],1j*V[nb-1:])
