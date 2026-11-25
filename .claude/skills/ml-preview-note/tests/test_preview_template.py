"""공유 템플릿(심링크)이 예습 조립기가 기대하는 모양인지 지킨다. 복습 쪽에서 템플릿을 바꾸면 여기서 먼저 깨진다."""

import os
import re
import unittest

from _preview_util import REVIEW_SKILL, SKILL

TEMPLATE = SKILL / "assets" / "note-template.html"
SLOTS = {"BRAND", "DESCRIPTION", "FOOTER", "PAGE_TITLE", "RANGE", "SCRIPTS", "SECTIONS", "SUBTITLE", "TITLE", "TOC"}


class TestSharedTemplate(unittest.TestCase):
    def test_relative_symlink_to_review_template(self):
        self.assertTrue(TEMPLATE.is_symlink())
        self.assertEqual(os.readlink(TEMPLATE).replace(os.sep, "/"), "../../ml-review-pack/assets/note-template.html")
        self.assertEqual(TEMPLATE.resolve(), (REVIEW_SKILL / "assets" / "note-template.html").resolve())

    def test_slots(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertEqual(set(re.findall(r"\{\{([A-Z_]+)\}\}", text)), SLOTS)

    def test_layer_styles(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        for sel in (".layer.eli5", ".layer.formal", ".layer.listen", ".badge.supp"):
            with self.subTest(sel=sel):
                self.assertIn(sel, text)

    def test_themed_scrollbar_tokens_and_rules(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"--scroll: #[0-9a-f]{6}; --scroll-hover: #[0-9a-f]{6};", text)), 3)
        for needle in ("--scroll: #c9d0db; --scroll-hover: #9aa3b2;", "--scroll: #3f414b; --scroll-hover: #5b5e6a;",
                       ".content::-webkit-scrollbar-thumb, .panel-inner::-webkit-scrollbar-thumb { background: var(--scroll);",
                       "scrollbar-color: var(--scroll) transparent;"):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
