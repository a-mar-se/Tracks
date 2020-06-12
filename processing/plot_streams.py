"""
@author: alejandro marquez seco
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
import glob


"""
from __init__
    ROI_center = [656, 395] #in pixels
    ROI_radius = 408

"""
# Plot ranges
x_range = 1280
y_range = 800


mesh_size = 10
folder =' C:/Users/Alejandro/Documents/UNEX/Clus/Chirality_plots/'
codigo = '*'+str(mesh_size)+'_binsx*'


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
    plt.show()
    
    
def read_csv(file):
    M = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if len(row)>0:
                M.append(row)
    if len(M)==1:
        M = np.array(M[0])
    return np.asarray(M)




files = glob.glob(codigo)
for filename in files:
    filename = filename.split(str(mesh_size)+'_binsx')[0]
    
    # Read the mesh in x and Y and the average velocities per cell Vx and Vy 
    X = np.array(read_csv(filename+str(mesh_size)+'_binsx.csv'),dtype=float)
    Y = np.array(read_csv(filename+str(mesh_size)+'_binsy.csv'),dtype=float)
    U = np.array(read_csv(filename+str(mesh_size)+'_vx.csv'),dtype=float)
    V = np.array(read_csv(filename+str(mesh_size)+'_vy.csv'),dtype=float)

    filename = filename.split('_binsx.csv')[0]
    plot_vortex( Y, X, U, V, filename)