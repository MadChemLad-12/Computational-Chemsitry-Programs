import numpy as np

def read_vasp_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    lattice_vectors = np.array([list(map(float, lines[i].split())) for i in range(2, 5)])
    atom_counts = list(map(int, lines[6].split()))
    total_atoms = sum(atom_counts)
    coord_type = lines[8].strip().lower()
    atom_positions = np.array([list(map(float, lines[i].split()[:3])) for i in range(9, 9 + total_atoms)])
    selective_dynamics = any('T' in line or 'F' in line for line in lines[9:9 + total_atoms])

    return {
        'header': lines[:8],
        'lattice_vectors': lattice_vectors,
        'coord_type': coord_type,
        'atom_positions': atom_positions,
        'selective_dynamics': selective_dynamics,
        'selective_dynamics_lines': lines[9:9 + total_atoms] if selective_dynamics else None,
        'footer': lines[9 + total_atoms:]
    }

def write_vasp_file(data, file_path, new_coord_type, new_atom_positions):
    with open(file_path, 'w') as file:
        file.writelines(data['header'])
        file.write(f"{new_coord_type.capitalize()}\n")
        
        for i, pos in enumerate(new_atom_positions):
            pos_line = " ".join(f"{x:.12f}" for x in pos)
            if data['selective_dynamics']:
                pos_line += " " + " ".join(data['selective_dynamics_lines'][i].split()[3:])
            file.write(f"{pos_line}\n")
        
        file.writelines(data['footer'])

def fractional_to_cartesian(lattice_vectors, atom_positions):
    return np.dot(atom_positions, lattice_vectors)

def cartesian_to_fractional(lattice_vectors, atom_positions):
    return np.dot(atom_positions, np.linalg.inv(lattice_vectors))

def convert_coordinates(file_path, output_path, target_format):
    data = read_vasp_file(file_path)

    if data['coord_type'] == target_format:
        print(f"The file is already in {target_format} format.")
        return

    if target_format == 'cartesian':
        new_atom_positions = fractional_to_cartesian(data['lattice_vectors'], data['atom_positions'])
    elif target_format == 'direct':
        new_atom_positions = cartesian_to_fractional(data['lattice_vectors'], data['atom_positions'])
    else:
        raise ValueError("Invalid target format. Choose either 'cartesian' or 'direct'.")

    write_vasp_file(data, output_path, target_format, new_atom_positions)
    print(f"Converted coordinates to {target_format} and saved to {output_path}.")

# Example usage:
input_file = 'CONTCAR_fr'
output_file = 'CONTCAR_Catest'
target_format = 'cartesian'  # or 'direct'

convert_coordinates(input_file, output_file, target_format)
