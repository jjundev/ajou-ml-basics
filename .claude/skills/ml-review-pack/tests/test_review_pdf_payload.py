import hashlib
import json
import unittest
from _util import FIXTURES, SKILL
from review_pdf_cards import read_cards, normalize_cards
from review_pdf_payload import to_workbook, inject_data
from review_pdf_types import ReviewPdfError

class TestPayload(unittest.TestCase):
    def setUp(self):
        self.path=FIXTURES/'pdf/복습문제_0101_Pdf_Test.html'
        self.ps=normalize_cards(read_cards(self.path),None,self.path)
    def test_separate_answer_and_preserve_proof_goal(self):
        ps=self.ps[:1]
        p=to_workbook(ps,{},'problems');a=to_workbook(ps,{},'answers')
        self.assertNotIn('solution',p['problems'][0])
        self.assertNotIn('ANSWER_ONLY_SENTINEL',json.dumps(p))
        self.assertIn('$a/b$',p['problems'][0]['html']['ask'])
        self.assertEqual(a['problems'][0]['solution']['steps'][0]['html'],'첫 단계 $a/b$.')
        self.assertIn(r'\frac{1}{5}',a['problems'][0]['solution']['answer'])
        self.assertEqual(p['problems'][0]['kind'],'예제')
        self.assertEqual(p['problems'][0]['number'],'P1')
        self.assertEqual(p['problems'][0]['section'],'MML Example 9.1')
    def test_missing_asset(self):
        with self.assertRaisesRegex(ReviewPdfError,'p2.*asset'):to_workbook(self.ps,{},'problems')
    def test_script_escape(self):
        t='<script id="workbook-data">__WORKBOOK_DATA__</script>'
        s=inject_data(t,{'text':'</script><script>bad</script>'})
        self.assertNotIn('</script><script>',s)
        self.assertEqual(json.loads(s.split('>',1)[1].rsplit('<',1)[0])['text'],'</script><script>bad</script>')
    def test_templates_unchanged(self):
        record=json.loads((SKILL/'assets/pdf-template-provenance.json').read_text())
        expected={'problem':'431fdafcd3bce6d86b2bb7881ed4332e6287a9b8c6bd8626628f9e673a4d2655','answer':'4d3a13379d759ae8b1b48dd27417919929b4e0bf94a686a7362b79719e949040'}
        for mode in expected:
            data=(SKILL/f'assets/pdf-{mode}.html').read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(),expected[mode])
            self.assertEqual(record['templates'][mode]['sha256'],expected[mode])
