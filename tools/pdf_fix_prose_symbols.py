"""Wrap Unicode math symbols used in prose with explicit math mode.

Why: myst-to-tex rewrites U+2192 to a bare \\rightarrow even when the arrow sits
in ordinary text, which is invalid LaTeX (the run then cascades into
"\\item invalid in math mode" errors) and breaks the PDF export. Writing
$\\rightarrow$ keeps HTML (MathJax) and LaTeX/PDF happy at the same time.

Only touches prose (outside $...$, $$...$$, inline code and fenced code) and only
markdown cells of notebooks, never code cells.
"""
import io
import json
import re
import sys

FENCE = chr(96) * 3
MATH_SPAN = re.compile(r'[$][$].*?[$][$]|[$][^$]*[$]')
INLINE_CODE = chr(96) + '[^' + chr(96) + ']*' + chr(96)
PROTECT = re.compile(r'(?s)(' + FENCE + r'.*?' + FENCE + r'|' + MATH_SPAN.pattern + r'|' + INLINE_CODE + r')')

REPLACEMENTS = {
    '→': '$' + chr(92) + 'rightarrow$',
    '⇒': '$' + chr(92) + 'Rightarrow$',
}

TARGETS = [
    'notebooks/other/Course-Opening.md',
    'notebooks/high-dimensional-spaces/Discrete-Optimization-and-Clustering.md',
    'notebooks/high-dimensional-spaces/High-Dimensional-Data-and-The-Curse-of-Dimensionality.ipynb',
    'notebooks/high-dimensional-spaces/Clustering-Validation-Metrics.ipynb',
    'notebooks/linear-algebra/PCA-Part2.ipynb',
]


def fix_text(text):
    out = []
    changed = 0
    for line in text.splitlines(keepends=True):
        parts = PROTECT.split(line)
        for i in range(0, len(parts), 2):        # even indices = prose
            for ch, rep in REPLACEMENTS.items():
                if ch in parts[i]:
                    changed += parts[i].count(ch)
                    parts[i] = parts[i].replace(ch, rep)
        out.append(''.join(parts))
    return ''.join(out), changed


def fix_md(path):
    raw = io.open(path, 'rb').read()
    crlf = b'\r\n' in raw
    text = raw.decode('utf-8').replace('\r\n', '\n')
    new, n = fix_text(text)
    if not n:
        return 0
    data = new.replace('\n', '\r\n') if crlf else new
    io.open(path, 'wb').write(data.encode('utf-8'))
    return n


def fix_ipynb(path):
    raw = io.open(path, 'rb').read()
    crlf = b'\r\n' in raw
    nb = json.loads(raw.decode('utf-8').replace('\r\n', '\n'))
    total = 0
    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'markdown':
            continue
        src = cell.get('source')
        if isinstance(src, list):
            joined, n = fix_text(''.join(src))
            if n:
                cell['source'] = joined.splitlines(keepends=True)
                total += n
        elif isinstance(src, str):
            new, n = fix_text(src)
            if n:
                cell['source'] = new
                total += n
    if not total:
        return 0
    out = json.dumps(nb, indent=1, ensure_ascii=False)
    if crlf:
        out = out.replace('\n', '\r\n') + '\r\n'
    else:
        out += '\n'
    io.open(path, 'wb').write(out.encode('utf-8'))
    return total


def main():
    grand = 0
    for p in TARGETS:
        n = fix_ipynb(p) if p.endswith('.ipynb') else fix_md(p)
        grand += n
        print('%-70s %d symbol(s) wrapped' % (p, n))
    print('total:', grand)
    return 0 if grand else 1


if __name__ == '__main__':
    sys.exit(main())