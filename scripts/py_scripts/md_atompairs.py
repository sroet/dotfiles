#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
import mdtraj as md
import numpy as np
import itertools as itt

def plot_dist(trj,topol,atom_lists=[[2626],[944,945,960,959]]):
    run = md.load(trj, top=topol)
    topology = run.topology
    residue_list = []
    for i in range(0,len(atom_lists)):
        for j in atom_lists[i]:
            residue_name = topology.atom(j).residue
            if len(residue_list) <= i:
                residue_list.append([residue_name])
            else:
                if residue_name not in residue_list[i]:
                    residue_list[i].append(residue_name)
#    print(residue_list)
    fig_name = ''
    for res in residue_list:
#        if len(res) == 1:
#            fig_name = fig_name + res[0]
#        else:
#            fig_name = fig_name + ','.join(res[:])
        res_name = str(res).strip('[]')
        res_name = res_name.replace(' ', '')
        fig_name = fig_name + res_name
        if res != residue_list[-1]:
            fig_name = fig_name + '_'

    pair_list = list(itt.product(atom_lists[0],atom_lists[1]))
#    print(pair_list)
#    pair_list_33_gtp = [[2626,945],[2626,944],[2626,960],[2626,959]]
    dist = md.compute_distances(run,list(pair_list))
#    print(dist)
    min_dist = np.amin(dist, axis = 1)
#    for i in dist:
#        min_value = min(i)
#        min_dist.append(min_value)

    print('Plotting '+fig_name)


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(min_dist)
    ax.set_ylabel('nm')
    ax.set_xlabel('frame')
    ax.set_title(fig_name)
#    plt.show()
    fig.savefig(fig_name+'.png')
#Only call main when this script is the main script

def main(traj,top):
    res30 = [454,455]
    res33 = [502,503]
    res62 = [944,945]
    res63 = [960,959]
    mg = [2670]
    gtp = [2647,2651]
    pg = [2626]
    dist_list = [[res30,gtp],[res33,mg],[res33,gtp],[res62+res63,pg]]
    for i in dist_list:
        plot_dist(traj,top,i)
if __name__ == "__main__":main(sys.argv[1],sys.argv[2])
