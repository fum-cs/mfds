"""Drop MyST's per-page notebook copies from the site artifact.

MyST writes a copy of every notebook into `_build/html/build/` so each page's
Downloads menu can offer the `.ipynb`.  The copies are byte-for-byte the files
already in the repository, so they only add weight to the artifact.

This script points those download links at the notebook in the repository
instead (GitHub serves it with the right name), then deletes the copies.  A copy
is only deleted after no page refers to it any more, so a link can never end up
404.  Notebooks that cannot be matched unambiguously to a repository file keep
their local copy.
"""

import hashlib
import os
import re
import subprocess
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "_build", "html")
BUILD = os.path.join(SITE, "build")
COPY = re.compile(r"^(?P<stem>.+)-[0-9a-f]{32}$")
TEXT_EXTENSIONS = {".html", ".json"}


def digest(path):
    hasher = hashlib.md5()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def repo_notebooks():
    """Map a copy to its repository file by content, with a name fallback."""
    listing = subprocess.run(
        ["git", "ls-files", "*.ipynb"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.split()

    by_hash = {}
    stems = []
    for path in listing:
        if path.startswith("notebooks/_build/"):
            continue
        by_hash.setdefault(digest(os.path.join(ROOT, path)), path)
        stems.append((os.path.splitext(os.path.basename(path))[0], path))
    return by_hash, stems


def repository_url():
    """Project URL taken from the git remote, e.g. https://github.com/fum-cs/mfds."""
    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()
    remote = remote.removesuffix(".git")
    if remote.startswith("git@github.com:"):
        remote = "https://github.com/" + remote.split(":", 1)[1]
    return remote


def remote_url(path, base_url):
    return f"{base_url.rstrip('/')}/raw/main/{quote(path)}"


def text_files():
    for current, _dirs, files in os.walk(SITE):
        for name in files:
            if os.path.splitext(name)[1].lower() in TEXT_EXTENSIONS:
                yield os.path.join(current, name)


def copy_files():
    """Every `<name>-<hash>.ipynb` anywhere in the site, not just in build/."""
    for current, _dirs, files in os.walk(SITE):
        for name in files:
            if name.endswith(".ipynb") and COPY.match(os.path.splitext(name)[0]):
                yield name, os.path.join(current, name)


def main():
    base_url = repository_url()

    if not os.path.isdir(SITE):
        print("no _build/html directory, nothing to prune")
        return 0

    by_hash, stems = repo_notebooks()
    copies = {
        name: (COPY.match(os.path.splitext(name)[0]).group("stem"), path)
        for name, path in sorted(copy_files())
    }

    print(f"{len(copies)} notebook copies, {len(by_hash)} distinct notebooks in the repository")

    replacements = {}
    unmatched = []
    for name, (stem, path) in copies.items():
        source = by_hash.get(digest(path))
        if source is None:
            # MyST may shorten the stem in the file name, so fall back to a
            # unique prefix match.
            matches = [candidate for candidate, repo_path in stems if candidate.startswith(stem)]
            if len(matches) == 1:
                source = dict(stems)[matches[0]]
        if source is None:
            unmatched.append(name)
            continue
        replacements[name] = remote_url(source, base_url)
    if unmatched:
        print(f"  no repository file for {len(unmatched)} copies, keeping them: {unmatched}")

    if not replacements:
        print("no downloadable replacement found, keeping every copy")
        return 0

    touched = 0
    for file_name in text_files():
        if os.path.basename(file_name).endswith(".ipynb"):
            continue
        with open(file_name, encoding="utf-8", errors="ignore") as handle:
            text = handle.read()
        new = text
        for name, url in replacements.items():
            if name not in new:
                continue
            # MyST writes the link as `build/<copy>`, `/build/<copy>`, or just
            # `/<copy>` in its asset index; every spelling becomes the URL.
            for form in (f"/build/{name}", f"build/{name}", f"/{name}"):
                new = new.replace(form, url)
            new = new.replace(name, url)
        if new != text:
            with open(file_name, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(new)
            touched += 1
    print(f"rewrote download links in {touched} files")

    # Delete a copy only when nothing references it any more.
    still_used = set()
    for file_name in text_files():
        if os.path.basename(file_name).endswith(".ipynb"):
            continue
        with open(file_name, encoding="utf-8", errors="ignore") as handle:
            text = handle.read()
        still_used.update(name for name in copies if name in text)

    freed = 0
    removed = 0
    for name, (_stem, path) in copies.items():
        if name in still_used:
            continue
        freed += os.path.getsize(path)
        os.remove(path)
        removed += 1
    print(f"removed {removed} copies ({freed / 1e6:.1f} MB); {len(still_used)} kept because a page still links to them")

    total = sum(
        os.path.getsize(os.path.join(current, name))
        for current, _dirs, files in os.walk(SITE)
        for name in files
    )
    print(f"_build/html is now {total / 1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
