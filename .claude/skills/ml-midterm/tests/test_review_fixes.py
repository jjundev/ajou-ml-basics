"""Regressions reproduced by the independent final reviewer."""
import json, unicodedata
from pathlib import Path
import pytest

@pytest.mark.parametrize('damage',['missing','reviewer','evidence','pages'])
def test_english_requires_visual_review(baseline,repo,monkeypatch,damage):
    import check_exam
    original=json.loads
    def damaged(text,*args,**kwargs):
        v=original(text,*args,**kwargs)
        if isinstance(v,dict) and 'english_digests' in v:
            if damage=='missing':v.pop('visual_review',None)
            elif damage=='pages':v['visual_review']['pages']=[]
            else:v['visual_review'][damage]=''
        return v
    monkeypatch.setattr(check_exam.json,'loads',damaged)
    assert check_exam.check_english_delivery(baseline,repo)

def test_delivery_requires_all_owned_files(baseline,repo,monkeypatch):
    import check_exam
    original=json.loads
    def incomplete(text,*args,**kwargs):
        v=original(text,*args,**kwargs)
        if isinstance(v,dict) and 'files' in v and 'subpart_count' in v:
            v['files']={k:h for k,h in v['files'].items() if k.endswith('.pdf')}
        return v
    monkeypatch.setattr(check_exam.json,'loads',incomplete)
    assert any('delivery missing' in e for e in check_exam.check_delivery(baseline,repo))

def add_image(exam,fragment=False):
    from test_build import source_for
    from PIL import Image
    source=source_for(exam)
    image=exam.output/'.pack/figures/diagram.png';image.parent.mkdir(parents=True,exist_ok=True)
    Image.new('RGB',(120,60),'blue').save(image)
    if fragment:
        p=exam.output/'.pack/explanations/p1.html'
        p.write_text(p.read_text(encoding='utf-8').replace('</p>','</p><figure><img src=".pack/figures/diagram.png" alt="test"></figure>',1), encoding='utf-8')
    else:
        source.write_text(source.read_text(encoding='utf-8').replace('<div class="ask">','<figure><img src=".pack/figures/diagram.png" alt="test"></figure><div class="ask">',1), encoding='utf-8')
    return source,image

@pytest.mark.pdf
def test_snapshot_resolves_original_relative_figure(exam,tmp_path):
    from build_exam import korean_pdf_source
    from review_pdf_render import freeze_figures
    from exam_adapter import read_cards
    source,image=add_image(exam)
    target=tmp_path/'stage/.pack/evidence/korean-pdf-source'/source.name
    korean_pdf_source(source,target,exam)
    assets=freeze_figures(read_cards(target,exam.profile),tmp_path/'frozen')
    assert assets and (target.parent/'.pack/figures/diagram.png').read_bytes()==image.read_bytes()

@pytest.mark.parametrize('fragment',[False,True])
def test_picture_change_invalidates_approval(repo,exam,tmp_path,fragment):
    from build_exam import build_explain,publish_explain
    from test_explain import approved_test_review
    source,image=add_image(exam,fragment);run=tmp_path/'run'
    result=build_explain(repo,exam.output,run);approved_test_review(result)
    image.write_bytes(image.read_bytes()+b'changed')
    with pytest.raises(ValueError,match='resource|reference|그림|참조'):publish_explain(repo,exam.output,run)

def test_actual_nfd_source_and_target(repo,exam):
    from test_build import source_for
    from exam_adapter import load_exam_source
    from exam_config import resolve_exam_target
    source=source_for(exam);nfd=source.with_name(unicodedata.normalize('NFD',source.name));source.rename(nfd)
    assert load_exam_source(nfd,exam.output/'.pack/blueprint.json',repo,exam).slug=='Midterm_Practice_02'
    assert resolve_exam_target(repo,str(nfd))==exam

def test_actual_nfd_round_discovery(tmp_path):
    from exam_config import next_round,config_for_round
    folder=tmp_path/unicodedata.normalize('NFD','중간고사대비')/unicodedata.normalize('NFD','예상문제_2회')
    folder.mkdir(parents=True)
    assert next_round(tmp_path)==3
    assert config_for_round(tmp_path,2).output==folder.resolve()

@pytest.mark.pdf
def test_actual_nfd_english_workflow(repo,exam,tmp_path):
    from test_build import source_for
    from english_pdf import build_english_pdf
    source=source_for(exam);nfd=source.with_name(unicodedata.normalize('NFD',source.name));source.rename(nfd)
    result=build_english_pdf(repo,exam.output,tmp_path/'run')
    report=json.loads(result['report'].read_text(encoding='utf-8'))
    assert report['logical_count']==10 and report['subpart_count']==42
