# chimod

`chimod` computes the **χ-models** of a propositional answer set program and uses them to decide
**χ-equivalence**: whether two programs have the same answer sets for every input fact set in a
given collection χ. It is the prototype accompanying the paper
*Model-Theoretic Characterization of Programs under Specific Inputs*, to appear in the Proceedings of the 18th International Conference on Logic Programming and Non-monotonic Reasoning.

- `chimod.py` prints the χ-models of one program.
- `chieq.py` decides whether two programs are χ-equivalent.

## Background

Let `χ ⊆ 2^A` be a collection of input fact sets. Programs `P` and `Q` are *χ-equivalent* if
`AS(P ∪ F) = AS(Q ∪ F)` for every `F ∈ χ`. A pair `⟨X, Y⟩` with `X ⊆ Y` is a *χ-model* of `P`
(Definition 4 of the paper) if:

1. `Y ⊨ P`;
2. `Y` is an answer set of `P ∪ X*` for some `X* ∈ χ` with `X* ⊆ Y`;
3. if `X ⊂ Y`, then `X ∈ χ`, `Y` is *not* an answer set of `P ∪ X`, and every `X'' ∈ χ` with
   `X ⊂ X'' ⊆ Y` has `Y ∈ AS(P ∪ X'')`.

Put differently, for each candidate answer set `Y`, the non-total χ-models list the maximal inputs
in χ that fail to produce `Y`. By Theorem 3, **P and Q are χ-equivalent iff their χ-models
coincide**. Special cases: χ = 2^A gives the UE-models, χ = 2^B the relativized B-UE-models, and
χ = {∅} gives exactly the pairs `⟨Y, Y⟩` with `Y ∈ AS(P)`.


## Repository layout

| Path | Content |
|---|---|
| `chimod.py` | Computes the χ-models of a program. |
| `chieq.py` | Decides χ-equivalence of two programs. |
| `asp-htmod-input-converter.py` | Converts a ground program in clingo syntax into htmod syntax. |
| `htmod/` | The htmod tool: the `htmod` wrapper script, the binaries `lp2dlp`, `boole`, `int`, and the original archive `htmod.tar`. |
| `htmod/*.lp`, `htmod/ht*` | Example programs in htmod syntax. |
| `chi*.txt` | χ files for the small examples. |
| `threshold-chi-generator.py`, `disj-chi-generator.py` | Generate the χ files for the two benchmarks. |
| `threshold_chi_files*/`, `disj_chi_files*/` | Generated χ files, with \|χ\| ∈ {1, 3, 6, …, 30}. The `*_one_line` variants hold the same sets written on a single line. |


## Quick start

All commands are run from the repository root. Paths are relative to the current directory.

**χ-models of the motivating example from the introduction.** The program is
`e ← a. c ← a. g ← a. f ∨ a ← e. f ∨ a ← g.` with χ = {{a}, {e}, {g}}:

```bash
$ python3 chimod.py htmod/mini3.lp chi_mini3.txt
< { e f }, { e f } >
< { f g }, { f g } >
< { a c e g }, { a c e g } >
```

## Input formats

### Programs (htmod syntax)

The SE-models (here-and-there models) of a program are computed by the external tool **htmod**, which is located as a 32-bit Linux binary in `htmod/`.

Both tools expect propositional programs in htmod's syntax. Write one rule per statement, each
ending with `.`:

| ASP | htmod |
|---|---|
| `a.` | `a.` |
| `a ∨ b ← c, not d.` | `c&!d -> a+b.` |
| `← a, not b.` | `a&!b -> 0.` |
| `a ∨ b.` | `a+b.` |
| `a ← not not b.` | `!!b -> a.` |


### Converting clingo programs

`asp-htmod-input-converter.py` translates a **ground** program in clingo syntax:

```bash
python3 asp-htmod-input-converter.py program.lp              # writes ./program_htmod.lp
```


### χ files

A χ file is a comma-separated list of sets:

```
{}, {a}, {a,b}
```

- `{}` is the empty set, i.e. the program without extra facts. It belongs to χ only if it is
  listed.


## Usage

### `chimod.py`: compute χ-models

```
python3 chimod.py <program> <chi-file>
```

It prints one χ-model per line as `< { X }, { Y } >`.


## Additional notes

htmod is included unchanged. The original archive is `htmod/htmod.tar`.

If you use this tool, please cite the paper *Model-Theoretic Characterization of Programs under Specific Inputs*.
<!-- TODO: add BibTeX once the proceedings are online -->
