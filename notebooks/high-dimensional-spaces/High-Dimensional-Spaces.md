<div class="langswitch langswitch-ltr">
  <strong>English</strong> · <a href="#lang-fa">فارسی</a>
</div>

# High Dimensional Spaces

![](img/banner.png)

A data set is an $n \times d$ matrix — $n$ points, $d$ coordinates — and in modern
work $d$ is often large: a $200\times300$ grayscale image is *one* point in
$\mathbb{R}^{60\,000}$, a document embedding has a few hundred coordinates, a
genome sample tens of thousands. Distances, neighbourhoods and centroids are
computed with exactly the formulas we use in the plane, but the geometry those
formulas describe is **not** the geometry of the plane. Almost all of the volume
of a cube lies near its corners, almost all of the volume of a ball lies in a thin
shell near its surface, and the nearest neighbour of a point is nearly as far away
as its farthest neighbour.

This part of the course builds that intuition, puts numbers on it, shows what it
does to the two algorithms we already use — **k-nearest neighbours** and
**k-means** — and then gives the constructive answer: **random projections**, which
shrink the dimension while keeping the distances, with the
**Johnson–Lindenstrauss lemma** as the guarantee. The pages, in the order of the
table of contents:

| page | what it does |
|---|---|
| [High Dimensional Data & The Curse of Dimensionality](High-Dimensional-Data-and-The-Curse-of-Dimensionality.ipynb) | The theory: cubes and spheres in $d$ dimensions, the empty centre, local neighbourhoods and the distance to the boundary, and random directions that are nearly orthogonal. |
| [Sampling in High Dimensional Spaces](High-Dimensional-Sampling.ipynb) | The laboratory: the thin-shell volume experiment, rejection sampling and its acceptance ratio, uniform points on a hypersphere (normalised Gaussian vectors) and inside the ball (inverse-transform radius), and the Gaussian annulus. |
| [kNN in high dimensional spaces](High-Dimensional-Data-and-kNN.ipynb) | An experiment: classification accuracy of a 5-nearest-neighbour classifier on synthetic data as the number of features grows from 2 to 100. |
| [k-means in high dimensional spaces](High-Dimensional-Data-and-K-Means.ipynb) | The same experiment for clustering: the adjusted Rand index of k-means against the true labels, as a function of $d$. |
| [Random Projection: Theory and Implementation](Random-Projection.ipynb) | The constructive answer: the Johnson–Lindenstrauss lemma, Gaussian and sparse (Achlioptas) projection matrices, the $1/\sqrt{k}$ scaling experiment, a Scikit-Learn check that pairwise distances survive the projection, and a short survey of compressed sensing. |

## Three facts behind the title

**1. The cube swallows the ball.** For a point $X$ uniform on $[-1,1]^d$, the
probability that it falls inside the inscribed unit ball is the ratio of the two
volumes,

$$
\mathbb{P}(\|X\|\le 1) = \frac{V_d}{2^d},
\qquad V_d = \frac{\pi^{d/2}}{\Gamma\!\left(\frac{d}{2}+1\right)},
$$

and this ratio tends to $0$. In high dimension a cube is essentially all corners.

**2. The ball is a shell.** The same computation for the radius gives, for any
fixed $\epsilon>0$,

$$
\mathbb{P}(\|X\| > 1-\epsilon) = 1-(1-\epsilon)^d \xrightarrow[d\to\infty]{} 1 .
$$

For $d=100$ and $\epsilon=0.05$ this probability is already $0.994$: the centre of
the ball is empty, and all the points are on the peel.

**3. Nearest and farthest neighbours look alike.** With $n$ points in the unit
cube, the typical distance to the nearest neighbour grows with $d$ while the
diameter stays fixed, so the ratio (farthest distance) / (nearest distance) tends
to $1$. A neighbourhood stops being *local*: it is no longer a small ball around
the query point, it is a slab that reaches across the whole data set.

Facts 1 and 2 are what the first page proves and draws; fact 3 is what the two
experiments measure, once for a classifier and once for a clustering. The last page
then shows that the same concentration is the *reason why* a random projection
works.

## Reading order and prerequisites

The pages are meant to be read in the order above. The only prerequisites are the
Euclidean norm and the distance formula, both from
[Norms](../linear-algebra/Norms.ipynb), plus the idea — introduced in
[Images as high dimensional data](Images-as-High-Dimensional-Data.ipynb) — that an
image is a vector and therefore a point in a high-dimensional space.

Reading the theory page first matters: without it the two experiments look like
"algorithms that get worse", when in fact the algorithms are doing exactly what
they were told and the *space* is what changed. The sampling
page then turns the same statements into measurements you can run yourself. In the other direction, the random
projection page is where the same facts turn into an algorithm, so it is worth
reading the theory page before it.

## Where this part sits in the course

- **Classification and Clustering.** The kNN page,
  [k-Nearest Neighbors and Classification Evaluation Metrics](kNN-Classification-Evaluation.ipynb),
  and the clustering pages, [Clustering](Clustering-Part1.ipynb),
  [k-means Clustering](Clustering-Part2.ipynb) and
  [Exhaustive Clustering](Exhaustive-Clustering.ipynb), are where these algorithms
  are defined. This part explains why their behaviour degrades as $d$ grows.
- **Low-rank approximation and PCA.** If distances stop being informative, one
  answer is to work in fewer dimensions by keeping the directions of largest
  variance: see [Principal Component Analysis, Part 1](../linear-algebra/PCA-Part1.ipynb)
  and [SVD for Image Compression](SVD-Image-Compression.ipynb). Random projection
  is the cheap, data-independent alternative to that idea, and the two are
  compared at the end of the last page.

## Exercises

1. Verify the three facts of this page numerically in a few lines of NumPy: the distance concentration, the volume ratio of ball and cube, and the thin-shell fraction.
2. Using the reading order given here, say which page you need *before* PCA, and why the order matters for a reader who has not seen eigenvalues before.
3. Write down one claim from each of the three pages of this part that would still hold in two dimensions, and one that is specific to high dimension.


## Sources

- A. Blum, J. Hopcroft, R. Kannan, *Foundations of Data Science*, the chapters on
  high-dimensional space, random projections and the Johnson–Lindenstrauss lemma.
- Achlioptas, D. (2003), *Database-friendly random projections:
  Johnson–Lindenstrauss with binary coins* — the sparse projection matrices used in
  the last page.
