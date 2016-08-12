#!/usr/bin/env python

import scipy
import matplotlib.pyplot as plt
import math
import warnings
def dok2xyz(dok_matrix):
    x = []
    y = []
    z = []
    for i in dok_matrix.items():
        try:
            x.append(i[0][0])
            y.append(i[0][1])
            z.append(i[1])
        except IndexError:
            raise TypeError('Expected a DOK matrix, got a '+type(dok_matrix))
    return x, y, z

def dok2plt(dok_matrix, figsize=(6,6), dpi=80, cmap='seismic', xmin=None,\
            xmax=None, ymin=None, ymax=None, vmin=-1, vmax=1):
    x, y, z = dok2xyz(dok_matrix)
    xfigsize = list(figsize)[0]
    yfigsize = list(figsize)[1]
    if xmin == None:
        xmin = min(x)
    if xmax == None:
        xmax = max(x)
    if ymin == None:
        ymin = min(y)
    if ymax == None:
        ymax = max(y)

    if ((xmax-xmin)/dpi) > xfigsize:
        old_dpi= dpi
        dpi = int(math.ceil((xmax-xmin)/xfigsize))
        warnings.warn('Increased standard dpi from '+str(old_dpi)+' to '\
                      +str(dpi)+'.')
    if ((ymax-ymin)/dpi) > yfigsize:
        dpi = int(math.ceil((ymax-ymin)/yfigsize))
        old_dpi = dpi
        warnings.warn('Increased standard dpi from '+str(old_dpi)+' to '\
                      +str(dpi)+'.')
    marker_size = max([min([int(xfigsize*dpi/(xmax-xmin)),\
                            int(yfigsize*dpi/(ymax-ymin))]),1])
    print('Using markersize of '+str(marker_size)+' pixels.')
    fig = plt.figure(figsize=figsize, dpi=dpi)
    plt.xlim([xmin,xmax])
    plt.ylim([ymin,ymax])
    plt.scatter(x, y, c=z, cmap=cmap, vmin=vmin, vmax=vmax, marker=',',\
                s=marker_size, lw=0)
    return fig,
