# Learning Foundations: Classification and Generalization

**Not in this course:** SVM (other course), Bayesian methods and HMM (other courses). The *kernel trick* is not an SVM topic and has its own page: [The Kernel Method](Kernel-Trick.md).

## Goals

- Classification problem: train/test split
- kNN revisited as a nonparametric baseline
- Occam’s razor and why simple models can generalize
- Uniform convergence and the VC *idea* (intuition, not full theory)

## Outline

1. Empirical risk vs true risk
2. Overfitting and model complexity
3. Why more data helps (informal)
4. Bias–variance link back to the bias–variance notebook

## Exercises

1. For a fixed classifier and a known data distribution, compute the true risk and the empirical risk on samples of size $10,100,1000$. Plot both and describe the gap.
2. Show that empirical risk minimisation over *all* functions has zero empirical risk and no guarantee of generalisation. Where exactly does a restriction on the hypothesis class enter the argument?
3. Prove that the VC dimension of intervals on the line is $2$: exhibit two shattered points and show that no three can be shattered.
4. Why is $K$-fold cross-validation preferable to a single train/test split when choosing a model? Give a case in which it is still optimistic.


## Sources

- Blum, Hopcroft, Kannan, *Foundations of Data Science*, Ch. 12 (selected)
