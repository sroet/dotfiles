#!/usr/bin/env python
# coding: utf-8

import mdtraj as md
import numpy as np
import matplotlib.pyplot as plt



def dihedral_rmsd(trj, ca_atoms, refframe = None, mode = 1):
    if refframe is None:
        refframe = trj[0]

    if len(refframe.xyz[0]) != len(trj.xyz[0]):
        raise Exception('Refframe has not the same amount of atoms as trj!')



    phi_indices, phi_angles = md.compute_phi(trj)
    psi_indices, psi_angles = md.compute_psi(trj)
    ref_phi_indices, ref_phi_angles = md.compute_phi(refframe)
    ref_psi_indices, ref_psi_angles = md.compute_psi(refframe)


    phi_indexlist = []
    psi_indexlist = []
    ref_phi_indexlist = []
    ref_psi_indexlist = []
    for i in ca_atoms:
        phi_itemindex, dump = np.where(phi_indices == i)
        phi_indexlist.append(phi_itemindex[0])
        psi_itemindex, dump = np.where(psi_indices == i)
        psi_indexlist.append(psi_itemindex[0])
        ref_phi_itemindex, dump = np.where(ref_phi_indices == i)
        ref_phi_indexlist.append(phi_itemindex[0])
        ref_psi_itemindex, dump = np.where(ref_psi_indices == i)
        ref_psi_indexlist.append(psi_itemindex[0])

    if mode == 1 or mode == 3:

        rmsd_data = np.zeros(shape=[len(phi_indexlist)+len(psi_indexlist),
                                    len(phi_angles)])
        ref_rmsd_data = np.zeros(shape=[len(phi_indexlist)+len(psi_indexlist),
                                    len(phi_angles)])


        for i, j in enumerate(phi_indexlist):
            rmsd_data[i*2, :] = phi_angles[:, j]
        for i, j in enumerate(psi_indexlist):
            rmsd_data[(i*2+1), :] = psi_angles[:, j]
        for i, j in enumerate(ref_phi_indexlist):
            ref_rmsd_data[i*2, :] = ref_phi_angles[:, j]
        for i, j in enumerate(ref_psi_indexlist):
            ref_rmsd_data[(i*2+1), :] = ref_psi_angles[:, j]

        temp_array = np.zeros(shape=[len(rmsd_data), len(rmsd_data[0])])
        for i in range(temp_array.shape[1]):
            temp_array[:, i] = ref_rmsd_data[:, 0]

        rmsd_data_dif = rmsd_data - temp_array
        rmsd_data_abs = np.absolute(rmsd_data_dif)
        over_pi = np.where(rmsd_data_abs > np.pi)
        for i, j in enumerate(over_pi[0]):
            rmsd_data_abs[j, over_pi[1][i]] -= np.pi

        rmsd = np.zeros(shape=[len(rmsd_data_abs[0])])
        rmsd = np.sum(rmsd_data_abs, axis=0)
        rmsd = rmsd/len(rmsd_data_abs)

    if mode == 2 or  mode == 3:
        rmsd_data_phi = np.zeros(shape=[len(phi_indexlist), len(phi_angles)])
        rmsd_data_psi = np.zeros(shape=[len(psi_indexlist), len(psi_angles)])
        ref_rmsd_data_phi = np.zeros(shape=[len(ref_phi_indexlist),
                                            len(ref_phi_angles)])
        ref_rmsd_data_psi = np.zeros(shape=[len(ref_psi_indexlist),
                                            len(ref_psi_angles)])

        for i, j in enumerate(phi_indexlist):
            rmsd_data_phi[i, :] = phi_angles[:, j]
        for i, j in enumerate(psi_indexlist):
            rmsd_data_psi[i, :] = psi_angles[:, j]

        for i, j in enumerate(ref_phi_indexlist):
            ref_rmsd_data_phi[i, :] = ref_phi_angles[:, j]
        for i, j in enumerate(ref_psi_indexlist):
            ref_rmsd_data_psi[i, :] = ref_psi_angles[:, j]

        temp_array_phi = np.zeros(shape=[len(rmsd_data_phi),
                                         len(rmsd_data_phi[0])])
        temp_array_psi = np.zeros(shape=[len(rmsd_data_psi),
                                         len(rmsd_data_psi[0])])

        for i in range(temp_array_phi.shape[1]):
            temp_array_phi[:, i] = ref_rmsd_data_phi[:, 0]
        for i in range(temp_array_psi.shape[1]):
            temp_array_psi[:, i] = ref_rmsd_data_psi[:, 0]

        rmsd_data_dif_psi = rmsd_data_psi - temp_array_psi
        rmsd_data_dif_phi = rmsd_data_phi - temp_array_phi
        rmsd_data_abs_psi = np.absolute(rmsd_data_dif_psi)
        rmsd_data_abs_phi = np.absolute(rmsd_data_dif_phi)

        over_pi_psi = np.where(rmsd_data_abs_psi > np.pi)
        over_pi_phi = np.where(rmsd_data_abs_phi > np.pi)


        for i, j in enumerate(over_pi_psi[0]):
            rmsd_data_abs_psi[j, over_pi_psi[1][i]] -= np.pi
        for i, j in enumerate(over_pi_phi[0]):
            rmsd_data_abs_phi[j, over_pi_phi[1][i]] -= np.pi

        rmsd_phi = np.zeros(shape=[len(rmsd_data_abs_phi[0])])
        rmsd_psi = np.zeros(shape=[len(rmsd_data_abs_psi[0])])
        rmsd_phi = np.sum(rmsd_data_abs_phi, axis=0)
        rmsd_psi = np.sum(rmsd_data_abs_psi, axis=0)

        rmsd_phi = rmsd_phi/len(rmsd_data_abs_phi)
        rmsd_psi = rmsd_psi/len(rmsd_data_abs_psi)
    if mode == 1:
        return(rmsd)
    if mode == 2:
        return(rmsd_phi,rmsd_psi)
    if mode == 3:
        return(rmsd, rmsd_phi, rmsd_psi)

def main():
    test_xtc = 'test_show/vis-md.xtc'
    test_pdb = 'test_show/vis-md.pdb'
    trj = md.load(test_xtc, top=test_pdb)
#    reference = md.load(test_pdb)
    topology = trj.topology
    ca_switch1 = topology.select('resSeq 30 to 38 and name CA')
    rmsd = dihedral_rmsd(trj, ca_switch1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(rmsd)
    ax.set_ylabel('radian')
    ax.set_xlabel('frame')
    ax.set_title('rmsd switch 1 dihedrals')
    plt.show


if __name__ == '__main__':
    main()
