#!/usr/bin/env python

import scipy


def dok2xyz(dok_matrix):
    if type(dok_matrix) is not scipy.sparse.dok.dok_matrix:
        print('Given matrix is not a dok matrix!')
        return 1
    x = []
    y = []
    z = []
    for i in dok_matrix.items():
        x.append(i[0][0])
        y.append(i[0][1])
        z.append(i[1])
    return x, y, z
