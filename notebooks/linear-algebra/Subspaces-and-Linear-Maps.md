# Subspaces and Maps to Other Spaces

**Status:** bridge page between the span/dependence notebooks and the eigen/SVD chapters.

The pages before this one answered questions *inside* $\mathbb{R}^n$: what a linear combination is,
when vectors are independent, what a span is. This page changes the point of view twice: first a
matrix is no longer a table of numbers but a **linear map** between two spaces, and then a subspace
is no longer a set of arrows but the **image** or the **kernel** of such a map. Both views are used
in every later chapter — projections in PCA, null spaces in least squares, feature maps in the
kernel page.

## 1. Subspaces, in one paragraph each

A subset $V\subseteq\mathbb{R}^n$ is a **subspace** if it contains $0$ and is closed under addition
and scalar multiplication. Three consequences we will use constantly:

- Every subspace is the **span** of some vectors, and a minimal spanning set is a **basis**. All
  bases of the same subspace have the same number of elements, its **dimension**.
- Subspaces of $\mathbb{R}^n$ come in dimensions $0,1,\dots,n$: a point, a line through the origin,
  a plane through the origin, and so on. The phrase *through the origin* is not decoration; a line
  that misses $0$ is not a subspace and averaging inside it leaves it.
- A subspace can be given in two ways, and the two descriptions are dual: as a **span**
  (parametrically, $V=\{Ax : x\in\mathbb{R}^k\}$) or as the **solution set of homogeneous
  equations** (implicitly, $V=\{x : Bx=0\}$). Converting between the two is Gaussian elimination.

Data example: the set of all images in a dataset, flattened, spans a subspace of $\mathbb{R}^{d}$
whose dimension is at most the number of images — usually far less, which is the whole premise of
low-rank approximation.

## 2. A matrix is a map

Fix $A\in\mathbb{R}^{m\times n}$ and read it column by column: $A = [a_1,\dots,a_n]$. Then $Ax$ is
the linear combination of the columns with coefficients $x_1,\dots,x_n$. So multiplication by $A$ is
the map

$$
T_A:\mathbb{R}^n\to\mathbb{R}^m,\qquad T_A(x) = Ax,
$$

and it is linear: $T_A(\alpha x+\beta y) = \alpha T_A(x)+\beta T_A(y)$. Conversely, **every** linear
map between these spaces is of this form for exactly one matrix: the $j$-th column of $A$ is the
image of the $j$-th basis vector. This is why the two objects are used interchangeably.

Two subspaces travel with $A$:

$$
\underbrace{\mathrm{Col}(A) = \{Ax : x\in\mathbb{R}^n\}}_{\text{image, in }\mathbb{R}^m}
\subseteq \mathbb{R}^m,
\qquad
\underbrace{\mathrm{Null}(A) = \{x : Ax = 0\}}_{\text{kernel, in }\mathbb{R}^n}
\subseteq \mathbb{R}^n .
$$

$\mathrm{Col}(A)$ is the set of targets the map can hit; $\mathrm{Null}(A)$ is the set of inputs it
collapses to zero. The **rank** is $\dim\mathrm{Col}(A)$, the number of independent columns;
the **nullity** is $\dim\mathrm{Null}(A)$; and the two are tied by

$$
\boxed{\;\mathrm{rank}(A) + \mathrm{nullity}(A) = n\;}
$$

which is the statement that every independent direction of the input either survives into the image
or is lost in the kernel, never both. In linear regression, $\mathrm{Null}(X)$ is exactly the
ambiguity in the coefficients: if $Xw = y$ has a solution, it has the affine set
$w + \mathrm{Null}(X)$ of them, and the pseudoinverse picks the shortest.

## 3. The geometry of the three families

| Map | Matrix form | What it does | Kernel |
|---|---|---|---|
| scaling along axes | $\mathrm{diag}(s_1,\dots,s_n)$ | stretches by $s_i$ | the axes with $s_i=0$ |
| rotation by $\theta$ | $\begin{pmatrix}\cos\theta&-\sin\theta\\ \sin\theta&\cos\theta\end{pmatrix}$ | turns the plane | $\{0\}$ |
| projection onto a subspace | $P = UU^\top$ with $U^\top U = I$ | keeps the $U$-part, discards the rest | $U^{\perp}$ |
| rank-one map | $uv^\top$ | collapses everything onto the line of $u$ | $v^{\perp}$ |

The projection row is the one that returns in PCA: $P$ is idempotent ($P^2=P$) and symmetric, and
$\mathrm{rank}(P) = \dim\mathrm{Col}(U)$ — the number of components kept.

## 4. Composition, inverse, change of basis

- **Composition is multiplication.** Applying $B$ after $A$ is the map $x\mapsto B(Ax) = (BA)x$.
  Order matters, and the identity $AB\neq BA$ in general is a statement about maps, not about
  arithmetic.
- **Inverse means invertible map.** $A$ is invertible iff $\mathrm{Null}(A)=\{0\}$, which for a
  square matrix is equivalent to full rank and to $\det A \neq 0$. A non-square matrix can be
  injective or surjective but not both; the pseudoinverse handles the general case.
- **Change of basis.** If $B$ has the new basis vectors as columns, then the matrix of the same map
  in the new basis is $B^{-1}AB$. Similar matrices represent the same map and therefore share
  eigenvalues — which is why the eigendecomposition $A = Q\Lambda Q^{-1}$ can be read as "the map is
  diagonal in the eigenbasis".

## 5. Data view: a map to another space

Everything above was written for $\mathbb{R}^n\to\mathbb{R}^m$, but the same words describe the step
that makes modern learning possible: a **feature map** $\phi:\mathcal{X}\to\mathcal{F}$ sends each
data point to another space, where a linear model may be enough. Two examples from this course:

- PCA is a map to a low-dimensional subspace, chosen to lose as little variance as possible.
- The kernel page replaces $\phi$ by its Gram matrix $K(x,z) = \phi(x)^\top\phi(z)$, so the map is
  never computed, only its inner products. The kernel is a similarity, and section 2 is why: an inner
  product *is* a coordinate-free description of the geometry in $\mathcal{F}$.

## Lab pointers

Read these notebooks next to this page, they are the computational half of it:
`Linear-Dependence-and-Span`, `Projection`, `Multiplying-Matrices-and-Vectors`, and then
`Eigendecomposition` for the change-of-basis statement of section 4.

## Exercises

1. Take a $2\times3$ matrix, describe its column space geometrically and give a basis for it.
2. Give a linear map that is not invertible, describe its kernel, and check that the dimensions satisfy rank plus nullity equals $3$.
3. Explain why a linear map is determined by the images of a basis, and use that to reconstruct a $2\times2$ matrix from two image vectors.
4. For $A=\begin{pmatrix}1&2&3\\2&4&6\end{pmatrix}$, find bases of $\mathrm{Col}(A)$ and $\mathrm{Null}(A)$ and verify rank plus nullity equals $3$. Why does the system $Ax=b$ have solutions only for some $b$, and how do you recognise those $b$?
5. Show that $P=UU^\top$ with $U^\top U=I$ satisfies $P^2=P$ and $P^\top=P$, and that $\mathrm{rank}(P)$ is the number of columns of $U$. Interpret both facts geometrically.
6. Let $B$ be the matrix whose columns are $(1,1)$ and $(1,-1)$. Compute $B^{-1}AB$ for a $2\times2$ symmetric $A$ of your choice and check that the eigenvalues did not change. What are the eigenvectors of $B^{-1}AB$ in terms of those of $A$?
7. Give a feature map $\phi:\mathbb{R}^2\to\mathbb{R}^3$ such that the XOR labelling becomes linearly separable, and write the three coordinates explicitly.

## Sources

- `linear-algebra-basics.md` and the linear-algebra notebooks
- Goodfellow et al., *Deep Learning*, Ch. 2 (as used in these notes)
- Strang, *Linear Algebra and Its Applications*, Ch. 3–4 (column space, null space, rank–nullity)
