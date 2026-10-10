import hashlib
import tempfile
import unicodedata
import unittest
from pathlib import Path
from _util import FIXTURES
from review_pdf_cards import read_cards, normalize_cards
from review_pdf_types import HOMEWORK, REVIEW, ReviewPdfError

SOURCE = FIXTURES / 'pdf/복습문제_0101_Pdf_Test.html'
HW_SOURCE = FIXTURES / 'pdf/과제9_Pdf_Test.html'
class TestCards(unittest.TestCase):
    def test_preserves_entity_tex_and_step_order(self):
        pack = read_cards(SOURCE)
        self.assertEqual([c.id for c in pack.cards], ['p1','p2'])
        self.assertEqual(len(pack.cards[1].figures), 1)
        self.assertEqual(pack.cards[0].steps, ('첫 단계 $a/b$.','둘째 단계 $1/5$.'))
        self.assertIn(r'\frac{1}{5}',pack.cards[0].answer_html)
        self.assertIn('&amp;',pack.cards[0].statement_html)
        ps = normalize_cards(pack,None,SOURCE)
        self.assertIn('$a/b$',ps[0].ask_html)
        self.assertNotIn('<table',ps[1].conditions_html)
    def invalid(self, text, message):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/SOURCE.name;p.write_text(text)
            with self.assertRaisesRegex(ReviewPdfError,message):read_cards(p)
    def test_duplicate_id(self):
        self.invalid(SOURCE.read_text().replace('id="p2"','id="p1"'),'duplicate')
    def test_missing_solution(self):
        self.invalid(SOURCE.read_text().replace('class="solution"','class="missing"'),'p1.*solution')
    def test_layout_stale_source(self):
        with self.assertRaisesRegex(ReviewPdfError,'stale'):
            normalize_cards(read_cards(SOURCE),{'source_sha256':'bad','problems':{}},SOURCE)
    def test_missing_ask_and_content_loss(self):
        sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ReviewPdfError,'p1.*ask'):
            normalize_cards(read_cards(SOURCE),{'source_sha256':sha,'problems':{'p1':{'conditions_html':'x'},'p2':{}}},SOURCE)
        with self.assertRaisesRegex(ReviewPdfError,'p1.*preserv'):
            normalize_cards(read_cards(SOURCE),{'source_sha256':sha,'problems':{'p1':{'conditions_html':'changed','ask_html':'goal'},'p2':{}}},SOURCE)


class TestHomeworkProfile(unittest.TestCase):
    def write(self, d, text, name=HW_SOURCE.name):
        p=Path(d)/name;p.write_text(text,encoding='utf-8');return p
    def test_reads_homework_pack(self):
        pack=read_cards(HW_SOURCE,HOMEWORK)
        self.assertEqual((pack.range,pack.slug),('9','Pdf_Test'))
        self.assertIs(pack.profile,HOMEWORK)
        self.assertEqual([c.source for c in pack.cards],['HW9 Problem 1','HW9 Problem 2'])
    def test_default_profile_is_review(self):
        self.assertIs(read_cards(SOURCE).profile,REVIEW)
        with self.assertRaisesRegex(ReviewPdfError,'invalid review filename'):read_cards(HW_SOURCE)
    def test_homework_rejects_mml_source(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.write(d,HW_SOURCE.read_text(encoding='utf-8').replace('HW9 Problem 1','MML Example 9.1'))
            with self.assertRaisesRegex(ReviewPdfError,'p1: invalid source'):read_cards(p,HOMEWORK)
    def test_homework_source_must_match_card_and_number(self):
        for wrong in ('HW9 Problem 2','HW8 Problem 1'):
            with self.subTest(wrong=wrong),tempfile.TemporaryDirectory() as d:
                p=self.write(d,HW_SOURCE.read_text(encoding='utf-8').replace('data-source="HW9 Problem 1"',f'data-source="{wrong}"'))
                with self.assertRaisesRegex(ReviewPdfError,'p1: source'):read_cards(p,HOMEWORK)
    def test_nfd_filename(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.write(d,HW_SOURCE.read_text(encoding='utf-8'),unicodedata.normalize('NFD',HW_SOURCE.name))
            self.assertEqual(read_cards(p,HOMEWORK).range,'9')
    def test_hint_label(self):
        self.assertEqual([c.hint_label for c in read_cards(HW_SOURCE,HOMEWORK).cards],['',''])
        with tempfile.TemporaryDirectory() as d:
            p=self.write(d,HW_SOURCE.read_text(encoding='utf-8').replace('<details class="hint">','<details class="hint" data-label="비율 $a/b$ &amp; 약분">',1))
            self.assertEqual(read_cards(p,HOMEWORK).cards[0].hint_label,'비율 $a/b$ &amp; 약분')
    def test_bad_hint_label(self):
        for bad in ('',' ','가'*61,'$$a$$'):
            with self.subTest(bad=bad),tempfile.TemporaryDirectory() as d:
                p=self.write(d,HW_SOURCE.read_text(encoding='utf-8').replace('<details class="hint">',f'<details class="hint" data-label="{bad}">',1))
                with self.assertRaisesRegex(ReviewPdfError,'p1: hint label'):read_cards(p,HOMEWORK)
    def test_profile_helpers(self):
        self.assertEqual(REVIEW.kind('MML Example 9.1'),'예제')
        self.assertEqual(REVIEW.kind('MML Exercise 6.1'),'연습문제')
        self.assertEqual(HOMEWORK.kind('HW1 Problem 7'),'과제')
        self.assertIsNone(REVIEW.expected_source('0909','p3'))
        self.assertEqual(HOMEWORK.expected_source('1','p7'),'HW1 Problem 7')
        self.assertEqual(HOMEWORK.stem_fmt.format(range='1',slug='Homework1'),'과제1_Homework1')
        self.assertEqual(HOMEWORK.title_fmt.format(range='1'),'머신러닝기초 과제1')
