import hashlib
import json
import unittest
from dataclasses import replace
from _util import FIXTURES, SKILL
from review_pdf_cards import read_cards, normalize_cards
from review_pdf_payload import to_workbook, inject_data, space_math
from review_pdf_types import HOMEWORK, ReviewPdfError

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
    def test_homework_kind_badge(self):
        path=FIXTURES/'pdf/과제9_Pdf_Test.html'
        ps=normalize_cards(read_cards(path,HOMEWORK),None,path)[:1]
        p=to_workbook(ps,{},'problems',profile=HOMEWORK)['problems'][0]
        self.assertEqual((p['kind'],p['section'],p['number']),('과제','HW9 Problem 1','P1'))
        self.assertEqual(to_workbook(self.ps[:1],{},'problems')['problems'][0]['kind'],'예제')
    def test_self_made_kind_hides_basis_toggle(self):
        ps=[replace(self.ps[0],card=replace(self.ps[0].card,source='자작 p1'))]
        p=to_workbook(ps,{},'problems')['problems'][0]
        self.assertEqual(p['kind'],'자작')
        self.assertEqual(p['html']['original'],'')
    def test_hint_label_falls_back(self):
        from dataclasses import replace
        ps=self.ps[:1]
        self.assertEqual(to_workbook(ps,{},'problems')['problems'][0]['hints'][0]['label'],'풀이 방향')
        card=replace(ps[0].card,hint_label='비율 $a/b$')
        ps=(replace(ps[0],card=card),)
        h=to_workbook(ps,{},'answers')['problems'][0]['hints'][0]
        self.assertEqual((h['label'],h['html']),('비율 $a/b$',card.hint_html))
    def test_spacing_reaches_every_field(self):
        from dataclasses import replace
        m=r'$\begin{bmatrix}1\\2\end{bmatrix}$'
        card=replace(self.ps[0].card,original_html=f'Let {m}.<div class="part">(a) go</div>',hint_html=f'see {m}',steps=(f'step {m}',),answer_html=f'ans {m}')
        ps=(replace(self.ps[0],card=card,conditions_html=f'given {m}',ask_html=f'find {m}'),)
        item=to_workbook(ps,{},'answers')['problems'][0]
        fields=[*item['html'].values(),item['hints'][0]['html'],item['solution']['steps'][0]['html'],item['solution']['answer']]
        for f in fields:self.assertIn(TALL+m+'</span>',f)
        self.assertIn(PART,item['html']['original'])
        self.assertEqual(item['hints'][0]['label'],'풀이 방향')
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


TALL='<span style="display:inline-block;margin:.8mm 0">'
GAP='<div style="margin-top:1.6mm">'
PART='<div class="part" style="margin-top:1.6mm">'

class TestSpaceMath(unittest.TestCase):
    def test_wraps_inline_matrix(self):
        m=r'$a=\begin{bmatrix}1\\2\end{bmatrix}$'
        self.assertEqual(space_math(f'Let {m}, so'),f'Let {TALL}{m}</span>, so')
    def test_wraps_braced_long_matrix(self):
        m=r'${\mathbf{C}=\begin{bmatrix}1 &amp; 2 &amp; 0\\-1 &amp; 3 &amp; 4\end{bmatrix}}$'
        self.assertEqual(space_math(m),TALL+m+'</span>')
    def test_leaves_long_unbraced_matrix(self):
        # 40자가 넘고 중괄호가 없으면 템플릿이 display로 바꾸므로 감싸지 않아요.
        m=r'$\mathbf{C}=\begin{bmatrix}1 &amp; 2 &amp; 0\\-1 &amp; 3 &amp; 4\end{bmatrix}$'
        self.assertEqual(space_math(m),m)
    def test_wraps_long_matrix_without_top_level_relation(self):
        # 관계 기호가 없거나 중괄호·\left…\right 안에만 있으면 템플릿이 inline으로 둬요.
        for m in (r'$\begin{bmatrix}1 &amp; 2 &amp; 0\\-1 &amp; 3 &amp; 4\\5 &amp; 0 &amp; -2\end{bmatrix}$',
                  r'$\left(\mathbf{C}=\begin{bmatrix}1 &amp; 2 &amp; 0\\-1 &amp; 3 &amp; 4\end{bmatrix}\right)$',
                  r'$\mathbf{C}\leftarrow\begin{bmatrix}1\end{bmatrix}$'):
            with self.subTest(m=m):self.assertEqual(space_math(m),TALL+m+'</span>')
    def test_leaves_long_matrix_split_at_leq(self):
        m=r'$\mathbf{C}\leq\begin{bmatrix}1 &amp; 2 &amp; 0\\-1 &amp; 3 &amp; 4\end{bmatrix}$'
        self.assertEqual(space_math(m),m)
    def test_leaves_plain_inline_and_display(self):
        s=r'$a+b$ and $$\begin{bmatrix}1\end{bmatrix}$$ and $\frac{1}{2}$'
        self.assertEqual(space_math(s),s)
    def test_spaces_stacked_displays(self):
        s='$$a$$ $$b$$\n$$c$$ text $$d$$'
        self.assertEqual(space_math(s),f'$$a$$ {GAP}$$b$$</div>\n{GAP}$$c$$</div> text $$d$$')
    def test_styles_part_blocks(self):
        self.assertEqual(space_math('x.<div class="part">(a) y</div>'),f'x.{PART}(a) y</div>')
    def test_idempotent(self):
        s=r'Let $\begin{bmatrix}1\end{bmatrix}$ $$a$$ $$b$$<div class="part">(a)</div>'
        once=space_math(s)
        self.assertEqual(space_math(once),once)
    def test_text_and_tex_unchanged(self):
        s=r'P &amp; Q $\begin{bmatrix}1\end{bmatrix}$ $$a$$ $$b$$ <div class="part">(a) $x$</div>'
        strip=lambda t:t.replace(TALL,'').replace('</span>','').replace(GAP,'').replace(PART,'<div class="part">').replace('$$</div>','$$')
        self.assertEqual(strip(space_math(s)),s)
