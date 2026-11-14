#!/usr/bin/env python3
"""
정리노트/복습문제 HTML 검사기 (표준 라이브러리만 사용).

- 공통 검사: lang, 중복 id, 외부 리소스 허용 목록, 수식 구분자, 링크, 남은 슬롯, 위젯 정적 대체물, 식 줄(ol.deriv) 형식
- manifest 검사: 섹션·토픽 id, 필수 용어, 레이어, 보충 배지, 예고 밖 금지어, 링크, 문제 카드
- 정리노트 검사: 녹음 위치(시각 없는 파트 포함), 전사·발언·오타 수정 경위
CLI:
  check_html.py FILE [FILE ...]
  check_html.py --manifest run/manifest.json --note NOTE.html --review REVIEW.html
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import defaultdict
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote
from unicodedata import normalize

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manifest as manifest_mod  # noqa: E402

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
CONTAINER_CLASSES = {"topic", "card"}
# 블록 경계에서 텍스트를 끊어 인접 수식이 "$$"로 붙지 않게 한다.
BLOCK_TAGS = {"p", "div", "li", "ol", "ul", "td", "th", "tr", "table", "h1", "h2", "h3", "h4", "section", "article",
              "details", "summary", "figure", "figcaption", "blockquote", "header", "footer", "label", "br",
              "dl", "dt", "dd"}
ALLOWED_EXTERNAL_PREFIXES = (
    "https://cdn.jsdelivr.net/npm/katex@0.16.11/",
    "https://cdn.jsdelivr.net/npm/pretendard@1.3.9/",
)
SUPP_LABEL = "보충 · 수업에서 유도하진 않았어요"
# 스킬 템플릿을 바꾸기 전에 만든 팩의 라벨도 받아 준다.
LEGACY_SUPP_LABELS = ("📎 보충 · 수업 미유도",)
CARD_PARTS = {"problem", "original", "hint", "solution", "answer"}
SUM_PANEL_ID = "sum-for"
SLOT_RE = re.compile(r"\{\{[A-Z_]+\}\}")
STT_PART = r"(?:P[0-9]+|Part\s+[0-9]+)\s+"
STT_TIME = r"~?[0-9]{1,3}:[0-5][0-9](?::[0-5][0-9])?(?![0-9:])"
STT_TIMESTAMP_RE = re.compile(
    rf"(?<![\w])(?:[0-9]{{4}}\s+(?:{STT_PART})?|{STT_PART}|수업\s+){STT_TIME}"
    rf"(?:\s*[-–—~,]\s*(?:{STT_PART})?{STT_TIME})*"
)
# Dates or recording context distinguish these from lecture titles such as Part 2.
STT_LOCATION_RE = re.compile(
    r"(?<!\w)(?:(?:[0-9]{4}\s+(?:전사\s+)?|(?:녹음|전사|STT)\s+)"
    r"(?:P[0-9]+|Parts?\s*[0-9]+)|Parts?\s+[0-9]{2,}|P[0-9]{2,})"
    r"(?:\s*[-–—~]\s*(?:(?:Parts?\s*|P))?[0-9]+)?",
    re.IGNORECASE,
)
EDITORIAL_HISTORY_RE = re.compile(
    r"(?:STT|전사)(?:의|에서(?:는)?|에(?:는)?)"
    r"|(?:말실수|오인식|정확한\s*시각\s*없음|(?:세부\s*)?시각\s*미제공)"
    r"|(?:수업|강의)[^\n.!?。]{0,220}?(?:구두로\s*언급|말했다가|말했지만|말한\s*부분|적었다가|읽었다가|정정)"
    r"|시각은[^\n.!?。]{0,100}?(?:녹음|파트)"
    r"|(?:슬라이드|TA[0-9]+\s*s[0-9]+)[^\n.!?。]{0,180}?(?:오타|바로잡|고쳤)"
)
REMOTE_PREFIXES = ("http://", "https://", "//")
# CSS 안의 url(...) 과 @import "..." 대상
CSS_URL_RE = re.compile(r"""url\(\s*['"]?([^'")\s]+)|@import\s+['"]([^'"]+)['"]""", re.IGNORECASE)


def is_remote(url: str) -> bool:
    return url.strip().lower().startswith(REMOTE_PREFIXES)


@dataclass
class Container:
    id: str
    classes: set[str]
    attrs: dict[str, str]
    section: str | None
    text: str = ""
    hrefs: list[str] = field(default_factory=list)
    child_classes: set[str] = field(default_factory=set)


@dataclass
class Doc:
    lang: str | None = None
    ids: set[str] = field(default_factory=set)
    duplicate_ids: set[str] = field(default_factory=set)
    id_section: dict[str, str | None] = field(default_factory=dict)
    hrefs: list[str] = field(default_factory=list)
    external_resources: list[str] = field(default_factory=list)
    section_text: dict[str, str] = field(default_factory=lambda: defaultdict(str))
    containers: dict[str, Container] = field(default_factory=dict)
    widgets: dict[str, set[str]] = field(default_factory=dict)
    scripts_by_id: dict[str, str] = field(default_factory=dict)
    body_text: str = ""
    body_origins: list[tuple[int, int]] = field(default_factory=list)


class _Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doc = Doc()
        # (tag, section_id, container_id, widget_id)
        self.stack: list[tuple[str, str | None, str | None, str | None]] = []
        self.raw_tag: str | None = None
        self.script_id: str | None = None

    def _context(self) -> tuple[str | None, str | None, str | None]:
        if not self.stack:
            return None, None, None
        _, sec, con, wid = self.stack[-1]
        return sec, con, wid

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        sec, con, wid = self._context()
        classes = set(a.get("class", "").split())
        if tag == "html":
            self.doc.lang = a.get("lang")
        el_id = a.get("id")
        if el_id:
            if el_id in self.doc.ids:
                self.doc.duplicate_ids.add(el_id)
            self.doc.ids.add(el_id)
        if tag == "section" and el_id:
            sec = el_id
        if el_id:
            self.doc.id_section[el_id] = sec
        if con is not None:
            self.doc.containers[con].child_classes |= classes
        if wid is not None:
            self.doc.widgets[wid] |= classes
        if el_id and classes & CONTAINER_CLASSES:
            self.doc.containers[el_id] = Container(el_id, classes, a, sec)
            con = el_id
        if el_id and "widget" in classes:
            self.doc.widgets[el_id] = set()
            wid = el_id
        if tag == "a" and "href" in a:
            self.doc.hrefs.append(a["href"])
            if con is not None:
                self.doc.containers[con].hrefs.append(a["href"])
        # 원격 리소스: 모든 태그의 src, 모든 <link>의 href (<a href>는 broken_links 담당)
        if is_remote(a.get("src", "")):
            self.doc.external_resources.append(a["src"])
        if tag == "link" and is_remote(a.get("href", "")):
            self.doc.external_resources.append(a["href"])
        if tag in ("script", "style"):
            self.raw_tag = tag
            self.script_id = el_id if tag == "script" else None
            if self.script_id:
                self.doc.scripts_by_id[self.script_id] = ""
        if tag in BLOCK_TAGS:
            self._emit("\n")
        if tag not in VOID_TAGS:
            self.stack.append((tag, sec, con, wid))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.raw_tag = None
            self.script_id = None
        if tag in BLOCK_TAGS:
            self._emit("\n")
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.raw_tag == "script":
            if self.script_id:
                self.doc.scripts_by_id[self.script_id] += data
            return
        if self.raw_tag == "style":
            for m in CSS_URL_RE.finditer(data):
                url = m.group(1) or m.group(2)
                if is_remote(url):
                    self.doc.external_resources.append(url)
            return
        self._emit(data)

    def _emit(self, data):
        if self.raw_tag:
            return
        sec, con, _ = self._context()
        offset = len(self.doc.body_text)
        line = self.getpos()[0]
        for part in data.splitlines(keepends=True):
            self.doc.body_origins.append((offset, line))
            offset += len(part)
            line += part.count("\n")
        self.doc.body_text += data
        if sec:
            self.doc.section_text[sec] += data
        if con:
            self.doc.containers[con].text += data


def parse_html(source: str) -> Doc:
    parser = _Parser()
    parser.feed(source)
    parser.close()
    return parser.doc


def parse_file(path: Path | str) -> Doc:
    return parse_html(Path(path).read_text(encoding="utf-8"))


def math_delimiter_errors(text: str) -> list[str]:
    errors: list[str] = []
    t = text.replace("\\$", "")
    if t.count("$$") % 2:
        errors.append("unbalanced $$ (display math)")
    t = re.sub(r"\$\$.*?\$\$", "", t, flags=re.S)
    if t.count("$") % 2:
        errors.append("unbalanced $ (inline math)")
    return errors


def broken_links(doc: Doc, base_dir: Path) -> list[str]:
    broken: list[str] = []
    cache: dict[Path, Doc] = {}
    for href in doc.hrefs:
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        path_part, _, frag = href.partition("#")
        if not path_part:
            if frag not in doc.ids:
                broken.append(href)
            continue
        target = (Path(base_dir) / unquote(path_part)).resolve()
        if not target.exists():
            broken.append(href)
            continue
        if frag and target.suffix == ".html":
            if target not in cache:
                cache[target] = parse_file(target)
            if frag not in cache[target].ids:
                broken.append(href)
    return broken


@dataclass(frozen=True)
class Problem:
    code: str
    where: str
    detail: str

    def __str__(self) -> str:
        return f"[{self.code}] {self.where}: {self.detail}"


class _DerivRows(HTMLParser):
    """ol.deriv의 각 li에서 .deriv-eq 수식 수와 .deriv-why 주석 글자를 모은다."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []  # 열린 요소의 역할: deriv, row, eq, why, details, other
        self.rows: list[dict] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        cls = (dict(attrs).get("class") or "").split()
        role = "other"
        if tag == "ol" and "deriv" in cls:
            role = "deriv"
        elif tag == "li" and self.stack and self.stack[-1] == "deriv":
            role = "row"
            self.rows.append({"eq": "", "why": "", "line": self.getpos()[0]})
        elif "deriv-eq" in cls and "row" in self.stack:
            role = "eq"
        elif "deriv-why" in cls and "row" in self.stack:
            role = "why"
        elif tag == "details":
            role = "details"
        if tag in ("script", "style"):
            self.skip += 1
        self.stack.append(role)

    def handle_endtag(self, tag):
        if tag in VOID_TAGS or not self.stack:
            return
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        self.stack.pop()

    def handle_data(self, data):
        if self.skip or not self.rows or "row" not in self.stack:
            return
        if "eq" in self.stack:
            self.rows[-1]["eq"] += data
        elif "why" in self.stack and "details" not in self.stack:
            self.rows[-1]["why"] += data


def deriv_row_errors(source: str) -> list[str]:
    """식 줄 + 주석(ol.deriv): 줄마다 디스플레이 수식 1개와 보이는 주석이 있어야 한다."""
    p = _DerivRows()
    p.feed(source)
    out = []
    for r in p.rows:
        n = len(re.findall(r"\$\$.+?\$\$", r["eq"], re.S))
        if n != 1:
            out.append(f"line {r['line']}: .deriv-eq 디스플레이 수식 {n}개 (1개여야 함)")
        if not r["why"].strip():
            out.append(f"line {r['line']}: .deriv-why 보이는 주석 없음")
    return out


def check_common(doc: Doc, source: str, path: Path) -> list[Problem]:
    name = Path(path).name
    out: list[Problem] = []
    if doc.lang != "ko":
        out.append(Problem("lang", name, f"<html lang> = {doc.lang!r}"))
    out += [Problem("duplicate-id", name, i) for i in sorted(doc.duplicate_ids)]
    out += [Problem("external", name, u) for u in doc.external_resources if not u.startswith(ALLOWED_EXTERNAL_PREFIXES)]
    out += [Problem("math", name, e) for e in math_delimiter_errors(doc.body_text)]
    out += [Problem("broken-link", name, h) for h in broken_links(doc, Path(path).parent)]
    out += [Problem("leftover-slot", name, s) for s in sorted(set(SLOT_RE.findall(source)))]
    out += [Problem("deriv-row", name, e) for e in deriv_row_errors(source)]
    out += [Problem("widget-static-missing", wid, "위젯에 .widget-static 정적 대체물이 없음")
            for wid, classes in sorted(doc.widgets.items()) if "widget-static" not in classes]
    return out


def check_note(doc: Doc, m: dict) -> list[Problem]:
    out: list[Problem] = []
    preview_section = None
    for sec in m["sections"]:
        if sec["id"] not in doc.ids:
            out.append(Problem("missing-section", sec["id"], "섹션 id 없음"))
        for t in sec["topics"]:
            if t["id"] == m["preview_topic"]:
                preview_section = sec["id"]
            con = doc.containers.get(t["id"])
            if con is None:
                out.append(Problem("missing-topic", t["id"], "토픽 없음"))
                continue
            if con.section != sec["id"]:
                out.append(Problem("wrong-section", t["id"], f"{con.section} 안에 있음 (기대: {sec['id']})"))
            out += [Problem("missing-term", t["id"], term) for term in t["required_terms"] if term not in con.text]
            out += [Problem("missing-layer", t["id"], layer) for layer in t["layers"] if layer not in con.child_classes]
            if t["supp"] and ("supp" not in con.child_classes
                              or not any(label in con.text for label in (SUPP_LABEL, *LEGACY_SUPP_LABELS))):
                out.append(Problem("missing-supp", t["id"], f"layer supp + '{SUPP_LABEL}' 필요"))
            # 페이지 요약 패널(#sum-for)이 있는 템플릿으로 만든 팩만 검사한다.
            if SUM_PANEL_ID in doc.ids and t["layers"] and "sum" not in con.child_classes:
                out.append(Problem("missing-sum", t["id"], '<div class="sum" hidden> 페이지 요약 없음'))
    texts: dict[str, str] = {}
    for sec in m["sections"]:
        if sec["id"] != preview_section:
            texts[sec["id"]] = doc.section_text.get(sec["id"], "")
            continue
        for t in sec["topics"]:
            if t["id"] != m["preview_topic"] and t["id"] in doc.containers:
                texts[t["id"]] = doc.containers[t["id"]].text
    for where, text in texts.items():
        out += [Problem("forbidden-term", where, term) for term in m["forbidden_outside_preview"] if term in text]
    for link in m["links"]:
        con = doc.containers.get(link["topic"])
        if con is None or link["href"] not in con.hrefs:
            out.append(Problem("missing-link", link["topic"], link["href"]))
    return out


def check_review(doc: Doc, m: dict) -> list[Problem]:
    out: list[Problem] = []
    out += [Problem("forbidden-term", "review", term) for term in m["forbidden_outside_preview"] if term in doc.body_text]
    for q in m["problems"]:
        card = doc.containers.get(q["id"])
        if card is None:
            out.append(Problem("missing-card", q["id"], "카드 없음"))
            continue
        if card.attrs.get("data-source") != q["source"]:
            out.append(Problem("card-source", q["id"], f"data-source={card.attrs.get('data-source')!r}"))
        missing = CARD_PARTS - card.child_classes
        if missing:
            out.append(Problem("card-parts", q["id"], ", ".join(sorted(missing))))
        out += [Problem("card-term", q["id"], term) for term in q["terms"] if term not in card.text]
    return out


def check_file(path: Path | str) -> list[Problem]:
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    doc = parse_html(source)
    out = check_common(doc, source, path)
    if normalize("NFC", path.name).startswith("정리노트_"):
        out += check_reader_prose(doc, path)
    return out


def check_reader_prose(doc: Doc, path: Path) -> list[Problem]:
    """Inspect reader text across inline tags, retaining source line numbers.

    Hidden summaries are included; scripts, styles and comments are excluded.
    """
    out: list[Problem] = []
    timestamps = list(STT_TIMESTAMP_RE.finditer(doc.body_text))
    matches = [("stt-timestamp", match) for match in timestamps]
    matches += [("stt-location", match) for match in STT_LOCATION_RE.finditer(doc.body_text)
                if not any(t.start() <= match.start() < t.end() for t in timestamps)]
    matches += [("editorial-history", match) for match in EDITORIAL_HISTORY_RE.finditer(doc.body_text)]
    starts = [offset for offset, _ in doc.body_origins]
    for code, match in sorted(matches, key=lambda item: item[1].start()):
        origin = bisect_right(starts, match.start()) - 1
        line = doc.body_origins[origin][1]
        out.append(Problem(code, f"{path.name}:{line}", match.group()))
    return out


def check_pack(m: dict, note_path: Path | str, review_path: Path | str) -> list[Problem]:
    out: list[Problem] = []
    for path, extra in ((note_path, check_note), (review_path, check_review)):
        source = Path(path).read_text(encoding="utf-8")
        doc = parse_html(source)
        out += check_common(doc, source, Path(path)) + extra(doc, m)
        if extra is check_note:
            out += check_reader_prose(doc, Path(path))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--manifest")
    ap.add_argument("--note")
    ap.add_argument("--review")
    args = ap.parse_args(argv)
    problems: list[Problem] = []
    if args.manifest:
        if not (args.note and args.review):
            ap.error("--manifest에는 --note와 --review가 필요")
        problems += check_pack(manifest_mod.load(args.manifest), args.note, args.review)
    for name in args.files:
        problems += check_file(name)
    for p in problems:
        print(p)
    print("OK" if not problems else f"FAIL ({len(problems)})")
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
