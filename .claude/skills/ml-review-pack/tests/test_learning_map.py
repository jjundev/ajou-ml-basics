"""The overview guard catches missing, hidden, and misplaced teaching introductions."""
import unittest
import _util
from check_learning_map import check_source

GOOD = '<main><section><article class="topic" id="s0-map" data-learning-map="v1"><h3>Goal</h3><div class="layer formal">' + ''.join('<p data-map="'+k+'">Readable explanation.</p>' for k in ('goal','bridge','result','formula','pitfall')) + '<table><tr><th>Choice</th></tr><tr><td>Result</td></tr></table></div></article></section></main>'
class TestLearningMap(unittest.TestCase):
    def test_complete_first_topic_passes(self):
        self.assertEqual(check_source(GOOD), [])
    def test_missing_introduction_fails(self):
        self.assertTrue(check_source('<main><article class="topic">Formula only.</article></main>'))
    def test_missing_purpose_fails(self):
        self.assertTrue(check_source(GOOD.replace('data-map="formula"','data-map="other"')))
    def test_empty_goal_fails(self):
        self.assertTrue(check_source(GOOD.replace('<p data-map="goal">Readable explanation.</p>','<p data-map="goal"></p>')))
    def test_hidden_introduction_fails(self):
        self.assertTrue(check_source(GOOD.replace('data-learning-map="v1"','data-learning-map="v1" hidden')))
    def test_late_introduction_fails(self):
        self.assertTrue(check_source(GOOD.replace('<section>','<section><article class="topic">Calculation.</article>')))
    def test_duplicate_introduction_fails(self):
        self.assertTrue(check_source(GOOD+GOOD))
