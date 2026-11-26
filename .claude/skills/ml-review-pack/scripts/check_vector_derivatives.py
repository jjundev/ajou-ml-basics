"""High-signal lint for course-authored row derivatives; not a symbolic proof.

Run only on material authored/converted to the course convention. Quoted original
exercises with an explicit different convention require human source comparison.
"""
import argparse
import html
import json
import re
from pathlib import Path


def check_text(text):
    text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
    errors = []
    if re.search(r'(?:gradient|기울기)\s*(?:는|은|:|=)?\s*(?:\$[^$]+\$\s*)?열벡터|열\s*gradient', text, re.I):
        errors.append('강의 관례와 다른 열 gradient 선언: 행벡터 미분인지 원문을 대조하세요')
    # Inspect only a displayed first derivative RHS, never arbitrary column data.
    for match in re.finditer(r'\\nabla[^=$]*=([^$]+)', text):
        rhs = re.split(r'\\(?:quad|qquad|Longrightarrow|Rightarrow|implies)', match[1])[0]
        compact = re.sub(r'\s+', '', rhs)
        bad = bool(re.match(r'Ax-b(?:[.,]|$)', compact))
        bad |= bool(re.search(r'\\Phi\^\\top(?:y|\(\\Phi\\theta-y\))', compact))
        bad |= bool(re.search(r'\\Phi\^\\top\\Phi\\theta|(?<![A-Za-z])2G\\theta', compact))
        bad |= bool(re.search(r'\\frac\{\\theta-m_0\}', compact))
        for matrix in re.findall(r'\\begin\{[pb]matrix\}(.*?)\\end\{[pb]matrix\}', compact):
            bad |= '\\\\' in matrix and '&' not in matrix
        if bad:
            errors.append('열 형태의 gradient 식: ' + match.group(0).strip()[:180])
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+', type=Path)
    args = parser.parse_args()
    errors = []
    for path in args.paths:
        try:
            errors += [f'{path}: {e}' for e in check_text(path.read_text(encoding='utf-8'))]
        except OSError as exc:
            errors.append(str(exc))
    print(json.dumps({'status': 'fail' if errors else 'pass', 'errors': errors}, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__':
    import sys
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
