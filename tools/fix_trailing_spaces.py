"""Strip trailing spaces left on list items after removing Persian glosses.

The kNN page had entries like `- **Medical Diagnostics** (تشخیص پزشکی)`; dropping
the parenthetical left two trailing spaces, which markdown reads as a hard line
break inside the list item.
"""
import io
import json
import re
import sys

PATTERN = re.compile(r'^(\s*[-*]\s+\*\*[^*]+\*\*)[ \t]+$')
TARGETS = [
    'notebooks/high-dimensional-spaces/kNN-Classification-Evaluation.ipynb',
    'notebooks/high-dimensional-spaces/Image-Clustering.ipynb',
    'notebooks/high-dimensional-spaces/BF-Clustering.ipynb',
    'notebooks/high-dimensional-spaces/SAT-Table.ipynb',
    'notebooks/high-dimensional-spaces/IRIS-Clustering.ipynb',
    'notebooks/high-dimensional-spaces/Image-Clustering-Hierarchical.ipynb',
    'notebooks/intro.md',
]
CRLF = '\r\n'


def clean_line(line):
    body = line.rstrip('\n')
    m = PATTERN.match(body)
    if m and body.rstrip() != body:
        return m.group(1) + '\n'
    return line


def main():
    total = 0
    for path in TARGETS:
        raw = io.open(path, 'rb').read()
        crlf = CRLF.encode() in raw
        if path.endswith('.ipynb'):
            nb = json.loads(raw.decode('utf-8').replace(CRLF, '\n'))
            n = 0
            for cell in nb.get('cells', []):
                src = cell.get('source')
                if isinstance(src, list):
                    cell['source'] = [clean_line(l) for l in src]
                    n += sum(1 for a, b in zip(src, cell['source']) if a != b)
            out = json.dumps(nb, indent=1, ensure_ascii=False)
            out = out.replace('\n', CRLF) + CRLF if crlf else out + '\n'
        else:
            text = raw.decode('utf-8').replace(CRLF, '\n')
            lines = text.splitlines(keepends=True)
            new = [clean_line(l) for l in lines]
            n = sum(1 for a, b in zip(lines, new) if a != b)
            out = ''.join(new).replace('\n', CRLF) if crlf else ''.join(new)
        if n:
            io.open(path, 'wb').write(out.encode('utf-8'))
        print('%-58s cleaned %d line(s)' % (path.split('/')[-1], n))
        total += n
    print('total:', total)
    return 0


if __name__ == '__main__':
    sys.exit(main())