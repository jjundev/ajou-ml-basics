import json, subprocess, sys
from pathlib import Path
import pytest

def cli(repo, *args):
    return subprocess.run([sys.executable,str(repo/'.claude/skills/ml-midterm/scripts/midterm_cli.py'),*map(str,args)],capture_output=True,text=True,encoding='utf-8')

def test_init_selects_next_and_rejects_existing(repo,tmp_path):
    r=cli(repo,'init','--repo',tmp_path,'--run',tmp_path/'run')
    assert r.returncode==0, r.stderr+r.stdout
    value=json.loads(r.stdout)
    assert value['round']==1 and value['mode']=='create'
    assert not (tmp_path/'중간고사대비').exists()
    r=cli(repo,'init','--repo',tmp_path,'--run',tmp_path/'run')
    assert r.returncode==1
    (tmp_path/'중간고사대비/예상문제_2회').mkdir(parents=True)
    r=cli(repo,'init','--repo',tmp_path,'--round',2,'--run',tmp_path/'collision')
    assert r.returncode==1
    r=cli(repo,'init','--repo',tmp_path,'--run',tmp_path/'next')
    assert json.loads(r.stdout)['round']==3

def test_explain_target_resolution(repo,exam,baseline):
    from exam_config import resolve_exam_target
    from test_build import source_for
    source=source_for(exam)
    explanation=exam.output/f'문제설명_{exam.range_}_{exam.slug}.html';explanation.write_text('test', encoding='utf-8')
    for target in (str(source),str(explanation)):
        assert resolve_exam_target(repo,target)==exam
    assert resolve_exam_target(repo,'중간고사 1회').round_number==1
    (exam.output/'중간고사예상_duplicate.html').write_text('', encoding='utf-8')
    with pytest.raises(ValueError,match='ambiguous'):resolve_exam_target(repo,str(source))
    with pytest.raises(ValueError):resolve_exam_target(repo,'../outside.html')

def test_cli_explain_never_runs_base(repo,exam,tmp_path,monkeypatch,capsys):
    from midterm_cli import main
    from test_explain import prepare,non_owned
    import build_exam
    prepare(exam);before=non_owned(exam)
    def forbidden(*a,**k):raise AssertionError('explain invoked base')
    monkeypatch.setattr(build_exam,'build_base',forbidden)
    assert main(['explain','--repo',str(repo),'--out',str(exam.output),'--run',str(tmp_path/'run')])==0
    assert non_owned(exam)==before

def test_check_rejects_incomplete_delivery(repo,exam,tmp_path):
    from test_explain import prepare,non_owned
    prepare(exam);before=non_owned(exam)
    r=cli(repo,'check','--repo',repo,'--out',exam.output)
    assert r.returncode==1, r.stdout+r.stderr
    value=json.loads(r.stdout)
    assert value['status']=='fail' and value['errors']
    assert before==non_owned(exam)

def test_publication_failure_restores_existing_files(repo,exam,tmp_path,monkeypatch):
    from test_explain import prepare,approved_test_review,non_owned
    from build_exam import build_explain,publish_explain
    import review_pdf_publish
    prepare(exam);before=non_owned(exam);run=tmp_path/'run'
    result=build_explain(repo,exam.output,run);approved_test_review(result)
    target=exam.output/result['artifacts'].html.name;target.write_text('previous valid explanation', encoding='utf-8')
    original=review_pdf_publish._replace_copy;calls=0
    def fail_second(src,dst):
        nonlocal calls
        calls+=1
        if calls==2:raise OSError('injected replacement failure')
        return original(src,dst)
    monkeypatch.setattr(review_pdf_publish,'_replace_copy',fail_second)
    with pytest.raises(ValueError):publish_explain(repo,exam.output,run)
    assert target.read_text(encoding='utf-8')=='previous valid explanation'
    assert all(non_owned(exam)[k]==v for k,v in before.items())
    assert not (run/'publish-result.json').exists()

def test_check_rejects_wrong_round_and_incomplete_browser(baseline,repo):
    from check_exam import validate_browser_report
    from exam_adapter import sha
    path=baseline/'문제설명_0909-1019_Midterm_Practice_01.html'
    report=json.loads((baseline/'.pack/evidence/browser-check.json').read_text(encoding='utf-8'))
    assert validate_browser_report(report,path)==[]
    report['original_checks'].pop()
    assert validate_browser_report(report,path)
    report=json.loads((baseline/'.pack/evidence/browser-check.json').read_text(encoding='utf-8'))
    report['html_sha256']='0'*64
    assert validate_browser_report(report,path)

def test_browser_report_uses_summary_terms_placement(baseline, tmp_path):
    from check_exam import validate_browser_report
    from exam_adapter import sha

    source = baseline/'문제설명_0909-1019_Midterm_Practice_01.html'
    html = source.read_text(encoding='utf-8')
    before, p8 = html.split('<article class="topic" id="p8">', 1)
    article, after = p8.split('</article>', 1)
    article = article.replace('data-problem-panel="terms"', 'data-problem-panel="terms" data-summary-terms=""', 1)
    path = tmp_path/'summary-terms.html'
    path.write_text(before+'<article class="topic" id="p8">'+article+'</article>'+after, encoding='utf-8')

    report = json.loads((baseline/'.pack/evidence/browser-check.json').read_text(encoding='utf-8'))
    report['html_sha256'] = sha(path)
    assert 'browser topic/tab mismatch' in validate_browser_report(report, path)
    report['tab_order'].remove('terms')
    assert validate_browser_report(report, path) == []

def test_source_round_and_repository_must_match(repo,exam,tmp_path):
    from test_build import source_for
    from exam_adapter import load_exam_source
    p=source_for(exam);bp=exam.output/'.pack/blueprint.json'
    wrong=p.with_name(p.name.replace('_02','_03'));wrong.write_text(p.read_text(encoding='utf-8'), encoding='utf-8')
    with pytest.raises(ValueError,match='identity'):load_exam_source(wrong,bp,repo,exam)
    with pytest.raises(ValueError):load_exam_source(p,bp,tmp_path,exam)
