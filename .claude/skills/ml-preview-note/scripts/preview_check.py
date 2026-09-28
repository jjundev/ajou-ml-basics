#!/usr/bin/env python3
"""
예습노트 HTML 검사기 (표준 라이브러리만 사용).

- 공통·계약 검사는 ml-review-pack의 check_common/check_note를 그대로 쓴다
  (예고 금지어는 없고, 보충 배지는 이 파일에서 "교과서 보충"으로 따로 검사한다).
- 예습 전용: 슬라이드 태그, 교과서 보충 배지, STT 레이어 금지, 분량(600자·eli5 2문장·listen 2항목).
- 분량은 레이어 안 글자만 센다. 공백, TeX($…$, $$…$$), 그림(svg·figure), 레이어 제목, 배지, 태그, 요약 패널은 뺀다.
CLI: preview_check.py --manifest RUN/manifest.json --note NOTE.html
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _review  # noqa: E402,F401
from check_html import VOID_TAGS, Problem, check_common, check_file, check_note, parse_html  # noqa: E402
import preview_manifest as pm  # noqa: E402

SUPP_LABEL = "교과서 보충"
STT_LAYERS = {"prof", "warn"}
MAX_CHARS = 600
MAX_ELI5_SENTENCES = 2
MAX_LISTEN_ITEMS = 2
LAYER_KINDS = ("eli5", "formal", "listen", "supp")
SKIP_TAGS = {"svg", "figure", "script", "style"}
SKIP_CLASSES = {"layer-title", "badge", "sum", "tags"}
MATH_RE = re.compile(r"\$\$.*?\$\$|\$[^$]*\$", re.S)


@dataclass
class TopicStats:
    text: str = ""
    eli5: str = ""
    listen_items: int = 0


class _StatsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stats: dict[str, TopicStats] = {}
        # (tag, topic_id, layer_kind, skip)
        self.stack: list[tuple[str, str | None, str | None, bool]] = []

    def _top(self) -> tuple[str | None, str | None, bool]:
        return self.stack[-1][1:] if self.stack else (None, None, False)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        cls = set(a.get("class", "").split())
        topic, layer, skip = self._top()
        if tag == "article" and "topic" in cls and a.get("id"):
            topic, layer = a["id"], None
            self.stats[topic] = TopicStats()
        if topic and tag == "div" and "layer" in cls:
            layer = next((k for k in LAYER_KINDS if k in cls), "other")
        skip = skip or tag in SKIP_TAGS or bool(cls & SKIP_CLASSES)
        if topic and layer and not skip:
            st = self.stats[topic]
            st.text += " "
            if layer == "eli5":
                st.eli5 += " "  # 블록 경계에서 문장이 붙지 않게
            if layer == "listen" and tag == "li":
                st.listen_items += 1
        if tag not in VOID_TAGS:
            self.stack.append((tag, topic, layer, skip))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        topic, layer, skip = self._top()
        if topic and layer and not skip:
            st = self.stats[topic]
            st.text += data
            if layer == "eli5":
                st.eli5 += data


def topic_stats(source: str) -> dict[str, TopicStats]:
    parser = _StatsParser()
    parser.feed(source)
    parser.close()
    return parser.stats


def visible_chars(text: str) -> int:
    return len(re.sub(r"\s", "", MATH_RE.sub("", text)))


def sentences(text: str) -> int:
    t = MATH_RE.sub("X", text).strip()
    return len([p for p in re.split(r"(?<=[.?!])\s+", t) if p.strip()])


def contract_view(m: dict) -> dict:
    """복습 check_note에 넘길 사본: 예고 금지어 없음, 보충 배지는 여기서 따로 검사."""
    v = copy.deepcopy(m)
    for sec in v["sections"]:
        for t in sec["topics"]:
            t["supp"] = False
    v["preview_topic"] = v["sections"][-1]["topics"][-1]["id"]
    v["forbidden_outside_preview"] = []
    return v


def check_preview(m: dict, note_path: Path | str) -> list[Problem]:
    path = Path(note_path)
    source = path.read_text(encoding="utf-8")
    doc = parse_html(source)
    out = check_common(doc, source, path) + check_note(doc, contract_view(m))
    stats = topic_stats(source)
    for sec in m["sections"]:
        for t in sec["topics"]:
            con = doc.containers.get(t["id"])
            if con is None or not t["layers"]:
                continue
            tag = f"{m['lecture']} {t['slides']}"
            if tag not in con.text:
                out.append(Problem("slide-tag", t["id"], f"'{tag}' 태그 없음"))
            if t["supp"] and ("supp" not in con.child_classes or SUPP_LABEL not in con.text):
                out.append(Problem("missing-supp", t["id"], f"layer supp + '{SUPP_LABEL}' 필요"))
            stt = STT_LAYERS & con.child_classes
            if stt:
                out.append(Problem("stt-layer", t["id"], ", ".join(sorted(stt))))
            st = stats.get(t["id"], TopicStats())
            n = visible_chars(st.text)
            if n > MAX_CHARS:
                out.append(Problem("topic-long", t["id"], f"본문 {n}자 > {MAX_CHARS}자"))
            k = sentences(st.eli5)
            if k > MAX_ELI5_SENTENCES:
                out.append(Problem("eli5-long", t["id"], f"쉽게 말하면 {k}문장 > {MAX_ELI5_SENTENCES}문장"))
            if st.listen_items > MAX_LISTEN_ITEMS:
                out.append(Problem("listen-long", t["id"], f"들을 때 포인트 {st.listen_items}개 > {MAX_LISTEN_ITEMS}개"))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--manifest")
    ap.add_argument("--note")
    args = ap.parse_args(argv)
    problems: list[Problem] = []
    if args.manifest:
        if not args.note:
            ap.error("--manifest에는 --note가 필요")
        try:
            problems += check_preview(pm.load(args.manifest), args.note)
        except pm.ManifestError as e:
            print(f"manifest 오류: {e}")
            return 1
    for name in args.files:
        problems += check_file(name)
    for p in problems:
        print(p)
    print("OK" if not problems else f"FAIL ({len(problems)})")
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
