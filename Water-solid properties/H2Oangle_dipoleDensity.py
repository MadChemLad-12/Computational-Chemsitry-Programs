import numpy as np
from scipy.spatial import distance
import math
import pandas as pd
import os
import matplotlib.pyplot as plt

def group_water_molecules(atoms, oxygen_label='O', hydrogen_label='H', max_oh_distance=1.2):
    oxygens = [atom for atom in atoms if atom[0] == oxygen_label]
    hydrogens = [atom for atom in atoms if atom[0] == hydrogen_label]

    water_molecules = []

    for oxygen in oxygens:
        o_coords = np.array(oxygen[1])
        bonded_hydrogens = []

        for hydrogen in hydrogens:
            h_coords = np.array(hydrogen[1])
            dist = distance.euclidean(o_coords, h_coords)
            if dist <= max_oh_distance:
                bonded_hydrogens.append(hydrogen)
                if len(bonded_hydrogens) == 2:
                    break

        if len(bonded_hydrogens) == 2:
            water_molecules.append((oxygen, bonded_hydrogens[0], bonded_hydrogens[1]))
        else:
            print(f"Could not find 2 hydrogens for oxygen at {o_coords}, found {len(bonded_hydrogens)} hydrogens.")

    return water_molecules

def calculate_plane(atoms, metal_label='Pt'):
    metal_atoms = [atom for atom in atoms if atom[0] == metal_label]
    z_coords = [atom[1][2] for atom in metal_atoms]
    z_plane = np.mean(z_coords)
    return z_plane

def calculate_angles(water_molecules, z_plane):
    angles = []
    for water in water_molecules:
        oxygen = water[0]
        hydrogen1 = water[1]
        hydrogen2 = water[2]
        
        o_coords = np.array(oxygen[1])
        h1_coords = np.array(hydrogen1[1])
        h2_coords = np.array(hydrogen2[1])

        # Calculate vectors OH1 and OH2
        oh1_vector = h1_coords - o_coords
        oh2_vector = h2_coords - o_coords
        
        # Calculate the dipole vector
        dipole_vector = (oh1_vector + oh2_vector) / 2.0
        
        # Calculate the angle of the dipole vector with the z-axis
        z_axis = np.array([0, 0, 1])
        dipole_angle = math.degrees(math.acos(np.dot(dipole_vector, z_axis) / np.linalg.norm(dipole_vector)))
        
        # Determine if the molecule is pointing up or down based on the z-coordinate of oxygen
        if o_coords[2] > z_plane:
            orientation = 'up'
        else:
            orientation = 'down'
        
        angles.append((oxygen, hydrogen1, hydrogen2, dipole_angle, orientation))

    return angles

def bond_length(water_molecules):
    bond_lengths = []
    for water in water_molecules:
        oxygen = water[0]
        hydrogen1 = water[1]
        hydrogen2 = water[2]

        o_coords = np.array(oxygen[1])
        h1_coords = np.array(hydrogen1[1])
        h2_coords = np.array(hydrogen2[1])

        oh1_length = distance.euclidean(o_coords, h1_coords)
        oh2_length = distance.euclidean(o_coords, h2_coords)

        bond_lengths.append((oxygen, hydrogen1, hydrogen2, oh1_length, oh2_length))

    return bond_lengths

def calculate_oxygen_distances_and_angles(water_molecules, z_plane):
    distances_and_angles = []
    for water in water_molecules:
        oxygen = water[0]
        o_coords = np.array(oxygen[1])
        distance_from_plane = abs(o_coords[2] - z_plane)

        hydrogen1 = water[1]
        hydrogen2 = water[2]
        h1_coords = np.array(hydrogen1[1])
        h2_coords = np.array(hydrogen2[1])

        # Calculate vectors OH1 and OH2
        oh1_vector = h1_coords - o_coords
        oh2_vector = h2_coords - o_coords
        
        # Calculate the dipole vector
        dipole_vector = (oh1_vector + oh2_vector) / 2.0
        
        # Calculate the angle of the dipole vector with the z-axis
        z_axis = np.array([0, 0, 1])
        dipole_angle = math.degrees(math.acos(np.dot(dipole_vector, z_axis) / np.linalg.norm(dipole_vector)))
        
        distances_and_angles.append((distance_from_plane, dipole_angle))
    return distances_and_angles

def process_files_in_directory(directory):
    all_data = []
    all_oxygen_distances_and_angles = []

    for filename in os.listdir(directory):
        if filename.startswith('CONTCAR'):
            filepath = os.path.join(directory, filename)
            atoms = read_contcar(filepath)
            z_plane = calculate_plane(atoms)
            water_molecules = group_water_molecules(atoms)
            angles = calculate_angles(water_molecules, z_plane)
            bond_lengths = bond_length(water_molecules)
            oxygen_distances_and_angles = calculate_oxygen_distances_and_angles(water_molecules, z_plane)
            all_oxygen_distances_and_angles.extend(oxygen_distances_and_angles)

            # Prepare data for export
            data = []
            for molecule, lengths in zip(angles, bond_lengths):
                oxygen, hydrogen1, hydrogen2, dipole_angle, orientation = molecule
                _, _, _, oh1_length, oh2_length = lengths
                data.append({
                    'Oxygen': oxygen[1],
                    'Hydrogen1': hydrogen1[1],
                    'Hydrogen2': hydrogen2[1],
                    'Dipole Angle': dipole_angle,
                    'OH1 Length': oh1_length,
                    'OH2 Length': oh2_length,
                    'Orientation': orientation,
                    'Filename': filename
                })
            all_data.extend(data)

    # Convert to DataFrame
    df = pd.DataFrame(all_data)

    # Save to Excel file
    output_filename = 'water_molecule_angles.xlsx'
    df.to_excel(output_filename, index=False)

    print(f'Data saved to {output_filename}')

    # Calculate density multiplied by cos(angle)
    distances = np.array([item[0] for item in all_oxygen_distances_and_angles])
    cos_angles = np.array([math.cos(math.radians(item[1])) for item in all_oxygen_distances_and_angles])
    
    # Create a histogram of distances
    bin_edges = np.histogram_bin_edges(distances, bins=30)
    hist, _ = np.histogram(distances, bins=bin_edges, density=True)
    
    # Calculate the mean cosine angle for each bin
    mean_cos_angles = []
    for i in range(len(bin_edges) - 1):
        bin_mask = (distances >= bin_edges[i]) & (distances < bin_edges[i + 1])
        if np.any(bin_mask):
            mean_cos_angles.append(np.mean(cos_angles[bin_mask]))
        else:
            mean_cos_angles.append(0)
    
    # Convert mean_cos_angles to a numpy array
    mean_cos_angles = np.array(mean_cos_angles)

    # Multiply the histogram density by the mean cosine angles
    weighted_density = hist * mean_cos_angles
    
    # Plot the weighted density
    plt.plot(bin_edges[:-1], weighted_density, marker='o')
    plt.xlabel('Distance from Pt Surface (Å)')
    plt.ylabel('Density * cos(angle)')
    plt.title('Weighted Density Profile of Water Molecules by Distance from Pt Surface')
    plt.grid(True)
    plt.savefig('oxygen_distance_weighted_density_distribution.png')
    plt.show()

def read_contcar(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    atoms = []
    atom_types = []
    for line in lines[5:6]:
        atom_types = line.split()
    
    atom_counts = []
    for line in lines[6:7]:
        atom_counts = list(map(int, line.split()))
    
    total_atoms = sum(atom_counts)
    coords_start_line = 9
    atom_data = lines[coords_start_line:coords_start_line + total_atoms]
    
    i = 0
    for atom_type, count in zip(atom_types, atom_counts):
        for _ in range(count):
            coords = list(map(float, atom_data[i].split()[:3]))
            atoms.append((atom_type, coords))
            i += 1
    
    return atoms

# Example usage
directory = r'C:\Users\jackh\OneDrive - Griffith University\Documents - Jack Hinsch (PhD)\CJmiscellaneous\Coding\H2O angle\Structures'
process_files_in_directory(directory)
