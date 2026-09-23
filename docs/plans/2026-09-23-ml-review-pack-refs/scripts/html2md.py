#!/usr/bin/env python3
r"""정리노트/복습문제 HTML → GitHub 마크다운 변환기 (표준 라이브러리만 사용).

- 본문, 수식($...$ / $$...$$), 목록, 표, 인용을 변환한다.
- <details>(원문/힌트/풀이)는 접히는 HTML <details>로 남긴다.
- 인라인 SVG 그림은 figures_<range>/ 에 스타일을 인라인한 독립 SVG로 내보낸다.
- 위젯은 .widget-static(정적 SVG·표)으로 대체한다. 없으면 "HTML 버전에서 조작" 안내만 남긴다.
- 표 안 수식의 \| 는 \Vert, | 는 \vert 로 바꾼다(GFM 표 구분자 충돌 방지).
CLI:
  html2md.py NOTE.html REVIEW.html            # 같은 폴더에 .md 두 개 + figures_<range>/
  html2md.py NOTE.html REVIEW.html --check    # 변환 후 누락 검사(수식·앵커·그림·링크)
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
NAME_RE = re.compile(r"^(정리노트|복습문제)_(\d{4}(?:-\d{4})?)_([A-Za-z0-9_]+)\.html$")
FONT = "-apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
LIGHT = {"ink": "#1b2130", "ink-2": "#4a5468", "line": "#dde2ea", "accent": "#2f6fdb", "warn": "#b54708",
         "prof": "#6941c6", "supp": "#067647", "danger": "#d92d20", "surface": "#ffffff"}
SVG_CSS = f"""
svg {{ color: {LIGHT['ink']}; font-family: {FONT}; }}
.fig-ink {{ stroke: {LIGHT['ink']}; fill: none; stroke-width: 2; }}
.fig-accent {{ stroke: {LIGHT['accent']}; fill: none; stroke-width: 2.5; }}
.fig-danger {{ stroke: {LIGHT['danger']}; fill: none; stroke-width: 2.5; }}
.fig-dot {{ fill: {LIGHT['accent']}; }}
.fig-text {{ fill: {LIGHT['ink']}; font-size: 13px; }}
.fig-muted {{ fill: {LIGHT['ink-2']}; font-size: 12px; }}
.axis {{ stroke: {LIGHT['line']}; stroke-width: 1.5; }}
.tick {{ fill: {LIGHT['ink-2']}; font-size: 11px; }}
.plot-truth {{ fill: none; stroke: {LIGHT['ink-2']}; stroke-width: 1.5; stroke-dasharray: 5 4; }}
.plot-fit {{ fill: none; stroke: {LIGHT['accent']}; stroke-width: 2.5; }}
.pt-train {{ fill: {LIGHT['accent']}; }}
.pt-test {{ fill: {LIGHT['warn']}; }}
.mark-ml {{ stroke: {LIGHT['accent']}; stroke-width: 1.5; stroke-dasharray: 3 3; }}
.mark-map {{ stroke: {LIGHT['supp']}; stroke-width: 1.5; stroke-dasharray: 3 3; }}
.plot-like {{ fill: none; stroke: {LIGHT['accent']}; stroke-width: 2; }}
.plot-prior {{ fill: none; stroke: {LIGHT['prof']}; stroke-width: 2; stroke-dasharray: 6 4; }}
.plot-post {{ fill: none; stroke: {LIGHT['supp']}; stroke-width: 3; }}
"""


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


class Node:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs or {}), parent, []

    @property
    def classes(self):
        return set(self.attrs.get("class", "").split())

    def find_all(self, pred):
        for c in self.children:
            if isinstance(c, Node):
                if pred(c):
                    yield c
                yield from c.find_all(pred)

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, [(k, v or "") for k, v in attrs], self.cur)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, [(k, v or "") for k, v in attrs], self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def serialize(node):
    if isinstance(node, str):
        return html.escape(node, quote=False)
    attrs = "".join(f' {k}="{html.escape(v)}"' for k, v in node.attrs.items())
    if not node.children and node.tag not in ("text",):
        return f"<{node.tag}{attrs}/>"
    return f"<{node.tag}{attrs}>" + "".join(serialize(c) for c in node.children) + f"</{node.tag}>"


# ---------------------------------------------------------------- inline

MATH_RE = re.compile(r"(\$\$.*?\$\$|\$[^$]+?\$)", re.S)


def escape_text(s):
    """Escape markdown-sensitive chars outside math."""
    parts = MATH_RE.split(s)
    out = []
    for i, p in enumerate(parts):
        if i % 2:  # math
            out.append(p)
        else:
            p = p.replace("<", "&lt;").replace(">", "&gt;")
            p = re.sub(r"(?<![\\*])\*(?!\*)", r"\\*", p)  # lone asterisks
            out.append(p)
    return "".join(out)


class Ctx:
    def __init__(self, link_map, fig_dir_abs, fig_dir_name):
        self.link_map, self.fig_dir_abs, self.fig_dir_name, self.figs = link_map, fig_dir_abs, fig_dir_name, []


def fix_href(href, ctx):
    for old, new in ctx.link_map:
        if href.startswith(old):
            return new + href[len(old):]
    return href


def inline(node, ctx):
    if isinstance(node, str):
        return escape_text(re.sub(r"\s+", " ", node))
    t, cls = node.tag, node.classes
    inner = lambda: "".join(inline(c, ctx) for c in node.children)
    if t in ("script", "style", "svg", "input", "nav"):
        return ""
    if t == "br":
        return "<br>"
    if t in ("b", "strong"):
        s = inner().strip()
        return f"**{s}**" if s else ""
    if t in ("i", "em"):
        s = inner().strip()
        return f"*{s}*" if s else ""
    if t == "code":
        return f"`{node.text()}`"
    if t in ("sub", "sup"):
        return f"<{t}>{inner().strip()}</{t}>"
    if t == "a":
        return f"[{inner().strip()}]({fix_href(node.attrs.get('href', ''), ctx)})"
    if t == "span" and ("layer-title" in cls or "badge" in cls):
        return f"**{inner().strip()}**"
    if t == "span" and cls & {"sw"}:
        return ""
    return inner()


# ---------------------------------------------------------------- blocks

BLOCK = {"p", "div", "section", "article", "main", "ul", "ol", "li", "table", "blockquote", "figure", "details",
         "h1", "h2", "h3", "h4", "header", "footer", "label", "figcaption", "summary", "thead", "tbody", "tr", "svg",
         "nav", "hr"}


def is_block(n):
    return isinstance(n, Node) and n.tag in BLOCK


def para(text):
    """Turn an inline string into markdown lines, lifting $$...$$ onto their own lines."""
    text = text.strip()
    if not text:
        return []
    lines = []
    for i, seg in enumerate(re.split(r"(\$\$.*?\$\$)", text, flags=re.S)):
        seg = seg.strip()
        if not seg:
            continue
        if i % 2:
            lines += ["", "$$", seg[2:-2].strip(), "$$", ""]
        else:
            lines.append(seg)
    # collapse leading/trailing blanks
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def join_blocks(blocks):
    out = []
    for b in blocks:
        if not b:
            continue
        if out:
            out.append("")
        out.extend(b)
    return out


def children_blocks(node, ctx):
    blocks, buf = [], []

    def flush():
        if buf:
            blocks.append(para("".join(buf)))
            buf.clear()

    for c in node.children:
        if is_block(c):
            flush()
            blocks.append(block(c, ctx))
        else:
            buf.append(inline(c, ctx))
    flush()
    return join_blocks(blocks)


def render_list(node, ctx, ordered):
    lines, n = [], 0
    for li in node.children:
        if not (isinstance(li, Node) and li.tag == "li"):
            continue
        n += 1
        marker = f"{n}. " if ordered else "- "
        body = children_blocks(li, ctx) or [""]
        pad = " " * len(marker)
        lines.append(marker + body[0])
        for l in body[1:]:
            lines.append(pad + l if l else "")
    return lines


def cell(node, ctx):
    s = "".join(inline(c, ctx) if not is_block(c) else " ".join(children_blocks(c, ctx)) for c in node.children)
    s = re.sub(r"\$\$(.*?)\$\$", r"$\1$", s.strip(), flags=re.S)
    parts = MATH_RE.split(s)
    fixed = []
    for i, p in enumerate(parts):
        if i % 2:
            fixed.append(p.replace("\\|", "\\Vert ").replace("|", "\\vert "))
        else:
            fixed.append(p.replace("|", "\\|"))
    return "".join(fixed).replace("\n", " ")


def render_table(node, ctx):
    rows = list(node.find_all(lambda n: n.tag == "tr"))
    grid = [[cell(c, ctx) for c in r.children if isinstance(c, Node) and c.tag in ("td", "th")] for r in rows]
    width = max(len(r) for r in grid)
    grid = [r + [""] * (width - len(r)) for r in grid]
    head = grid[0]
    lines = ["| " + " | ".join(h or " " for h in head) + " |", "|" + "---|" * width]
    lines += ["| " + " | ".join(c for c in r) + " |" for r in grid[1:]]
    return lines


def export_svg(svg, ctx, name=None):
    sid = name or svg.attrs.get("id") or f"fig-auto-{len(ctx.figs) + 1}"
    vb = svg.attrs.get("viewBox", "0 0 600 300").split()
    w, h = vb[2], vb[3]
    body = "".join(serialize(c) for c in svg.children)
    attrs = {k: v for k, v in svg.attrs.items() if k not in ("id", "class")}
    attr_s = "".join(f' {k}="{html.escape(v)}"' for k, v in attrs.items())
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"{attr_s}>'
           f"<style>{SVG_CSS}</style>"
           f'<rect x="{vb[0]}" y="{vb[1]}" width="{w}" height="{h}" rx="10" fill="{LIGHT["surface"]}"/>'
           f"{body}</svg>\n")
    fname = f"{sid}.svg"
    with open(os.path.join(ctx.fig_dir_abs, fname), "w", encoding="utf-8") as f:
        f.write(doc)
    ctx.figs.append(fname)
    return f"{ctx.fig_dir_name}/{fname}"


def render_widget(node, ctx):
    wid = node.attrs.get("id")
    static = next(node.find_all(lambda n: "widget-static" in n.classes), None)
    note = " *(정적 스냅샷 — 직접 조작은 HTML 버전)*" if static else " *(인터랙티브 — HTML 버전에서 조작)*"
    lines = []
    for c in node.children:
        if not isinstance(c, Node):
            continue
        if c.tag == "h4":
            if wid:
                lines += ["", f'<a id="{wid}"></a>']
            lines += ["", "#### " + "".join(inline(x, ctx) for x in c.children).strip() + note]
        elif c.tag == "p" and "legend" in c.classes:
            parts = [inline(x, ctx).strip() for x in c.children]
            lines += ["", "범례: " + " · ".join(x for x in parts if x)]
        elif c.tag == "p":
            lines += [""] + para("".join(inline(x, ctx) for x in c.children))
    if static:
        lines += [""] + children_blocks(static, ctx)
    return lines


def heading(level, node, ctx, anchor=None):
    text = "".join(inline(c, ctx) for c in node.children).strip()
    out = []
    if anchor:
        out.append(f'<a id="{anchor}"></a>')
        out.append("")
    out.append("#" * level + " " + text)
    return out


def block(node, ctx):
    t, cls = node.tag, node.classes
    if t in ("nav", "script", "style") or "topbar" in cls or "progress" in cls:
        return []
    if t in ("h1", "h2", "h3", "h4"):
        anchor = node.attrs.get("id")
        if t in ("h2", "h3") and node.parent is not None and node.parent.attrs.get("id") and node.parent.tag in ("section", "article"):
            anchor = node.parent.attrs["id"]
        return heading(int(t[1]), node, ctx, anchor)
    if t in ("ul", "ol"):
        items = [c for c in node.children if isinstance(c, Node) and c.tag == "li"]
        lettered = items and all(re.match(r"\s*\([a-z]\)", c.text()) for c in items)
        return render_list(node, ctx, t == "ol" and not lettered)
    if t == "table":
        return render_table(node, ctx)
    if t == "blockquote":
        body = children_blocks(node, ctx)
        return ["> " + l if l else ">" for l in body]
    if t == "figure":
        svg = next(node.find_all(lambda n: n.tag == "svg"), None)
        cap = next(node.find_all(lambda n: n.tag == "figcaption"), None)
        alt = (svg.attrs.get("aria-label", "그림") if svg else "그림").replace("[", "(").replace("]", ")")
        lines = [f"![{alt}]({export_svg(svg, ctx)})"] if svg else []
        if cap:
            lines += ["", "*" + "".join(inline(c, ctx) for c in cap.children).strip() + "*"]
        return lines
    if t == "svg":
        return [f"![{node.attrs.get('aria-label', '그림')}]({export_svg(node, ctx)})"]
    if t == "p" and "answer" in cls:
        lines = para("".join(inline(c, ctx) for c in node.children))
        if lines:
            lines[0] = re.sub(r"^정답:", "**✅ 정답:**", lines[0])
        return lines
    if t == "details":
        summary = next((c for c in node.children if isinstance(c, Node) and c.tag == "summary"), None)
        stext = "".join(inline(c, ctx) for c in summary.children).strip() if summary else "펼치기"
        rest = Node("div")
        rest.children = [c for c in node.children if c is not summary]
        body = children_blocks(rest, ctx)
        return [f"<details><summary>{stext}</summary>", ""] + body + ["", "</details>"]
    if t == "summary":
        return []
    if t == "label" and "done" in cls:
        return ["- [ ] 풀었음"]
    if t == "div" and "widget" in cls:
        return render_widget(node, ctx)
    if t == "div" and "legend-bar" in cls:
        parts = ["".join(inline(c, ctx) for c in x.children).strip() for x in node.children if isinstance(x, Node)]
        return ["범례: " + " · ".join(p for p in parts if p)]
    if t == "div" and "tags" in cls:
        parts = ["".join(inline(c, ctx) for c in s.children).strip() for s in node.children if isinstance(s, Node)]
        return ["*" + " · ".join(p for p in parts if p) + "*"]
    if t == "header" and "card-head" in cls:
        parts = ["".join(inline(c, ctx) for c in s.children).strip() for s in node.children if isinstance(s, Node)]
        return ["**" + " · ".join(p for p in parts if p) + "**"]
    if t == "div" and "layer" in cls:
        return children_blocks(node, ctx)
    if t == "article" and "card" in cls:
        kids = [c for c in node.children if isinstance(c, Node)]
        head = [c for c in kids if c.tag == "header"]
        h3 = [c for c in kids if c.tag == "h3"]
        reordered = Node("article", node.attrs)
        reordered.children = h3 + head + [c for c in node.children if not (isinstance(c, Node) and (c in head or c in h3))]
        for c in reordered.children:
            if isinstance(c, Node):
                c.parent = reordered
        return children_blocks(reordered, ctx) + ["", "---"]
    if t == "article":
        anchor_done = any(isinstance(c, Node) and c.tag == "h3" for c in node.children)
        body = children_blocks(node, ctx)
        if not anchor_done and node.attrs.get("id"):
            body = [f'<a id="{node.attrs["id"]}"></a>', ""] + body
        return body + ["", "---"]
    if t == "section":
        body = children_blocks(node, ctx)
        if not any(isinstance(c, Node) and c.tag == "h2" for c in node.children) and node.attrs.get("id"):
            body = [f'<a id="{node.attrs["id"]}"></a>', ""] + body
        return body
    if t == "footer":
        return ["---", ""] + children_blocks(node, ctx)
    if t == "hr":
        return ["---"]
    return children_blocks(node, ctx)


def toc(body_node, ctx):
    lines = ["**목차**", ""]
    for sec in body_node.find_all(lambda n: n.tag == "section" and n.attrs.get("id")):
        h2 = next((c for c in sec.children if isinstance(c, Node) and c.tag == "h2"), None)
        if not h2:
            continue
        lines.append(f"- [{h2.text().strip()}](#{sec.attrs['id']})")
        for art in sec.children:
            if isinstance(art, Node) and art.tag == "article" and art.attrs.get("id"):
                h3 = next((c for c in art.children if isinstance(c, Node) and c.tag == "h3"), None)
                if h3:
                    lines.append(f"  - [{h3.text().strip()}](#{art.attrs['id']})")
    return lines


def convert(path, out_path, ctx, intro):
    b = Builder()
    b.feed(_read(path))
    body = next(b.root.find_all(lambda n: n.tag == "body"))
    main = next(body.find_all(lambda n: n.tag == "main"))
    hero = next(main.find_all(lambda n: "hero" in n.classes))
    footer = next(body.find_all(lambda n: n.tag == "footer"), None)
    parts = [block(hero, ctx), intro, toc(main, ctx)]
    for c in main.children:
        if isinstance(c, Node) and c is not hero:
            parts.append(block(c, ctx))
    if footer:
        parts.append(block(footer, ctx))
    lines = join_blocks(parts)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).replace("---\n\n---", "---")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text.strip() + "\n")


MD_MATH_RE = re.compile(r"\$\$.*?\$\$|\$[^$]+?\$", re.S)
SKIP_CHECK = {"script", "style", "svg", "nav"}
SKIP_CHECK_CLASSES = {"controls", "topbar"}


def _norm_math(s):
    s = s.replace("\\Vert", "\\|").replace("\\vert", "|")
    return re.sub(r"[\s$]", "", s)


def html_math_and_ids(path):
    """HTML 본문(스크립트·SVG·위젯 조작부 제외)의 수식 토큰과 앵커 대상 id."""
    b = Builder()
    b.feed(_read(path))
    body = next(b.root.find_all(lambda n: n.tag == "body"))
    texts, ids = [], []

    def walk(n):
        if isinstance(n, str):
            texts.append(n)
            return
        if n.tag in SKIP_CHECK or n.classes & SKIP_CHECK_CLASSES:
            return
        if n.tag in BLOCK or n.tag in ("td", "th", "br"):
            texts.append("\n")
        if n.attrs.get("id") and (n.tag in ("section", "article") or "widget" in n.classes):
            ids.append(n.attrs["id"])
        for c in n.children:
            walk(c)
        if n.tag in BLOCK or n.tag in ("td", "th"):
            texts.append("\n")

    walk(body)
    return MD_MATH_RE.findall("".join(texts)), ids


def check_md(html_path, md_path):
    """변환 결과 검사. 문제 문자열 목록을 돌려준다(빈 목록이면 통과)."""
    md = _read(md_path)
    md_dir = os.path.dirname(os.path.abspath(md_path))
    problems = []
    md_norm = _norm_math(md)
    maths, ids = html_math_and_ids(html_path)
    problems += [f"수식 누락: {m[:60]}" for m in maths if _norm_math(m) not in md_norm]
    anchors = set(re.findall(r'<a id="([^"]+)"></a>', md))
    problems += [f"앵커 누락: {i}" for i in ids if i not in anchors]
    for img in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", md):
        if not os.path.exists(os.path.join(md_dir, img)):
            problems.append(f"그림 없음: {img}")
    for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", md):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        path_part, _, frag = target.partition("#")
        if not path_part:
            if frag not in anchors:
                problems.append(f"링크 앵커 없음: {target}")
            continue
        if not path_part.endswith(".md"):
            continue
        other = os.path.join(md_dir, path_part)
        if not os.path.exists(other):
            problems.append(f"링크 파일 없음: {target}")
        elif frag and f'<a id="{frag}"></a>' not in _read(other):
            problems.append(f"링크 앵커 없음: {target}")
    return problems


def convert_pack(note_path, review_path):
    """두 HTML을 같은 폴더에 .md로 변환한다. (md 경로 두 개, 그림 파일 수)를 돌려준다."""
    out_dir = os.path.dirname(os.path.abspath(note_path))
    names = [os.path.basename(note_path), os.path.basename(review_path)]
    matches = [NAME_RE.match(n) for n in names]
    if not all(matches) or matches[0].group(1) != "정리노트" or matches[1].group(1) != "복습문제":
        raise ValueError(f"파일명 규칙 위반: {names}")
    if os.path.dirname(os.path.abspath(review_path)) != out_dir:
        raise ValueError("두 HTML은 같은 폴더에 있어야 함")
    fig_name = f"figures_{matches[0].group(2)}"
    fig_abs = os.path.join(out_dir, fig_name)
    os.makedirs(fig_abs, exist_ok=True)
    link_map = [(n, n[:-5] + ".md") for n in names]
    intros = [
        [f"> 이 문서는 `{names[0]}`의 마크다운 버전입니다. 그림은 `{fig_name}/` 폴더의 SVG로, "
         "인터랙티브 위젯은 정적 스냅샷으로 옮겼습니다. 수식은 `$…$` / `$$…$$` (GitHub, Obsidian, Typora 등에서 렌더링) 입니다."],
        [f"> 이 문서는 `{names[1]}`의 마크다운 버전입니다. "
         "📖 원문 · 💡 힌트 · ✅ 풀이는 접혀 있으니 먼저 스스로 풀어 본 뒤 펼치세요."],
    ]
    outs, fig_count = [], 0
    for name, intro in zip(names, intros):
        ctx = Ctx(link_map, fig_abs, fig_name)
        out = os.path.join(out_dir, name[:-5] + ".md")
        convert(os.path.join(out_dir, name), out, ctx, intro)
        outs.append(out)
        fig_count += len(ctx.figs)
    return outs, fig_count


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("note")
    ap.add_argument("review")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    outs, fig_count = convert_pack(args.note, args.review)
    for out in outs:
        print(out)
    print(f"figures: {fig_count}")
    if not args.check:
        return 0
    problems = []
    for html_path, md_path in zip((args.note, args.review), outs):
        problems += [f"{os.path.basename(md_path)}: {p}" for p in check_md(html_path, md_path)]
    for p in problems:
        print(p)
    print("OK" if not problems else f"FAIL ({len(problems)})")
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
