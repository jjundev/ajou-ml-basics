#!/usr/bin/env python3
"""정리 노트를 넣을 복습노트 날짜 폴더(복습노트/<MMDD>/.pack)를 고른다. 파일을 쓰지 않는다.

사용법:
    python3 pick_date.py <work>/meta.json --repo <저장소 루트> [--date MMDD]

판단 순서:
  1. --date 지정 → 그 폴더가 있는지만 확인
  2. 강의노트 PDF에서 영상 id/URL 검색 → 그 쪽(page)의 가을 학기 슬라이드 날짜 → 없으면 PDF 전체에서 가장 이른 날짜
  3. 링크가 없으면 영상 제목·전사본 키워드와 각 날짜 정리노트 md의 겹침 점수
결과 JSON을 출력한다. 확정 못 하면 exit 2 와 후보 목록.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path

MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8,
          "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12}
DATE_RE = re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept?|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),\s*20\d{2}")
STOP = set("""the a an and or of to in on for with is are was were be been this that these those it its
we you they i he she as at by from but not so if then than there here what which who how when where
can will would could should do does did have has had our your their them us my me just like very
really going gonna get got one two also all any some more most much many let lets okay right well
now see say said thing things way know think want need make made because about into over only
same other each every first second next last video hello thanks thank going""".split())


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def existing_dates(repo: Path) -> list[str]:
    root = repo / "복습노트"
    if not root.is_dir():
        return []
    return sorted(nfc(d.name) for d in root.iterdir()
                  if d.is_dir() and re.fullmatch(r"\d{4}", nfc(d.name)) and (d / ".pack").is_dir())


def fall_dates(text: str) -> list[str]:
    out = []
    for m in DATE_RE.finditer(text):
        mon = MONTHS.get(m.group(1).lower()[:4].rstrip("."), MONTHS.get(m.group(1).lower()[:3]))
        day = int(m.group(2))
        if mon and mon >= 8 and 1 <= day <= 31:  # 템플릿 꼬리말(봄 학기 날짜)은 무시
            out.append(f"{mon:02d}{day:02d}")
    return out


def pdf_pages(pdf: Path) -> list[str]:
    try:
        txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True,
                             text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return txt.split("\f")


def by_link(repo: Path, vid: str, dates: list[str]) -> dict | None:
    pdfs = sorted((repo / "강의노트").rglob("*.pdf"))
    for pdf in pdfs:
        pages = pdf_pages(pdf)
        for i, page in enumerate(pages):
            if vid not in page:
                continue
            page_dates = [d for d in fall_dates(page) if d in dates]
            all_dates = sorted({d for d in fall_dates("\n".join(pages)) if d in dates})
            pick = (page_dates or all_dates or [None])[0]
            lec = re.search(r"Lecture\s*0?(\d+)", pdf.name)
            evidence = f"{pdf.name} {i + 1}쪽에 영상 링크"
            if pick:
                return {"date": pick, "lecture": f"Lecture{int(lec.group(1)):02d}" if lec else None,
                        "method": "link", "evidence": f"{evidence} → 슬라이드 날짜 {pick}",
                        "candidates": all_dates}
            return {"date": None, "method": "link", "evidence": f"{evidence}, 그러나 그 강의 날짜의 "
                    f"복습노트 폴더가 없음 (슬라이드 날짜: {sorted(set(fall_dates(chr(10).join(pages))))})",
                    "candidates": []}
    return None


def tokens(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z][a-z\-]{3,}", text.lower()) if w not in STOP]


def by_keywords(repo: Path, meta: dict, dates: list[str]) -> dict:
    src = meta.get("title", "")
    tp = meta.get("transcript")
    if tp and Path(tp).is_file():
        src += "\n" + Path(tp).read_text(encoding="utf-8")
    top = [w for w, _ in Counter(tokens(src)).most_common(40)]
    title_words = set(tokens(meta.get("title", "")))
    scores = []
    for d in dates:
        notes = list((repo / "복습노트" / d / ".pack").glob("정리노트_*.md"))
        text = "\n".join(n.read_text(encoding="utf-8", errors="ignore") for n in notes).lower()
        text += " " + " ".join(n.stem.lower().replace("_", " ") for n in notes)
        s = sum(1 for w in top if w in text) + sum(3 for w in title_words if w in text)
        scores.append((s, d))
    scores.sort(reverse=True)
    best = scores[0] if scores else (0, None)
    second = scores[1][0] if len(scores) > 1 else 0
    cands = [{"date": d, "score": s} for s, d in scores[:3]]
    if best[1] and best[0] >= 8 and best[0] > second:
        return {"date": best[1], "lecture": None, "method": "keywords",
                "evidence": f"영상 키워드와 정리노트 겹침 점수 {best[0]} (2위 {second})", "candidates": cands}
    return {"date": None, "method": "keywords",
            "evidence": f"키워드 점수로 확정 불가 (1위 {best[0]}, 2위 {second})", "candidates": cands}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("meta")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--date")
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
    dates = existing_dates(repo)

    if args.date:
        ok = args.date in dates
        res = {"date": args.date if ok else None, "method": "argument",
               "evidence": "사용자가 지정한 날짜" if ok else f"복습노트/{args.date}/.pack 이 없음",
               "candidates": dates[-5:]}
    else:
        res = by_link(repo, meta["id"], dates) or by_keywords(repo, meta, dates)

    if res.get("date"):
        res["pack_dir"] = str(repo / "복습노트" / res["date"] / ".pack" / f"영상정리_{meta['slug']}")
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get("date") else 2


if __name__ == "__main__":
    raise SystemExit(main())
