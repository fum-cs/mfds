# Subspaces and Maps to Other Spaces

**Status:** outline — bridge span/dependence notebooks to linear maps.

## Goals

- Vector spaces and subspaces (span, basis, dimension — recap)
- A matrix as a **map** \(T: \mathbb{R}^n \to \mathbb{R}^m\)
- Image (range) and kernel (null space)
- Change of coordinates and embedding into other feature spaces

## Outline

1. Subspaces defined by span and linear equations
2. Column space vs null space
3. Linear maps: projection, rotation, scaling
4. Data view: each feature map sends points to a new space
5. Lab pointers: `Linear-Dependence-and-Span`, `Projection`, `Multiplying-Matrices-and-Vectors`

## Exercises

1. Take a $2\times3$ matrix, describe its column space geometrically and give a basis for it.
2. Give a linear map that is not invertible, describe its kernel, and check that the dimensions satisfy rank plus nullity equals $3$.
3. Explain why a linear map is determined by the images of a basis, and use that to reconstruct a $2\times2$ matrix from two image vectors.


## Sources

- `linear-algebra-basics.md` and the linear-algebra notebooks
- Goodfellow et al., *Deep Learning*, Ch. 2 (as used in these notes)
