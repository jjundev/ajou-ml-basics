import sys,json,copy,unicodedata
from pathlib import Path
import pytest
TOOLS=Path(__file__).resolve().parents[1];sys.path.insert(0,str(TOOLS))
REPO=next(p for p in TOOLS.parents if (p/'.git').exists());OUT=TOOLS.parents[1]

def test_blueprint_scope_and_split():
 from exam_adapter import validate_blueprint
 b=json.loads((OUT/'.pack/blueprint.json').read_text())
 assert validate_blueprint(b,REPO)==[]
 for mutate in [lambda v:v['questions'].pop(),lambda v:v['questions'][0].update(kind='model_analysis'),lambda v:v.update(range='0909-1101')]:
  bad=copy.deepcopy(b);mutate(bad);assert validate_blueprint(bad,REPO)

def test_reference_hash_and_unicode_paths():
 from exam_adapter import validate_blueprint,resolve
 b=json.loads((OUT/'.pack/blueprint.json').read_text());p=b['sources'][0]['path']
 assert resolve(REPO,unicodedata.normalize('NFC',p))==resolve(REPO,unicodedata.normalize('NFD',p))
 b['sources'][0]['sha256']='0'*64;assert validate_blueprint(b,REPO)
 with pytest.raises(ValueError): resolve(REPO,'../outside')

def test_cards_and_provenance_reject_mismatch(tmp_path):
 from exam_adapter import load_exam_source,STEM
 from check_exam import validate_cards
 source=OUT/(STEM+'.html'); bp=OUT/'.pack/blueprint.json'
 assert validate_cards(source,bp,REPO)==[]
 bad=tmp_path/source.name;bad.write_text(source.read_text().replace('data-origin-ref="HW1 P6-P8"','data-origin-ref="MML invented"'))
 with pytest.raises(ValueError,match='origin mismatch'):load_exam_source(bad,bp,REPO)

def test_subparts_and_blind_input():
 from check_exam import validate_answer_checks
 from exam_adapter import load_exam_source,STEM,parse
 pack=load_exam_source(OUT/(STEM+'.html'),OUT/'.pack/blueprint.json',REPO)
 checks=json.loads((OUT/'.pack/evidence/answer-checks.json').read_text())['items']
 assert validate_answer_checks(pack,checks)==[]
 bad=copy.deepcopy(checks);bad.pop(next(iter(bad)));assert validate_answer_checks(pack,bad)
 bad=copy.deepcopy(checks);bad[next(iter(bad))]['status']='disputed';assert validate_answer_checks(pack,bad)
 root=parse((OUT/'.pack/evidence/blind-input.html').read_text())
 assert not list(root.find_all(lambda n: bool(n.classes & {'solution','answer','hint'})))
 assert len(list(root.find_all(lambda n:'problem' in n.classes)))==10

def test_problem_payload_has_no_solution_or_hint():
 from exam_adapter import EXAM,STEM
 from build_exam import problem_payload
 data=problem_payload(OUT/(STEM+'.html'))
 assert len(data['problems'])==10
 assert all('solution' not in p and not p['hints'] for p in data['problems'])
 assert all(p['html']['ask'] and p['html']['conditions'] for p in data['problems'])

@pytest.mark.pdf
def test_pdf_pair_and_page_mapping():
 import fitz
 from exam_adapter import STEM,sha
 report=json.loads((OUT/'.pack/evidence/pdf-validation.json').read_text())
 for mode,suffix in [('problems','문제'),('answers','답안')]:
  assert set(report['pages'][mode])=={f'p{i}' for i in range(1,11)}
  assert all(report['pages'][mode].values())
  p=OUT/(STEM+'-'+suffix+'.pdf');assert sha(p)==report['pdfs'][mode]['sha256']
  with fitz.open(p) as doc:
   assert len(doc)==report['pdfs'][mode]['page_count']
   assert all((page.rect.width,page.rect.height)==(1440,810) and page.get_text().strip() for page in doc)

def test_unreviewed_and_stale_inputs_rejected():
 from exam_adapter import load_exam_source,STEM
 from mpe_contract import validate_reviews
 from build_exam import build_explain
 from tempfile import TemporaryDirectory
 pack=load_exam_source(OUT/(STEM+'.html'),OUT/'.pack/blueprint.json',REPO)
 fragments={p.id:(OUT/f'.pack/explanations/{p.id}.html').read_text() for p in pack.problems}
 reviews=json.loads((OUT/'.pack/evidence/approved-review.json').read_text())
 assert validate_reviews(pack,fragments,reviews)==[]
 bad=copy.deepcopy(reviews);key=next(iter(bad['independent']['items']));bad['independent']['items'][key]['status']='not_run'
 assert validate_reviews(pack,fragments,bad)
 bad=copy.deepcopy(reviews);bad['input_hash']='0'*64;assert validate_reviews(pack,fragments,bad)
 fragments['p1']+=' changed';assert validate_reviews(pack,fragments,reviews)

def test_final_links_and_complete_pair(tmp_path):
 from check_exam import check_delivery
 from exam_adapter import STEM
 assert check_delivery(OUT,REPO)==[]
 # A source directory containing no delivered pair must be refused, never silently passed.
 assert check_delivery(tmp_path,REPO)

@pytest.mark.browser
def test_all_topics_and_responsive_panels():
 report=json.loads((OUT/'.pack/evidence/browser-check.json').read_text())
 assert report['status']=='pass'
 assert report['topic_ids']==[f'p{i}' for i in range(1,11)]
 assert set(report['viewports'])=={'1280x900','1024x900','375x812'}
 assert report['errors']==[]
 assert all(x['horizontal_overflow']==0 and x['katex_errors']==0 for x in report['screens'])

def test_delivery_missing_or_changed_file_is_rejected(tmp_path):
 from check_exam import check_file_hashes
 from exam_adapter import sha
 p=tmp_path/'problem.pdf';p.write_bytes(b'original')
 files={'problem.pdf':sha(p)}
 assert check_file_hashes(tmp_path,files,tmp_path)==[]
 p.write_bytes(b'changed');assert check_file_hashes(tmp_path,files,tmp_path)
 p.unlink();assert check_file_hashes(tmp_path,files,tmp_path)

@pytest.mark.pdf
def test_continuation_pages_keep_original_problem_ids():
 # Actual measured Chrome stress build; report never substitutes for real artifact review.
 report=json.loads((OUT/'.pack/evidence/pagination-stress.json').read_text())
 assert report['source_fixture']=='temporary long p8 answer; final questions unchanged'
 assert len(report['pages']['answers']['p8'])>1
 assert set(report['pages']['answers'])=={f'p{i}' for i in range(1,11)}
 assert report['errors']==[]

@pytest.mark.parametrize('id_', ['p4','p7'])
def test_answer_pdf_source_includes_every_requested_intermediate(id_):
 from exam_adapter import read_cards,EXAM,STEM
 import html
 cards={c.id:c for c in read_cards(OUT/(STEM+'.html'),EXAM).cards}
 first={k:html.unescape(v.steps[0]) for k,v in cards.items()}
 # Both were requested in (a), and must be in the PDF's solution payload, not only HTML 'start'.
 if id_=='p4':
  assert r'\Phi=\begin{pmatrix}1&-1\\1&0\\1&1\end{pmatrix}' in first['p4']
 else:
  assert r'-\log p(\theta\mid y,\Phi)' in first['p7']
  assert r'\frac{\|y-\Phi\theta\|^2}{2\sigma^2}' in first['p7']
  assert r'\frac{\|\theta-m_0\|^2}{2\tau^2}' in first['p7']
