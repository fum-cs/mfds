# Perceptron and Online Learning

## Goals

- Linear separators
- The perceptron update rule
- Perceptron convergence theorem (idea)
- Online learning mistake bound (sketch)
- Connection to gradient descent / SGD (see the notebooks in this folder)

## Outline

1. Linear score functions
2. Perceptron algorithm
3. Why it converges on separable data
4. From batch to online updates
5. Demo: 2D perceptron vs kNN

## Exercises

1. Run the perceptron on linearly separable two-dimensional data and count the updates. Compare with the bound $(R/\gamma)^2$, computing the margin $\gamma$ and the radius $R$ of your data.
2. Show that a single perceptron cannot represent XOR and give the smallest change of architecture that can.
3. Derive the perceptron update rule as stochastic gradient descent on the hinge loss $\max(0,-y\,w^\top x)$, and explain what online means for the optimisation.


## Sources

- Blum, Hopcroft, Kannan, *Foundations of Data Science*, Ch. 12–13 (selected)
