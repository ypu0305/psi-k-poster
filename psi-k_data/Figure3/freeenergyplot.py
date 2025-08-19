#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 16:12:23 2025

@author: ypu
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from ase.io import read, write
from ase import Atoms
from ase.neighborlist import neighbor_list
structure = 'AA08'
filename_H = '/home/ypu/Documents/github/psi-k-poster/psi-k_data/Figure3/data/traj/2Dhistogram_'+structure+'.txt'
H =  np.loadtxt(filename_H)
filename_xedges = '/home/ypu/Documents/github/psi-k-poster/psi-k_data/Figure3/data/traj/x_edges_'+structure+'.txt'
filename_yedges = '/home/ypu/Documents/github/psi-k-poster/psi-k_data/Figure3/data/traj/y_edges_'+structure+'.txt'
x_edges = np.loadtxt(filename_xedges)
y_edges = np.loadtxt(filename_yedges)
filename_carbon_up='/home/ypu/Documents/github/psi-k-poster/psi-k_data/Figure3/data/traj/carbon_position_up_'+structure+'.txt'
filename_carbon_down='/home/ypu/Documents/github/psi-k-poster/psi-k_data/Figure3/data/traj/AA08/carbon_position_down_'+structure+'.txt'
carbon_positions_up = np.loadtxt(filename_carbon_up)
carbon_positions_down = np.loadtxt(filename_carbon_down)
filename_bond_up='/home/ypu/Documents/github/psi-k-poster/psi-k_data/Figure3/data/traj/AA08/bond_list_up_'+structure+'.txt'
filename_bond_down='/home/ypu/Documents/github/psi-k-poster/psi-k_data/Figure3/data/traj/AA08/bond_list_down_'+structure+'.txt'
bond_up=np.loadtxt(filename_bond_up)
bond_down=np.loadtxt(filename_bond_down)
i_list_up=bond_up[:,0].astype(int)
j_list_up=bond_up[:,1].astype(int)
i_list_down=bond_down[:,0].astype(int)
j_list_down=bond_down[:,1].astype(int)
#############################################################
fig = plt.figure(1,figsize=(7.5, 6))
contourplot2 = fig.subplots()
X, Y = np.meshgrid((x_edges[:-1] + x_edges[1:]) / 2, (y_edges[:-1] + y_edges[1:]) / 2)
# Define contour levels based on probability values
levels = np.linspace(H.min(), H.max(), 15)  
cmap = plt.cm.RdYlGn_r  # Reverse RdYlGn (High=Red, Low=Green)
new_colors = cmap(np.linspace(1, 0, 256))

######################################################################
custom_cmap = mcolors.ListedColormap(new_colors)  # Create new colormap
contour_filled = contourplot2.contourf(X, Y, H.T, levels=levels, cmap=custom_cmap)  # Transpose H to match axes
contour_lines = contourplot2.contour(X, Y, H.T, levels=levels, colors='black', linewidths=0.5)
cbar = plt.colorbar(contour_filled, ax=contourplot2)
cbar.set_label('∆G / meV', fontsize=14)
for i, j in zip(i_list_up, j_list_up):
    x_coords = [carbon_positions_up[i][0], carbon_positions_up[j][0]]
    y_coords = [carbon_positions_up[i][1], carbon_positions_up[j][1]]
    contourplot2.plot(x_coords, y_coords, color='black', linewidth=1.5)
for i, j in zip(i_list_down, j_list_down):
    x_coords = [carbon_positions_down[i][0], carbon_positions_down[j][0]]
    y_coords = [carbon_positions_down[i][1], carbon_positions_down[j][1]]
    contourplot2.plot(x_coords, y_coords, color='blue', linewidth=1.5, linestyle='--')
contourplot2.set_xlim(0.5,8.2)
contourplot2.set_ylim(0.5,9.2)
contourplot2.set_xlabel(r'X ($\AA$)')
contourplot2.set_ylabel(r'Y ($\AA$)')
contourplot2.set_title(f'Free energy profile of {structure} (600K)', y=1)
