"""Regression contracts for the common explanation update; synthetic inputs only."""
import sys, json
from pathlib import Path
from dataclasses import replace
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from mpe_types import SourcePack
from mpe_render import build_explanation, check_artifacts
from mpe_source import load_source, resolve_sources, subparts
from helpers import fragment, problem


def synthetic(tmp_path):
    repo=tmp_path/'repo'
    src=repo/'복습노트/1007/복습문제_1007_Test.html'
    src.parent.mkdir(parents=True)
    src.write_text('<html><body id="p1">fixture</body></html>',encoding='utf-8')
    p=problem()
    pack=SourcePack('review','1007','Test',src,'0'*64,(p,))
    return repo,pack,{p.id:fragment(p)}


def test_stage_has_separate_problem_and_original(tmp_path):
    repo,pack,fragments=synthetic(tmp_path)
    a=build_explanation(pack,fragments,tmp_path/'stage',repo)
    text=a.html.read_text(encoding='utf-8')
    from mpe_shared import parse
    doc=parse(text)
    assert len(list(doc.find_all(lambda n:n.attrs.get('data-problem-for')=='p1')))==1
    assert 'id="panel-prob"' in text
    assert 'data-original-problem="p1"' in text
    assert check_artifacts(pack,a)==[]


def test_legacy_policy_cannot_reuse_approval():
    from mpe_review_policy import carry_reviews
    old={'content':{'status':'pass'},'independent':{'status':'pass'}}
    fresh={'content':{'status':'not_run'},'independent':{'status':'not_run'}}
    result=carry_reviews(old,fresh,[],True)
    assert result['content']['status']=='not_run'
    assert result['independent']['status']=='not_run'


def test_current_policy_reuses_only_when_inputs_and_references_verified():
    from mpe_review_policy import carry_reviews, POLICY_VERSION
    old={'review_policy_version':POLICY_VERSION,'content':{'status':'pass'},'independent':{'status':'pass'}}
    fresh={'content':{'status':'not_run'},'independent':{'status':'not_run'},'browser':{'status':'not_run'}}
    assert carry_reviews(old,fresh,[],True)['content']['status']=='pass'
    assert carry_reviews(old,fresh,[],True)['browser']['status']=='not_run'
    assert carry_reviews(old,fresh,[],False)['independent']['status']=='not_run'


def test_old_policy_rejected_by_review_gate(tmp_path):
    from mpe_contract import initial_reviews,validate_reviews
    repo,pack,fragments=synthetic(tmp_path)
    review=initial_reviews(pack,fragments)
    review.pop('review_policy_version',None)
    assert any('검토 기준' in e for e in validate_reviews(pack,fragments,review))


def test_source_svg_numeric_stroke_width_is_allowed(tmp_path):
    repo,pack,fragments=synthetic(tmp_path)
    p=replace(pack.problems[0],figures_html=('<svg viewBox="0 0 20 20"><path style="stroke-width:2px" d="M0 0L10 10"/></svg>',))
    pack=replace(pack,problems=(p,))
    a=build_explanation(pack,fragments,tmp_path/'stage',repo)
    assert 'stroke-width:2px' in a.html.read_text(encoding='utf-8')


def test_all_selects_only_reviews_newest_first(tmp_path):
    repo=tmp_path/'repo'
    for name in ['복습노트/1007/복습문제_1007_A.html','복습노트/1014/복습문제_1014_B.html','과제/과제1/과제1_Homework1.html']:
        p=repo/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('fixture')
    assert [p.parent.name for p in resolve_sources(repo,'all')]==['1014','1007']


def test_choices_are_not_question_subparts():
    assert subparts('<ol class="choices"><li>(a) A</li><li>(b) B</li></ol>','')==('main',)


def test_choice_model_is_validated_and_embedded(tmp_path):
    from mpe_choices import choice_models
    from mpe_shared import parse
    statement='<ul class="choices"><li>A</li><li>B</li></ul>'
    model={'cards':{'p1':{'answer':'B','mode':'single','options':[{'id':'A','index':0},{'id':'B','index':1}]}}}
    html='<script type="application/json" id="review-interaction-model">'+json.dumps(model)+'</script>'
    choices=choice_models(html,{'p1':statement})
    assert choices['p1'].answer=='B'
    repo,pack,fragments=synthetic(tmp_path)
    p=replace(pack.problems[0],conditions_html=statement,choice=choices['p1'])
    a=build_explanation(replace(pack,problems=(p,)),fragments,tmp_path/'stage',repo)
    doc=parse(a.html.read_text(encoding='utf-8'))
    script=next(doc.find_all(lambda n:n.attrs.get('id')=='explain-choice-model'))
    assert json.loads(script.text())['p1']=={'answer':'B','mode':'single','options':['A','B']}
    model['cards']['p1']['answer']='guessed'
    bad='<script id="review-interaction-model" type="application/json">'+json.dumps(model)+'</script>'
    assert choice_models(bad,{'p1':statement})=={}


def test_canonically_equal_sibling_directory_is_not_inside_repo(tmp_path):
    import unicodedata
    from mpe_source import inside
    from mpe_types import ExplainError
    repo=tmp_path/'저장소'
    other=tmp_path/unicodedata.normalize('NFD','저장소')
    repo.mkdir();other.mkdir()
    source=other/'outside.txt';source.write_text('outside')
    with pytest.raises(ExplainError,match='저장소 밖'):
        inside(source,repo)


def published_fixture(tmp_path, reference=False):
    import shutil
    from mpe_cli import extract, load_run, build, load_artifacts, load_fragments
    from helpers import approved
    repo=tmp_path/'published-repo'
    source=repo/'복습노트/1007/복습문제_1007_Test.html'
    source.parent.mkdir(parents=True)
    source.write_text('<section id="questions"><article class="card" id="p1" data-source="MML Exercise 1.1"><h3>1. scalar</h3><div class="problem"><div class="conditions"><p>$A=1$</p></div><div class="ask"><p>Compute.</p></div></div><details class="original"><summary>original</summary><blockquote>Compute the scalar.</blockquote></details><details class="hint"><summary>hint</summary><p>substitute</p></details><details class="solution"><summary>solution</summary><ol class="steps"><li>substitute</li></ol><p class="answer">1</p></details></article></section>',encoding='utf-8')
    run=tmp_path/'first-run'
    target='1007' if False else str(source)
    assert extract(repo,target,run)==0
    item=load_run(run)[0]
    for problem in item['pack'].problems:
        (item['folder']/'explanations'/f'{problem.id}.html').write_text(fragment(problem),encoding='utf-8')
    build(item,load_fragments(item))
    artifacts=load_artifacts(item)
    reviews=approved(item['pack'],load_fragments(item),artifacts)
    if reference:
        from mpe_source import sha256
        ref=repo/'reference.html';ref.write_text('<p>theory</p>',encoding='utf-8')
        reviews['references']=[{'path':str(ref),'sha256':sha256(ref)}]
    destination=item['pack'].path.parent
    shutil.copytree(artifacts.html.parent,destination,dirs_exist_ok=True)
    data=destination/artifacts.manifest.relative_to(artifacts.html.parent).parent
    (data/'validation.json').write_text(json.dumps(reviews),encoding='utf-8')
    return repo,source,data


def rebuilt_review(tmp_path,repo,source):
    from mpe_cli import rerender, load_run
    run=tmp_path/'rebuilt'
    assert rerender(repo,'1007' if False else str(source),run)==0
    folder=load_run(run)[0]['folder']
    return json.loads((folder/'review.json').read_text(encoding='utf-8'))


def test_rerender_current_policy_preserves_only_content_checks(tmp_path):
    repo,source,data=published_fixture(tmp_path)
    review=rebuilt_review(tmp_path,repo,source)
    assert review['content']['status']=='pass'
    assert review['independent']['status']=='pass'
    assert review['browser']['status']=='not_run'
    assert review['source_visual']['status']=='not_run'


def test_rerender_legacy_policy_requires_fresh_content_checks(tmp_path):
    repo,source,data=published_fixture(tmp_path)
    p=data/'validation.json';old=json.loads(p.read_text());old.pop('review_policy_version')
    p.write_text(json.dumps(old),encoding='utf-8')
    review=rebuilt_review(tmp_path,repo,source)
    assert review['content']['status']=='not_run'
    assert review['independent']['status']=='not_run'


@pytest.mark.parametrize('action',['change','remove'])
def test_rerender_changed_or_missing_reference_resets_approval(tmp_path,action):
    repo,source,data=published_fixture(tmp_path,reference=True)
    ref=repo/'reference.html'
    if action=='remove': ref.unlink()
    else: ref.write_text('<p>different theory</p>')
    review=rebuilt_review(tmp_path,repo,source)
    assert review['content']['status']=='not_run'
    assert review['independent']['status']=='not_run'


def test_rerender_rejects_changed_published_fragment(tmp_path):
    from mpe_cli import rerender
    repo,source,data=published_fixture(tmp_path)
    p=data/'fragments/p1.html';p.write_text(p.read_text()+'<p>tampered</p>')
    assert rerender(repo,'1007' if False else str(source),tmp_path/'rebuilt')==1


def test_reference_relocation_cannot_compare_replacement_image_to_itself(tmp_path):
    from mpe_rerender import equivalent_text
    repo=tmp_path/'repo';source=repo/'1007/reference.html'
    target=source.parent/'.pack/figures/image.png';target.parent.mkdir(parents=True)
    target.write_bytes(b'changed-image')
    assert not equivalent_text(b'<img src="figures/image.png">',b'<img src=".pack/figures/image.png">',source,source,repo)


def test_reference_image_dependency_must_have_its_own_hash(tmp_path):
    from mpe_rerender import verified_references
    from mpe_source import sha256
    repo=tmp_path/'repo';repo.mkdir()
    ref=repo/'theory.html';ref.write_text('<img src="theory.png">')
    image=repo/'theory.png';image.write_bytes(b'old-image')
    records=[{'path':str(ref),'sha256':sha256(ref)}]
    assert verified_references(records,repo,repo)[1] is False
    records.append({'path':str(image),'sha256':sha256(image)})
    assert verified_references(records,repo,repo)[1] is True
    image.write_bytes(b'changed-image')
    assert verified_references(records,repo,repo)[1] is False


def test_source_image_unicode_spelling_resolves_before_hashing(tmp_path):
    import unicodedata
    repo,pack,fragments=synthetic(tmp_path)
    base=pack.path.parent
    (base/'그림.png').write_bytes(b'fixture-image')
    p=replace(pack.problems[0],figures_html=('<img src="'+unicodedata.normalize('NFD','그림.png')+'" alt="fixture">',))
    result=build_explanation(replace(pack,problems=(p,)),fragments,tmp_path/'stage',repo)
    assert result.html.is_file()
