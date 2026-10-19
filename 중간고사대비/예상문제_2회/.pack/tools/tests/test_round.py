from pathlib import Path
import json,sys
O=Path(__file__).resolve().parents[3];sys.path.insert(0,str(O/'.pack/tools'))
def test_round_and_novel_questions():
 from exam_adapter import STEM,validate_blueprint,REPO
 b=json.loads((O/'.pack/blueprint.json').read_text());assert validate_blueprint(b,REPO)==[]
 q=json.loads((O/'.pack/questions.json').read_text());old=json.loads((O.parent/'예상문제_1회/.pack/questions.json').read_text())
 assert len(q)==10 and all(x['conditions']!=y['conditions'] and x['asks']!=y['asks'] for x,y in zip(q,old))
 assert 'Midterm_Practice_02' in STEM

def test_requested_title():
 from exam_adapter import STEM
 p=O/'문제설명_0909-1019_Midterm_Practice_02.html'
 s=p.read_text();assert '<title>머신러닝기초 중간고사 모의평가 2회 문제설명</title>' in s
 assert '모의평가 1회' not in s
