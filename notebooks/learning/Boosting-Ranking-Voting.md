# Boosting Sketch, Ranking, and Voting

## Goals

- Weak vs strong learning (idea)
- Boosting as a sketch (AdaBoost intuition)
- Ranking: Borda count, comparison to matrix methods
- Voting: basic rules and paradoxes
- Optional footnote: PageRank as linear algebra (not a Markov-chain chapter)

## Outline

1. Combining weak classifiers
2. Boosting idea (no full proofs)
3. Aggregating preferences: ranking & voting
4. Student-talk-friendly topics from this page

## Exercises

1. Trace three rounds of AdaBoost by hand on four two-dimensional points, computing the weights, the error $\varepsilon_t$ and $\alpha_t$ at each round. Verify that the training error reaches zero.
2. Show that the exponential loss $\sum_i e^{-y_iF(x_i)}$ upper-bounds the $0$–$1$ loss, and explain why minimising the former is a sensible surrogate.
3. Treat PageRank as a voting rule on a four-node graph: compute the stationary distribution with and without damping, and describe how one high-degree node changes the ranking.


## Sources

- Blum, Hopcroft, Kannan, *Foundations of Data Science*, selected sections
