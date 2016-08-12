#! /usr/bin/env python3
# coding: utf-8

import itertools as itt
import mdtraj as md
import numpy as np
import matplotlib.pyplot as plt
from md_distance import md_distance
from refframes import refframe_switch1
from refframes import refframe_switch2



def main(source, run, chunk_size=100):
    if source == 'vreede':
        current_dir = '/home/sanderroet/Ras-JV/'+run+'/analysis/'
        name = 'vreede_'+run
    elif source == 'carbon':
        current_dir = '/home/sanderroet/carbon/kras_100ns/'+run+'/analysis/'
        name = 'carbon_'+run
    elif source == 'cartesius':
        current_dir = '/home/sanderroet/cartesius/vreede_'+run+\
            '_continue/analysis/'
        name = 'vreede_'+run+'_continue'
    xtc = current_dir + 'vis-md.xtc'
    pdb = current_dir + 'vis-md.pdb'
    chunk = 0
    for trj in md.iterload(xtc, top = pdb, chunk = chunk_size):
        print('Running chunk '+str(chunk)+' of '+source+' '+run, end='.\r')
        if chunk == 0:
            topology = trj.topology

            gly60 = topology.select('protein and (resSeq 60)')
            gly12 = topology.select('protein and (resSeq 12)')
            gln61 = topology.select('protein and resSeq 61 and not backbone and not name H')
            arg68 = topology.select('protein and resSeq 68 and name O')
            met72 = topology.select('protein and resSeq 72 and name H')
            GTP = topology.select('((resname GTP) and not element H) or element Mg')
            glu63 = topology.select('protein and (resSeq 63) and name CG')
            glu62 = topology.select('protein and (resSeq 62) and name CG')
            switch2 = topology.select('protein and(resSeq 61 to 66)')

            pairs = [
                     [gly60,gly12],
                     [arg68,met72],
                     [gln61,gly12],
                     [glu63,GTP],
                     [glu62,GTP]
                    ]
            pair_list = []
            for i in pairs:
                pair_list.append(list(itt.product(i[0],i[1])))
            results_dist = []
            results_COM = []

        for i, e in enumerate(pair_list):
            if chunk == 0:
                results_dist.extend(md_distance(trj, e , mode = 'min'))
            else:
                temp, = md_distance(trj, e, mode = 'min')
                results_dist[i] += temp
                #results_dist[i].append(md_distance(trj, e , mode = 'min'))

        GTP_COM = topology.select('resname GTP or element Mg')
        gtp_trj = trj.atom_slice(GTP_COM)
        switch2_trj = trj.atom_slice(switch2)
        gtp_center = md.compute_center_of_mass(gtp_trj)
        switch2_center = md.compute_center_of_mass(switch2_trj)

        distances = gtp_center - switch2_center
        for i in distances:
            temp = (i[0]**2) + (i[1]**2) + (i[2]**2)
            results_COM.append(temp**(0.5))
        chunk += 1
    print('\x1b[2K\r', end='')
    print('Plotting '+source+' '+run+'.', end='\r')
    temp = -1
    foo = -1
    for i in range(len(results_dist[0])):
        if results_dist[0][i] >0.6 and results_dist[2][i] > 0.8\
           and results_dist[3][i] > 1.0 and results_dist[4][i] > 1.0 \
                and results_COM[i] > 1.975 and temp == -1:# and results_dist[1][i] >0.52:
            print(source+' '+run+' has an open state in frame '+str(i))
            temp = i
            foo = -1
        elif (results_dist[0][i] < 0.3 or results_dist[2][i] < 0.3\
           or results_dist[3][i] < 0.6 or results_dist[4][i] < 0.6) \
                and results_COM[i] < 1.6 and foo == -1:# and results_dist[1][i] >0.52:
            print(source+' '+run+' has an closed state in frame '+str(i))
            foo = i
            temp = -1
    plots = (len(results_dist)+1)/2
    if int(plots) != plots:
        plots = int(plots)+1
    else:
        plots = int(plots)
    fig, axarr = plt.subplots(plots,2, figsize = (12,6*plots))
    # print(plots)
    for i, e in enumerate(results_dist):
        y = e
        x = range(len(e))
        lbl = str(topology.atom(pairs[i][0][0]).residue) + '--' + str(topology.atom(pairs[i][1][0]).residue)
        try:
            start, stop = refframe_switch2[name]
        except KeyError:
            start = []
            stop = []
        if plots > 1:
            a = int(i/2)
            b = i-a*2
            axarr[a, b].plot(x,y, label = lbl)


            for i, j in enumerate(start):
                x = range(j,stop[i])
                y = e[j:stop[i]]
                axarr[a,b].plot(x,y, c='green')
            x = range(len(e))
            if lbl == 'GLY60--GLY12':
                refline_open = 0.6 #0.67
                refline_closed = 0.3
            elif lbl == 'ARG68--MET72':
                refline_open = 0.52 #0.5
                refline_closed = 0.25
            elif lbl == 'GLN61--GLY12':
                refline_open = 0.8 #0.85
                refline_closed = 0.3
            elif lbl == 'GLU63--GTP201':
                refline_open = 1.0 #1.0
                refline_closed = 0.6
            elif lbl == 'GLU62--GTP201':
                refline_open = 1.0 #1.15
                refline_closed = 0.6
            else:
                refline_open = 0.5
                refline_closed = 0.5
            axarr[a, b].plot([x[0],x[-1]],[refline_open, refline_open], c='red')
            axarr[a, b].plot([x[0],x[-1]],[refline_closed, refline_closed], c='red')
            axarr[a,b].set_ylim([0.0,2.0])
            axarr[a,b].set_ylabel('nm')
            axarr[a,b].set_xlabel('frame')
            axarr[a,b].set_title(source+'_'+run)
            axarr[a,b].legend()
        else:
            a = i
            axarr[a].plot(x,y, label = lbl)
            for i, j in enumerate(start):
                x = range(j,stop[i])
                y = e[j:stop[i]]
                axarr[a].plot(x,y, c='green')
            x = range(len(e))
            axarr[a].plot([x[0],x[-1]],[0.6,0.6], c='red')
            axarr[a].plot([x[0],x[-1]],[0.5,0.5], c='red')
            axarr[a].set_ylim([0.0,2.0])
            axarr[a].set_ylabel('nm')
            axarr[a].set_xlabel('frame')
            axarr[a].set_title(source+'_'+run)
            axarr[a].legend()
    for i, e in enumerate([results_COM]):
        y = e
        x = range(len(e))
        b += 1
        if b >= len(axarr[0]):
            b = 0
            a += 1
        if i == 0:
            lbl = 'COM_GTP_switch2'
            try:
                start, stop = refframe_switch2[name]
            except KeyError:
                start = []
                stop = []
        axarr[a,b].plot(x,y, label = lbl)
        for i, j in enumerate(start):
            x1 = range(j,stop[i])
            y1 = e[j:stop[i]]
            axarr[a,b].plot(x1,y1, c='green')
        axarr[a,b].plot([x[0],x[-1]],[1.975,1.975], c='red')
        axarr[a,b].plot([x[0],x[-1]],[1.6,1.6], c='red')
        axarr[a,b].set_ylim([1.5,2.5])
        axarr[a,b].set_ylabel('nm')
        axarr[a,b].set_xlabel('frame')
        axarr[a,b].set_title('COM_switch2_'+source+'_'+run)
        axarr[a,b].legend()
    fig.savefig(current_dir+'proposed_switch2.png')
    print('\x1b[2K\r', end='')
if __name__ == '__main__':

    for source in ['carbon', 'vreede', 'cartesius']:
        if source == 'carbon' or source == 'vreede':
            run_range = range(4)
        elif source == 'cartesius':
            run_range = [1,3]
        for run_index in run_range:
            run = 'run'+str(run_index)
            #print('Running '+source+' '+run)
            main(source, run, chunk_size = 4000)
            print('Done with '+source+'-'+run+'.')
