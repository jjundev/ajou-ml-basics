#!/usr/bin/env python3
"""
정리노트/복습문제 HTML 구조 검사기 (표준 라이브러리만 사용).

- parse_html / parse_file: id, 링크, 섹션·컨테이너별 텍스트, 인라인 스크립트 수집
- math_delimiter_errors: KaTeX 구분자($, $$) 짝 검사
- broken_links: 앵커/상대경로 링크 검사
CLI: python3 scripts/check_notes_html.py <file.html> [...]
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
CONTAINER_CLASSES = {"topic", "card"}
BLOCK_TAGS = {"p", "div", "li", "td", "th", "tr", "h1", "h2", "h3", "section", "article", "summary", "details", "figure", "figcaption", "ul", "ol", "table", "h4", "blockquote", "header", "footer", "label", "br", "dl", "dt", "dd"}


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
    scripts_by_id: dict[str, str] = field(default_factory=dict)
    body_text: str = ""


class _Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doc = Doc()
        self.stack: list[tuple[str, str | None, str | None]] = []  # (tag, section_id, container_id)
        self.raw_tag: str | None = None
        self.script_id: str | None = None

    def _context(self) -> tuple[str | None, str | None]:
        if not self.stack:
            return None, None
        _, sec, con = self.stack[-1]
        return sec, con

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        sec, con = self._context()
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
        if el_id and classes & CONTAINER_CLASSES:
            self.doc.containers[el_id] = Container(el_id, classes, a, sec)
            con = el_id
        if tag == "a" and "href" in a:
            self.doc.hrefs.append(a["href"])
            if con is not None:
                self.doc.containers[con].hrefs.append(a["href"])
        if tag == "script" and a.get("src"):
            self.doc.external_resources.append(a["src"])
        if tag == "link" and "stylesheet" in a.get("rel", "") and a.get("href"):
            self.doc.external_resources.append(a["href"])
        if tag in ("script", "style"):
            self.raw_tag = tag
            self.script_id = el_id if tag == "script" else None
            if self.script_id:
                self.doc.scripts_by_id[self.script_id] = ""
        if tag in BLOCK_TAGS:
            self.handle_data("\n")
        if tag not in VOID_TAGS:
            self.stack.append((tag, sec, con))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.raw_tag = None
            self.script_id = None
        if tag in BLOCK_TAGS:
            self.handle_data("\n")
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
            return
        sec, con = self._context()
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


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    status = 0
    for name in argv:
        path = Path(name)
        doc = parse_file(path)
        problems = [f"duplicate id: {i}" for i in sorted(doc.duplicate_ids)]
        problems += math_delimiter_errors(doc.body_text)
        problems += [f"broken link: {h}" for h in broken_links(doc, path.parent)]
        print(f"{path}: {'OK' if not problems else 'FAIL'}")
        for problem in problems:
            print(f"  - {problem}")
        status |= int(bool(problems))
    return status


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    sys.exit(main())
