# Production

Instructions for building the course book. Students can use the pre-compiled site and do not need this.

## Generate the online book

Install `jupyter-book`:

```
pip install jupyter-book
```

Configuration is `notebooks/_config.yml`; the table of contents is `notebooks/_toc.yml`. The cover page is `notebooks/intro.md`.

From the `notebooks` directory:

```
cd notebooks
jupyter-book build ./
```

Publish to GitHub Pages:

```
pip install ghp-import
ghp-import -n -p -f ./_build/html
```

Optional PDF:

```
jupyter-book build --builder pdflatex ./
```

If notebook execution fails during PDF builds, set `execute_notebooks: off` in `_config.yml` (already the default here).
