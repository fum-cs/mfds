#!/usr/bin/env python
"""Build the English and the Persian edition of the book, and wire the switch.

    python tools/build_sites.py            # both editions
    python tools/build_sites.py en         # English only
    python tools/build_sites.py fa         # Persian only

The English edition is built at the site root and the Persian one under /fa/,
so the Persian project is built with BASE_URL=/fa (MyST bakes that prefix into
every internal link and asset path). The Persian build is then copied into the
English output, which is what makes one static site out of two projects.

Finally the placeholder language links (<a href="#lang-en"> / "#lang-fa">) are
replaced by relative paths of the right depth for each page, and the Persian
pages get lang="fa" dir="rtl" on the <html> element — MyST's theme hardcodes
lang="en", and nothing in myst.yml can change that yet.

Requires Jupyter Book 2 on PATH, or set JB to its executable.
"""

from __future__ import annotations

import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "_build" / "html"
FA_OUT = ROOT / "fa" / "_build" / "html"

JB = os.environ.get("JB", "jupyter-book")


def build(where: pathlib.Path, base_url: str | None) -> None:
    env = {k: v for k, v in os.environ.items() if k != "PORT"}
    env.pop("BASE_URL", None)
    if base_url:
        env["BASE_URL"] = base_url
    print(f"[build] {where.relative_to(ROOT)}  BASE_URL={base_url or '(none)'}")
    subprocess.run([JB, "build", "--html"], cwd=where, env=env, check=True)


def fix_switch(pages: list[pathlib.Path], language: str) -> None:
    """Point the placeholder link at the other edition, relative to the page."""
    for page in pages:
        rel = page.relative_to(OUT)                      # e.g. fa/x/y/index.html
        depth = len(rel.parts) - 1                       # directory levels in the URL
        up = "../" * depth
        # From any page, "up" reaches the site root, where the English edition
        # lives; the Persian edition lives one level down, at /fa/.
        target = up + "fa/" if language == "en" else (up or "./")
        text = page.read_text(encoding="utf-8")
        # MyST resolves a bare fragment against the current page, so the marker
        # arrives as href="/fa/#lang-en" or href="/#lang-fa"; rewrite whatever
        # attribute holds it.
        marker = "fa" if language == "en" else "en"
        new = re.sub(rf'href="[^"]*#lang-{marker}"', f'href="{target}"', text)
        if language == "fa" and '<html lang="en"' in new:
            new = new.replace('<html lang="en"', '<html lang="fa" dir="rtl"', 1)
        if new != text:
            page.write_text(new, encoding="utf-8")


def pages_under(directory: pathlib.Path) -> list[pathlib.Path]:
    return sorted(p for p in directory.rglob("*.html") if "_assets" not in p.parts)


def main(argv: list[str]) -> int:
    which = argv[1] if len(argv) > 1 else "both"

    # On GitHub Pages the site lives under /<repository>, and the workflow sets
    # BASE_URL for that; locally it is unset and the site is served from /. The
    # Persian edition always sits one level down, at <base>/fa.
    en_base = os.environ.get("BASE_URL", "").rstrip("/")
    fa_base = f"{en_base}/fa"

    if which in {"both", "en"}:
        build(ROOT, en_base or None)
    if which in {"both", "fa"}:
        build(ROOT / "fa", fa_base)
        if FA_OUT.is_dir():
            shutil.rmtree(OUT / "fa", ignore_errors=True)
            shutil.copytree(FA_OUT, OUT / "fa")

    if which in {"both", "fa"}:
        fa_pages = [p for p in pages_under(OUT / "fa")]
        fix_switch(fa_pages, "fa")
        print(f"[switch] {len(fa_pages)} Persian pages point back to the English root")

    if which in {"both", "en"}:
        en_pages = [p for p in pages_under(OUT) if p.relative_to(OUT).parts[0] != "fa"]
        fix_switch(en_pages, "en")
        print(f"[switch] {len(en_pages)} English pages point to /fa/")

    print(f"[done] serve {OUT} and open / and /fa/")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
