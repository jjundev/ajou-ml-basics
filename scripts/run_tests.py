"""Run every test suite in its own process on macOS, Windows and Linux.

Suites reuse module names (``_util``, ``test_delivery`` ...), so they cannot be
collected by one pytest process.

    uv run python scripts/run_tests.py              # everything
    uv run python scripts/run_tests.py ml-midterm   # suites whose name matches
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NO_TESTS_COLLECTED = 5


def broken_links(root=ROOT):
    """Tracked symlinks that were not checked out as working symlinks."""
    listing = subprocess.run(['git', '-C', str(root), 'ls-files', '-s', '-z'],
                             capture_output=True, check=True).stdout.decode('utf-8')
    paths = [entry.split('\t', 1)[1] for entry in listing.split('\0') if entry.startswith('120000 ')]
    return [p for p in paths if not (root / p).is_symlink() or not (root / p).exists()]


def suites(root=ROOT):
    """(name, command) for each suite, discovered from the directory layout."""
    found = []
    for folder in [root / 'tests', *sorted((root / '.claude/skills').glob('*/tests'))]:
        name = folder.relative_to(root).parts[-2] if folder.parent != root else 'tests'
        if any(folder.glob('test_*.py')):
            found.append((name, [sys.executable, '-m', 'pytest', str(folder), '-q', '--tb=short', '-rfE',
                                 '-p', 'no:cacheprovider']))
        scripts = sorted([*folder.glob('*.test.js'), *folder.glob('*.test.cjs')])
        if scripts:
            found.append((name + ' (node)', ['node', '--test', *map(str, scripts)]))
    return found


def main(filters):
    links = broken_links()
    if links:
        print('심볼릭 링크가 올바르게 받아지지 않았습니다:', *links, sep='\n  ')
        print('Windows: 개발자 모드를 켜고 `git config core.symlinks true` 설정 후 위 파일을 다시 체크아웃하세요.')
        return 2
    selected = [s for s in suites() if not filters or any(f in s[0] for f in filters)]
    if not selected:
        print('일치하는 테스트 묶음이 없습니다:', *filters)
        return 2
    if any(command[0] == 'node' for _, command in selected) and not shutil.which('node'):
        print('node를 찾을 수 없습니다. Node.js를 설치하세요.')
        return 2
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    failed = []
    for name, command in selected:
        print(f'\n===== {name}', flush=True)
        code = subprocess.run(command, cwd=ROOT, env=env).returncode
        if code:
            failed.append(name + (' (수집된 테스트 없음)' if code == NO_TESTS_COLLECTED else ''))
    print(f'\n통과 {len(selected) - len(failed)} / 실패 {len(failed)}', *failed, sep='\n  ')
    return 1 if failed else 0


if __name__ == '__main__':
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
