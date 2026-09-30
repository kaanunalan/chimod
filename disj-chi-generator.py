# Generates chi files for program "disjunctive propagation"

import os
import random

# Seed for reproducibility
random.seed(2)

# Define the predicates and the indices
predicates = ["trigger", "activate", "backup"]
indices = list(range(1, 3))

# Create a list of all possible atoms, e.g., 'trigger_1', 'activate_1', 'backup_1', ..., 'backup_8'
all_atoms = [f"{pred}_{idx}" for pred in predicates for idx in indices]

# Desired chi sizes (number of sets in each chi)
chi_sizes = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]

# Directory to save files
output_dir = "chi_files"
os.makedirs(output_dir, exist_ok=True)

# Initialize chi as a list of sets
current_chi = []

for chi_size in chi_sizes:
    # Copy previous chi sets as a starting point
    new_chi = current_chi.copy()

    # Add new random sets until chi reaches desired size
    while len(new_chi) < chi_size - 1:
        # Randomly choose how many atoms will be in this set (from 1 up to the total pool size)
        set_size = random.randint(1, len(all_atoms))

        # Randomly pick atoms without duplicates from our mixed pool
        new_set = frozenset(random.sample(all_atoms, set_size))

        # Only add if it's unique and not already in chi
        if new_set not in new_chi:
            new_chi.append(new_set)

    # Save all elements of this chi to a single file in requested format
    filename = f"{output_dir}/disj-chi-size-{chi_size}.txt"
    with open(filename, "w") as f:
        chi_strings = []
        # Always include empty set
        chi_strings.append("{}")
        for s in new_chi:
            # Sort the atoms so the files look clean and consistent
            atoms_str = ",".join(sorted(s))
            chi_strings.append(f"{{{atoms_str}}}")

        # Join all chi elements with newlines and trailing commas
        #f.write(",\n".join(chi_strings) + "\n")
        # Join all chi elements with spaces
        f.write(",".join(chi_strings) + "\n")

    # Update current_chi for next iteration
    current_chi = new_chi

print(f"All chi files generated in '{output_dir}'")