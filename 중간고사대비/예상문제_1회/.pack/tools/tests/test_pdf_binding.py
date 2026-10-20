from pathlib import Path
import pytest,json,shutil
OUT=Path(__file__).resolve().parents[3]
REPO=next(p for p in OUT.parents if (p/'.git').exists())

def test_original_only_change_preserves_korean_pdf_binding():
 from pdf_binding import korean_content_digest,check_pdf_binding
 from exam_adapter import STEM
 snapshot=OUT/'.pack/evidence/korean-pdf-source'/(STEM+'.html')
 assert korean_content_digest(snapshot)==korean_content_digest(OUT/(STEM+'.html'))
 assert check_pdf_binding(OUT,REPO)==[]

@pytest.mark.parametrize('field',['statement','answer','order'])
def test_korean_statement_or_answer_change_rejected(tmp_path,field):
 from pdf_binding import korean_content_digest
 from exam_adapter import STEM
 text=(OUT/(STEM+'.html')).read_text(encoding='utf-8')
 if field=='statement':text=text.replace('열벡터 $v_1','다른 열벡터 $v_1',1)
 elif field=='answer':text=text.replace('class="answer"','class="answer">changed</div><div',1)
 else:text=text.replace('id="p1"','id="p99"',1)
 target=tmp_path/(STEM+'.html');target.write_text(text,encoding='utf-8')
 try:assert korean_content_digest(target)!=korean_content_digest(OUT/(STEM+'.html'))
 except ValueError:pass

def test_missing_snapshot_or_changed_pdf_report_rejected(tmp_path):
 from pdf_binding import check_pdf_binding
 target=tmp_path/'pack';shutil.copytree(OUT,target)
 report=target/'.pack/evidence/pdf-validation.json';report.write_text(report.read_text()+' ')
 assert check_pdf_binding(target,tmp_path)

def test_missing_or_stale_english_pdf_rejected(tmp_path):
 from check_exam import check_english_delivery
 assert check_english_delivery(tmp_path,tmp_path)
 assert check_english_delivery(OUT,REPO)==[]

@pytest.mark.parametrize('field',['pdf','source','mapping','page_id','report_errors'])
def test_english_delivery_rejects_tampering(tmp_path,field):
 from check_exam import check_english_delivery
 from exam_adapter import STEM
 target=tmp_path/'pack';shutil.copytree(OUT,target)
 # Scope this fixture to the English delivery; establish a valid baseline first.
 delivery=json.loads((target/'.pack/delivery.json').read_text())
 delivery['files'][STEM+'-문제-English.pdf']='bound-by-report'
 (target/'.pack/delivery.json').write_text(json.dumps(delivery),encoding='utf-8')
 assert check_english_delivery(target,REPO)==[]
 report=target/'.pack/evidence/english-pdf-validation.json';value=json.loads(report.read_text())
 if field=='pdf':
  p=target/(STEM+'-문제-English.pdf');p.write_bytes(p.read_bytes()+b'changed')
 elif field=='source':
  p=target/(STEM+'.html');p.write_text(p.read_text()+' ',encoding='utf-8')
 elif field=='mapping':value['pages']['p1']=[]
 elif field=='page_id':value['page_ids'][0]='p2'
 else:value['errors']=['unresolved geometry']
 report.write_text(json.dumps(value),encoding='utf-8')
 assert check_english_delivery(target,REPO)
