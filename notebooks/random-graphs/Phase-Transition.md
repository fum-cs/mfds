# Giant Component and Phase Transition

## Goals

- Branching-process intuition for component sizes
- The critical threshold $p = 1/n$
- Emergence of a giant component
- Connectivity and cycles at a high level

## Outline

1. Component of a vertex as a branching process
2. Supercritical vs subcritical regimes
3. Phase transition in $G(n,p)$
4. Small World (Watts–Strogatz) as a brief survey

## Exercises

1. Model the component of a vertex as a branching process with Poisson offspring of mean $c=np$. Show that the survival probability is zero for $c\le1$ and solve $1-s=e^{-cs}$ for $c>1$.
2. Simulate $G(n,p)$ for $n=10^4$ with $p$ around $1/n$, plot the size of the largest component against $np$, and locate the transition.
3. Explain why the threshold is $p=1/n$ and not a constant: rescale $p$ by $n$ and say which quantity stays fixed.


## Sources

- Blum, Hopcroft, Kannan, *Foundations of Data Science*, Ch. 7–8
