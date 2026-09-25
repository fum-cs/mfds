# Semesters

One living repo. Snapshot each offering with a git tag; do not rename the repo.

| Tag | Offering | Role | Notes |
|---|---|---|---|
| `Fall-2025` | Fall 2025 | Materials as previously taught (LA + high-dim/clustering lineage) | Frozen before the apps-first restructure. |
| *(untagged)* | Next offering | MFDS restructured (topic-ordered book) | Applications first: images → kNN/k-means → curse → SVD/PCA → random graphs → learning foundations. No SVM; Bayes/HMM/MCMC deferred to SML. |

## End-of-term checklist

1. Update this table (one row: tag, term, role, what changed).
2. Commit the term’s final edits on `main`.
3. Tag and push:
   ```
   git tag -a YYYY-term -m "Snapshot: ..."
   git push origin YYYY-term
   ```
   Use tags like `Fall-2025`, `2026-fall`.
4. Publish the book as usual (`jupyter-book build` + `ghp-import`).

## Links

- Current book (always latest): https://fum-cs.github.io/mfds/
- Frozen source for a past term: `https://github.com/fum-cs/mfds/tree/<tag>`
- GitHub Pages serves the latest `gh-pages` build only — it cannot show a past tag’s HTML at the same URL.
