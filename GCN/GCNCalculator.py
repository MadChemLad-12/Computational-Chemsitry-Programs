import numpy as np
from scipy.spatial import KDTree

def read_poscar(filename):
    """Reads a POSCAR file and returns a list of atoms with their positions."""
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    lattice_vectors = np.array([list(map(float, lines[i].split())) for i in range(2, 5)])
    scaling_factor = float(lines[1])
    lattice_vectors *= scaling_factor
    
    atom_types = lines[5].split()
    atom_counts = list(map(int, lines[6].split()))
    
    total_atoms = sum(atom_counts)
    
    if lines[8].strip().lower() in ["cartesian", "direct"]:
        coords_start_line = 9
    else:
        coords_start_line = 8
    
    is_direct = lines[8].strip().lower() == "direct"
    
    atom_positions = np.array([list(map(float, lines[coords_start_line + i].split()[:3])) for i in range(total_atoms)])
    
    if is_direct:
        # Convert from fractional (direct) to Cartesian coordinates
        atom_positions = np.dot(atom_positions, lattice_vectors)
    
    atoms = []
    for atom_type, count in zip(atom_types, atom_counts):
        for i in range(count):
            atoms.append((atom_type, atom_positions[i]))

    return atoms

def calculate_coordination_numbers(atoms, cutoff_distance):
    """Calculate the coordination number for each atom."""
    positions = np.array([atom[1] for atom in atoms])
    tree = KDTree(positions)
    
    coordination_numbers = []
    for i, atom in enumerate(atoms):
        neighbors = tree.query_ball_point(positions[i], cutoff_distance)
        coordination_number = len(neighbors) - 1  # Exclude the atom itself
        coordination_numbers.append(coordination_number)
    
    return coordination_numbers

def calculate_gcn(target_atom_index, atoms, coordination_numbers, cutoff_distance):
    """Calculate the generalized coordination number for a specific atom."""
    positions = np.array([atom[1] for atom in atoms])
    tree = KDTree(positions)
    
    neighbors = tree.query_ball_point(positions[target_atom_index], cutoff_distance)
    
    print(f"\nAtom {target_atom_index + 1} Neighbors within {cutoff_distance} Å:")
    for i in neighbors:
        if i != target_atom_index:
            distance = np.linalg.norm(positions[target_atom_index] - positions[i])
            print(f"Neighbor {i + 1}: Distance = {distance:.2f} Å, Coordination = {coordination_numbers[i]}")
    
    gcn = sum(coordination_numbers[i]/12 for i in neighbors if i != target_atom_index)
    
    return gcn

def main():
    filename = 'YOUR_FILE_NAME'
    cutoff_distance = 3.0  # Increase to your preference
    target_atom_index = 310  # Atom index (zero-based)
    
    atoms = read_poscar(filename)
    
    # Print out atom positions for verification
    print("Atom positions:")
    for i, atom in enumerate(atoms):
        print(f"Atom {i + 1}: {atom[1]}")
    
    coordination_numbers = calculate_coordination_numbers(atoms, cutoff_distance)
    
    gcn = calculate_gcn(target_atom_index, atoms, coordination_numbers, cutoff_distance)
    
    print(f"\nThe generalized coordination number (GCN) for atom at index {target_atom_index + 1} is: {gcn}")

if __name__ == "__main__":
    main()
