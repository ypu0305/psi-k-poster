import matplotlib.pyplot as plt
import numpy as np

# Sample data
structure='AB08'
potential_energy_file='/home/ypu/Documents/github/psi-k-poster/psi-k_data/Figure2/data/potential_energy/potential_energy_'+structure
diffusion_coefficient_file='/home/ypu/Documents/github/psi-k-poster/psi-k_data/Figure2/data/diffusion_coeffcient/D_'+structure
U = np.loadtxt(potential_energy_file)
U = U-U.min()
T = np.arange(100, 601, 20)
D_data=np.loadtxt(diffusion_coefficient_file)
D = D_data[:,0]
D_err=D_data[:,1]

##################################################
fig, ax1 = plt.subplots(figsize=(11, 6))
# First y-axis (energy)
ax1.plot(T, U, color='black', marker='o', markersize=10, label='U', linewidth=2)
ax1.set_ylabel(r'Potential energy [eV]', fontsize=22, color='black')
ax1.tick_params(axis='y', labelcolor='black')

# # Second y-axis (diffusion)
ax2 = ax1.twinx()
ax2.errorbar(T, D, yerr=D_err, color='purple',capsize=5, markersize=10, marker='x', label='D', linewidth=2)
ax2.fill_between(T, D - D_err, D + D_err, color='purple', alpha=0.2)
ax2.set_ylabel(r'D [Å$^2$ ps$^{-1}$]', fontsize=22, color='black')
ax2.set_yticks([0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45])
ax1.set_yticks([0,5,10,15,20,25,30,35,40])
ax2.tick_params(axis='y', labelcolor='black')
ax1.set_xlabel('Temperature [K]', fontsize=22)
ax1.tick_params(labelsize=22)
ax2.tick_params(labelsize=22)

ax1.axvline(190, color='black', linestyle='--', linewidth=1)
ax1.text(135, 30, 'Solid', ha='center', fontsize=22)
ax1.text(395, 30, 'Liquid', ha='center', fontsize=22)

# Adjust layout
plt.tight_layout()
plt.show()
