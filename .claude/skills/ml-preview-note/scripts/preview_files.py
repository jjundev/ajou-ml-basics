#!/usr/bin/env python3
"""
예습노트 대상 Lecture 고르기와 기존 예습노트 백업 (표준 라이브러리만 사용).

- 같은 번호에 _rev PDF가 있으면 그것을 쓰고, slug에서 _rev를 뺀다.
- 인자가 없으면 번호가 가장 큰 Lecture. 그 예습노트가 이미 있으면 멈춘다(지난 강의로 내려가지 않는다).
- macOS NFD 폴더·파일명도 NFC로 비교해 찾는다.
CLI:
  preview_files.py pick --repo REPO [--lecture L03]       → "L03<TAB>PDF 경로<TAB>slug"
  preview_files.py backup --repo REPO --lecture L03 --run RUN
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time
import unicodedata

PDF_RE = re.compile(r"Lecture(\d{2})_([A-Za-z0-9_]+?)(_rev)?\.pdf")
LECTURES_DIR = "강의노트"
NOTES_DIR = "예습노트"


class PickError(RuntimeError):
    pass


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def child(parent: Path | None, name: str) -> Path | None:
    """parent 안에서 NFC 이름이 name인 항목(NFD 이름 포함)."""
    if parent is None or not parent.is_dir():
        return None
    for entry in os.listdir(parent):
        if nfc(entry) == name:
            return parent / entry
    return None


def lecture_pdfs(repo) -> dict[str, tuple[Path, str]]:
    d = child(Path(repo), LECTURES_DIR)
    if d is None:
        raise PickError(f"{LECTURES_DIR}/ 폴더 없음: {repo}")
    found: dict[str, tuple[Path, str, bool]] = {}
    for entry in sorted(os.listdir(d)):
        m = PDF_RE.fullmatch(nfc(entry))
        if not m:
            continue
        lec, slug, rev = f"L{m.group(1)}", m.group(2), bool(m.group(3))
        if lec not in found or (rev and not found[lec][2]):
            found[lec] = (d / entry, slug, rev)
    return {k: (p, s) for k, (p, s, _) in sorted(found.items())}


def has_note(repo, lecture: str) -> bool:
    d = child(child(Path(repo), NOTES_DIR), lecture)
    return d is not None and any(
        nfc(n).startswith(f"예습노트_{lecture}_") and n.endswith(".html") for n in os.listdir(d))


def pick(repo, lecture: str | None = None) -> tuple[str, Path, str]:
    pdfs = lecture_pdfs(repo)
    if not pdfs:
        raise PickError(f"{LECTURES_DIR}/에 LectureNN_*.pdf 없음. 새 강의노트가 올라왔는지 ajou-bb로 확인하세요.")
    available = ", ".join(pdfs)
    if lecture is not None:
        lecture = normalize_lecture(lecture)
        if lecture not in pdfs:
            raise PickError(f"{lecture} 강의노트 없음. 사용 가능: {available}")
    else:
        lecture = max(pdfs)
        if has_note(repo, lecture):
            raise PickError(f"최신 강의 {lecture}의 예습노트가 이미 있어요. 새 강의노트가 올라왔는지 ajou-bb로 확인하세요. "
                            f"다시 만들려면 {lecture}를 인자로 주세요. 사용 가능: {available}")
    pdf, slug = pdfs[lecture]
    return lecture, pdf, slug


def normalize_lecture(arg: str) -> str:
    """"L03", "l03", "L3", "3", "03" → "L03"."""
    m = re.fullmatch(r"[Ll]?(\d{1,2})", arg.strip())
    if not m:
        raise PickError(f"Lecture 형식이 아님: {arg!r} (예: L03)")
    return f"L{int(m.group(1)):02d}"


def _count(p: Path) -> int:
    return sum(len(files) for _, _, files in os.walk(p)) if p.is_dir() else 1


def backup(repo, lecture: str, run) -> Path | None:
    run = Path(run)
    try:
        lecture = normalize_lecture(lecture)
    except PickError as e:
        raise PickError(f"백업 중단: {e}") from e
    if not run.is_dir():
        raise PickError(f"백업 중단: run 폴더 없음: {run}")
    src = child(child(Path(repo), NOTES_DIR), lecture)
    if src is None:
        return None
    hits = sorted((nfc(n), src / n) for n in os.listdir(src)
                  if nfc(n).startswith(f"예습노트_{lecture}_") or nfc(n) == f"figures_{lecture}")
    if not hits:
        return None
    dst = Path(tempfile.mkdtemp(prefix=time.strftime("previous-%Y%m%d-%H%M%S-"), dir=run))  # 항상 새 폴더
    for name, path in hits:
        if path.is_dir():
            shutil.copytree(path, dst / name)
        else:
            shutil.copy2(path, dst / name)
    want, got = sum(_count(p) for _, p in hits), _count(dst)
    if got != want:
        raise PickError(f"백업 실패: 파일 {want}개 중 {got}개만 복사됨 → {dst}")
    return dst


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick")
    p.add_argument("--repo", required=True)
    p.add_argument("--lecture")
    b = sub.add_parser("backup")
    b.add_argument("--repo", required=True)
    b.add_argument("--lecture", required=True)
    b.add_argument("--run", required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "pick":
            lecture, pdf, slug = pick(args.repo, args.lecture)
            print(f"{lecture}\t{pdf}\t{slug}")
        else:
            dst = backup(args.repo, args.lecture, args.run)
            print(f"백업: {dst}" if dst else "백업할 기존 예습노트 없음")
    except PickError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    sys.exit(main())
