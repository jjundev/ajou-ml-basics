#!/usr/bin/env python3
"""
manifest + 조각 파일 → 정리노트/복습문제 HTML 두 개 (표준 라이브러리만 사용).

실행 폴더 구조:
  RUN/manifest.json
  RUN/sections/<section-id>.html   (섹션 안쪽: <article class="topic"> 들, <script> 가능)
  RUN/cards/<problem-id>.html      (<article class="card"> 하나)
조각 안의 {{NOTE_HREF}} / {{REVIEW_HREF}} 는 실제 파일명으로 바뀐다.
<script> 블록은 조각에서 빼서 </body> 앞({{SCRIPTS}})으로 모은다.
CLI: assemble.py --run RUN --out 복습노트/<range>
"""

from __future__ import annotations

import argparse
import html
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manifest as manifest_mod  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets"
SLOT_RE = re.compile(r"\{\{([A-Z_]+)\}\}")
SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.S | re.I)


class AssembleError(RuntimeError):
    pass


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def fill(template: str, values: dict[str, str]) -> str:
    missing = sorted(set(SLOT_RE.findall(template)) - values.keys())
    if missing:
        raise AssembleError(f"템플릿 슬롯 값 없음: {missing}")
    return SLOT_RE.sub(lambda mo: values[mo.group(1)], template)


def split_scripts(fragment: str) -> tuple[str, list[str]]:
    scripts = SCRIPT_RE.findall(fragment)
    return SCRIPT_RE.sub("", fragment), scripts


def read_fragment(path: Path, m: dict) -> str:
    if not path.exists():
        raise AssembleError(f"조각 파일 없음: {path}")
    text = path.read_text(encoding="utf-8")
    return text.replace("{{NOTE_HREF}}", manifest_mod.note_name(m)).replace("{{REVIEW_HREF}}", manifest_mod.review_name(m))


def build_note(m: dict, run_dir: Path) -> str:
    sections, scripts = [], []
    for sec in m["sections"]:
        body, found = split_scripts(read_fragment(run_dir / "sections" / f"{sec['id']}.html", m))
        scripts += found
        sections.append(f'    <section id="{sec["id"]}"><h2>{esc(sec["title"])}</h2>\n{body.strip()}\n    </section>')
    return fill((ASSETS / "note-template.html").read_text(encoding="utf-8"), {
        "PAGE_TITLE": esc(f"머신러닝기초 정리노트 {m['range']}"),
        "BRAND": "정리노트",
        "DESCRIPTION": esc(m["note_subtitle"]),
        "TOC": "".join(f'<a href="#{s["id"]}">{esc(s["short"])}</a>' for s in m["sections"]),
        "TITLE": esc(m["note_title"]),
        "SUBTITLE": esc(m["note_subtitle"]),
        "SECTIONS": "\n".join(sections),
        "FOOTER": m["footer_note"],
        "SCRIPTS": "\n".join(f"  {s}" for s in scripts),
        "RANGE": m["range"],
    })


def build_review(m: dict, run_dir: Path) -> str:
    parts, scripts = [], []
    for part in m["parts"]:
        cards = []
        for q in (q for q in m["problems"] if q["part"] == part["id"]):
            body, found = split_scripts(read_fragment(run_dir / "cards" / f"{q['id']}.html", m))
            scripts += found
            cards.append(body.strip())
        parts.append(f'    <section id="{part["id"]}"><h2>{esc(part["title"])}</h2>\n' + "\n".join(cards) + "\n    </section>")
    return fill((ASSETS / "review-template.html").read_text(encoding="utf-8"), {
        "PAGE_TITLE": esc(f"머신러닝기초 복습문제 {m['range']}"),
        "DESCRIPTION": esc(m["review_title"]),
        "TOC": "".join(f'<a href="#{p["id"]}">{esc(p["short"])}</a>' for p in m["parts"]),
        "NOTE_HREF": manifest_mod.note_name(m),
        "TITLE": esc(m["review_title"]),
        "INTRO": m["review_intro"],
        "PARTS": "\n".join(parts),
        "FOOTER": m["footer_review"],
        "SCRIPTS": "\n".join(f"  {s}" for s in scripts),
        "RANGE": m["range"],
    })


def assemble(run_dir: Path | str, out_dir: Path | str, *, include_pdf_links: bool = False) -> tuple[Path, Path]:
    run_dir, out_dir = Path(run_dir), Path(out_dir)
    m = manifest_mod.load(run_dir / "manifest.json")
    out_dir.mkdir(parents=True, exist_ok=True)
    note_path = out_dir / manifest_mod.note_name(m)
    review_path = out_dir / manifest_mod.review_name(m)
    # 둘 다 만든 뒤에 쓴다: 조각이 하나라도 없으면 어느 파일도 바뀌지 않는다.
    note_html, review_html = build_note(m, run_dir), build_review(m, run_dir)
    if include_pdf_links:
        from review_pdf_links import add_pdf_links
        from review_pdf_types import ReviewPdfError
        from build_review_pdf import _verify_pdf
        import fitz
        try:
            for name in manifest_mod.pdf_names(m['range'], m['slug']):
                path = out_dir / name
                if not path.is_file():
                    raise AssembleError(f"검증된 PDF 쌍이 필요합니다: {path}")
                with fitz.open(path) as doc:
                    count = len(doc)
                _verify_pdf(path, count)
            note_html = add_pdf_links(note_html, m['range'], m['slug'], len(m['problems']))
        except (ReviewPdfError, OSError, fitz.FileDataError) as e:
            raise AssembleError(f"PDF 링크 실패: {e}") from e
    note_path.write_text(note_html, encoding="utf-8")
    review_path.write_text(review_html, encoding="utf-8")
    return note_path, review_path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pdf-links", action="store_true")
    args = ap.parse_args(argv)
    try:
        for path in assemble(args.run, args.out, include_pdf_links=args.pdf_links):
            print(path)
    except (AssembleError, manifest_mod.ManifestError) as e:
        print(f"assemble 실패: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
