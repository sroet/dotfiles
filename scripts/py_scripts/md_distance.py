#!/usr/bin/env python

import matplotlib.pyplot as plt
import mdtraj as md
import numpy as np

def md_distance(trj, pair_list, mode = 'raw'):
    distances = md.compute_distances(trj, pair_list)
    if mode == 'min':
        min_dist = []
        for i in distances:
            min_dist.append(min(i))
        return min_dist,
    elif mode == 'raw':
        return distances,

    elif mode == 'max':
        max_dist = []
        for i in distances:
            max_dist.append(max(i))
        return max_dist,

def gen_pairs(residuelist):
    atoms1 = residuelist[0]
    atoms2 = residuelist[1]
    pair_list = []
    for i,e1 in enumerate(atoms1):
        for j,e2 in enumerate(atoms2):
            pair_list.append([e1,e2])
    return pair_list

def main():
    run = md.load('vis-md_combined.xtc', top='vis-md_combined.pdb')
    topology = run.topology

    atom_list = [454,455,502,503,2670,2647,2651,2626,945,944,943,958,959,960]

    for i in atom_list:
        print(topology.atom(i))

    pair_list_33_gtp = [[2626,945],[2626,944],[2626,960],[2626,959]]
    min_dist_33_gtp = md_distance(run,pair_list_33_gtp)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(min_dist_33_gtp)
    fig.savefig('min_dist_30_gtp.png')
#Only call main when this script is the main script
if __name__ == "__main__":main()
