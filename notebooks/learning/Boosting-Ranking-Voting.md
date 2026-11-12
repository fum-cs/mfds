# Boosting Sketch, Ranking, and Voting

(For other courses)

This page is a survey, not a session: it collects the three places where "combining many weak
decisions" appears in the course — boosting a classifier, aggregating a ranking, and voting — and it
shows that the three are the same kind of object, an average of experts with weights.

## 1. From weak to strong

A **weak learner** is a rule that does slightly better than chance on any distribution over the
data: for some $\gamma>0$, its error is at most $\tfrac12-\gamma$. A **strong learner** can reach
any target error with enough data. The surprising fact of boosting (Kearns' question, answered by
Schapire in 1990) is that the two are equivalent: a weak learner repeated on reweighted data
produces a strong one. Boosting is therefore *not* a new hypothesis class; it is a way of turning a
small class into a large one, and its complexity is controlled by the number of rounds, not by the
dimension.

## 2. AdaBoost in five lines

Labels $y_i\in\{-1,+1\}$, weights $D_1(i)=1/n$, and for $t=1,\dots,T$:

$$
\varepsilon_t=\sum_i D_t(i)\,\mathbb{1}\{h_t(x_i)\neq y_i\},
\qquad
\alpha_t=\tfrac12\log\frac{1-\varepsilon_t}{\varepsilon_t},
\qquad
D_{t+1}(i)=\frac{D_t(i)\,e^{-\alpha_t y_i h_t(x_i)}}{Z_t},
$$

and the final classifier is the weighted vote $H(x)=\operatorname{sign}\big(\sum_t\alpha_t h_t(x)\big)$,
with $Z_t$ the normalising constant. Three readings of the same update:

- **Reweighting.** A point that the current rule gets wrong gets its weight multiplied by
  $e^{\alpha_t}>1$; a point it gets right is down-weighted. The next weak learner is forced to
  concentrate on the mistakes of the previous ones.
- **A vote.** $\alpha_t$ is the weight of the expert: zero for an error of $\tfrac12$, growing
  without bound as $\varepsilon_t\to0$. A perfect rule would get infinite weight, which is why in
  practice $\varepsilon_t$ is clipped away from $0$.
- **Gradient descent.** AdaBoost is forward stagewise minimisation of the exponential loss
  $\sum_i e^{-y_i F(x_i)}$ over $F=\sum_t\alpha_t h_t$, one coordinate at a time. That is the same
  "fit the negative gradient" idea as the gradient descent page, with a different loss.

The classical guarantee is the training-error bound
$\hat L_n(H)\le \prod_t 2\sqrt{\varepsilon_t(1-\varepsilon_t)}$, which is at most
$2^T\prod_t\sqrt{\varepsilon_t}$; if every $\varepsilon_t\le \tfrac12-\gamma$ the product decays
geometrically and the training error reaches zero in $O(\log n/\gamma^2)$ rounds. Note what the
bound does *not* say: it is about training error, and boosting can overfit when the weak learners
are too strong or the data are noisy.

## 3. Ranking as a linear-algebra problem

Given $n$ items and a set of pairwise comparisons ("$i$ beats $j$"), the task is a global order.

- **Borda count.** Each voter ranks the items; item $i$ receives the sum of its ranks (or of
  $n-\text{rank}$), and the items are sorted by that score. Equivalently, item $i$ gets one point
  for every item it beats in every voter's list, so the Borda score of $i$ is
  $\sum_{j} \#\{\text{voters ranking } i \text{ above } j\}$.
- **Pairwise matrix.** Collect the results in a matrix $W$ with $W_{ij}$ = number of voters who
  prefer $i$ to $j$. Then $W+W^\top = m\,\mathbf{1}\mathbf{1}^\top - (\text{ties})$, and the row sums
  of $W$ are the Borda scores. Ranking is now a matrix problem: a score vector is the stationary
  object of $W$, which is exactly the PageRank computation of the random-walks page when $W$ is
  normalised row by row.
- **The catch.** No method is simultaneously faithful to all pairwise majorities (Arrow's theorem
  for social choice, and the Condorcet paradox below), so "the" ranking always involves a choice of
  aggregation. Saying which axiom you are willing to lose is part of the modelling.

## 4. Voting rules and their paradoxes

| Rule | Aggregates | Fails |
|---|---|---|
| plurality | first places only | a Condorcet winner can lose |
| Borda | full ranking | irrelevant alternatives can change the outcome |
| pairwise majority | each pair | can be cyclic (Condorcet paradox) |
| PageRank on the comparison graph | weighted votes, damped | sensitive to the damping factor |

**Condorcet paradox.** Three voters, three candidates: $A\succ B\succ C$, $B\succ C\succ A$,
$C\succ A\succ B$. Pairwise, $A$ beats $B$, $B$ beats $C$, $C$ beats $A$: the majority relation has
a cycle, so no total order agrees with it. This is the same phenomenon as a non-transitive
tournament, and it is why the PageRank fix (damping, which makes the walk ergodic) is not a
technicality but a modelling assumption.

## 5. Why this page is a survey

Boosting, ranking and voting each deserve a course. Here they appear for three reasons: the
exponential-loss view of section 2 closes the loop with gradient descent; section 3 is the one place
where a matrix of pairwise data replaces a matrix of features, which is the "data as a graph" idea
of the random-graphs chapter; and section 4 warns that "combine the numbers and sort" is a modelling
decision with axioms attached. The exercises below are the intended use of the page.

## Exercises

1. Trace three rounds of AdaBoost by hand on four two-dimensional points, computing the weights, the error $\varepsilon_t$ and $\alpha_t$ at each round. Verify that the training error reaches zero.
2. Show that the exponential loss $\sum_i e^{-y_iF(x_i)}$ upper-bounds the $0$–$1$ loss, and explain why minimising the former is a sensible surrogate.
3. Treat PageRank as a voting rule on a four-node graph: compute the stationary distribution with and without damping, and describe how one high-degree node changes the ranking.
4. Verify that AdaBoost's weight update keeps $\sum_i D_{t+1}(i)=1$, and compute $Z_t$ in closed form for a two-class problem with $\varepsilon_t$ known.
5. Construct a profile of five voters and four candidates with a Condorcet cycle, then compute the Borda ranking and show that it disagrees with the pairwise majority on at least one pair.
6. Write the Borda scores as a row sum of the pairwise matrix $W$, and explain what happens to them when a candidate is removed from every ballot. Which axiom of Arrow's list does that violate?

## Sources

- Blum, Hopcroft, Kannan, *Foundations of Data Science*, selected sections.
- Freund, Y. and Schapire, R., "A decision-theoretic generalization of on-line learning and an application to boosting", *JCSS* 55(1), 1997.
- Hastie, Tibshirani, Friedman, *The Elements of Statistical Learning*, 2nd ed., Ch. 10 (boosting as stagewise additive modelling).
- Langville, A. and Meyer, C., *Google's PageRank and Beyond*, Ch. 1–2 (ranking from pairwise data).
