"""
@author: alejandro marquez seco
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
import glob

x_range = 1280
y_range = 800

"""
from __init__
    ROI_center = [656, 395] #in pixels
    ROI_radius = 408

"""

def plot_vortex(Y, X, U, V,filename):
    speed = np.sqrt(U**2 + V**2)

    fig = plt.figure(figsize=(10, 5))
    gs = gridspec.GridSpec(nrows=1, ncols=2)

    # Varying color along a streamline
    ax1 = fig.add_subplot(gs[0, 0])
    strm = ax1.streamplot(X, Y, U, V, color=np.sqrt((U**2)+(V**2)), linewidth=2, cmap='Blues')
    coly = fig.colorbar(strm.lines)
    coly.ax.set_ylabel('Modulus Velocity')
    ax1.set_title('Varying Color')
    ax1.set_aspect('equal')
    ax1.set_xlim([00,x_range])
    ax1.set_ylim([0,y_range])
    ax1.invert_yaxis()
    
    #  Varying line width along a streamline
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_aspect('equal')
    lw = 5*speed / speed.max()
    ax2.streamplot(X, Y, U, V, density=0.6, color='k', linewidth=lw)
    ax2.set_title('Varying Line Width')
    ax2.set_xlim([00,x_range])
    ax2.set_ylim([0,y_range])
    ax2.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(filename+'_'+str(x_range)+'.png')
    
    