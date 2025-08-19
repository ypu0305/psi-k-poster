import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create a figure and axis
fig, ax = plt.subplots(figsize=(14, 10))
lines = [
    [10, 0, 600],  # Second line
    [14, 0, 600],  # Third line
]
for line in lines:
    y, x_start, x_end = line
    ax.hlines(y, x_start, x_end, colors='black', linewidth=1)

lines = [
    [200, 6, 10],  
    [400, 10, 14],  
    ]

for i, line in enumerate(lines):
    x, y_start, y_end = line
    ax.vlines(x, y_start, y_end, colors='blue', linewidth=2)
    
x, y_start, y_end = [400,14,18]
ax.vlines(x, y_start, y_end, colors='blue', linewidth=2, linestyle='--')
####################################################
ax.set_xlabel('Temperature [K]', fontsize=22)
ax.set_ylabel('Density [mols / unit cell]', fontsize=22)
ax.tick_params(labelsize=22)
ax.set_yticks([8,12,16])

ax.set_xlim(0, 600)
ax.set_ylim(6, 18)

# Show the grid and plot
ax.grid(False)
plt.show()
