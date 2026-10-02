# mfds — Jupyter Book v2 cleanup (todo for next session)

## 1. Context
- Target repo: `C:\git\fum-cs\mfds` (Git Bash: `/c/git/fum-cs/mfds`) — *Mathematical Foundations of Data Science*, M.Sc. Data Science track, Ferdowsi University of Mashhad (instructor: Mahmood Amintoosi).
- This repo and `C:\git\fum-cs\machine-learning` were migrated Jupyter Book v1 → v2 (MyST) on a different Linux machine; exact Python/library versions may differ there. Final site output is produced by `.github/workflows/deploy.yml` (GitHub Pages via GitHub Actions; node 24.x, `npm install -g jupyter-book`, `jupyter-book build --html`). The workflow file itself is already correct — identical to machine-learning's; no changes needed there.
- Reference repo where the same cleanup is DONE: `C:\git\fum-cs\machine-learning` (`/c/git/fum-cs/machine-learning`). Match its conventions: Title-Case hyphenated filenames, `Part1`/`Part2` suffixes, `Appendix-` prefix, semicolon-separated `{cite}` keys, zero broken references.
- Working tree currently clean at `10c4b19` ("Migrate to Jupyter Book 2 (MyST): replace _config/_toc with myst.yml").

## 2. Environment (this Windows machine)
- Shell: Git Bash. The terminal resets its working directory between commands — always `cd /c/git/fum-cs/mfds` at the start of every command. (In this environment, do not pass a `cwd` option to the terminal tool — it fails to spawn bash; commands without it run from the machine-learning repo root.)
- Python: `/c/Programs/Anaconda3/python` (Python 3.12.4). There is no `python3` alias.
- Reference Jupyter Book toolchain: `/tmp/jb2/node_modules/.bin/jupyter-book` → **jupyter-book v2.1.7** (myst 1.11.0), **Node v24.13.0**, npm 11.6.2. `/tmp` may be wiped between sessions; CI installs the latest via npm instead.
- Local build: `cd /c/git/fum-cs/mfds && /tmp/jb2/node_modules/.bin/jupyter-book build --html`
- Success criteria: rendered pages in `_build/site/content/*.json` == number of `file:` entries in `myst.yml` `toc` (**67**), with no errors/warnings.

## 3. MyST v2 / myst.yml gotchas (learned in machine-learning — apply here)
- `toc`, `exports`, `bibliography` must be nested under `project:` — top-level keys are silently ignored. (mfds already nests them correctly.)
- `exports:` does NOT accept `format: html` (allowed: pdf, tex, pdf+tex, typst, docx, xml, md, meca, cff). HTML is built by `jupyter-book build --html` via the `site:` block. → **mfds `myst.yml` currently contains the invalid `exports: - format: html`; remove it.**
- MyST v2 citation syntax: multiple keys in one `{cite}` role are separated by a **semicolon `;`**, not commas.

## 4. Tasks
1. **Numeric prefixes — already done.** All files lack numeric prefixes (verified; nothing to do).
2. **Fix myst.yml**: remove the invalid `exports: - format: html` entry.
3. **Fix citations** (only 2 source files use `{cite}`):
   - `notebooks/linear-algebra/PCA part 2.ipynb`: `{cite}`JMIV-2022,Fathy08outlier,Amintoosi07icics,Amintoosi94QR`` → replace commas with `;`.
   - `notebooks/high-dimensional-spaces/Clustering-Validation-Metrics.ipynb`: `{cite}`zaki2020data``.
   - **All five keys are missing from `notebooks/references.bib`** (which currently holds only 5 leftover template entries: `holdgraf_evidence_2014`, `holdgraf_rapid_2016`, `holdgraf_portable_2017`, `holdgraf_encoding_2017`, `ruby` — look like Jupyter Book example leftovers; remove unless wanted).
   - Copy the 5 entries from `/c/git/fum-cs/machine-learning/notebooks/references.bib`: `JMIV-2022` (line 407), `Fathy08outlier` (1171), `Amintoosi07icics` (1183), `zaki2020data` (1433), `Amintoosi94QR` (1450). Their `preview` fields point to images that are not tracked in git — drop the field or ignore it; mfds does not use bib previews.
4. **Unify naming** to Title-Case + hyphens, `Part1`/`Part2` suffixes (no spaces/underscores/commas). Update `myst.yml` toc (67 entries) and any in-notebook links. Renames within a folder keep relative image paths intact.
   - 13 linear-algebra files currently quoted in myst.yml because of spaces/commas, e.g.:
     - `Scalars, Vectors, Matrices, and Tensors.ipynb` → `Scalars-Vectors-Matrices-and-Tensors.ipynb`
     - `Multiplying Matrices and Vectors.ipynb` → `Multiplying-Matrices-and-Vectors.ipynb`
     - `Identity and Inverse Matrices.ipynb` → `Identity-and-Inverse-Matrices.ipynb`
     - `Linear Dependence and Span.ipynb` → `Linear-Dependence-and-Span.ipynb`
     - `Special Kinds of Matrices and Vectors.ipynb` → `Special-Kinds-of-Matrices-and-Vectors.ipynb`
     - `Singular Value Decomposition.ipynb` → `Singular-Value-Decomposition.ipynb`
     - `The Moore-Penrose Pseudoinverse.ipynb` → `The-Moore-Penrose-Pseudoinverse.ipynb`
     - `The Trace Operator.ipynb` → `The-Trace-Operator.ipynb`
     - `The Determinant.ipynb` → `The-Determinant.ipynb`
     - `Low-Rank Matrix Approximation.ipynb` → `Low-Rank-Matrix-Approximation.ipynb`
     - `Example - Principal Components Analysis.ipynb` → `Example-Principal-Components-Analysis.ipynb`
     - `PCA part 1.ipynb` / `PCA part 2.ipynb` → `PCA-Part1.ipynb` / `PCA-Part2.ipynb`
   - Underscore/lowercase/mixed-case files: `image_01_intro.ipynb`, `image_02_seg_k-means.ipynb`, `image_03_seg_coords.ipynb`, `image_clustering.ipynb`, `image-clustering_HC.ipynb`, `high_dim_and_KNN.ipynb`, `high_dim_and_k-means.ipynb`, `lecture2_2_gradient-descent.ipynb`, `lecture2_3_stochastic-gradient-descent.ipynb`, `plot_pca_vs_lda.ipynb`, `SVD_image_compression.ipynb`, `Dimensionality-reduction_01.ipynb`, `Dimensionality-reduction_02.ipynb` (→ `...-Part1`/`...-Part2`), `SAT_Table.ipynb`, `BF-clustering.ipynb`, `LVQ.ipynb`, `NQueen.ipynb`, `App-PCA.ipynb`, `k-means-clustering.ipynb`, `kmeans-clustering-iris.ipynb`, `high-dim-intro.md`, `intro.md`, `misc.md`.
5. **Folder structure — keep as-is (decision).** Keep the topical multi-folder layout (`high-dimensional-spaces/`, `learning/`, `linear-algebra/`, `other/`, `python/`, `random-graphs/`). Rationale: ~100 files would be unwieldy in one flat folder; the grouping is pedagogical; JB v2's TOC handles subdirectory paths fine; per-topic `images/`/`img/` folders keep relative image paths intact. (machine-learning's single flat folder is a historical artifact, not a requirement.)
6. **Reference audit** (machine-learning had 17 broken refs to fix; mfds needs the same sweep):
   - Verify every local image/attachment path in `.md`/`.ipynb` resolves (check `images/`, `img/`, `*.jpg`/`*.png` links).
   - Non-standard assets to check: `high-dimensional-spaces/SAT-Solver.cpp`, `linear-algebra/Notes.txt`, `notebooks/requirements.txt`, `notebooks/learning/utils/` (imported by the learning notebooks — must stay importable when notebooks execute during build).
   - **Unreferenced tracked files** (delete or wire in): `misc/Course-Syllabus.pdf` (not referenced anywhere), `temp/` (5 files), `_v1_backup/` (git history already preserves v1), `linear-algebra/Notes.txt`, `notebooks/test_svd.jpg`, `notebooks/H-Mehr.jpg`, `notebooks/M-Amintoosi.jpg` (commented out in `intro.md`).
   - Root pages `README.md`, `ROADMAP.md`, `semesters.md`, `production.md` are **not** in the TOC — decide whether to add them or leave as repo-only docs.
7. **Verify build locally** (command in §2): all 67 pages render, no "file not found" or "no bibtex key" warnings, notebooks execute.
8. **Commit** in logical chunks with short imperative subjects (repo style, e.g. "Rename notebooks to drop numeric prefixes and unify naming"). Do **not** push unless asked; CI (deploy.yml) deploys on push to `main`.

## 5. Notes
- `notebooks/_build/`, `_build/`, `__pycache__/`, `.freebuff/` are gitignored — never commit build output.
- TOC currently has 67 `file:` entries and every tracked `.md`/`.ipynb` under `notebooks/` is listed — no dangling TOC entries.
