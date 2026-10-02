# Production

Instructions for building the course book. Students can use the pre-compiled site and do not need this.

## Generate the online book

The book is built with **Jupyter Book 2** (MyST engine).

The old Jupyter Book v1 setup (`notebooks/_config.yml` + `notebooks/_toc.yml`) is archived
in `_v1_backup/`, and the last v1 state is tagged `jupyter-book-v1` on GitHub
(use `git checkout jupyter-book-v1` to go back to it).

Install v2:

```
pip install jupyter-book        # v2.x — wraps the MyST engine
# or: npm install -g mystmd
```

On this workstation, `jupyter-book` 2.1.7 lives in the `pytorch` env:
`/data/python-envs/pytorch/bin/jupyter-book`.

All configuration now lives in a single `myst.yml` at the repository root:
metadata (title, author, copyright, logo, favicon), the bibliography,
exports, and the table of contents. The cover page is still `notebooks/intro.md`.

Build the static site from the repository root (not from `notebooks/`):

```
jupyter book build --html
```

Gotcha: if your shell exports `PORT` (this one has `PORT=0`), unset it for the
build — MyST reads `PORT` and the static export then tries to fetch pages from
`http://localhost:0` and fails:

```
env -u PORT jupyter book build --html
```

The site is written to `_build/html/`.

### Deploying to GitHub Pages (automatic)

Pushes to `main` are built and deployed by GitHub Actions — see
`.github/workflows/deploy.yml` (it installs `jupyter-book` via npm, runs
`jupyter-book build --html` with `BASE_URL=/mfds`, and publishes to Pages).
Nothing to do by hand; watch progress under the repo's **Actions** tab. The
Pages *Source* setting must stay **GitHub Actions**.

### Serving the book locally

Option A — live-reload dev server (rebuilds content as you edit):

```
env -u PORT jupyter book start     # http://localhost:3000
```

Option B — serve the already-built static site on any port:

```
cd _build/html
python3 -m http.server 8811 --bind 127.0.0.1
```

(The site is a JS-driven static site: always open it through a web server,
not by double-clicking `index.html`.)

### Stopping local servers

If a server runs in a terminal, stop it with `Ctrl-C` there. Background
servers can be found and killed by port:

```
ss -tlnp | grep -E ':(3000|3001|8811)'   # find listeners + PIDs
kill <PID>                               # graceful
kill -9 <PID>                            # if it ignores SIGTERM
```

One-liners:

```
fuser -k 3000/tcp              # free port 3000
kill $(lsof -t -i:8811)        # free port 8811 (needs lsof)
```

`jupyter book start` spawns a Node "book-theme" server; if one is left over:

```
pkill -f "book-theme/server.js"
pkill -f "myst"
```

### Pushing the rendered book to GitHub Pages (manual fallback)

For a project site (https://fum-cs.github.io/mfds/), rebuild with the correct
base URL first, then push `_build/html`:

```
BASE_URL=/mfds/ env -u PORT jupyter book build --html
pip install ghp-import
ghp-import -n -p -f ./_build/html
```

## LaTeX and PDF output

The book can also be rendered as LaTeX source and as a PDF. Both come out of the
**same pipeline**, so they are two stopping points rather than two pipelines:

```
notebooks/*.md, *.ipynb  ->  LaTeX (.tex)  ->  TeX engine (xelatex)  ->  PDF
                              ^-- build --tex      ^-- build --pdf
```

`build --tex` stops at the generated `.tex` (a deliverable you can edit, compile or
hand to a journal); `build --pdf` additionally compiles it. Notebook **code and
stored outputs are included** in both (the PDF is ~14 MB / ~390 pages), and
interactive HTML/widget output never makes it into a PDF.

### Prerequisites

```bash
pandoc --version          # any modern pandoc
xelatex --version         # a full TeX Live installation (the template uses xelatex)
```

On this workstation: pandoc 3.10 and TeX Live 2024.

### Configuring the exports

Both formats are configured in `project.exports` in `myst.yml`, using the
`plain_latex_book` template:

```yaml
  exports:
    - format: pdf
      template: plain_latex_book
      output: _build/exports/mfds-book.pdf
      articles: &book_articles      # the list is shared with the tex export
        - file: notebooks/intro.md
          title: "Mathematical Foundations of Data Science"
          level: 0                   # 0 -> \chapter, 1 -> \section
        ...
    - format: tex
      template: plain_latex_book
      output: _build/exports/mfds-book-tex.zip
      articles: *book_articles
```

Three things matter here:

* **`level` per article.** By default MyST renders every page at `\section`,
  which is wrong for the `book` class. `0` makes a chapter (`\chapter`), `1` a
  section. The list above mirrors `project.toc`: the first page of each group is
  a chapter, the rest are sections.
* **`title` per article.** Without it, pages whose first heading is not an `H1`
  silently lose their heading and the chapter disappears from the book.
* The YAML anchor (`&book_articles` / `*book_articles`) avoids repeating 61
  entries twice.

### Building

```bash
env -u PORT jupyter-book build --tex    # -> _build/exports/mfds-book-tex.zip
env -u PORT jupyter-book build --pdf    # -> _build/exports/mfds-book.pdf  (~2 min)
env -u PORT jupyter-book build -a       # every configured export
```

`PORT` must be unset here too (see the gotcha above).

### LaTeX gotchas in this repository

These are real failure modes found while producing the PDF; all of them are
silent in HTML and only bite in the LaTeX/PDF export:

1. **Unicode arrows in prose.** myst-to-tex rewrites `→` to a bare `\rightarrow`
   *outside* math mode, and LaTeX then cascades into
   `Command \item invalid in math mode`. Write `$\rightarrow$` instead.
2. **`%` at the end of inline math.** In `$1 - (0.99)^2 \simeq 2%$` the `%`
   comments out the closing `$`, the math never closes, and **xelatex exits 1
   while printing no error at all**. Escape it: `2\%$`.
3. **Unicode glyphs the font lacks are dropped silently** (LaTeX only warns
   "Missing character"): Persian letters, `₁₂₃` subscripts, `ő` in
   Erdős–Rényi, box-drawing characters in stored outputs. Keep the prose ASCII
   or use math mode; check the count with `grep -c 'Missing character'` in the
   build log.
4. **BibTeX and non-ASCII fields.** Persian author names in `references.bib`
   make BibTeX fail with `name has a comma at the end`; wrap such fields in an
   extra brace group. Note that BibTeX ignores `%` comments *inside* an entry.
5. HTML is unaffected by all of the above, but fixing it in the source fixes
   both outputs.

### Helper scripts

`tools/` holds the diagnostics used for this work:

| script | purpose |
| --- | --- |
| `pdf_scan_unicode.py` | lists Unicode math symbols in prose (breaks the PDF) |
| `pdf_fix_prose_symbols.py` | wraps them in math mode |
| `translate_persian_to_english.py` | the Persian -> English pass (already applied) |
| `fix_trailing_spaces.py` | cleans list items left with trailing spaces |
| `pdf_bisect_latex.py`, `pdf_bisect_binary.py` | find the chapter that makes xelatex fail |

### Not covered by CI

`.github/workflows/deploy.yml` builds **HTML only**. The PDF is produced locally;
adding it to CI would need a job that installs TeX Live and uploads
`_build/exports/`.
