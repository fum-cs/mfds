# Discrete Optimization, Truth Tables, and Clustering

In the k-means pages we *used* a clustering algorithm. There we mentioned, in one
sentence, that finding the best clustering by trying every possibility is
"clearly infeasible", because there are too many possible partitions. This page
stops at that sentence and takes it seriously.

The plan is:

1. describe a clustering as a *discrete object* (a labeling, or a partition);
2. enumerate all such objects for small data, using **recursion**;
3. **count** them, using **Stirling numbers** of the second kind;
4. see why the count kills exhaustive search, and why we still care about it.

The three notebooks that follow are the laboratory part of this page:

| notebook | what it enumerates | new idea |
|---|---|---|
| [SAT-Table](SAT-Table.ipynb) | all $0/1$ assignments of $n$ variables | recursion, generators, Stirling numbers |
| [N-Queen](N-Queen.ipynb) | all placements of $n$ queens | recursion **with pruning** (constraints) |
| [BF-Clustering](BF-Clustering.ipynb) | all 2-clusterings of $n$ points | exhaustive optimization, SSE/WCSS |

## 1. A clustering is a discrete object

Let $\mathbf{D} = \{\mathbf{x}_1,\ldots,\mathbf{x}_n\}$ be our data and let $k$
be the number of groups we want. A clustering is a partition
$\mathcal{C} = \{C_1,\ldots,C_k\}$ of the data points: every point is in exactly
one cluster, and no cluster is empty.

When we write a program, we usually do not store a partition as a family of
sets. We store a **label vector**

$$
\mathbf{z} = (z_1, z_2, \ldots, z_n), \qquad z_i \in \{1,2,\ldots,k\},
$$

where $z_i$ is the number of the cluster that contains $\mathbf{x}_i$. The
partition is then
$C_j = \{\mathbf{x}_i : z_i = j\}$.

Two facts about label vectors are essential, and both are easy to forget:

- **Labels are names, not numbers.** If we exchange the names $1$ and $2$ in
  $\mathbf{z}$, the partition does not change. Every partition with $k$
  non-empty blocks can be written with $k!$ different label vectors. So counting
  label vectors *over-counts* partitions by a factor of $k!$.
- **Empty clusters are not clusters.** The label vector
  $\mathbf{z} = (1,1,\ldots,1)$ describes one cluster, not $k$. If we want
  exactly $k$ clusters we must require all $k$ labels to appear.

Nevertheless, *searching* over label vectors is the natural thing for a
computer: it is just a vector of $n$ integers, each with $k$ possible values.
Optimization means: among all $k^n$ such vectors, find the one that makes some
score as small as possible.

## 2. Truth tables: the simplest discrete search space

Take $k = 2$, so each label is a bit. A vector of $n$ bits is a row of the
**truth table** of $n$ Boolean variables. For $n = 3$:

| row | $z_1$ | $z_2$ | $z_3$ |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 1 | 0 |
| 3 | 0 | 1 | 1 |
| 4 | 1 | 0 | 0 |
| 5 | 1 | 0 | 1 |
| 6 | 1 | 1 | 0 |
| 7 | 1 | 1 | 1 |

There are $2^3 = 8$ rows. With three loops we can write them all:

```python
for z1 in range(2):
    for z2 in range(2):
        for z3 in range(2):
            print(z1, z2, z3)
```

This code does not generalize: for $n = 50$ variables we would need 50 nested
loops, which nobody writes. The general version needs a different idea —
**recursion**: one loop that decides $z_i$, and then calls itself to decide the
rest. That is exactly what `SAT_Table` does in the
[SAT-Table](SAT-Table.ipynb) notebook.

The size of this space grows fast:

| $n$ | $2^n$ | $n^n$ (labels $0..n-1$) |
|---|---|---|
| 10 | 1 024 | $10^{10}$ |
| 20 | 1 048 576 | $1.05\times 10^{26}$ |
| 30 | 1 073 741 824 | $2.06\times 10^{44}$ |
| 50 | $1.13\times 10^{15}$ | $8.88\times 10^{84}$ |
| 100 | $1.27\times 10^{30}$ | $10^{200}$ |

An image with $200\times 300$ pixels has $n = 60\,000$ points, so even the
*binary* space has $2^{60000}$ labelings. Comparing one labeling per nanosecond
would take longer than the age of the universe, by a lot. Enumeration is a tool
for understanding, not for real data.

## 3. Counting clusterings: Stirling numbers

How many ways are there to split $n$ *distinct* objects into exactly $k$
non-empty groups, when the groups themselves are not numbered (a partition)?
The answer has a name: the **Stirling number of the second kind**,

$$
S(n,k) = \left\{ \begin{matrix} n \\ k \end{matrix} \right\}.
$$

> **A warning about the name.** *Stirling's formula* (or *Stirling's
> approximation*) is the estimate $n! \approx \sqrt{2\pi n}\,(n/e)^n$ for the
> factorial. *Stirling numbers* are something else: counts of permutations
> (first kind) and of partitions (second kind). In this course we only need the
> second kind, and we write $S(n,k)$ for it.

Small values:

| $n \backslash k$ | 1 | 2 | 3 | 4 | 5 | $\sum_k S(n,k)$ |
|---|---|---|---|---|---|---|
| 1 | 1 | | | | | 1 |
| 2 | 1 | 1 | | | | 2 |
| 3 | 1 | 3 | 1 | | | 5 |
| 4 | 1 | 7 | 6 | 1 | | 15 |
| 5 | 1 | 15 | 25 | 10 | 1 | 52 |
| 6 | 1 | 31 | 90 | 65 | 15 | 203 |

Each row of the table adds up to a **Bell number** $B_n$: the number of
partitions of $n$ objects into *any* number of blocks,
$B_n = \sum_{k=1}^{n} S(n,k)$. The sequence $1, 2, 5, 15, 52, 203, 877, 4140,
21147, 115975,\ldots$ is the number of clusterings of $n$ points if we do not
fix $k$ in advance. Note how small these numbers still are: for $n=10$ there
are only 115 975 clusterings, so brute force is genuinely possible for tiny
datasets — and that is exactly what the BF-Clustering notebook exploits.

### The recurrence

The standard way to compute $S(n,k)$ is a recurrence. Look at object $n$ (the
last one). In any partition into $k$ blocks there are two possibilities:

1. object $n$ is **alone** in its block. The other $n-1$ objects then form a
   partition into $k-1$ blocks: $S(n-1,k-1)$ ways;
2. object $n$ is **not alone**. Remove it: the remaining $n-1$ objects form a
   partition into $k$ blocks, $S(n-1,k)$ ways, and object $n$ can be added to
   any of those $k$ blocks: $k \cdot S(n-1,k)$ ways.

Adding the two disjoint cases,

$$
S(n,k) = k\,S(n-1,k) + S(n-1,k-1),
$$

with base cases $S(n,1) = S(n,n) = 1$ and $S(n,k) = 0$ for $k > n$. This is a
direct transcription of "split the first decision into cases", i.e. the same
style of thinking as recursion. The notebook turns it into a Python function,
memoizes it, and cross-checks it against the closed form

$$
S(n,k) = \frac{1}{k!}\sum_{j=0}^{k} (-1)^j \binom{k}{j} (k-j)^n .
$$

### What the numbers say about clustering

- For $k=2$ there is a closed form, $S(n,2) = 2^{n-1}-1$: the block that
  contains point 1 is determined by which of the other $n-1$ points join it,
  and a block and its complement give the same partition, so $2^{n-1}$ subsets
  collapse to $2^{n-1}-1$ partitions. That is the number the BF-Clustering
  notebook walks through.
- With 150 points and $k=3$ we get $S(150,3) \approx 6.17 \times 10^{70}$
  clusterings. At $10^9$ scorings per second this is about
  $2 \times 10^{54}$ years. Exhaustive search is not slow; it is *impossible*.
- In general $S(n,k)$ grows like $k^n/k!$ for fixed $k$, and $B_n$ grows
  super-exponentially. This is why every clustering chapter, after stating the
  problem, immediately replaces enumeration by heuristics: k-means, hierarchical
  clustering, LVQ {cite}`zaki2020data`.

Exhaustive search therefore has two honest uses: on *tiny* data it gives the
true optimum, which we can use to check whether a heuristic (k-means) found the
global optimum or only a local one; and theoretically it defines the problem —
"clustering" *means* minimizing a score over the set of partitions, and the
count tells us how large that set is.

## 4. Recursion, the tool of this chapter

All three notebooks are built on one programming idea, so it is worth stating
plainly. A **recursive function** solves a problem by calling *itself* on a
smaller instance of the same problem. It needs exactly two parts:

- a **base case**: the smallest instance, answered directly (here: "all $n$
  decisions are made, so record the result");
- a **recursive case**: do one decision, then delegate the remaining decisions
  to a recursive call.

Three habits prevent almost all beginner bugs:

1. **Make progress.** Every call must work on a strictly smaller instance, or
   the program never stops. Here the counter $i$ always increases, and the base
   case tests $i = n$.
2. **`return` is not `yield`.** A `return` inside the loop of the recursive case
   leaves the function after the *first* child is explored, so we see only one
   leaf of the whole search tree. To emit *all* leaves we either fill an output
   list, or make the function a **generator** with `yield` / `yield from`.
3. **Beware of shared, mutable state.** The elegant trick of writing the
   decision straight into the array (`for x[i] in range(2)`) means that one
   single array travels through the whole recursion. If we store *references* to
   it, every "row" we saved turns out to be the same object, and at the end all
   rows look identical. Either copy (`x.copy()`) or consume the value
   immediately.

The second and the third point appear, with the wrong code and its wrong
output, in the SAT-Table notebook; all three come back in the other two.

## 5. The three notebooks

### SAT-Table — enumerate and count

Writes the truth table three ways (nested loops, recursion, generator), fixes
the two classic failures (`return` instead of `yield`; the aliasing trap), then
counts rows: $2^n$ for bits, $S(n,k)$ for partitions. Ends with a memoized
version of the Stirling recurrence and a table showing why recomputation
without memoization is hopeless.

### N-Queen — recursion with pruning

A placement of $n$ queens is an assignment too: one column per row. But now
there are **hard constraints** (no shared column or diagonal), and they are
checked *before* recursing, so most of the tree is never visited. Comparing the
number of visited nodes with $n^n$ is the cleanest demonstration of why
constraints matter. The notebook also counts all solutions for $n \le 10$
(1, 0, 0, 2, 10, 4, 40, 92, 352, 724) and shows one solution as a picture.

The same notebook then drops the constraints and only *counts violations* — a
soft objective instead of a feasibility test. That is precisely the step from
"find an assignment satisfying the rules" to "find the assignment with the
smallest cost", which is what clustering is.

### BF-Clustering — exhaustive optimization

Enumerates all 2-clusterings with the same recursion, keeps only the ones with
two non-empty clusters, and scores each by the within-cluster sum of squares
(WCSS/SSE). The minimum over all candidates is the true optimum. The notebook
then:

- derives the pairwise form $\sum_{i<j}\|\mathbf{x}_i-\mathbf{x}_j\|^2 =
  |C|\sum_i \|\mathbf{x}_i-\boldsymbol\mu\|^2$ (Lemma 2 of
  [Clustering-Part2](Clustering-Part2.ipynb)) and uses it as a cross-check of
  the code;
- explains why the scalar formula `math.sqrt((a-b)**2)` fails on points, and
  replaces it by a coordinate-wise distance (`np.linalg.norm` and
  `scipy.spatial.distance.cdist` are the library versions of the same thing);
- compares the exhaustive optimum with k-means, which may stop in a local
  minimum;
- counts candidates with $S(n,2) = 2^{n-1}-1$ and, for general $k$, with
  $S(n,k)$ — verifying a recursive enumeration against the Stirling recurrence.

## 6. What to remember

- A clustering is a *partition*; a program represents it as a label vector, and
  labels are arbitrary names.
- The number of partitions of $n$ points into $k$ non-empty clusters is the
  Stirling number $S(n,k)$; the number of labelings is $k^n$; the two differ by
  the $k!$ relabelings (and by the empty clusters).
- Recursion is how we enumerate a space of $n$ decisions without writing $n$
  loops; generators are how we hand the results out one by one; memoization is
  how we avoid recomputing the same subproblem.
- Exhaustive search is exact but feasible only for very small $n$. Its value is
  to *define* the optimization problem and to *test* heuristics such as k-means.

## Exercises

1. List by hand the $S(4,2)=7$ partitions of $\{1,2,3,4\}$ into two non-empty
   blocks, and check them against $2^{3}-1$.
2. Modify `SAT_Table` so each variable takes values $0,1,2$. How many rows does
   it print for $n=4$? How many for general $n$?
3. Prove $S(n,2) = 2^{n-1}-1$ (hint: in a partition into two blocks, decide for
   each of the points $2,\ldots,n$ whether it joins the block of point 1).
4. Prove and check numerically the Bell recurrence
   $B_{n+1} = \sum_{j=0}^{n}\binom{n}{j} B_j$.
5. How long would $2^{60}$ operations take at one operation per nanosecond?
   Compare with the age of the universe ($\approx 1.4\times10^{10}$ years).
6. In BF-Clustering, how many 2-clusterings does a dataset with $n=20$ points
   have? How long would scoring them take at $10^6$ per second?

## Sources

- T. Hastie, R. Tibshirani, J. Friedman, *The Elements of Statistical
  Learning*, Sec. 14.3 (cluster analysis, combinatorial view).
- {cite}`zaki2020data`, Ch. 17 (clustering; the remark that there are about
  $k^n/k!$ clusterings of $n$ points into $k$ groups).
- Any combinatorics text, for Stirling numbers and Bell numbers.
- Class notebooks: [SAT-Table](SAT-Table.ipynb), [N-Queen](N-Queen.ipynb),
  [BF-Clustering](BF-Clustering.ipynb); `SAT-Solver.cpp` in the same folder is
  an optional C++ reference for the same idea.
