#!/usr/bin/env python3
"""Content checks for 과제/과제1/과제1_Homework1.html (과제1 카드)."""

from pathlib import Path
import html
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude/skills/ml-review-pack/scripts"))

from review_pdf_cards import normalize_cards, read_cards  # noqa: E402
from review_pdf_payload import has_top_level_relation, to_workbook  # noqa: E402
from review_pdf_types import HOMEWORK  # noqa: E402

CARDS = ROOT / "과제/과제1/과제1_Homework1.html"
PART_OPEN = '<div class="part">'
TALL_OPEN = '<span style="display:inline-block;margin:.8mm 0">'
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

    def test_original_has_no_problem_number(self):
        # 문제 번호는 페이지 상단과 출처에 이미 있어요.
        for card in read_cards(CARDS, HOMEWORK).cards:
            with self.subTest(card=card.id):
                self.assertNotRegex(card.original_html, r"Problem \d+")

    def test_each_part_starts_a_new_line(self):
        # 소문항 표지 (a)~(e)는 문장 첫머리에 올 때 위 여백을 둔 새 블록에서 시작해요. "part (a)"처럼 가리키는 말은 빼요.
        parts = 0
        for card in read_cards(CARDS, HOMEWORK).cards:
            markers = re.findall(r"(.{0,60})\(([a-e])\) ", card.original_html)
            with self.subTest(card=card.id):
                for before, letter in markers:
                    if before.endswith("part "):
                        continue
                    parts += 1
                    self.assertTrue(before.endswith(PART_OPEN), (letter, before))
        self.assertEqual(parts, 39)

    def test_cards_carry_no_inline_styles(self):
        # 여백은 PDF 변환기(space_math)가 넣어요. 카드는 내용만 담아요.
        self.assertNotIn("style=", CARDS.read_text(encoding="utf-8"))

    def test_pdf_payload_spaces_tall_math(self):
        # 변환 결과에서 연달은 display 식이 붙어 있지 않고, 문장 속 행렬은 여백 블록에 들어가요.
        problems = normalize_cards(read_cards(CARDS, HOMEWORK), None, CARDS)
        items = to_workbook(problems, {}, "answers", profile=HOMEWORK)["problems"]
        fields = [f for it in items for f in (*it["html"].values(), it["solution"]["answer"], *(s["html"] for s in it["solution"]["steps"]))]
        for f in fields:
            self.assertNotRegex(f, r"\$\$\s*\$\$")
        text = "".join(fields)
        wrapped = 0
        for m in re.finditer(r"\$\$[\s\S]+?\$\$|\$[^$]+?\$", text):
            tex = m.group(0)
            if tex.startswith("$$") or r"\begin{" not in tex:
                continue
            if len(tex) - 2 > 40 and has_top_level_relation(tex[1:-1]):
                continue  # 템플릿이 display로 바꿔 줄을 나눠요.
            with self.subTest(tex=tex[:50]):
                self.assertTrue(text[: m.start()].endswith(TALL_OPEN))
            wrapped += 1
        self.assertGreater(wrapped, 50)
        self.assertEqual(text.count('<div class="part" style="margin-top:1.6mm">'), 39)

    def test_every_card_has_short_hint(self):
        for card in read_cards(CARDS, HOMEWORK).cards:
            with self.subTest(card=card.id):
                self.assertTrue(card.hint_label)


if __name__ == "__main__":
    unittest.main()
