"""One-off: build the 0909-0916 regression manifest from the repo's contract test constants.
Usage: python3 make_regression_manifest.py <repo-root> <out.json>
"""
import json
import os
import re
import sys
import unicodedata

repo, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(repo, "tests"))
sys.path.insert(0, os.path.join(repo, "scripts"))
import test_notes_html as t  # noqa: E402

pack = os.path.join(repo, "복습노트")
files = {unicodedata.normalize("NFC", f): f for f in os.listdir(pack)}
note = open(os.path.join(pack, files["정리노트_0909-0916_When_Models_Meet_Data.html"]), encoding="utf-8").read()
review = open(os.path.join(pack, files["복습문제_0909-0916_When_Models_Meet_Data.html"]), encoding="utf-8").read()
nav = dict(re.findall(r'<a href="#(s\d)">(.*?)</a>', note))


def strip(s):
    return re.sub(r"<[^>]+>", "", s).strip()


sections = []
for sid in t.SECTION_IDS:
    title = strip(re.search(rf'<section id="{sid}"><h2>(.*?)</h2>', note).group(1))
    topics = []
    for tid in t.TOPIC_IDS[sid]:
        h3 = re.search(rf'<article class="topic" id="{tid}">\s*<h3>(.*?)</h3>', note, re.S).group(1)
        topics.append({"id": tid, "title": strip(h3), "required_terms": t.REQUIRED_TERMS[tid],
                       "layers": ["eli5", "formal", "prof"] if sid in t.LAYERED_SECTIONS else [],
                       "supp": tid in t.SUPP_TOPICS})
    sections.append({"id": sid, "title": title, "short": nav[sid], "topics": topics})

problems = []
for pid, spec in t.PROBLEMS.items():
    card = re.search(rf'<article class="card" id="{pid}".*?</article>', review, re.S).group(0)
    problems.append({"id": pid, "part": "partA" if int(pid[1:]) <= 5 else "partB", "source": spec["source"],
                     "variant": int(pid[1:]) <= 5, "anchor": spec["anchor"],
                     "level": re.search(r'<span class="badge level">(★+)', card).group(1).count("★"),
                     "date": re.search(r"📅 (\d{4})", card).group(1), "terms": spec["terms"], "answer": ""})

manifest = {
    "course": "머신러닝기초", "range": "0909-0916", "slug": "When_Models_Meet_Data",
    "note_title": "When Models Meet Data — 5살도 이해하는 정리노트",
    "note_subtitle": "정방철 교수님 머신러닝기초 · 0909 · 0914 · 0916 수업 (Lecture00~02, MML 8장)",
    "review_title": "복습문제 10선 — 0909~0916 수업 범위",
    "review_intro": "(regression fixture)", "footer_note": "(regression fixture)", "footer_review": "(regression fixture)",
    "sessions": [{"date": d, "stt": f"STT/{d} 머러기.md", "summary": f"summaries/stt-{d}.md", "slides": s}
                 for d, s in (("0909", "L01 s1–8"), ("0914", "L01 s7–15"), ("0916", "L01 s14–17, L02 s2–6"))],
    "sections": sections, "preview_topic": "s5-next", "forbidden_outside_preview": t.FORBIDDEN_OUTSIDE_NEXT,
    "parts": [{"id": "partA", "title": "A. 교과서 본문 예제 (MML 8장)", "short": "A 교과서 예제"},
              {"id": "partB", "title": "B. 교과서 연습문제", "short": "B 교과서 연습문제"}],
    "problems": problems,
    "links": [{"topic": "s5-links", "href": h} for h in t.S5_LINK_HREFS],
}
with open(out, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("sections", len(sections), "problems", len(problems))
