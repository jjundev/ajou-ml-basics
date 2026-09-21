#!/usr/bin/env python3
"""Unit tests for scripts/review_answers.py (복습문제 정답 키)."""

from fractions import Fraction as F
from pathlib import Path
import math
import sys
import unittest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from review_answers import (  # noqa: E402
    beta_bernoulli_posterior,
    coin_estimates,
    ex61_conditionals,
    ex61_marginals,
    ex64_bag2_given_mango,
    ex71_stationary_points,
    map_l2_lambda,
)


class TestExercise61(unittest.TestCase):
    def test_marginals(self):
        px, py = ex61_marginals()
        self.assertEqual(px, [F(16, 100), F(17, 100), F(11, 100), F(22, 100), F(34, 100)])
        self.assertEqual(py, [F(26, 100), F(47, 100), F(27, 100)])
        self.assertEqual(sum(px), 1)
        self.assertEqual(sum(py), 1)

    def test_conditionals(self):
        x_given_y1, y_given_x3 = ex61_conditionals()
        self.assertEqual(x_given_y1, [F(1, 26), F(1, 13), F(3, 26), F(5, 13), F(5, 13)])
        self.assertEqual(y_given_x3, [F(3, 11), F(5, 11), F(3, 11)])


class TestExercise64(unittest.TestCase):
    def test_bayes_bag2(self):
        self.assertEqual(ex64_bag2_given_mango(), F(1, 3))


class TestBetaBernoulli(unittest.TestCase):
    def test_posterior_parameters(self):
        self.assertEqual(beta_bernoulli_posterior(4, 4, 10, 2), (6, 12))

    def test_class_coin_example(self):
        ml, map_, pred = coin_estimates(10, 2, 4, 4)
        self.assertEqual(ml, F(1, 5))
        self.assertEqual(map_, F(5, 16))
        self.assertEqual(pred, F(1, 3))

    def test_uniform_prior_map_equals_ml(self):
        ml, map_, _ = coin_estimates(10, 2, 1, 1)
        self.assertEqual(map_, ml)


class TestExercise71(unittest.TestCase):
    def test_stationary_points(self):
        pts = ex71_stationary_points()
        self.assertEqual(len(pts), 2)
        (x1, k1), (x2, k2) = pts
        self.assertAlmostEqual(x1, -2 - math.sqrt(5))
        self.assertEqual(k1, "max")
        self.assertAlmostEqual(x2, -2 + math.sqrt(5))
        self.assertEqual(k2, "min")


class TestMapL2(unittest.TestCase):
    def test_lambda(self):
        self.assertEqual(map_l2_lambda(1, F(1, 2), 10), F(1, 5))


if __name__ == "__main__":
    unittest.main()
