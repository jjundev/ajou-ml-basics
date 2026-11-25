#!/usr/bin/env python3
"""
manifest + 섹션 조각 → 예습노트 HTML 하나 (표준 라이브러리만 사용).

실행 폴더 구조:
  RUN/manifest.json
  RUN/sections/<section-id>.html   (섹션 안쪽: <article class="topic"> 들)
템플릿은 ml-review-pack과 공유한다(assets/note-template.html 심링크).
CLI: preview_assemble.py --run RUN --out 예습노트/<Lxx>
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _review  # noqa: E402,F401
from assemble import AssembleError, esc, fill, split_scripts  # noqa: E402  (복습 스킬 공용)
import preview_manifest as pm  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets"
BRAND = "예습노트"


def read_fragment(path: Path) -> str:
    if not path.exists():
        raise AssembleError(f"조각 파일 없음: {path}")
    return path.read_text(encoding="utf-8")


def build_note(m: dict, run_dir: Path) -> str:
    sections, scripts = [], []
    for sec in m["sections"]:
        body, found = split_scripts(read_fragment(run_dir / "sections" / f"{sec['id']}.html"))
        scripts += found
        sections.append(f'    <section id="{sec["id"]}"><h2>{esc(sec["title"])}</h2>\n{body.strip()}\n    </section>')
    return fill((ASSETS / "note-template.html").read_text(encoding="utf-8"), {
        "PAGE_TITLE": esc(f"머신러닝기초 예습노트 {m['lecture']}"),
        "BRAND": BRAND,
        "DESCRIPTION": esc(m["note_subtitle"]),
        "TOC": "".join(f'<a href="#{s["id"]}">{esc(s["short"])}</a>' for s in m["sections"]),
        "TITLE": esc(m["note_title"]),
        "SUBTITLE": esc(m["note_subtitle"]),
        "SECTIONS": "\n".join(sections),
        "FOOTER": m["footer_note"],
        "SCRIPTS": "\n".join(f"  {s}" for s in scripts),
        "RANGE": m["lecture"],
    })


def assemble(run_dir: Path | str, out_dir: Path | str) -> Path:
    run_dir, out_dir = Path(run_dir), Path(out_dir)
    m = pm.load(run_dir / "manifest.json")
    html = build_note(m, run_dir)  # 조각이 하나라도 없으면 여기서 멈춰 아무 파일도 만들지 않는다
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / pm.note_name(m)
    path.write_text(html, encoding="utf-8")
    return path


def other_notes(path: Path, lecture: str) -> list[str]:
    """같은 폴더에 남은 다른 slug의 예습노트(slug를 바꿔 다시 만들었을 때)."""
    prefix = f"예습노트_{lecture}_"
    return sorted(n for n in (unicodedata.normalize("NFC", e) for e in os.listdir(path.parent))
                  if n.startswith(prefix) and n.endswith(".html") and n != path.name)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        path = assemble(args.run, args.out)
        print(path)
        lecture = path.name.split("_")[1]
        for name in other_notes(path, lecture):
            print(f"경고: 다른 slug의 예습노트가 남아 있어요(지우지 않음): {name}", file=sys.stderr)
    except (AssembleError, pm.ManifestError) as e:
        print(f"assemble 실패: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    sys.exit(main())
