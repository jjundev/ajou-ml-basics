#!/usr/bin/env python3
"""
복습노트/<날짜>/ 정리: HTML과 복습문제 PDF 쌍은 날짜 폴더에 두고 나머지는 .pack/ 아래로 옮긴다
(표준 라이브러리만 사용).

- 이동은 `git mv`로 한다(추적되지 않은 항목은 일반 이동).
- 최상위 HTML의 href/src 중 옮긴 항목을 가리키는 것에 `.pack/`을 붙인다.
- .pack/으로 옮긴 MD의 상대 링크는 새 위치 기준으로 고친다: 함께 옮긴 항목은 그대로, 나머지는 `../`를 붙인다.
- 이미 .pack/이 있는 날짜 폴더는 건너뛴다(여러 번 실행해도 결과가 같다).
- 끝나면 모든 HTML·MD의 상대 링크가 실제 파일을 가리키는지 검사한다.

CLI: python3 scripts/migrate_pack_layout.py [--apply] [--repo REPO]   (기본은 계획만 출력)
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unicodedata
from urllib.parse import quote, unquote

PACK_DIR = ".pack"  # ml-review-pack/scripts/manifest.py의 PACK_DIR과 같은 값
DATE_RE = re.compile(r"\d{4}(?:-\d{4})?")
REVIEW_PDF_RE = re.compile(r"복습문제_.*-(문제|답안)\.pdf")
ATTR_RE = re.compile(r'(\b(?:href|src)=")([^"]*)(")')
MD_LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def _relative(target: str) -> bool:
    return bool(target) and not target.startswith(("#", "/")) and not SCHEME_RE.match(target)


def _first(path: str) -> str:
    return nfc(unquote(path.removeprefix("./").split("/", 1)[0]))


def rewrite_html(text: str, moved: set[str]) -> str:
    """최상위 HTML: 옮긴 항목을 가리키는 링크에 .pack/을 붙인다."""
    def fix(m):
        target = m[2]
        if _relative(target) and _first(target.partition("#")[0]) in moved:
            encoded = "%" in target
            prefix = quote(PACK_DIR) if encoded else PACK_DIR
            return m[1] + prefix + "/" + target.removeprefix("./") + m[3]
        return m[0]
    return ATTR_RE.sub(fix, text)


def rewrite_md(text: str, moved: set[str]) -> str:
    """.pack/으로 옮긴 MD: 함께 옮긴 항목은 그대로, 날짜 폴더 기준이던 나머지 링크는 ../를 붙인다."""
    def fix(m):
        target = m[2]
        path = target.partition("#")[0]
        if not _relative(target) or not path or _first(path) in moved:
            return m[0]
        return m[1] + "../" + target.removeprefix("./") + m[3]
    return ATTR_RE.sub(fix, MD_LINK_RE.sub(fix, text))


def unrewrite_html(text: str) -> str:
    """rewrite_html의 역변환: .pack/ 접두를 뗀다."""
    return ATTR_RE.sub(lambda m: m[1] + m[2][len(PACK_DIR) + 1:] + m[3]
                       if m[2].startswith(PACK_DIR + "/") else m[0], text)


def unrewrite_md(text: str, moved: set[str]) -> str:
    """rewrite_md의 역변환: 붙였던 ../ 하나를 뗀다."""
    def fix(m):
        target = m[2]
        if target.startswith("../") and _first(target[3:].partition("#")[0]) not in moved:
            return m[1] + target[3:] + m[3]
        return m[0]
    return ATTR_RE.sub(fix, MD_LINK_RE.sub(fix, text))


def legacy_files(day: Path) -> dict[str, bytes]:
    """.pack 형식 날짜 폴더를 옮기기 전 형식으로 되돌린 {날짜 폴더 기준 경로: 바이트}.

    승인 당시 해시(문제설명 manifest·validation)를 현재 파일로 검증할 때 쓴다."""
    pack = day / PACK_DIR
    moved = {nfc(p.name) for p in pack.iterdir()}
    out = {}
    for html in day.glob("*.html"):
        out[html.name] = unrewrite_html(html.read_text(encoding="utf-8")).encode("utf-8")
    for pdf in day.glob("*.pdf"):
        if REVIEW_PDF_RE.fullmatch(nfc(pdf.name)):
            out[pdf.name] = pdf.read_bytes()
    for file in pack.rglob("*"):
        if file.is_file():
            rel = file.relative_to(pack)
            data = file.read_bytes()
            if len(rel.parts) == 1 and file.suffix == ".md":
                data = unrewrite_md(data.decode("utf-8"), moved).encode("utf-8")
            out[rel.as_posix()] = data
    return out


def _exists(path: Path) -> bool:
    return any(Path(unicodedata.normalize(f, str(path))).exists() for f in ("NFC", "NFD"))


def broken_links(file: Path) -> list[str]:
    text = file.read_text(encoding="utf-8")
    targets = [m[2] for m in ATTR_RE.finditer(text)]
    if file.suffix == ".md":
        targets += [m[2] for m in MD_LINK_RE.finditer(text)]
    out = []
    for target in targets:
        path = target.partition("#")[0]
        if _relative(target) and path and not _exists(file.parent / unquote(path)):
            out.append(target)
    return out


def _move(src: Path, dst: Path, repo: Path) -> None:
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", str(src)], cwd=repo,
                             capture_output=True).returncode == 0
    if tracked:
        subprocess.run(["git", "mv", str(src), str(dst)], cwd=repo, check=True)
    else:
        shutil.move(str(src), str(dst))


def migrate_day(day: Path, repo: Path, apply: bool) -> list[str]:
    if (day / PACK_DIR).exists():
        return []
    entries = [p for p in sorted(day.iterdir()) if p.suffix != ".html" and p.name != ".DS_Store"
               and not REVIEW_PDF_RE.fullmatch(nfc(p.name))]
    if not apply or not entries:
        return [p.name for p in entries]
    moved = {nfc(p.name) for p in entries}
    pack = day / PACK_DIR
    pack.mkdir()
    for p in entries:
        _move(p, pack / p.name, repo)
    for html in day.glob("*.html"):
        html.write_text(rewrite_html(html.read_text(encoding="utf-8"), moved), encoding="utf-8")
    for md in pack.glob("*.md"):
        md.write_text(rewrite_md(md.read_text(encoding="utf-8"), moved), encoding="utf-8")
    return [p.name for p in entries]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    notes = next((p for p in repo.iterdir() if nfc(p.name) == "복습노트"), None)
    if notes is None:
        print("복습노트/ 없음", file=sys.stderr)
        return 1
    days = sorted(p for p in notes.iterdir() if p.is_dir() and DATE_RE.fullmatch(nfc(p.name)))
    for day in days:
        names = migrate_day(day, repo, args.apply)
        print(f"{nfc(day.name)}: {'옮김' if args.apply else '옮길 항목'} {len(names)}개", *names, sep="\n  ")
    if not args.apply:
        return 0
    problems = []
    for day in days:
        for file in [*day.glob("*.html"), *(day / PACK_DIR).glob("*.md")]:
            problems += [f"{file.relative_to(repo)}: {t}" for t in broken_links(file)]
    print(*problems, sep="\n")
    print("OK" if not problems else f"FAIL ({len(problems)})")
    return int(bool(problems))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    sys.exit(main())
