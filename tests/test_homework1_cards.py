#!/usr/bin/env python3
"""Content checks for 과제/과제1/과제1_Homework1.html (과제1 카드)."""

from pathlib import Path
import html
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude/skills/ml-review-pack/scripts"))

from review_pdf_cards import read_cards  # noqa: E402
from review_pdf_types import HOMEWORK  # noqa: E402

CARDS = ROOT / "과제/과제1/과제1_Homework1.html"
MATRIX = re.compile(r"\\begin\{bmatrix\}.*?\\end\{bmatrix\}", re.S)


def matrices(fragment):
    return {re.sub(r"\s+", "", m) for m in MATRIX.findall(html.unescape(fragment))}


class TestOriginals(unittest.TestCase):
    def test_original_carries_every_given_matrix(self):
        # 조건에 준 행렬은 원문(영어 전문)에도 있어야 해요.
        for card in read_cards(CARDS, HOMEWORK).cards:
            conditions = card.statement_html.split('<div class="ask">')[0]
            with self.subTest(card=card.id):
                self.assertLessEqual(matrices(conditions), matrices(card.original_html))


if __name__ == "__main__":
    unittest.main()
