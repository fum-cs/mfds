# Markov Chains, Random Walks, and PageRank

A graph has so far been a *static* object: who is connected to whom. A **random walk** turns it into
a process — a token that moves from vertex to vertex — and that process has a limiting behaviour
which is, remarkably, computable. Three useful things come out of this single idea:

- the *stationary distribution* of the walk, which ranks vertices by how often the walk visits them;
- **PageRank**, which is that ranking with one modification that makes it well defined on the web;
- **Markov chain Monte Carlo**, a way to sample from a distribution we can evaluate but not
  normalise — the machinery behind the E-step of EM and behind Bayesian computation.

Only matrix–vector multiplication is needed, plus the eigenvalue idea from the
[spectral clustering page](../high-dimensional-spaces/Spectral-Clustering.ipynb): the same spectrum
answers both "how does this graph split?" and "how fast does a walk explore it?".

## 1. The walk and its transition matrix

Let $G$ be an undirected graph with adjacency matrix $A$ and degrees $\deg(v)$. From vertex $u$ we
pick one of its $\deg(u)$ neighbours uniformly and step there. The whole rule is a row-stochastic
matrix,

$$P = D^{-1}A, \qquad P_{uv} = \frac{A_{uv}}{\deg(u)}, \qquad \sum_{v} P_{uv} = 1 .$$

With $p_t$ a *row* vector holding the probability of being at each vertex after $t$ steps,

$$p_{t+1} = p_t P .$$

So a random walk is repeated multiplication by a fixed matrix — the same operation as in the
matrix product page, and the same "power iteration" that computes dominant eigenvectors in the SVD
chapter.

**Worked example: a path of three vertices.** For $1-2-3$ the degrees are $1,2,1$ and

$$P = \begin{pmatrix} 0 & 1 & 0 \\ \tfrac12 & 0 & \tfrac12 \\ 0 & 1 & 0 \end{pmatrix},
\qquad p_0 = (1,0,0).$$

Then $p_1 = (0,1,0)$, $p_2 = (\tfrac12,0,\tfrac12)$, $p_3 = (0,1,0)$, and so on forever: the walk
**never settles**. It is forced to alternate between the two sides. This is *periodicity*, and it is
why the plain walk is not yet a ranking method.

## 2. Stationary distribution

A distribution $\pi$ is stationary when $\pi P = \pi$: started in $\pi$, the law of the walk never
changes. For an undirected graph the stationary distribution is proportional to the degrees,

$$\pi_v = \frac{\deg(v)}{2m}, \qquad m = |E| ,$$

and the check is one line:

$$(\pi P)_u = \sum_v \pi_v P_{vu}
= \sum_v \frac{\deg(v)}{2m}\cdot\frac{A_{vu}}{\deg(v)}
= \frac{1}{2m}\sum_v A_{vu} = \frac{\deg(u)}{2m} = \pi_u .$$

The walk therefore **spends time at a vertex in proportion to its degree**. Existence and uniqueness
come from Perron–Frobenius: $P$ has eigenvalue $1$ with a non-negative eigenvector, and if the graph
is connected and aperiodic (for instance has one self-loop) every other eigenvalue satisfies
$|\lambda| < 1$.

## 3. How fast the walk mixes

Order the eigenvalues $1 = \lambda_1 > \lambda_2 \ge \cdots \ge \lambda_n \ge -1$. Then

$$\|p_t - \pi\|_1 \;\le\; \sqrt{n}\,|\lambda_2|^t ,$$

so the **spectral gap** $1-|\lambda_2|$ is the mixing rate: a large gap means fast exploration. Here
the page meets the spectral clustering one. For the random-walk Laplacian
$L_{rw} = I - D^{-1}A$ we have

$$\lambda_2(L_{rw}) = 1 - \lambda_2(P),$$

i.e. *the eigenvalue that decides whether a graph falls apart into clusters also decides how quickly
a walk forgets where it started.* Two questions, one spectrum.

## 4. PageRank: the walk that cannot get stuck

Ranking web pages by $\pi_v \propto \deg(v)$ fails for two reasons: a page with no out-links traps the
walk, and a bipartite or periodic structure prevents convergence. PageRank repairs both with a single
device, a **teleport** — with probability $\alpha$, jump to a uniformly random page:

$$\tilde P = (1-\alpha)P + \frac{\alpha}{n}\mathbf{1}\mathbf{1}^{\top}.$$

The stationary distribution of the damped chain solves

$$\pi = \pi\tilde P
\iff
\big(I - (1-\alpha)P\big)\,\pi = \frac{\alpha}{n}\mathbf{1},$$

a linear system, equivalently an eigenproblem for $\tilde P$ with eigenvalue $1$. The chain is now
aperiodic and irreducible, $\pi$ exists and is unique, and power iteration converges at rate
$(1-\alpha)|\lambda_2|$.

**Worked example.** For the three-vertex path with $\alpha = 0.15$, the equations
$\pi_j = \frac{\alpha}{n} + (1-\alpha)\sum_i \pi_i P_{ij}$ give

$$\pi \approx (0.257,\; 0.486,\; 0.257),$$

against $(0.25, 0.50, 0.25)$ for the undamped walk. The ordering is unchanged; teleport pulls every
value a little toward $1/n$. Page and Brin used $\alpha \approx 0.15$. Concentrating the teleport on a
seed set instead of the uniform distribution gives *personalised* PageRank, which is how
neighbourhood-based recommenders and citation impact measures use the same iteration.

## 5. MCMC: sampling from what you can only evaluate

Suppose we want to sample from $\pi(x) \propto f(x)$ where $f$ is known but its normalising constant
is not — a Bayesian posterior, a Boltzmann distribution, the conditional law inside an E-step.
Direct sampling is out of reach, but a Markov chain *whose stationary distribution is $\pi$* is
enough: run it long and keep the states.

**Metropolis–Hastings.** At state $x$ propose $x' \sim q(\cdot\mid x)$ and accept with probability

$$\alpha(x \to x') = \min\left(1,\;
\frac{f(x')\,q(x\mid x')}{f(x)\,q(x'\mid x)}\right),$$

otherwise stay where you are. Only the ratio of $f$ appears, never its normalising constant — that
is the entire trick. The chain satisfies *detailed balance*,

$$\pi(x)\,q(x'\mid x)\,\alpha(x\to x') = \pi(x')\,q(x\mid x')\,\alpha(x'\to x),$$

which implies $\pi$ is stationary. **Gibbs sampling** is the special case "resample one coordinate
from its full conditional", for which the acceptance probability is exactly $1$; it is the standard
tool for latent-variable models.

Three practical facts worth stating once: discard a *burn-in*; consecutive samples are correlated, so
the effective sample size is smaller than the iteration count; and a chain can look healthy in a trace
plot while mixing badly — hence several chains and a comparison of their answers.

## 6. Where this leads

- **Hidden Markov models** are a Markov chain on *hidden states* plus an emission model. The forward
  recursion is the walk of §1 with a reweighting by the likelihood at every step, which is why its
  cost is $O(n^2T)$ rather than the $O(n^T)$ of enumerating state sequences.
- **Spectral clustering** uses the same spectrum as §3 for a different question (where to cut).
- **EM** needs expectations that Gibbs and Metropolis–Hastings can supply when the E-step cannot be
  computed in closed form.

## Exercises

1. For the three-vertex path compute $P^2$ and $P^3$, and explain the alternation using the
   eigenvalues of $P$ (they are $1, 0, -1$).
2. Show that a bipartite graph gives $\lambda = -1$ for $P$ and hence period $2$, and that adding a
   single self-loop removes the period without changing the stationary distribution.
3. Implement PageRank by power iteration on a random $10\times10$ directed graph. Plot
   $\|\pi_{t+1}-\pi_t\|_1$ and check that it falls by a factor $\approx(1-\alpha)|\lambda_2|$ per
   iteration.
4. Write Metropolis–Hastings for $\pi(x)\propto e^{-x^2/2}\left(1+\sin^2 3x\right)$ on the line,
   and compare the normalised histogram with the exact density.

## Sources

- T. Hastie, R. Tibshirani, J. Friedman, *The Elements of Statistical Learning*, 2nd ed.,
  §14.10 (PageRank) and §8.6 (MCMC).
- M. J. Zaki, W. Meira Jr., *Data Mining and Machine Learning*, ch. 5 (Markov chains and random
  walks on graphs).
- A. Blum, J. Hopcroft, R. Kannan, *Foundations of Data Science*, ch. 5–6 (random walks, Markov
  chains, mixing).
