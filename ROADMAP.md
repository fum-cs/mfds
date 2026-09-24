# MFDS Roadmap — Mathematical Foundations of Data Science

**Course:** مبانی ریاضی علوم داده / Mathematical Foundations of Data Science  
**Repo:** `C:\git\fum-cs\mfds`  
**Main text:** A. Blum, J. Hopcroft, R. Kannan, *Foundations of Data Science*  
  [https://www.cs.cornell.edu/jeh/book.pdf](https://www.cs.cornell.edu/jeh/book.pdf)  
**Status:** This file is the work plan. Execute it in a **new chat** (or continue here). Do not mix with the Machine Learning course work.

---

## 0. Course identity (draft for README / index later)

**Position in the curriculum**  
A broad foundations course spanning mathematics, probability/statistics, and theoretical computer science as they relate to **data**: how we represent it, process it, and analyze it. Many syllabus items are full topics in their own right (SVD/PCA, random graphs, Markov chains, learning theory, clustering, probabilistic graphical models). This course gives the **shared mathematical language** and core results at an introductory graduate level.

**Goal**  
Build first-pass fluency in high-dimensional geometry, spectral methods, random graphs, random walks / MCMC, basic learning theory, clustering principles, and latent-variable / message-passing models—enough to read data-science papers and to use these ideas in later courses and research.

**Audience**  
Mixed backgrounds (math, CS, engineering). Assume linear algebra + probability basics; include short refreshers where cheap.

**Primary source**  
Blum–Hopcroft–Kannan (BHK) throughout. Secondary: original papers or standard notes only when BHK is thin (e.g. MH/Gibbs details, SVM, boosting).

---

## 1. Official syllabus (from curriculum)

**هدف:** آشنایی اولیه با گستره وسیعی از مباحث ریاضیات، آمار و علوم کامپیوتر نظری که در درک بنیادین داده‌ها و نمایش/پردازش/تحلیل آن‌ها مؤثرند.

**سرفصل‌ها (topics):**

1. **فضاهای با-بعد بالا / High-dimensional spaces**  
   concentration of measure · law of large numbers · high-dimensional geometry · random point in the unit ball · Gaussian in high dimensions · random projections · Johnson–Lindenstrauss («قضیه مسطح‌سازی»)
2. **تجزیه مقادیر تکین / SVD**  
   best low-rank approximation · singular vs eigen vectors · power method · applications: PCA, clustering, Gaussian mixtures, ranking, optimization, overcomplete (low-rank / sparse) matrices
3. **گراف‌های تصادفی / Random graphs**  
   Erdős–Rényi · giant component & phase transition · branching processes · cycles and connectivity · non-homogeneous growth · Small World
4. **قدم زدن تصادفی و زنجیرهای مارکفی / Random walks & Markov chains**  
   stationary distributions · MCMC · Metropolis–Hastings · Gibbs sampling · walks on undirected graphs · walks in Euclidean space · web as a Markov chain
5. **یادگیری ماشین (مبانی نظری) / Learning theory**  
   classification · Occam’s razor & uniform convergence · perceptron · random/stochastic gradient · online learning · SVM · nonlinear separators & kernels · weak/strong learning · boosting · VC dimension
6. **خوشه‌بندی / Clustering**  
   k-means · spectral clustering · recursive bipartitioning · dense submatrices · stream-based methods · local clustering · principles of clustering
7. **مدل‌های مارکفی نهان و مدل‌های گرافی و انتشار باور / HMM & graphical models & BP**  
   HMM · graphical models · belief propagation · Bayesian / Markov fields · junction tree algorithm
8. **موضوعات دیگر / Other**  
   ranking · voting · low-rank matrices & compressed sensing

---

## 2. Proposed teaching order (easy → hard, prerequisites first)

Design principle: **geometry of data first** (why high-d is different), **linear algebra of data** (SVD/PCA), then **randomness** (graphs, walks), then **learning**, then **structure discovery** (clustering, HMM/PGM), then **survey of “other”**.

> Suggested **14 weeks × 2 sessions = 28 sessions**. Tune session counts after you choose how deep to go (this course is survey-like in places).

| # | Block / title | Sessions (sugg.) | Prerequisites | BHK / source | Existing in mfds? |
|---|---|---|---|---|---|
| 1 | Intro: what is “foundations of data science”; course map | 1 | — | Ch. 1 / book preface | **New** short md |
| 2 | Linear algebra refresh (vectors, matrices, norms, projections) | 1–2 | — | BHK App. + `mfds` LA notebooks | **Yes** `notebooks/linear-algebra/*` |
| 3 | Probability & concentration primer | 1–2 | #2 | BHK Ch. 2–3 | **New** (or light md) |
| 4 | High-dimensional spaces I: geometry & concentration | 2 | #2–3 | BHK Ch. 2–3 | **Partial** `high_dim_and_CD`, `high-dim-intro.md` |
| 5 | High-dimensional spaces II: Gaussians, random point in ball, random projections & JL | 2 | #4 | BHK Ch. 3–4 | **Partial** `Random-Projection` is in **a4ds**, not mfds |
| 6 | SVD I: definition, eigenvectors of $A^T A$, power method | 2 | #2 | BHK Ch. 4–5 | **Yes** `linear-algebra/2.8 Singular Value Decomposition`, `2.7 Eigendecomposition` |
| 7 | SVD II: low-rank approximation, PCA | 2 | #6 | BHK Ch. 5–6 | **Yes** `2.12 Example - PCA`, `App-PCA`, `Dimensionality-reduction_01/02`, `plot_pca_vs_lda` |
| 8 | SVD applications: mixtures, ranking, optimization (survey) | 1 | #7 | BHK Ch. 5–6 | **New** short md or expand App-PCA |
| 9 | Random graphs I: Erdős–Rényi, giant component, phase transition | 2 | #3 | BHK Ch. 7 | **New** |
| 10 | Random graphs II: connectivity, cycles, Small World | 1–2 | #9 | BHK Ch. 7–8 | **New** |
| 11 | Markov chains I: definitions, stationary distribution, random walks | 2 | #3 | BHK Ch. 6 / 9–10 | **New** |
| 12 | Markov chains II: MCMC, Metropolis–Hastings, Gibbs | 2 | #11 | BHK Ch. 10–11 | **New** |
| 13 | Learning theory I: classification, uniform convergence, Occam | 2 | #3–4 | BHK Ch. 12 | **New** |
| 14 | Learning theory II: perceptron, SGD/online, margins & SVM/kernels | 2 | #13 | BHK Ch. 12–13 | **New** (SVM is required *here* even if another course covers it in ML) |
| 15 | Learning theory III: boosting & VC dimension | 1–2 | #14 | BHK Ch. 12–13 | **New** |
| 16 | Clustering I: k-means & principles of clustering | 1–2 | #2–3 | BHK Ch. 1 | **Yes** `k-means-clustering`, `Silhouette-clustering`, `BF-clustering` |
| 17 | Clustering II: spectral, recursive bipartitioning, streams, local | 2 | #6–7, #16 | BHK Ch. 1–2 | **Partial** `LVQ`, image clustering; spectral = **New** |
| 18 | HMM & graphical models I: HMM, BP on trees | 2 | #11 | BHK Ch. 15–16 | **New** |
| 19 | PGM II: Markov fields, junction tree (survey) | 1 | #18 | BHK Ch. 16 | **New** |
| 20 | Other: ranking, voting, compressed sensing (survey) | 1–2 | #6–7 | BHK Ch. 4–5 / 14 | **New** |
| 21 | Project / review / buffer | 2 | all | — | **New** `Project.md` |

**Exclude if you must cut time:** SVM depth (point to ML colleague’s course—but this syllabus lists it), streaming clustering, junction tree details, compressed sensing proofs. Prefer cutting proofs over cutting whole blocks.

**Reuse from sibling courses (copy into `notebooks/`, prefer **newer** when names collide):**

| Need | Candidate sources |
|---|---|
| Random projection / JL | `a4ds/high-dimensional-spaces/Random-Projection.ipynb` |
| Curse of dimensionality (richer) | `a4ds/.../High-Dimensional-Data-and-The-Curse-of-Dimensionality.ipynb` (used in MFDS lineage; verify date) |
| kNN evaluation / bias–variance | already in mfds/a4ds |
| PCA depth | `SML` `13/14-PCA*`, `a4ds` `05.09-PCA*` |
| HMM | `SML` `15-Hidden-Markov-Models`, `machine-learning` `08 - Hidden Markov Models` |
| Kernel / SVM (if not writing fresh) | `machine-learning` SVM appendix (optional) |
| Spectral clustering / BP | likely **must write** or pull lecture notes; check `learning-theory` |

---

## 3. Inventory (mfds as of this note)

**Already in `C:\git\fum-cs\mfds\notebooks`:**

- `intro.md`, `high-dimensional-spaces/*`  
  including: `high-dim-intro.md`, `high_dim_and_CD`, `high_dim_and_KNN`, `high_dim_and_k-means`, `k-means-clustering`, `kmeans-clustering-iris`, `Silhouette-clustering`, `BF-clustering`, `Bias-Variance-Tradeoff`, `Dimensionality-reduction_01/02`, `plot_pca_vs_lda`, `App-PCA`, `LVQ`, image clustering notebooks, `misc.md`, SAT/NQueen (unrelated? decide keep/drop)
- `linear-algebra/*`  
  Goodfellow-style: 2.1–2.12 (tensors → PCA example), SVD, eigendecomposition, Moore-Penrose, projection, low-rank approx
- Root: `README.md` (short), no `semesters.md`, no course-plan file yet
- `_toc.yml` exists (high-dim + LA parts)

**Missing for full syllabus (priority):**

| Priority | Topic | Kind |
|---|---|---|
| P0 | Random graphs (ER, giant component, Small World) | New notebooks or BHK-based notes |
| P0 | Markov chains & MCMC (MH, Gibbs) | New |
| P0 | Learning theory (uniform convergence, VC, boosting) | New |
| P0 | Perceptron / online / SVM+kernels (BHK track) | New or adapted |
| P1 | Spectral clustering | New |
| P1 | HMM + BP | Copy/adapt from SML/ML |
| P1 | JL lemma / random projections | Copy from a4ds |
| P2 | Compressed sensing, ranking, voting | Survey md |
| P2 | Streams / local clustering | Survey md |

---

## 4. Work checklist (do in order in the next chat)

### Phase A — Planning freeze
- [ ] Confirm session count (28 vs fewer) and which topics are “survey only”
- [ ] Confirm notation note (same issue as ML: unify later; BHK-style for math)
- [ ] Decide: keep SAT/NQueen/LVQ/image-clustering in main TOC or move to Appendix

### Phase B — Repo hygiene (like ML course)
- [ ] Tag current state if you want a freeze: `git tag -a YYYY-term -m "..."` (see `machine-learning/semesters.md` pattern)
- [ ] Add `semesters.md` (tag history + end-of-term checklist)
- [ ] Add `ROADMAP.md` updates as phases complete (this file)

### Phase C — Content assembly (copy + rename + assets)
- [ ] Copy newer notebooks from `a4ds` / `SML` / `machine-learning` where §2 says “Partial”
- [ ] Copy `img/` assets with each notebook (same rule as ML: merge into `notebooks/img/`, do not clobber)
- [ ] Create numbered sequence `01 … NN` matching the block order in §2
- [ ] Placeholders for P0 gaps (md stubs: `Random-Graphs.md`, `Markov-Chains-MCMC.md`, `Learning-Theory.md`, …) so TOC is complete
- [ ] Rewrite `notebooks/_toc.yml` to the new order (main + appendix)
- [ ] Verify every `_toc.yml` entry exists on disk

### Phase D — Course pages (like ML course)
- [ ] Rewrite root `README.md`: aim, syllabus outline, BHK as main text, build from `notebooks/`, semester tags
- [ ] Rewrite `notebooks/index.md`: position in curriculum, goals, prerequisites, student work, AI policy (reuse ML wording), assessment, teaching method, textbooks + related papers
- [ ] Update `notebooks/_config.yml`: title `Mathematical Foundations of Data Science`, author, copyright 2026, sane `execute.exclude_patterns`
- [ ] Fix `production.md` if present (build from `notebooks/`)
- [ ] `requirements.txt` as needed (numpy/scipy/matplotlib/networkx for random graphs; sklearn optional)

### Phase E — Fill P0 content (largest chunk)
- [ ] Random graphs (2 sessions)
- [ ] Markov chains + MCMC (2–3 sessions)
- [ ] Learning theory + SVM/kernels + boosting/VC (3–4 sessions)
- [ ] Spectral clustering (1 session)
- [ ] HMM + BP (2 sessions) — prefer copy/adapt
- [ ] Surveys: ranking, voting, compressed sensing (1–2 sessions)

### Phase F — Polish (defer until structure is stable)
- [ ] Notation alignment with BHK
- [ ] Image path fixes inside notebooks
- [ ] Optional PDF build (`jupyter-book build --builder pdflatex`)

### Phase G — Publish
- [ ] Commit + push
- [ ] `jupyter-book build` + `ghp-import` when ready for Pages
- [ ] Tag end-of-term when the offering ends

---

## 5. How this was done for Machine Learning (pattern to repeat)

1. **Syllabus first** → 14-week table with EN/FA titles and session counts  
2. **Reuse-first** → copy notebooks from sibling repos; newer date wins on name collisions  
3. **Numbered files + `_toc.yml`** aligned to teaching order; extras go to Appendix  
4. **Images with notebooks** → merge into `notebooks/img/`  
5. **Placeholders** for student seminars / missing topics  
6. **README + index + `_config.yml`** revised to the course plan (aim, outcomes, refs, policy)  
7. **`semesters.md` + git tags** for multi-year maintenance  
8. Content deep-edit only after structure is approved  

---

## 6. Open choices (decide before Phase C)

1. **Session count** for this course (28 like ML, or denser survey in fewer weeks)?  
2. **How much proof** (BHK is proof-heavy; first-semester mixed cohort may want intuition + one key proof per block)?  
3. **SVM:** full treatment here (syllabus lists it) vs pointer to the other course (user previously put SVM elsewhere for ML only).  
4. **Main language of notebooks:** English (current material) — keep?  
5. **Assessment:** project / problem sets / seminars? (ML used ranking + VC seminars—same idea for voting/ranking here?)

---

## 7. First actions for the new chat

1. Read this file and `C:\git\fum-cs\mfds\README.md`.  
2. Confirm §6 open choices with the user (or accept defaults: 28 sessions, intuition-first, SVM as in syllabus at moderate depth, English notebooks).  
3. Execute **Phase B → C → D** (structure + pages) before writing large new notebooks.  
4. Use the Machine Learning repo as the **process reference** (not content): `C:\git\fum-cs\machine-learning\semesters.md`, `_toc.yml`, `README.md`, `notebooks/index.md`.

— End of roadmap —
