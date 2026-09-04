# This script checks if given two programs are chi-equivalent.

import argparse

from chimod import run

def print_models(models):
    for model in models:
        print("< { " + " ".join(sorted(model[0])) + " }, { " + " ".join(sorted(model[1])) + " } >")

def show_differences(chi_models_1, chi_models_2):
    diff1 = chi_models_1 - chi_models_2
    diff2 = chi_models_2 - chi_models_1

    print("\nModels in program1 but not in program2:")
    print_models(diff1)

    print("\nModels in program2 but not in program1:")
    print_models(diff2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check chi-equivalence between two ASP programs."
    )

    parser.add_argument("program1", help="First ASP program (in htmod input format)")
    parser.add_argument("program2", help="Second ASP program (in htmod input format)")
    parser.add_argument("chi_file", help="Chi file")
    parser.add_argument(
        "-d", "--diff",
        action="store_true",
        help="Print the models that differ"
    )

    args = parser.parse_args()

    chi_models_1 = run(args.program1, args.chi_file)
    chi_models_2 = run(args.program2, args.chi_file)

    if chi_models_1 == chi_models_2:
        print("True")
    else:
        print("False")
        if args.diff:
            show_differences(chi_models_1, chi_models_2)

