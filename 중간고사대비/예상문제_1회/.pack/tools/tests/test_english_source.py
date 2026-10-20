from pathlib import Path
import pytest,copy,re
OUT=Path(__file__).resolve().parents[3]
REPO=next(p for p in OUT.parents if (p/'.git').exists())

def test_english_payload_excludes_korean_original_hints_and_solutions():
 from english_source import load_english_problems,english_payload
 from exam_adapter import STEM,subparts
 ps=load_english_problems(OUT/(STEM+'.html'),OUT/'.pack/blueprint.json',REPO)
 assert [p.card.id for p in ps]==[f'p{i}' for i in range(1,11)]
 assert [len(subparts(p.ask_html,'')) for p in ps]==[3,3,3,3,3,5,6,6,5,5]
 payload=english_payload(ps)
 assert all(p['html']['original']=='' and not p['hints'] and 'solution' not in p for p in payload['problems'])
 assert not re.search('[가-힣ㄱ-ㅎㅏ-ㅣ]',str(payload))

@pytest.mark.parametrize('mutation',['missing','duplicate','empty','empty_markup','korean','reorder'])
def test_missing_duplicate_or_empty_english_fields_rejected(tmp_path,mutation):
 from english_source import load_english_problems
 from exam_adapter import STEM
 text=(OUT/(STEM+'.html')).read_text(encoding='utf-8')
 if mutation=='missing':text=text.replace('data-english-title','data-no-title',1)
 if mutation=='duplicate':text=text.replace('data-english-title','data-english-title',1).replace('</h4>','</h4><h4 data-english-title>Duplicate</h4>',1)
 if mutation=='empty':text=re.sub(r'(<h4 data-english-title(?:="")?>).*?(</h4>)',r'\1\2',text,count=1)
 if mutation=='empty_markup':text=re.sub(r'(<h4 data-english-title(?:="")?>).*?(</h4>)',r'\1<span> </span>\2',text,count=1)
 if mutation=='korean':text=re.sub(r'(<h4 data-english-title(?:="")?>)',r'\1한글',text,count=1)
 if mutation=='reorder':text=text.replace('data-english-part="a"','data-english-part="z"',1)
 source=tmp_path/(STEM+'.html');source.write_text(text,encoding='utf-8')
 with pytest.raises(ValueError):load_english_problems(source,OUT/'.pack/blueprint.json',REPO)

@pytest.mark.parametrize('ask',[
 '<ol type="a"><li data-english-part="a">First</li></ol><ol type="a"><li data-english-part="b">Second</li></ol>',
 '<ol type="a"><li data-english-part="a">First<ol><li data-english-part="b">Second</li></ol></li></ol>',
 '<ol type="1"><li data-english-part="a">First</li><li data-english-part="b">Second</li></ol>',
 '<ol type="a" start="2"><li data-english-part="a">First</li><li data-english-part="b">Second</li></ol>',
 '<ol type="a"><li data-english-part="a">First</li><li value="1" data-english-part="b">Second</li></ol>',
 '<div data-english-part="a"></div><ol type="a"><li>First</li><li data-english-part="b">Second</li></ol>'
])
def test_single_list_direct_children_and_displayed_labels_required(ask):
 from english_source import english_fields
 original='<h4 data-english-title>Title</h4><div data-english-conditions>Conditions</div><div data-english-ask>'+ask+'</div>'
 with pytest.raises(ValueError):english_fields(original,'p1',('a','b'))
