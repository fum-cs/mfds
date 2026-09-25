## Computer Science Dept, Ferdowsi University of Mashhad

# Mathematical Foundations of Data Science

مبانی ریاضی علوم داده

A course in the **Data Science** track (M.Sc. Mathematics) on the shared mathematical language of **data**: how we represent, process, and analyze it. Applications come first (images, kNN, k-means); the math is introduced when it explains what you already saw.

- [Course Jupyter Book](https://fum-cs.github.io/mfds/)

**Instructor:** Mahmood Amintoosi  
**TA-Head:** Hoda MehrBagherpour

Past offerings are frozen with git tags — see [semesters.md](semesters.md). The **Fall-2025** tag is the pre-restructure snapshot.

## Course aim

Build first-pass fluency in the mathematics that underpins data science: matrices and images, distance-based classification and clustering, high-dimensional geometry and the curse of dimensionality, SVD/PCA and low-rank structure, random graphs, and basic learning foundations. By the end of the course, students should be able to use these tools on real datasets in notebooks, explain why high dimension changes behavior, and read more advanced material (e.g. Blum–Hopcroft–Kannan) with the right background.

**Not covered here** (taught in other courses): Bayesian methods and HMM (Statistical Machine Learning); SVM and kernels; MCMC / graphical models.

## Topics (outline)

1. Data, matrices, and images (Python/NumPy warm-up; image as matrix)  
2. Classification and clustering (kNN, k-means, image segmentation, silhouette, BF clustering, LVQ)  
3. High-dimensional spaces and the curse of dimensionality  
4. Linear algebra and SVD (span, special matrices, projection, eigen/SVD, pseudoinverse, trace, determinant)  
5. Low-rank approximation, PCA, and dimensionality reduction  
6. Random graphs (Erdős–Rényi, phase transition) and light random walks  
7. Learning foundations (bias–variance, generalization, perceptron, GD/SGD, boosting/ranking survey)  
8. Additional topics (random projections, compressed sensing)  

## Main references

Primary text for the mathematical foundations:

- A. Blum, J. Hopcroft, and R. Kannan, *Foundations of Data Science*.  
  [PDF](https://www.cs.cornell.edu/jeh/book.pdf)

Main reference books (also used in related FUM courses):

1. M. J. Zaki and W. Meira Jr., *Data Mining and Machine Learning: Fundamental Concepts and Algorithms*. Cambridge University Press, 2020.  
2. R. O. Duda, P. E. Hart, and D. G. Stork, *Pattern Classification*, 2nd ed. John Wiley & Sons, 2001.  
3. T. Hastie, R. Tibshirani, and J. Friedman, *The Elements of Statistical Learning*, 2nd ed. Springer, 2009.  
4. C. M. Bishop, *Pattern Recognition and Machine Learning*. Springer, 2006.  
5. K. P. Murphy, *Machine Learning: A Probabilistic Perspective*. MIT Press, 2012.  
6. S. Theodoridis, *Machine Learning: A Bayesian and Optimization Perspective*, 2nd ed. Academic Press, 2020.  
7. J. VanderPlas, *Python Data Science Handbook*. O’Reilly Media, 2016. [GitHub notebooks](https://github.com/jakevdp/PythonDataScienceHandbook)

Selected research and survey papers may be used for seminars (e.g. random graphs; ranking).

## Prerequisites

- Linear algebra  
- Basic probability and statistics  
- Elementary programming (Python is learned in parallel in this course)  

A short NumPy / data-matrix warm-up is included at the start.

## Build

From the `notebooks` folder:

```
jupyter-book build ./
ghp-import -n -p -f ./_build/html
jupyter-book build --builder pdflatex ./
```

See also [production.md](production.md).

## Semester snapshots

At the end of each offering, tag the final state (do not rename this repo):

```
git tag -a YYYY-term -m "Snapshot: ..."
git push origin YYYY-term
```

Then add a row in [semesters.md](semesters.md).
