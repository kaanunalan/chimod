# This script checks if a given ht model is a chi-model.

import sys
import os
import subprocess
import re
from itertools import combinations

def parse_chi(chi_file):
    # Reads a chi file consisting of one line of comma-separated sets, e.g., {}, {a}, {a, b}.
    # Empty set must always be included.
    with open(chi_file) as f:
        line = f.readline().strip()

    blocks = re.findall(r"\{([^}]*)\}", line)

    chi = []
    for block in blocks:
        block = block.strip()

        if block == "":  # empty set {}
            chi.append(frozenset())
        else:
            atoms = [a.strip() for a in block.split(",") if a.strip()]
            chi.append(frozenset(atoms))
    return chi    

def parse_htmod_output(htmod_output):
    ht_models = []
    for line in htmod_output.splitlines():
        match = re.match(r"<\s*\{(.*?)\},\s*\{(.*?)\}\s*>", line)
        if match:
            here, there = match.groups()
            here_list = here.split() if here.strip() else []
            there_list = there.split() if there.strip() else []
            ht_models.append((here_list, there_list))
    return ht_models

def call_htmod(htmod_input):
    input_file = htmod_input
    
    htmod_dir = os.path.join(os.path.dirname(__file__), "htmod")
    script_path = os.path.join(htmod_dir, "htmod")

    subprocess_output = subprocess.run([script_path, input_file], cwd=htmod_dir, capture_output=True, text=True)
    return parse_htmod_output(subprocess_output.stdout)


def get_all_sets_between(x, y):
    # Get all X' such that $x \subseteq X' \subseteq y$
    x_set = frozenset(x)
    y_set = frozenset(y)
    difference = list(y_set - x_set)

    sets = []

    for r in range(len(difference) + 1):
        for subset in combinations(difference, r):
            x_prime = x_set.union(subset)
            sets.append(x_prime)
    return sets


def convert_to_set(models):
    # Converts a list like [([a,b], [b]), ([], [a])] into a set of (frozenset, frozenset) pairs.
    return {
        (frozenset(x), frozenset(y))
        for x, y in models
    }


def check_condition_ii(ht_model, ht_models, chi):
    y = frozenset(ht_model[1])
    x_star_candidates = get_all_sets_between([], y)
    condition_flag = False
    for x_star in x_star_candidates:
        if x_star in chi:
            condition_flag = True
            x_prime_candidates = get_all_sets_between(x_star, y)
            ht_sets = convert_to_set(ht_models)
            for x_prime in x_prime_candidates:
                if x_prime != y:
                    if (x_prime, y) in ht_sets:
                        condition_flag = False
                        break
            if condition_flag:
                return True
    return condition_flag


def check_condition_iii(ht_model, ht_models, chi):
    x = frozenset(ht_model[0])
    y = frozenset(ht_model[1])
    if x < y:
        if x not in chi:
            return False
        x_prime_candidates = get_all_sets_between(x, y)
        ht_sets = convert_to_set(ht_models)
        for x_prime in x_prime_candidates:
            if x_prime != y:
                if (x_prime, y) in ht_sets:
                    x_double_prime_candidates = get_all_sets_between(x, x_prime)
                    for x_double_prime in x_double_prime_candidates:
                        if x != x_double_prime:
                            if x_double_prime in chi:
                                return False
    return True


def print_chi_models(chi_models):
    for chi_model in chi_models:
        print("< { " + " ".join(sorted(chi_model[0])) + " }, { " + " ".join(sorted(chi_model[1])) + " } >")
    


def run(htmod_input, chi_file):
    chi = parse_chi(chi_file)
    ht_models = call_htmod(htmod_input)
    chi_models = []
    for ht_model in ht_models:
        if check_condition_ii(ht_model, ht_models, chi):
            if check_condition_iii(ht_model, ht_models, chi):
                chi_models.append(ht_model)
    return convert_to_set(chi_models)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 chimod.py <htmod-input> <chi-file>")
        sys.exit(1)
    
    chi_models = run(sys.argv[1], sys.argv[2])
    
    print_chi_models(sorted(chi_models))

