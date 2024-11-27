import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def read_xyz(file_path):
    """Read XYZ file and return atoms and their positions."""
    atoms = []
    positions = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[2:]:  # Skip the first two lines
            parts = line.split()
            atoms.append(parts[0])
            positions.append([float(x) for x in parts[1:4]])
    return atoms, np.array(positions)

def calculate_distance_to_surface(water_positions, pt_positions):
    """Calculate the distance of water molecules to the Pt surface."""
    pt_surface_z = np.mean(pt_positions[:, 2])  # Assume Pt surface at average z position of Pt atoms
    distances = water_positions[:, 2] - pt_surface_z
    return distances

def plot_density(distances, bins=50):
    """Plot the density of water molecules over the distance to the Pt surface."""
    density, bin_edges = np.histogram(distances, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    plt.figure(figsize=(8, 6))
    plt.plot(bin_centers, density, label='Water Density')
    plt.xlabel('Distance to Pt Surface (Å)')
    plt.ylabel('Density')
    plt.title('Density of Water Molecules Over Distance to Pt Surface')
    plt.legend()
    plt.grid(True)
    plt.show()

    return bin_centers, density

# Path to your XYZ file
xyz_file_path = 'CONTCAR100_FIX.xyz'

# Read the XYZ file
atoms, positions = read_xyz(xyz_file_path)

# Separate water and Pt positions
water_positions = positions[np.array(atoms) == 'O']  # Assuming O represents water molecules
pt_positions = positions[np.array(atoms) == 'Pt']

# Calculate distances
distances = calculate_distance_to_surface(water_positions, pt_positions)

# Plot density and get the data
bin_centers, density = plot_density(distances)

# Debugging lengths of arrays
print(f"Length of distances: {len(distances)}")
print(f"Length of bin_centers: {len(bin_centers)}")
print(f"Length of density: {len(density)}")

# Ensure all arrays have the same length
# Only 'distances' might be different in length, so we remove it from the DataFrame
data = {
    'Bin Centers (Å)': bin_centers,
    'Density': density
}

df = pd.DataFrame(data)
excel_file_path = 'density_data.xlsx'
df.to_excel(excel_file_path, index=False)
print(f"Data saved to {excel_file_path}")
