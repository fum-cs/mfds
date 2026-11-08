![](img/banner.png)

# Example: Human Tumor Microarray Data

**Mahmood Amintoosi, Fall 2026**

Computer Science Dept, Ferdowsi University of Mashhad

## Where this example sits

Section 14.3.8 of {cite}`hastie2009esl` (pp. 512–514) is a worked case of
**high-dimensional clustering**: what happens when a clustering algorithm is
applied to data where the number of measurements per object is far larger than
the number of objects. It is worth reading as a case study rather than as an
algorithm, because the algorithm is plain K-means and everything interesting is
in how the result is *interpreted* — and in what the book says is wrong with it.

## The data

* A **6830 × 64** matrix of real numbers: one row per **gene**, one column per
  **tissue sample**, each entry an expression measurement.
* The objects to be clustered are the **samples**: sample *j* is the vector of
  its 6830 expression values, i.e. a point in `R^6830`.
* Every sample carries a label from the pathology report: *breast, CNS, colon,
  K562, leukemia, MCF7, melanoma, NSCLC, ovarian, prostate, renal*, and a few
  *unknown*.
* The labels are **not used** by the clustering. They are looked at afterwards,
  to see what the clusters turned out to contain.

The setting is `p = 6830` and `n = 64`: the distances between samples are computed
in a space where there are far more directions than points, which is exactly the
regime discussed on the
[curse-of-dimensionality page](High-Dimensional-Data-and-The-Curse-of-Dimensionality.ipynb).

## The question the example asks

If two tumors arose in the same tissue, their gene-expression profiles should be
more similar to each other than to tumors of another tissue. If that is true, an
**unsupervised** method — one that never sees the pathology labels — should
recover the tissue of origin by itself. A successful clustering would then be a
diagnostic aid: a new sample joins the group it resembles, and the group has a
name.

That is a stronger claim than "the samples cluster": it says the *labels are
recoverable from the measurements*, and it can be tested because the labels
exist.

## The experiment

K-means is run on the 64 sample vectors, with `K` from 1 to 10, and the total
within-cluster sum of squares is recorded for each — the book's Figure 14.8. The
curve has **no clear kink**, which is the honest outcome more often than the
textbook habit suggests; the choice of `K` is therefore made *for illustration*,
and the book takes `K = 3`.

The result is reported as a contingency table of clusters against the pathology
labels (Table 14.2), reproduced below.

| Cluster | Breast | CNS | Colon | K562 | Leukemia | MCF7 | Melanoma | NSCLC | Ovarian | Prostate | Renal | Unknown | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | 3 | 5 | 0 | 0 | 0 | 0 | 1 | 7 | 6 | 2 | 9 | 1 | 34 |
| **2** | 2 | 0 | 0 | 2 | 6 | 2 | 7 | 2 | 0 | 0 | 0 | 0 | 21 |
| **3** | 2 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |

Three things stand out in that table.

* **Cluster 3 is the colon cancers.** All seven colon samples land there, plus
  two breast samples. A cluster that is 78% one tissue type was found without
  ever being told what the tissues were.
* **Cluster 2 is a family of blood and skin tumors** — the leukemias, K562, MCF7,
  melanoma, plus part of the NSCLC group.
* **Cluster 1 collects everything else** — CNS, ovarian, renal, prostate, most of
  the NSCLC — the largest and least pure group, which is what one expects from
  `K = 3` on twelve types.

## The finding the book highlights

> We see that the procedure is successful at grouping together samples of the
> same cancer. In fact, the two breast cancers in the second cluster were later
> found to be misdiagnosed and were melanomas that had metastasized.

This is the most quoted sentence of the section, and it should be quoted with its
qualifications. What the clustering did was place two samples labelled *breast*
next to the melanoma group; the subsequent re-examination is what established that
the labels were wrong. The algorithm proposed a suspicion; the pathologist
confirmed it. An unsupervised method can be *right against its labels* — but only
a follow-up investigation turns that into knowledge.

## The two shortcomings the book names

Section 14.3.8 is not only a success story. The book lists two defects of K-means
in this application:

1. **No ordering inside a cluster.** K-means returns sets, not sequences; the
   samples of a cluster have to be listed alphabetically, which says nothing
   about how similar they are to each other.
2. **Memberships are not nested.** The solution for `K = 4` need not refine the
   solution for `K = 3`: a cluster can be split and recombined in arbitrary ways
   when `K` changes. A table built for one `K` therefore cannot be extended when
   `K` is revised.

Both defects point to the same repair, which is why the book says *hierarchical
clustering is probably preferable for this application*: a dendrogram gives a
linear ordering of the samples and a **nested family** of partitions, so the
analyst can choose the number of groups *after* seeing the structure instead of
before.

## What this example teaches

* **Clusters are not classes.** The label of a cluster is assigned afterwards, by
  looking at what fell into it; the algorithm itself never had a name for it.
* **A contingency table is the right way to report a clustering when labels
  exist** — it shows both the purity and the mistakes, and it would hide nothing
  if a cluster were a mixture of three tissues.
* **The elbow can be absent.** A flat inertia curve is information: it says the
  data has no natural number of groups at this scale.
* **`n = 64` is small.** With 6830 genes and 64 samples, a handful of samples can
  dominate a cluster; the apparent success is strong but not a statistical proof.
* **Selection matters.** The clustering above uses all 6830 genes; restricting to
  the genes that vary most, or that correlate with survival, changes the
  distances, and the choice of genes is a modelling decision made by the analyst.

## Questions for class

1. Why is the *samples* dimension clustered, and not the genes? What would
   clustering the 6830 genes mean, and what would a cluster of genes represent?
2. Table 14.2 has 12 tissue types and `K = 3`. What is lost by forcing twelve
   into three? Which types would you expect to be conflated first?
3. If the two breast samples had *not* been re-examined, what would the honest
   conclusion of the experiment have been?
4. The inertia curve has no kink. What else could be used to choose `K`, and what
   would each criterion cost in interpretation?
5. K-means used Euclidean distance on 6830-dimensional vectors. What happens to
   that distance if one gene has a much larger variance than the rest, and what is
   the standard repair?

## Sources

* The example, its numbers, Table 14.2 and the quotations: §14.3.8 of
  {cite}`hastie2009esl`, pp. 512–514; the data set itself is described in Chapter 1
  of the same book and is distributed with it.
* The remedy the book recommends for the two shortcomings — the dendrogram and the
  nested partitions — is the subject of the
  [hierarchical clustering page](Image-Clustering-Hierarchical.ipynb).
* The high-dimensional setting in which these distances are computed is discussed
  in [High-Dimensional Spaces](High-Dimensional-Spaces.md).
