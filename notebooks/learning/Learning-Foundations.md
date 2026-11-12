# Learning Foundations: Classification and Generalization

**Not in this course:** SVM (other course), Bayesian methods and HMM (other courses). The *kernel trick* is not an SVM topic and has its own page: [The Kernel Method](Kernel-Trick.md).

## Goals

- Classification problem: train/test split
- kNN revisited as a nonparametric baseline
- Occam’s razor and why simple models can generalize
- Uniform convergence and the VC *idea* (intuition, not full theory)

## 1. Two risks, one gap

A classifier is a function $h:\mathcal{X}\to\{-1,+1\}$ chosen from a class $\mathcal{H}$. Fix a
loss, say the 0–1 loss $\ell(h(x), y) = \mathbb{1}\{h(x)\neq y\}$. There are two numbers attached to
$h$, and they are different objects:

$$
\text{true risk } L(h) = \mathbb{E}_{(x,y)\sim P}\big[\ell(h(x),y)\big],
\qquad
\text{empirical risk } \hat L_n(h) = \frac1n\sum_{i=1}^{n}\ell(h(x_i),y_i).
$$

The first is a property of $h$ alone, but it depends on the unknown distribution $P$; the second can
be computed from the sample $S=\{(x_i,y_i)\}_{i=1}^n$ but is a random variable. **Empirical risk
minimisation** (ERM) returns

$$
\hat h = \arg\min_{h\in\mathcal{H}} \hat L_n(h),
$$

and the only question that matters is how far $L(\hat h)$ can be from $\hat L_n(\hat h)$ — the
*generalisation gap*. Everything in this page is a bound on that gap.

Two immediate observations set the agenda.

- **ERM over all functions is useless.** If $\mathcal{H}$ is the set of *all* functions
  $\mathcal{X}\to\{-1,+1\}$, the predictor that memorises the sample has $\hat L_n = 0$ and no
  guarantee on $L$: on a new point it can be wrong with probability one. The restriction to a
  smaller class $\mathcal{H}$ is what makes learning possible, and the *size* of that class will
  appear explicitly in the bounds.
- **The gap must be uniform.** We do not need $\hat L_n(h)\approx L(h)$ for the $h$ we happen to
  output; we need it for *every* $h\in\mathcal{H}$ simultaneously, because the output itself
  depends on the sample. That "for every" is what costs the extra $\log$ factors below.

## 2. Uniform convergence, finitely many hypotheses

Suppose $\mathcal{H}$ is finite, $|\mathcal{H}| = M$, and the loss is bounded in $[0,1]$. For a
fixed $h$, Hoeffding's inequality gives

$$
\mathbb{P}\big(|\hat L_n(h) - L(h)| \ge \varepsilon\big) \le 2e^{-2n\varepsilon^{2}} .
$$

A union bound over the $M$ hypotheses, followed by choosing $\varepsilon$ so that the right side is
at most $\delta$, yields: with probability at least $1-\delta$, **simultaneously for all
$h\in\mathcal{H}$**,

$$
\big|\hat L_n(h) - L(h)\big| \;\le\; \sqrt{\frac{\log M + \log(2/\delta)}{2n}} .
$$

This is the whole idea of statistical learning theory, and it already answers the practical
questions:

- **More data helps like $1/\sqrt n$.** With $M = 1000$ hypotheses and $n = 1000$ samples the gap is
  about $\sqrt{6.9/2000}\approx 0.059$, that is six percentage points; $n = 10^4$ halves it.
- **More hypotheses hurt like $\sqrt{\log M}$.** Growing the class from $10^3$ to $10^6$ hypotheses
  costs a factor $\sqrt{2}$ in the gap, not a factor $1000$. This is why rich classes are usable at
  all, and why the relevant complexity is logarithmic in the number of models.
- **The bound is loose on purpose.** It holds for adversarial $P$ and for the worst $h$; on any
  real problem the true gap is much smaller. Its value is the shape of the trade-off, not the
  constant.

## 3. Infinitely many hypotheses: the VC idea

A linear classifier on $\mathbb{R}^d$ has infinitely many parameter vectors, so $M=\infty$ and the
union bound dies. What replaces $M$ is the number of *distinguishable behaviours on $n$ points*.
A hypothesis class **shatters** a set of $n$ points if it can realise all $2^n$ labellings of them;
the **VC dimension** is the largest $n$ for which some set of $n$ points is shattered.

| Class on $\mathbb{R}$ or $\mathbb{R}^2$ | VC dimension | Why |
|---|---|---|
| constant classifiers | 0 | one behaviour only |
| thresholds $\mathbb{1}\{x \ge t\}$ | 1 | two points: one labelling impossible |
| intervals $[a,b]$ | 2 | two points shattered; with three, the middle alone cannot be isolated |
| half-spaces (lines) in $\mathbb{R}^2$ | 3 | any three non-collinear points; four points of a convex quadrilateral defeat it |
| half-spaces in $\mathbb{R}^d$ | $d+1$ | the classical count |

The theorem we will not prove says the gap is controlled by $V$, the VC dimension, in place of
$\log M$:

$$
L(\hat h) \;\le\; \hat L_n(\hat h) + O\!\left(\sqrt{\frac{V\log n + \log(1/\delta)}{n}}\right)
\qquad\text{with high probability,}
$$

and, conversely, no algorithm can learn a class of infinite VC dimension in this distribution-free
sense. So $V$ is a *capacity*: it must be finite, but it may grow with the data, and the price is
one more $\log n$. The constants in the theorem are useless in practice (they are far too
pessimistic for a few thousand samples), which is why the rest of the course measures the gap with
data splits rather than with the bound.

## 4. Measuring the gap: splits and cross-validation

The theory says the gap exists; practice needs a number for it.

1. **Train / validation / test.** Fit on the training part, choose hyperparameters (number of
   neighbours, number of components, kernel width) on the validation part, and report the test
   error **once**. The test set is a proxy for $L(\hat h)$, so it must not influence any choice.
2. **$k$-fold cross-validation.** Split into $k$ folds, train on $k-1$, validate on the held-out
   fold, average. It uses the data more efficiently and gives a variance estimate; it is
   $k$ times more expensive.
3. **Leakage.** Standardising, selecting features, or tuning on the full data before splitting makes
   the estimate optimistic. The rule is mechanical: *anything fitted* — means, variances, PCA
   directions, selected features — is fitted **inside** each fold.
4. **What cross-validation cannot see.** It estimates the error of the *procedure* on data from the
   same distribution. Distribution shift, duplicated rows across folds, and time-ordered data break
   it silently; for the last one the split must respect time.

The run of numbers we produce in the labs — validation accuracy against $k$ in kNN, against $K$ in
k-means, against the number of components in PCA — is this section being used, not a separate topic.

## 5. Occam, bias, variance

The bounds above are worst case; the reason simple models often win in practice is the
bias–variance decomposition of the squared error,

$$
\mathbb{E}\big[(y - \hat f(x))^2\big] = \text{noise} + \big(\text{bias}\big)^2 + \text{variance},
$$

where the bias grows and the variance shrinks as the class gets richer. The best model sits where
the two cross, which is a *different* question from "which class has smaller VC dimension" — a
small class can be badly biased. The [Bias–Variance Tradeoff](../high-dimensional-spaces/Bias-Variance-Tradeoff.ipynb)
page does this decomposition with numbers; here we only note that the two stories (capacity bounds
and bias–variance) describe the same U-shaped curve from two directions.

A practical checklist that follows from the page, useful for the assignments:

- Report **both** training and validation error; a small training error alone says nothing.
- Say which quantity was used to make each choice; anything tuned on the test set invalidates it.
- Compare against a **baseline** (the majority class, or 1-NN) before claiming a method works.
- When adding parameters, say what the class gained in capacity and what it cost in variance.

## Exercises

1. For a fixed classifier and a known data distribution, compute the true risk and the empirical risk on samples of size $10,100,1000$. Plot both and describe the gap.
2. Show that empirical risk minimisation over *all* functions has zero empirical risk and no guarantee of generalisation. Where exactly does a restriction on the hypothesis class enter the argument?
3. Prove that the VC dimension of intervals on the line is $2$: exhibit two shattered points and show that no three can be shattered.
4. Why is $K$-fold cross-validation preferable to a single train/test split when choosing a model? Give a case in which it is still optimistic.
5. Use the union bound of section 2 with $M=2^{10}$ and $\delta=0.05$ to find the sample size needed for a gap of $0.02$; compare with the same computation for $M=10$. Which of the two grows faster in $M$, the gap or the sample size?
6. Give a labelling of four points in general position in $\mathbb{R}^2$ that no line can realise, and one of five points that *is* realisable, to see why the VC dimension of half-spaces is $d+1$ and not more.
7. A colleague standardises the features and runs PCA on all data before the cross-validation split, then reports a very low error. Explain precisely which estimate is biased and how to repair the pipeline.

## Sources

- Blum, Hopcroft, Kannan, *Foundations of Data Science*, Ch. 12 (selected).
- Hastie, Tibshirani, Friedman, *The Elements of Statistical Learning*, 2nd ed., §7.1–7.3 (model
  assessment and the bias–variance decomposition) and §7.9 (VC dimension).
- Shalev-Shwartz, Ben-David, *Understanding Machine Learning*, Ch. 2–6 (ERM, uniform convergence,
  VC dimension).
