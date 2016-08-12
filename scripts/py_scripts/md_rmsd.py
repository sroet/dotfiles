#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
import mdtraj as md
import numpy as np
import itertools as itt

def plot_rmsd(target,reference,atom_list=[],fig_name='rmsd'):
    print('Calculating RMSD')
    rmsd = md.rmsd(target,reference,atom_indices=atom_list)

    print('Plotting RMSD to '+fig_name+'.png')
    print(rmsd)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(rmsd)
    ax.set_ylabel('nm')
    ax.set_xlabel('frame')
    ax.set_title(fig_name)
#    plt.show()
    fig.savefig(fig_name+'.png')
#Only call main when this script is the main script

def main(trj,topol,reference):
    target = md.load(trj, top=topol)
    reference = md.load(reference)

    topology = target.topology
    switch1 = topology.select("residue 12 to 13")
    print(switch1)
#    plot_rmsd(target,reference,gtp,'switch1_rmsd')
if __name__ == "__main__":main(sys.argv[1],sys.argv[2],sys.argv[3])
