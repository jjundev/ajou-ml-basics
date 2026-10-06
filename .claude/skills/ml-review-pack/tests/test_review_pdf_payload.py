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
        self.assertEqual(record['source_commit'], '757fa081521008d46542e23d5a1a53112391aed2')
        expected = {'problem': '1ddb009d96f3a844778bd8f4378126d0fd52d037296dff89223adb69bc38bdc7', 'answer': '557b30b2918b4b41ff37763c80869ce28ce6b55f81c42e1ce34bfa30af3c1b06', 'video': 'd56658538e1b67df08a7eea0282e733afd999c6255e58ecc13cd4c72d13ad870'}
        for mode, sha in expected.items():
            entry = record['templates'][mode]
            self.assertEqual(entry['sha256'], sha)
            self.assertEqual(hashlib.sha256((SKILL/'assets'/entry['local_path']).read_bytes()).hexdigest(),sha)
