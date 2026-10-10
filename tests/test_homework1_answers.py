#!/usr/bin/env python3
"""Unit tests for scripts/homework1_answers.py (과제1 정답 키)."""

from fractions import Fraction as F
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from homework1_answers import (  # noqa: E402
    P22, bm, col, det, fr, inv, key, main, mat, missing, p17_ml, p19_map, p23, p24, p25,
)

CARD = (
    '<article class="card" id="p4" data-source="HW1 Problem 4"><h3>P4. t</h3>'
    '<div class="problem"><div class="conditions">c</div><div class="ask">a</div></div>'
    '<details class="original"><summary>o</summary>x</details><details class="hint"><summary>h</summary>y</details>'
    '<details class="solution"><summary>s</summary><ol class="steps"><li>z</li></ol>'
    '<p class="answer">$\\det(\\mathbf{A})=10$, $\\det(\\mathbf{B})=6$, $\\det(\\mathbf{C})=-6$, $\\det(\\mathbf{D})=0$</p>'
    '</details></article>'
)


class TestFormat(unittest.TestCase):
    def test_fr(self):
        self.assertEqual(fr(3), '3')
        self.assertEqual(fr(F(-4, 5)), '-\\frac{4}{5}')

    def test_bm_column(self):
        self.assertEqual(bm(col(1, F(1, 3))), '\\begin{bmatrix}1\\\\\\frac{1}{3}\\end{bmatrix}')


class TestValues(unittest.TestCase):
    def test_linear_algebra(self):
        self.assertEqual(det(mat([[1, 3, 5], [2, 4, 6], [0, 2, 4]])), 0)
        self.assertEqual(inv(mat([[1, -2], [3, 1]])), mat([[F(1, 7), F(2, 7)], [F(-3, 7), F(1, 7)]]))

    def test_regression(self):
        self.assertEqual(p17_ml(), col(F(7, 3), 1))
        self.assertEqual(p19_map(1), col(F(7, 4), F(2, 3)))
        self.assertEqual(p19_map(F(1, 4)), col(1, F(1, 3)))
        self.assertEqual(p23(), (F(8, 5), F(4, 3)))
        self.assertEqual(p24(), (3, F(5, 2)))

    def test_gaussian(self):
        mu, s = p25()
        self.assertEqual(mu, col(F(3, 11), F(4, 11)))
        self.assertEqual(s, mat([[F(7, 11), F(2, 11)], [F(2, 11), F(10, 11)]]))
        self.assertEqual(P22['c'][1], mat([[8, 0], [0, 4]]))


class TestMissing(unittest.TestCase):
    def test_all_25_keys(self):
        self.assertEqual(sorted(key(), key=lambda p: int(p[1:])), [f'p{i}' for i in range(1, 26)])

    def test_entity_and_whitespace_normalized(self):
        answers = {
            'p4': '정답: $\\det(\\mathbf{A}) = 10$, $\\det(\\mathbf{B})=6$, $\\det(\\mathbf{C})=-6$, $\\det(\\mathbf{D})=0$',
            'p21': '$\\bar{\\mathbf{x}}=\\begin{bmatrix} 2 \\\\ 3 \\end{bmatrix}$, '
                   '$\\mathbf{S}=\\begin{bmatrix}1 &amp; 1\\\\ 1 &amp; 2\\end{bmatrix}$',
        }
        out = missing(answers)
        self.assertEqual([m for m in out if m.startswith(('p4:', 'p21:'))], [])
        self.assertIn('p1: no card', out)

    def test_wrong_value_reported(self):
        self.assertIn('p4: missing \\det(\\mathbf{A})=10', missing({'p4': '$\\det(\\mathbf{A})=11$'}))

    def test_main_reads_homework_cards(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / '과제1_Test.html'
            p.write_text(f'<section id="hw1">{CARD}</section>', encoding='utf-8')
            self.assertEqual(main([str(p), 'p4']), 0)
            self.assertEqual(main([str(p)]), 1)


if __name__ == '__main__':
    unittest.main()
