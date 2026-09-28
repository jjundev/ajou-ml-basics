#!/usr/bin/env python3
"""
예습노트 HTML → GitHub 마크다운 (표준 라이브러리만 사용).

ml-review-pack의 html2md 변환·검사 함수를 그대로 쓴다. 그림은 같은 폴더의 figures_<Lxx>/에 SVG로 내보낸다.
CLI:
  preview_md.py 예습노트_<Lxx>_<slug>.html            # 같은 폴더에 .md + figures_<Lxx>/
  preview_md.py 예습노트_<Lxx>_<slug>.html --check    # 변환 후 누락 검사(수식·앵커·그림·링크)
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _review  # noqa: E402,F401
import html2md  # noqa: E402  (복습 스킬 공용)

NAME_RE = re.compile(r"예습노트_(L\d{2})_([A-Za-z0-9_]+)\.html")


def convert_note(note_path: Path | str) -> tuple[Path, int]:
    src = Path(note_path).resolve()
    name = html2md.nfc(src.name)
    m = NAME_RE.fullmatch(name)
    if not m:
        raise ValueError(f"파일명 규칙 위반: {name}")
    fig_name = f"figures_{m.group(1)}"
    fig_abs = src.parent / fig_name
    fig_abs.mkdir(exist_ok=True)
    for entry in os.listdir(fig_abs):  # 다시 변환할 때 이전 실행의 고아 SVG를 남기지 않는다(.svg만, 이 폴더만)
        old = fig_abs / entry
        if entry.lower().endswith(".svg") and old.is_file() and not old.is_symlink():
            old.unlink()
    md_name = name[:-5] + ".md"
    ctx = html2md.Ctx([(name, md_name)], str(fig_abs), fig_name, prefix="note", registry=set())
    intro = [f"> `{name}`를 마크다운으로 옮겼어요. 그림은 `{fig_name}/` 폴더의 SVG예요. "
             "수식은 `$…$` / `$$…$$`라서 GitHub, Obsidian, Typora에서 보여요."]
    out = src.parent / md_name
    html2md.convert(str(src), str(out), ctx, intro)
    return out, len(ctx.registry)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("note")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    if not Path(args.note).is_file():
        print(f"노트 파일 없음: {args.note}", file=sys.stderr)
        return 1
    try:
        out, figs = convert_note(args.note)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    print(out)
    print(f"figures: {figs}")
    if not args.check:
        return 0
    problems = html2md.check_md(str(Path(args.note).resolve()), str(out))
    for p in problems:
        print(f"{out.name}: {p}")
    print("OK" if not problems else f"FAIL ({len(problems)})")
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
