from pathlib import Path
import re,json,pytest
OUT=Path(__file__).resolve().parents[3]
REPO=next(p for p in OUT.parents if (p/'.git').exists())

def test_english_template_translates_visible_labels():
 from english_pdf import english_template
 text=english_template(REPO,'video-16x9')
 assert 'lang="en"' in text
 for label in ['Original problem','Given','Tasks']:assert label in text
 # Comments and unused KIND_SLUG keys are not printed; inspect the real PDF below.
 assert "block('조건'" not in text and "block('구할 것'" not in text

@pytest.mark.pdf
def test_english_pdf_is_16x9_and_contains_no_korean():
 import fitz
 from exam_adapter import STEM,sha
 pdf=OUT/(STEM+'-문제-English.pdf')
 assert pdf.is_file()
 report=json.loads((OUT/'.pack/evidence/english-pdf-validation.json').read_text())
 assert report['pdf_sha256']==sha(pdf)
 with fitz.open(pdf) as doc:
  assert all((p.rect.width,p.rect.height)==(1440,810) for p in doc)
  assert not re.search('[가-힣ㄱ-ㅎㅏ-ㅣ]',''.join(p.get_text() for p in doc))
  assert all(min(p.get_pixmap(clip=fitz.Rect(0,675,1440,810),alpha=False).samples)==255 for p in doc)
 assert set(report['pages'])=={f'p{i}' for i in range(1,11)}

@pytest.mark.pdf
def test_long_english_questions_keep_labels_across_pages(tmp_path):
 from dataclasses import replace
 import fitz
 from exam_adapter import STEM
 from english_source import load_english_problems
 from english_pdf import build_problems
 ps=list(load_english_problems(OUT/(STEM+'.html'),OUT/'.pack/blueprint.json',REPO))
 p=ps[7]
 ask=re.sub(r'(<li[^>]*>)([\s\S]*?)(</li>)',lambda m:m[1]+m[2]+('<p>'+m[2]+'</p>')*3+m[3],p.ask_html)
 ps[7]=replace(p,ask_html=ask)
 pdf,report=build_problems(REPO,ps,tmp_path/'live-stress')
 assert len(report['pages']['p8'])>1
 with fitz.open(pdf) as doc:
  texts=[doc[n-1].get_text() for n in report['pages']['p8']]
  # Inspect printed labels, not data-english-part attributes that could disagree.
  labels=[label for text in texts for label in re.findall(r'(?m)^\s*([a-f])\.\s*$',text)]
  assert labels==list('abcdef')
  assert 'Problem 8 (continued)' in texts[1]
  for text in texts:assert p.card.title in text
