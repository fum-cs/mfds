# Gaussian Random Projection

**Status:** outline — expand with notation and a small NumPy demo.

## Goals

- Project \(\mathbb{R}^n \to \mathbb{R}^m\) with a **random Gaussian** matrix
- Scaling so expected lengths are preserved
- Compare with other random maps (e.g. sparse / Achlioptas-style)

## Outline

1. Projection matrix \(R \in \mathbb{R}^{m \times n}\) with i.i.d. Gaussian entries
2. Typical length preservation after projection
3. Simple experiment: pairwise distances before/after
4. Link to the Johnson–Lindenstrauss lemma

## Sources

- `Random-Projection.ipynb` in this folder
- Blum–Hopcroft–Kannan, random projections sections
