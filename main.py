#!/usr/bin/env python

import argparse
import numpy as np
from scipy.sparse.linalg import eigs
from time import perf_counter

def setup_argparse():

    parser = argparse.ArgumentParser(
        description="Silly numpy perf tests"
    )

    # Required
    parser.add_argument("--matsize", type=int, required=True, help="base matrix row size")
    parser.add_argument("--nrand", type=int, required=True, help="number of runs per benchmark")
    parser.add_argument("--ndims", type=int, required=False, default=3, help="number of sizes to check")

    return parser.parse_args()

def main():

    args = setup_argparse()

    NDIMS = args.ndims
    DIMS1 = [args.matsize*(i+1) for i in range(NDIMS)]
    # Increase second dim to avoid numpy's Cholesky choking
    # on positive semidefinite
    DIMS2 = [(args.matsize + 1)*(i+1) for i in range(NDIMS)]
    NRAND = args.nrand

    np.show_config()

    # Why do people like this language? LOOK AT THIS!
    AA = np.atleast_2d(np.arange(1,501))
    BB = np.sin(AA.T + AA**2).astype(np.double)

    tt = perf_counter()
    xx, vv = np.linalg.eig(BB)
    tt = perf_counter() - tt
    print(f'eig:  {tt:8.4f} sec')
    print(xx[:2])

    tmult = np.zeros((NDIMS, NRAND))
    teigh = np.zeros((NDIMS, NRAND))
    teigs = np.zeros((NDIMS, NRAND))
    tchol = np.zeros((NDIMS, NRAND))

    for kk in range(NDIMS):
        DIM1 = DIMS1[kk]
        DIM2 = DIMS2[kk]

        print('')
        print(f'--- dim(A) = {DIM1:5d} x {DIM2:5d} ---')
        for nn in range(NRAND):
            AA = np.random.randn(DIM1, DIM2).astype(np.double)

            tt = perf_counter()
            BB = np.matmul(AA, AA.T)
            tmult[kk,nn] = perf_counter() - tt

            tt = perf_counter()
            xx, vv = np.linalg.eigh(BB)
            teigh[kk,nn] = perf_counter() - tt

            tt = perf_counter()
            xx, vv = eigs(BB)
            teigs[kk,nn] = perf_counter() - tt

            tt = perf_counter()
            CC = np.linalg.cholesky(BB)
            tchol[kk,nn] = perf_counter() - tt

        print('B = A*A^T: {0:8.4f} +/- {1:8.4f} sec'.format(tmult[kk,:].mean(), tmult[kk,:].std()))
        print('eigh(B):   {0:8.4f} +/- {1:8.4f} sec'.format(teigh[kk,:].mean(), teigh[kk,:].std()))
        print('eigs(B):   {0:8.4f} +/- {1:8.4f} sec'.format(teigs[kk,:].mean(), teigs[kk,:].std()))
        print('chol(B):   {0:8.4f} +/- {1:8.4f} sec'.format(tchol[kk,:].mean(), tchol[kk,:].std()))


if __name__ == "__main__":
    main()
