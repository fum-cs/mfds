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

### PDF (optional)

Uncomment `- format: pdf` in `myst.yml` and run:

```
env -u PORT jupyter book build --pdf
```

(PDF export in v2 goes through Typst. Notebooks are not executed by default —
use `jupyter book build --html --execute` to run them.)
