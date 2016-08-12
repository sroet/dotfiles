#!/usr/bin/env python

import mdtraj as md
import numpy as np

def dihedral_rmsd(trj, ca_list = []):
    phi_indices, phi_angles = md.compute_phi(trj)
    psi_indices, psi_angles = md.compute_psi(trj)
    phi_indexlist = []
    psi_indexlist = []
    for i in ca_list:
        phi_itemindex, dump = np.where(phi_indices == i)
        phi_indexlist.append(phi_itemindex[0])
        psi_itemindex, dump = np.where(psi_indices == i)
        psi_indexlist.append(psi_itemindex[0])

    rmsd_data_raw = np.zeros(shape = [len(phi_indexlist)+len(psi_indexlist),\
                                      len(phi_angles)])

    for i,j in enumerate(phi_indexlist):
        rmsd_data_raw[i*2,:] = phi_angles[:,j]
    for i,j in enumerate(psi_indexlist):
        rmsd_data_raw[(i*2+1),:] = psi_angles[:,j]

    temp_array = np.zeros(shape=[len(rmsd_data_raw),len(rmsd_data_raw[0])])
    for i in range(temp_array.shape




