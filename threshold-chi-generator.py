# Generates chi files for program "threshold-style activation"

import random
import os

# Seed for reproducibility
random.seed(2)

# List of all possible sensors (domain)
all_sensors = list(range(1, 9))

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
    while len(new_chi) < chi_size-1:
        # Randomly choose number of sensors in this set
        set_size = random.randint(1, len(all_sensors))
        # Randomly pick sensors without duplicates
        new_set = frozenset(random.sample(all_sensors, set_size))
        # Only add if it's not already in chi
        if new_set not in new_chi:
            new_chi.append(new_set)
    
    # Save all elements of this chi to a single file in requested format
    filename = f"{output_dir}/threshold-chi-size-{chi_size}.txt"
    with open(filename, "w") as f:
        chi_strings = []
        # Always include empty set
        chi_strings.append("{}")
        for s in new_chi:
            sensors = ",".join(f"sensor_{x}" for x in sorted(s))
            chi_strings.append(f"{{{sensors}}}")
        # Join all chi elements with spaces
        f.write(",".join(chi_strings) + "\n")
    
    # Update current_chi for next iteration
    current_chi = new_chi

print(f"All chi files generated in '{output_dir}'")