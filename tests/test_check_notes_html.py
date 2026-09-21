#!/usr/bin/env python3
"""Unit tests for scripts/check_notes_html.py."""

from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from check_notes_html import broken_links, math_delimiter_errors, parse_file, parse_html  # noqa: E402

FIXTURE = """<!DOCTYPE html>
<html lang="ko"><head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<style>.x{color:red}</style>
</head><body>
<section id="s1"><h2>제목</h2>
  <article class="topic" id="s1-a"><h3>토픽</h3>
    <div class="layer eli5"><p>비유 $a$ <br> 문장</p><svg id="fig-a"><path d="M0 0"/></svg></div>
    <div class="layer formal">$$x^2$$ <a href="#s1">위로</a></div>
  </article>
</section>
<section id="s2"><p>둘째 섹션</p></section>
<script id="widget-math">function f(){ return `${1}`; }</script>
</body></html>"""


class TestParse(unittest.TestCase):
    def setUp(self):
        self.doc = parse_html(FIXTURE)

    def test_lang_and_ids(self):
        self.assertEqual(self.doc.lang, "ko")
        self.assertTrue({"s1", "s1-a", "fig-a", "s2", "widget-math"} <= self.doc.ids)
        self.assertEqual(self.doc.duplicate_ids, set())

    def test_id_section_mapping(self):
        self.assertEqual(self.doc.id_section["fig-a"], "s1")
        self.assertEqual(self.doc.id_section["s1-a"], "s1")

    def test_section_text_and_container(self):
        self.assertIn("비유", self.doc.section_text["s1"])
        self.assertIn("둘째 섹션", self.doc.section_text["s2"])
        con = self.doc.containers["s1-a"]
        self.assertEqual(con.section, "s1")
        self.assertIn("문장", con.text)
        self.assertTrue({"layer", "eli5", "formal"} <= con.child_classes)
        self.assertEqual(con.hrefs, ["#s1"])

    def test_scripts_and_styles_excluded_from_text(self):
        self.assertNotIn("return", self.doc.body_text)
        self.assertNotIn("color:red", self.doc.body_text)
        self.assertIn("function f()", self.doc.scripts_by_id["widget-math"])

    def test_external_resources(self):
        self.assertEqual(len(self.doc.external_resources), 2)

    def test_duplicate_ids_detected(self):
        doc = parse_html('<div id="a"></div><p id="a"></p>')
        self.assertEqual(doc.duplicate_ids, {"a"})


class TestMathDelimiters(unittest.TestCase):
    def test_balanced(self):
        self.assertEqual(math_delimiter_errors("a $x$ b $$y$$ c \\$5"), [])

    def test_unbalanced_inline(self):
        self.assertEqual(math_delimiter_errors("a $x b"), ["unbalanced $ (inline math)"])

    def test_unbalanced_display(self):
        self.assertIn("unbalanced $$ (display math)", math_delimiter_errors("$$x"))


class TestBrokenLinks(unittest.TestCase):
    def test_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "sub dir").mkdir()
            (base / "sub dir" / "b.html").write_text('<p id="there"></p>', encoding="utf-8")
            a = base / "a.html"
            a.write_text(
                '<p id="here"></p>'
                '<a href="#here"></a><a href="#nope"></a>'
                '<a href="sub%20dir/b.html#there"></a><a href="sub%20dir/b.html#gone"></a>'
                '<a href="missing.html"></a><a href="https://example.com"></a>',
                encoding="utf-8",
            )
            broken = broken_links(parse_file(a), base)
            self.assertEqual(broken, ["#nope", "sub%20dir/b.html#gone", "missing.html"])


if __name__ == "__main__":
    unittest.main()
