import numpy as np
from scipy.spatial import distance
import math
import pandas as pd
import os

def group_water_molecules(atoms, oxygen_label='O', hydrogen_label='H', max_oh_distance=1.2):
    oxygens = [atom for atom in atoms if atom[0] == oxygen_label]
    hydrogens = [atom for atom in atoms if atom[0] == hydrogen_label]

    water_molecules = []
    missing_hydrogens_messages = []

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
            message = f"Could not find 2 hydrogens for oxygen at {o_coords}, found {len(bonded_hydrogens)} hydrogens."
            print(message)
            missing_hydrogens_messages.append(message)

    return water_molecules, missing_hydrogens_messages

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
        
        # Calculate the angle of each OH vector with the z-plane normal (z-axis)
        z_axis = np.array([0, 0, 1])
        oh1_angle = math.degrees(math.acos(np.dot(oh1_vector, z_axis) / np.linalg.norm(oh1_vector)))
        oh2_angle = math.degrees(math.acos(np.dot(oh2_vector, z_axis) / np.linalg.norm(oh2_vector)))
        
        # Adjust angles for water molecules below the z-plane
        #print(z_plane)
        #print("here are the old cords")
        #print(o_coords[2])
        #print(oh1_angle)
        #print("Here are the new cords")
        
        if o_coords[2] > z_plane:
            oh1_angle = (180 - oh1_angle) 
            oh2_angle = (180 - oh2_angle) 
        #print(o_coords[2])
        #print(oh1_angle)


        # Determine if the molecule is pointing up or down based on the z-coordinate of oxygen
        if ((oh1_angle + oh2_angle) / 2)  > 90:
            orientation = 'up'
        else:
            orientation = 'down'
        #print(orientation)
        angles.append((oxygen, hydrogen1, hydrogen2, oh1_angle, oh2_angle, orientation))

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

def find_oxygen_to_pt_distances(atoms, water_molecules, metal_label='Pt'):
    pt_atoms = [atom for atom in atoms if atom[0] == metal_label]
    pt_coords = np.array([atom[1] for atom in pt_atoms])

    distances = []
    for water in water_molecules:
        oxygen = water[0]
        o_coords = np.array(oxygen[1])
        min_distance = np.min(np.linalg.norm(pt_coords - o_coords, axis=1))
        distances.append((oxygen, min_distance))

    return distances

def read_contcar(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    lattice_vectors = np.array([list(map(float, line.split())) for line in lines[2:5]])
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

    # Check if coordinates are fractional or Cartesian
    coord_type = lines[8].strip().lower()
    fractional = 'direct' in coord_type or 'fractional' in coord_type

    i = 0
    for atom_type, count in zip(atom_types, atom_counts):
        for _ in range(count):
            coords = list(map(float, atom_data[i].split()[:3]))
            if fractional:
                coords = np.dot(coords, lattice_vectors)  # Convert to Cartesian
            atoms.append((atom_type, coords))
            i += 1

    return atoms

# Function to process multiple files
def process_files_in_directory(directory):
    all_data = []
    all_missing_hydrogens = []

    for filename in os.listdir(directory):
        if filename.startswith('CONTCAR'):
            file_path = os.path.join(directory, filename)
            atoms = read_contcar(file_path)
            z_plane = calculate_plane(atoms)
            water_molecules, missing_hydrogens_messages = group_water_molecules(atoms)
            angles = calculate_angles(water_molecules, z_plane)
            bond_lengths = bond_length(water_molecules)
            oxygen_to_pt_distances = find_oxygen_to_pt_distances(atoms, water_molecules)

            # Prepare data for export
            data = []
            for molecule, lengths, pt_distance in zip(angles, bond_lengths, oxygen_to_pt_distances):
                oxygen, hydrogen1, hydrogen2, oh1_angle, oh2_angle, orientation = molecule
                _, _, _, oh1_length, oh2_length = lengths
                _, o_to_pt_distance = pt_distance
                data.append({
                    'Filename': filename,
                    'Oxygen': oxygen[1],
                    'Hydrogen1': hydrogen1[1],
                    'Hydrogen2': hydrogen2[1],
                    'OH1 Angle': oh1_angle,
                    'OH2 Angle': oh2_angle,
                    'OH1 Length': oh1_length,
                    'OH2 Length': oh2_length,
                    'Orientation': orientation,
                    'Oxygen-Pt Distance': o_to_pt_distance
                })

            all_data.extend(data)
            all_missing_hydrogens.extend(missing_hydrogens_messages)

    # Convert to DataFrame and save to Excel file
    df = pd.DataFrame(all_data)
    output_filename = 'water_molecule_angles_all_files_test.xlsx'
    df.to_excel(output_filename, index=False)

    # Append the missing hydrogens messages to the Excel file
    with pd.ExcelWriter(output_filename, mode='a', if_sheet_exists='overlay') as writer:
        missing_df = pd.DataFrame(all_missing_hydrogens, columns=['Missing Hydrogens Messages'])
        missing_df.to_excel(writer, sheet_name='Missing Hydrogens', index=False)

    print(f'Data saved to {output_filename}')

# Example usage
directory = r'your directory'
process_files_in_directory(directory)
