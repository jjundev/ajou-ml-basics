import json, copy
from pathlib import Path
import pytest

def prepare(exam):
    from exam_adapter import assemble_cards
    assemble_cards(exam.output/'.pack/cards', exam.output/(exam.stem+'.html'), exam)
    for suffix in ('-문제.pdf','-답안.pdf','-문제-English.pdf'):
        (exam.output/(exam.stem+suffix)).write_bytes(b'unchanged-test-only')

def non_owned(exam):
    from exam_adapter import sha
    paths = list((exam.output/'.pack/cards').glob('*.html')) + list(exam.output.glob('*'))
    return {str(p):sha(p) for p in paths if p.is_file()}

def approved_test_review(result):
    """Synthetic approvals ONLY for publication gate tests, never deliverables."""
    from mpe_render import dump
    p = result['review_path']; v = json.loads(p.read_text(encoding='utf-8'))
    for k in ('source_visual','content','independent','browser'):
        v[k].update(status='pass',reviewer='TEST FIXTURE',evidence='synthetic gate test')
        for item in v[k].get('items',{}).values():
            item.update(status='pass',reviewer='TEST FIXTURE',evidence='synthetic gate test',method='proof',conclusion='test only')
    dump(p,v)

def test_explanations_override_stale_inventory(repo, exam, tmp_path):
    from build_exam import build_explain
    prepare(exam)
    for name in ('solutions.json','panel-content.json'):
        (exam.output/'.pack'/name).write_text('{"old":"STALE ANSWER"}', encoding='utf-8')
    result = build_explain(repo,exam.output,tmp_path/'run')
    assert 'STALE ANSWER' not in result['artifacts'].html.read_text(encoding='utf-8')
    assert 'STALE ANSWER' not in result['artifacts'].md.read_text(encoding='utf-8')
    from mpe_contract import validate_fragment
    for p in result['pack'].problems:
        assert validate_fragment(p,(exam.output/f'.pack/explanations/{p.id}.html').read_text(encoding='utf-8')) == []

def test_build_resets_reviews_and_preserves_problem_files(repo,exam,tmp_path):
    from build_exam import build_explain
    prepare(exam); before=non_owned(exam)
    result=build_explain(repo,exam.output,tmp_path/'run')
    review=json.loads(result['review_path'].read_text(encoding='utf-8'))
    assert all(review[k]['status']=='not_run' for k in ('source_visual','content','independent','browser'))
    assert non_owned(exam)==before
    text=result['artifacts'].html.read_text(encoding='utf-8')
    assert '머신러닝기초 중간고사 모의평가 2회 문제설명' in text
    assert exam.reading_key in text
    from urllib.parse import unquote
    assert exam.stem+'.html' in unquote(text)

@pytest.mark.parametrize('change',['unreviewed','source','fragment','reference','artifact','policy'])
def test_publish_rejects_stale_or_unreviewed(repo,exam,tmp_path,change):
    from build_exam import build_explain,publish_explain
    prepare(exam); run=tmp_path/'run'; result=build_explain(repo,exam.output,run)
    if change!='unreviewed': approved_test_review(result)
    if change=='source':
        p=result['pack'].path;p.write_text(p.read_text(encoding='utf-8')+' changed', encoding='utf-8')
    if change=='fragment':
        p=exam.output/'.pack/explanations/p1.html';p.write_text(p.read_text(encoding='utf-8')+' changed', encoding='utf-8')
    if change=='reference':
        v=json.loads(result['review_path'].read_text(encoding='utf-8'));v['references'][0]['sha256']='0'*64
        result['review_path'].write_text(json.dumps(v), encoding='utf-8')
    if change=='artifact':
        p=result['artifacts'].html;p.write_text(p.read_text(encoding='utf-8')+' changed', encoding='utf-8')
    if change=='policy':
        v=json.loads(result['review_path'].read_text(encoding='utf-8'));v['review_policy_version']='old'
        result['review_path'].write_text(json.dumps(v), encoding='utf-8')
    with pytest.raises(ValueError): publish_explain(repo,exam.output,run)

def test_publish_only_owns_explanation_files(repo,exam,tmp_path):
    from build_exam import build_explain,publish_explain
    prepare(exam); before=non_owned(exam);run=tmp_path/'run'
    result=build_explain(repo,exam.output,run);approved_test_review(result)
    published=publish_explain(repo,exam.output,run)
    assert all('문제설명' in p.name or '.pack' in p.parts for p in published)
    assert all(non_owned(exam)[k]==v for k,v in before.items())
