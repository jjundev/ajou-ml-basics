"""노트·복습문제 템플릿의 테마 스크롤바(토큰 3블록 + 규칙)를 지킨다."""

import re
import unittest

from _util import SKILL

TEMPLATES = ("note-template.html", "review-template.html")
LIGHT = "--scroll: #c9d0db; --scroll-hover: #9aa3b2;"
DARK = "--scroll: #3f414b; --scroll-hover: #5b5e6a;"


class TestScrollbarTheme(unittest.TestCase):
    def test_tokens_in_every_theme_block(self):
        for name in TEMPLATES:
            text = (SKILL / "assets" / name).read_text(encoding="utf-8")
            with self.subTest(template=name):
                self.assertEqual(len(re.findall(r"--scroll: #[0-9a-f]{6}; --scroll-hover: #[0-9a-f]{6};", text)), 3)
                self.assertEqual(text.count(LIGHT), 1)
                self.assertEqual(text.count(DARK), 2)

    def test_rules_cover_both_scroll_containers(self):
        for name in TEMPLATES:
            text = (SKILL / "assets" / name).read_text(encoding="utf-8")
            with self.subTest(template=name):
                for needle in (
                    ".content::-webkit-scrollbar, .panel-inner::-webkit-scrollbar { width: 8px; }",
                    ".content::-webkit-scrollbar-thumb, .panel-inner::-webkit-scrollbar-thumb { background: var(--scroll);",
                    ".content::-webkit-scrollbar-thumb:hover, .panel-inner::-webkit-scrollbar-thumb:hover { background: var(--scroll-hover); }",
                    "scrollbar-color: var(--scroll) transparent;",
                ):
                    self.assertIn(needle, text)

    def test_panel_width_variable_kept(self):
        for name in TEMPLATES:
            text = (SKILL / "assets" / name).read_text(encoding="utf-8")
            with self.subTest(template=name):
                self.assertIn("--scrollbar: 16px;", text)


if __name__ == "__main__":
    unittest.main()
