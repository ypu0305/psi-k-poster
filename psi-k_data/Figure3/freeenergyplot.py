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

stride = 1
structure = 'AA08'
T=600
cell = np.array([
    [8.55600, 0.00000, 0.00000],
    [0.00000, 9.88000, 0.00000],
    [0.00000, 0.00000, 30.0000]
])
# Apply the cell
filename='/home/ypu/Documents/Data/daint/PIMD_result250313/'+structure+'/'+str(int(T/100-1))+'_simulation.pos_00.extxyz'
atoms_list = read(filename,'::'+str(stride))
carbon_x_up = []
carbon_y_up = []
carbon_x_down = []
carbon_y_down = []
carbon_positions = []
carbon_indices = []
if len(carbon_positions) == 0:
    carbon_indices = [i for i, atom in enumerate(atoms_list[0]) if atom.symbol == 'C']
    carbon_positions = atoms_list[0].get_positions()[carbon_indices]
    carbon_positions = [pos for pos in carbon_positions if pos[0] < 12 and pos[1] < 15]
    carbon_positions_up = [pos for pos in carbon_positions if pos[2] > 15]
    carbon_positions_down = [pos for pos in carbon_positions if pos[2] < 15]
    for pos in carbon_positions_up:
        carbon_x_up.append(pos[0])
        carbon_y_up.append(pos[1])
    for pos in carbon_positions_down:
        carbon_x_down.append(pos[0])
        carbon_y_down.append(pos[1])
carbon_atoms_up = Atoms('C' * len(carbon_positions_up), positions=carbon_positions_up, cell=cell)
i_list_up, j_list_up, _ = neighbor_list('ijS', carbon_atoms_up, cutoff=1.45)
carbon_atoms_down = Atoms('C' * len(carbon_positions_down), positions=carbon_positions_down, cell=cell)
i_list_down, j_list_down, _ = neighbor_list('ijS', carbon_atoms_down, cutoff=1.45)
###################################################################################3
x_data=[]
y_data=[]
for atoms in atoms_list:
    atoms.set_cell(cell)
    atoms.wrap()
    oxygen_list = [atom.position for atom in atoms if atom.symbol == 'O']
    for position in oxygen_list:
        x_data.append(position[0])
        y_data.append(position[1])

fig = plt.figure(1,figsize=(7.5, 6))
contourplot2 = fig.subplots()
# Define 2D histogram bins
x_bins = np.linspace(0, 8.5, 30)  # X bin edges
y_bins = np.linspace(0, 9.5, 30)  # Y bin edges
# Compute the 2D histogram (frequency count)
H, x_edges, y_edges = np.histogram2d(x_data, y_data, bins=[x_bins, y_bins])
H += 0.6
# Normalize histogram to get probability density
H = H / np.sum(H)  # Convert counts to probabilities
H = np.log(H)
H = -H*T*8.62e-5*1000
H = H-H.min()
# Convert bin edges to centers for plotting
X, Y = np.meshgrid((x_edges[:-1] + x_edges[1:]) / 2, (y_edges[:-1] + y_edges[1:]) / 2)
# Define contour levels based on probability values
levels = np.linspace(H.min(), H.max(), 15)  
# levels = levels[:-2]
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
contourplot2.set_xlim(0.5,8.5)
contourplot2.set_ylim(0.5,9.5)
contourplot2.set_xlabel(r'X ($\AA$)')
contourplot2.set_ylabel(r'Y ($\AA$)')
contourplot2.set_title(f'Free energy profile of {structure} ({T}K)', y=1)