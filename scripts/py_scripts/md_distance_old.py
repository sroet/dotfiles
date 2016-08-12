#!/usr/bin/env python

import matplotlib.pyplot as plt
import mdtraj as md
import numpy as np

def main():
    run = md.load('vis-md_combined.xtc', top='vis-md_combined.pdb')
    topology = run.topology

    atom_list = [454,455,502,503,2670,2647,2651,2626,945,944,943,958,959,960]

    for i in atom_list:
        print(topology.atom(i))

    pair_list_33_gtp = [[2626,945],[2626,944],[2626,960],[2626,959]]
    dist_33_gtp = md.compute_distances(run,pair_list_33_gtp)
    min_dist_33_gtp = []
    for i in dist_33_gtp:
        min_value = min(i)
        min_dist_33_gtp.append(min_value)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(min_dist_33_gtp)
    savefig(min_dist_30_gtp.png)
#Only call main when this script is the main script
if __name__ == "__main__":main()
