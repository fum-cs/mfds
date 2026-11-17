<div class="langswitch langswitch-ltr">
  <strong>English</strong> · <a href="#lang-fa">فارسی</a>
</div>

# Clustering Tumors by Gene Expression

![](img/banner.png)

Computer Science Dept, Ferdowsi University of Mashhad

## The question

A pathologist names a tumor by looking at tissue under a microscope. A
microarray asks a different question of the same sample: which of several
thousand genes are being transcribed, and how strongly. If the tissue of origin
is written into that expression profile, then a **clustering algorithm — which
never sees the diagnosis — should be able to recover it**. That is the claim
this example tests, and it is a stronger claim than "the samples form groups":
it says the diagnosis is *contained in the measurements*.

The experiment is small enough to follow by hand, and it is a good first case
study because the algorithm is ordinary k-means; all the judgement is in how the
output is read.

## The data

* A matrix of **6830 rows (genes) × 64 columns (samples)** of expression values.
* The objects to cluster are the **samples**. Sample $j$ is the vector of its
  6830 measurements, i.e. a point in $\mathbb{R}^{6830}$. Two samples are close
  when their whole profiles agree, not when one particular gene agrees.
* Each sample also carries a **pathology label**: breast, CNS, colon, K562,
  leukemia, MCF7, melanoma, NSCLC, ovarian, prostate, renal, or *unknown*. (K562
  and MCF7 are cell lines rather than primary tumors, which matters later.)
* The labels are **withheld during clustering**. They are used afterwards, to
  ask what each cluster turned out to contain.

With $p = 6830$ and $n = 64$ there are far more directions than points: the
distances live in the regime described on the
[curse-of-dimensionality page](High-Dimensional-Data-and-The-Curse-of-Dimensionality.ipynb).
Every distance is estimated from 64 points only, so no cluster boundary here is
sharp in a statistical sense.

## Deciding what "similar" means

K-means needs a distance before it needs anything else, and on expression data
the choice does more work than the algorithm:

* **Euclidean distance on raw values** is dominated by the genes with the largest
  variance and by the overall brightness of the array.
* **Correlation distance** ($1 - \rho$ between two profiles) compares *shape*
  instead of level, and is the usual default for expression data, because a
  sample can be brighter overall without being a different tissue.
* **Standardizing each gene** (subtracting its mean, dividing by its standard
  deviation across samples) puts all 6830 genes on the same footing and is what
  makes "many small agreements" count as much as "one large one".

Whatever is chosen must be reported: two analyses of the same matrix with
different distances are two different experiments, and they can disagree
completely about which samples are neighbours.

## Running k-means

For a fixed $K$, k-means alternates two steps until the assignment stops
changing:

1. assign each sample to its nearest centroid;
2. move each centroid to the mean of the samples assigned to it.

The quantity it decreases is the **within-cluster sum of squares**

$$
\mathrm{WSS}(K) = \sum_{k=1}^{K} \sum_{x \in C_k} \lVert x - \mu_k \rVert^2 .
$$

Two practical points that this example makes concrete:

* **$K$ is not estimated by the algorithm.** One plots $\mathrm{WSS}(K)$ against
  $K$ and looks for an elbow; on data like this the curve falls smoothly enough
  that no value stands out, so $K$ has to be *chosen for the purpose at hand*.
  Here $K = 3$ was fixed, which is a deliberate coarsening: eleven tissue types
  are being squeezed into three groups.
* **K-means stops at a local minimum.** Different random starts give different
  answers; a single run is not a result. The standard guard is to restart many
  times and keep the solution with the smallest WSS.

## The result

Running k-means with $K = 3$ and then opening the envelope — counting which
pathology labels landed in which cluster — gives:

| Cluster | Breast | CNS | Colon | K562 | Leukemia | MCF7 | Melanoma | NSCLC | Ovarian | Prostate | Renal | Unknown | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | 3 | 5 | 0 | 0 | 0 | 0 | 1 | 7 | 6 | 2 | 9 | 1 | 34 |
| **2** | 2 | 0 | 0 | 2 | 6 | 2 | 7 | 2 | 0 | 0 | 0 | 0 | 21 |
| **3** | 2 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |

Read it by rows, not by eye-catching cells:

* **Cluster 3 is essentially the colon cancers**: all seven colon samples, plus
  two breast samples. A group that is 78% one tissue was found without the
  algorithm ever being told what the tissues were.
* **Cluster 2 gathers the blood and skin tumors**: the six leukemias with the
  K562 and MCF7 lines, the melanomas, and two NSCLC samples.
* **Cluster 1 is the remainder**: CNS, ovarian, renal, prostate, most NSCLC, a
  few breast and one melanoma sample. It is the largest and least pure group,
  which is what one should expect when eleven types are forced into three boxes.

A table like this — clusters against known labels — is the right way to report a
clustering when labels exist, because it shows both the purity of a cluster and
its mistakes. A summary that only says "the clusters correspond to tissue types"
hides exactly the information a reader needs.

## A label that turned out to be wrong

The two *breast* samples sitting inside the melanoma-dominated cluster were
re-examined after the clustering. They were not breast cancers: they were
melanomas that had metastasized to the breast.

This is the most valuable outcome in the whole example, and it is worth being
precise about what happened. The clustering did not "discover the truth"; it
produced a *suspicion* — these two profiles look like that group, not like the
group their labels claim. A pathologist then checked, and the suspicion was
confirmed. Unsupervised learning can be right *against* its labels, but only a
follow-up investigation turns that into knowledge. Without the re-examination,
the honest conclusion would have been "two samples are inconsistent with their
labels, for reasons unknown".

## What k-means cannot give here

Two limits of the method show up sharply in this application:

1. **No order inside a cluster.** K-means returns sets. The members of cluster 1
   can only be listed alphabetically, which says nothing about which of them are
   most alike; a reader who wants "these nine samples form a subgroup" gets no
   help.
2. **No nesting across $K$.** The solution for $K = 4$ need not refine the
   solution for $K = 3$: clusters can be split, merged and reshuffled when $K$
   changes. A table built for one $K$ cannot be extended when the number of
   groups is revised, so every change of $K$ costs a new interpretation.

Both are cured by the same change of report: **hierarchical clustering** returns
a dendrogram, which orders the samples along a line and gives a nested family of
partitions — one picture from which any number of clusters can be read off after
seeing the structure. For a study like this one, where the number of groups is
unknown and the ordering within a group is meaningful, the dendrogram is the more
informative object; k-means is the cheaper summary. See
[hierarchical clustering](Hierarchical-Clustering.ipynb).

## Limits of the conclusion

* **$n = 64$.** A single atypical sample can pull a centroid, and one sample
  moving between clusters changes the table visibly. The agreement is strong but
  it is not a significance test.
* **Gene selection is a modelling decision.** Clustering all 6830 genes gives one
  answer; restricting to genes that vary most across samples, or that correlate
  with survival, changes every distance and can change the clusters.
* **Missing values and preprocessing.** Expression matrices are noisy and often
  incomplete; how the gaps are filled (row means, $k$-nearest neighbours, a
  low-rank fit) moves samples as much as a different distance would.
* **One run proves nothing.** With random initialization, report the best of many
  restarts, and check how often the same partition is recovered.

## Summary

* Clustering on expression profiles recovers tissue of origin well enough to be
  useful, using no labels at all.
* The interesting part of the result is the contingency table, not the clusters
  themselves: it exposes both the clean groups and the mixed ones.
* A cluster that disagrees with a label is a hypothesis about the label, to be
  checked outside the algorithm.
* When the number of groups is unknown and the ordering inside a group matters,
  a dendrogram answers more questions than a set of centroids.
* $p \gg n$ makes every distance noisy; report the preprocessing and the number
  of restarts, or the result is not reproducible.

## Questions for class

1. Why are the **samples** clustered and not the 6830 genes? What would a cluster
   of genes mean, and what would you learn from one?
2. The table has eleven tissue types and $K = 3$. Which types would you expect to
   be merged first, and does the table agree with your expectation?
3. If the two "breast" samples had never been re-examined, what would the correct
   conclusion of the experiment have been?
4. Cluster 2 mixes leukemia, K562, MCF7 and melanoma. Is that a failure of
   k-means, of the distance, or of forcing eleven types into three clusters?
5. How would you check that a cluster is stable rather than an accident of the
   random initialization?

## Exercises

1. Compute the correlation-distance matrix of the $64 \times 6830$ matrix, run
   average-linkage hierarchical clustering, and compare the top two splits with
   clusters 3 and 2 above.
2. Rerun k-means with 50 random starts and record how often the $K = 3$ table
   above is reproduced exactly. What does the answer say about the reported
   result?
3. Standardize the genes before clustering and compare the resulting table with
   the one shown. Which clusters survive the change?
4. Plot $\mathrm{WSS}(K)$ for $K = 1,\ldots,10$. Is there an elbow? If not, state
   a criterion other than the elbow for choosing $K$, and its cost.

## Source and further reading

The data set (NCI60 tumor cell lines) and the analysis summarized above are from
**§14.3.8, "Example: Human Tumor Microarray Data", pp. 512–514** of
{cite}`hastie2009esl`; the table is that section's cross-tabulation of three
k-means clusters against the pathology labels, and the two mislabelled samples
are reported there. The high-dimensional setting is discussed in
[High-Dimensional Spaces](High-Dimensional-Spaces.md), and the alternative
report — the dendrogram — in
[hierarchical clustering](Hierarchical-Clustering.ipynb).
