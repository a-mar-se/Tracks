"""
@author: alejandro marquez seco
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
from stream_lines import plot_vortex

"""
from __init__
    ROI_center = [656, 395] #in pixels
    ROI_radius = 408

"""


def save_avg_vels(folder,filename):  

    # Defining mesh size, pixel limits (image size in pixels) and mesh cell width and height
    mesh_size = 2
    shape=(mesh_size,mesh_size)
    max_x = 1280
    max_y = 800
    min_x = 00
    min_y = 00
    intervalx = (max_x-min_x)/(mesh_size)
    intervaly = (max_y-min_y)/(mesh_size)

    # Getting the identification code of each file
    experiment_idd = filename.split('_roi_velocities.pkl')[0]
    experiment_id = experiment_idd.split('\\')[-1]
    experiment_id = experiment_id.split('/')[-1]
    experiment_id +='_'+str(mesh_size)
           
    # Extracting data       
    new_dict = pd.read_pickle(str(filename), compression='xz')
    XX = new_dict['vx']
    YY = new_dict['vy']
    x = new_dict['x']
    y = new_dict['y']
    
    # Getting mesh points
    bins_X = np.linspace(min_x, max_x, mesh_size+1, endpoint= True)
    bins_XX = np.linspace(min_x+intervalx/2., max_x-intervalx/2., mesh_size,endpoint= True)
    bins_Y = np.linspace(min_y, max_y, mesh_size+1,endpoint= True)
    bins_YY = np.linspace(min_y+intervaly/2., max_y-intervaly/2., mesh_size,endpoint= True)
  
    # Defining matrixes that will contain the velocities and number of occurrences on a mesh cell
    VX = np.zeros(shape, dtype=float)
    VY = np.zeros(shape, dtype=float)
    counts = np.zeros(shape, dtype=float)

    # Summing all velocities contained in a cell
    for i in range(0,len(x)):
        for ranges_y in range(0,len(bins_Y)-1):
            for ranges_x in range(0,len(bins_X)-1):
                if bins_X[ranges_x]<x[i]<bins_X[ranges_x+1] and bins_Y[ranges_y]<y[i]<bins_Y[ranges_y+1]:
                    VX[ranges_y][ranges_x] += XX[i]
                    VY[ranges_y][ranges_x]+= YY[i]
                    counts[ranges_y][ranges_x] += 1
      
    # Averaging the velocities in a cell
    for ranges_y in range(0,len(bins_Y)-1):
        for ranges_x in range(0,len(bins_X)-1):
            if counts[ranges_y][ranges_x]>0:
                VX[ranges_y][ranges_x] = VX[ranges_y][ranges_x]/counts[ranges_y][ranges_x]
                VY[ranges_y][ranges_x] = VY[ranges_y][ranges_x]/counts[ranges_y][ranges_x] 
    
    # Saving the mesh and velocities into csv files for later access
    with open(experiment_id+'_vx.csv', mode='w') as emp_file:
        emp_writer = csv.writer(emp_file, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in VX:
            emp_writer.writerow(i)
            
    with open(experiment_id+'_vy.csv', mode='w') as emp_file:
        emp_writer = csv.writer(emp_file, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in VY:
            emp_writer.writerow(i) 
            
    with open(experiment_id+'_binsx.csv', mode='w') as emp_file:
        emp_writer = csv.writer(emp_file, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        emp_writer.writerow(bins_XX)
            
    with open(experiment_id+'_binsy.csv', mode='w') as emp_file:
        emp_writer = csv.writer(emp_file, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        emp_writer.writerow(bins_YY)
   
    # Getting the plot and saving it into a png file
    plot_vortex(bins_YY, bins_XX, VX, VY, experiment_id)


# Folder that contains the files to be processed and this file
folder = 'C:/Users/Alejandro/Documents/UNEX/procesado/renivelado/'

# When running on cluster:
# folder = '/mnt/beegfs/alejandroms/Chirality_plots/'

# Code to be found
codigo = '*_roi_velocities.pkl*'
files = glob.glob(codigo)

for file in files:
    save_avg_vels(folder,file)
    
    