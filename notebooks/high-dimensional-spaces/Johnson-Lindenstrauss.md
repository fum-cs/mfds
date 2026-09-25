# Johnson–Lindenstrauss Lemma

**Status:** outline — state the lemma carefully and connect to the lab.

## Goals

- Statement: \(n\) points can be embedded into \(m = O(\varepsilon^{-2}\log n)\) dimensions while preserving pairwise distances within \(1\pm\varepsilon\)
- Why this is a “flattening” / dimensionality-reduction guarantee
- Use cases: nearest neighbors, clustering in high-d data

## Outline

1. Distance preservation, not exact reconstruction
2. Dependence on \(n\), \(\varepsilon\), and failure probability
3. Gaussian random projections as a constructive map
4. Lab pointer: `Random-Projection.ipynb`, `Gaussian-Random-Projection.md`

## Sources

- Johnson–Lindenstrauss (1984); Achlioptas (2003) for sparse variants
- Blum–Hopcroft–Kannan, random projections / JL discussion
