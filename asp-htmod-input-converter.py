# Converts an ASP input file into a HT-model compatible format:
# 1. Remove parentheses and turn commas into underscores in predicates: pred(1,2) -> pred1_2
# 2. Convert rules of the form: a | b :- c, not d.  ->  c&!d -> a+b
# Write the output to a new file with suffix _htmod.lp in the current working directory.

import re
import sys
from pathlib import Path
import os

def convert_predicates(atom: str) -> str:
    # Convert atom like pred(1,2) -> pred1_2
    atom = atom.strip()
    # Remove parentheses and replace commas with underscores
    atom = re.sub(r'\(([^)]*)\)', lambda m: '_' + m.group(1).replace(',', '_'), atom)
    return atom

def convert_rule(line: str) -> str:
    # Convert ASP rule like: a | b :- c, not d. -> c&!d -> a+b
    line = line.strip().rstrip('.')
    
    if not line:
        return ''
    
    # Split head and body
    if ':-' in line:
        head, body = line.split(':-', 1)
    else:
        head, body = line, ''

    # Convert head: replace | with +
    head_atoms = [convert_predicates(atom) for atom in head.split('|')]
    head_str = '+'.join(head_atoms)

    # Convert body: replace ',' with '&', 'not' with '!'
    if body:
        body_atoms = []
        for atom in body.split(','):
            atom = atom.strip()
            if atom.startswith('not '):
                atom = '!' + convert_predicates(atom[4:])
            else:
                atom = convert_predicates(atom)
            body_atoms.append(atom)
        body_str = '&'.join(body_atoms)
        return f"{body_str} -> {head_str}."
    else:
        return f" -> {head_str}" if head_str else ''

def convert_file(file_path: str):
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"Error: File {file_path} not found.")
        return

    output_lines = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('%'):  # skip empty lines and comments
                continue
            converted = convert_rule(line)
            if converted:
                output_lines.append(converted)

    # New file in the current working directory
    new_file_name = file_path.stem + '_htmod.lp'
    new_file_path = Path(os.getcwd()) / new_file_name

    with open(new_file_path, 'w') as f:
        f.write('\n'.join(output_lines) + '\n')

    print(f"Converted file written to {new_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python asp_htmod_input_converter.py <asp_file.lp>")
        sys.exit(1)
    asp_file = sys.argv[1]
    convert_file(asp_file)