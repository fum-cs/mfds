"""Binary-search which set of chapters makes xelatex exit non-zero.

Compiles the generated book with `\\includeonly` restricted to a subset of the
included articles. Prints the smallest failing subset.
"""
import io
import os
import subprocess
import sys

BUILD = sys.argv[1] if len(sys.argv) > 1 else '.'
BS = chr(92)


def includes_of(master):
    out = []
    i = 0
    while True:
        i = master.find(BS + 'include{', i)
        if i < 0:
            break
        j = master.find('}', i)
        out.append(master[i + len(BS) + 8:j])
        i = j
    return out


def compile_subset(master, names, tag):
    joined = ','.join(names)
    patched = master.replace(
        BS + 'begin{document}',
        BS + 'includeonly{' + joined + '}' + chr(10) + BS + 'begin{document}', 1)
    name = 'bisect-%s.tex' % tag
    io.open(name, 'w', encoding='utf-8').write(patched)
    r = subprocess.run(['xelatex', '-interaction=batchmode', '-file-line-error', name],
                       capture_output=True, text=True)
    return r.returncode


def main():
    os.chdir(BUILD)
    master = io.open('mfds-book.tex', encoding='utf-8').read()
    incs = includes_of(master)
    print('includes:', len(incs), '| baseline (all):', compile_subset(master, incs, 'all'))
    lo, hi = 0, len(incs)
    step = 0
    while hi - lo > 1:
        step += 1
        mid = (lo + hi) // 2
        first = incs[lo:mid]
        second = incs[mid:hi]
        rc_first = compile_subset(master, first, 'a%d' % step)
        rc_second = compile_subset(master, second, 'b%d' % step)
        print('step %d: [%d:%d] rc=%s | [%d:%d] rc=%s'
              % (step, lo, mid, rc_first, mid, hi, rc_second))
        if rc_first != 0:
            hi = mid
        elif rc_second != 0:
            lo = mid
        else:
            print('  -> failure needs the combination of both halves')
            break
    print('candidate window: %s' % incs[lo:hi])


if __name__ == '__main__':
    main()