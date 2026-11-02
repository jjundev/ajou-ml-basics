"""Real local CLI/render/browser integration with fake PCM; no paid API calls."""
import argparse,base64,contextlib,io,json,subprocess,sys,wave
from pathlib import Path
from unittest.mock import patch
from _util import ROOT,SKILL,pcm
from test_selection import fixture,manifest_for
from lib.cache import atomic_json,file_hash
from lib.verify import review_fingerprint
from lib.math_evidence import validate_math_evidence
from video import main as video_main


def call(args):
    output=io.StringIO()
    with contextlib.redirect_stdout(output): status=video_main([str(a) for a in args])
    data=json.loads(output.getvalue())
    if status:raise RuntimeError(json.dumps(data,ensure_ascii=False))
    return data


def author(run,plan,clip):
    m=manifest_for(plan,clip);sid=m['scenes'][0]['id']
    m['scenes'][0].update(visual='회귀선과 잔차 제곱합',motion='기울기별 그래프 상태 비교')
    base=m['segments'][0]
    m['segments']=[dict(base,id='seg-'+label,text=f'기울기가 {w}일 때 잔차 제곱합은 {sse}입니다.',caption=f'w = {w} · SSE = {sse}') for label,w,sse in [('start',0,5),('middle',1,0),('end',2,5)]]
    m['coverage_reviews'][0]['segment_ids']=[x['id'] for x in m['segments']]
    atomic_json(run/'manifest.json',m)
    calc=run/'source/calculations';calc.mkdir(parents=True)
    script=calc/'example.py'
    script.write_text("import json\nfrom pathlib import Path\npoints=[(0,0),(1,1),(2,2)]\nrows=[{'w':w,'sse':sum((y-w*x)**2 for x,y in points)} for w in range(3)]\nassert [r['sse'] for r in rows]==[5,0,5]\nPath(__file__).with_name('result.json').write_text(json.dumps(rows))\n")
    subprocess.run([sys.executable,str(script)],check=True)
    rows=json.loads((calc/'result.json').read_text())
    states=[]
    for label,row in zip(['start','middle','end'],rows):
        x=lambda v:70+140*v
        y=lambda v:280-55*v
        points=''.join(f'<circle cx="{x(v)}" cy="{y(v)}" r="6" fill="#f2f4f6"/>' for v in range(3))
        residuals=''.join(f'<line x1="{x(v)}" y1="{y(v)}" x2="{x(v)}" y2="{y(row["w"]*v)}" stroke="#f5a15c" stroke-width="3"/>' for v in range(3))
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="320" viewBox="0 0 480 320"><path d="M70 40V280H420" stroke="#a3abb8" fill="none"/><text x="425" y="290" fill="#f2f4f6">x</text><text x="40" y="35" fill="#f2f4f6">y</text><path d="M70 280 L350 {y(2*row["w"])}" stroke="#3182f6" stroke-width="4"/>{residuals}{points}<text x="80" y="25" fill="#f2f4f6">w={row["w"]}, SSE={row["sse"]}</text></svg>'
        path=run/'assets'/f'{label}.svg';path.parent.mkdir(exist_ok=True);path.write_text(svg)
        states.append({'label':label,'figure_path':path.relative_to(run).as_posix(),'values':row})
    paths=[script,calc/'result.json']+[run/x['figure_path'] for x in states]
    evidence={'schema_version':1,'scenes':[{'scene_id':sid,'mode':'numeric','formula_refs':['SSE=sum((y_i-w*x_i)^2)'],
      'conditions':['Intercept 0; points (0,0),(1,1),(2,2)'],'axes':['x: input','y: observed/predicted'],
      'units':['dimensionless'],'dimensions':['w: scalar'],'calculation_script':script.relative_to(run).as_posix(),
      'calculation_result':(calc/'result.json').relative_to(run).as_posix(),'states':states}],
      'file_hashes':{p.relative_to(run).as_posix():file_hash(p) for p in paths}}
    atomic_json(run/'source/math-evidence.json',evidence)
    assert not validate_math_evidence(run,m)
    fragment=run/'source/scene-fragments';fragment.mkdir()
    images=''.join(f'<img id="{sid}-{x["label"]}" class="video-graph-state" src="{x["figure_path"]}" alt="기울기 {x["values"]["w"]} 그래프">' for x in states)
    body=f'<section class="topic"><h3>회귀선과 잔차 제곱합</h3><div class="tags"><span class="tag">머신러닝기초 · 계산 검증</span></div><div class="layer eli5"><p class="lead">직선이 바뀌면 잔차도 바뀝니다.</p></div><div class="video-graph-stack">{images}</div><div class="layer formal"><p>$$\\mathrm{{SSE}}=\\sum_i(y_i-w x_i)^2$$</p><p>표기 점검: $\\frac{{1}}{{2}}$, $\\int_0^1 x^2 dx$, $x_i$</p></div></section>'
    (fragment/(sid+'.html')).write_text(body)
    motions=[]
    for index,state in enumerate(states):
        label=state['label'];motions.append({'target':'#'+sid+'-'+label,'segment_id':'seg-'+label,'kind':'reveal','from':{'opacity':0},'to':{'opacity':1},'duration_s':.05})
        if index:motions.append({'target':'#'+sid+'-'+states[index-1]['label'],'segment_id':'seg-'+label,'kind':'reveal','from':{'opacity':1},'to':{'opacity':0},'duration_s':.05})
    atomic_json(fragment/(sid+'.motion.json'),motions)
    return m


def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--assets',default=str(SKILL/'assets/runtime'))
    p.add_argument('--hyperframes-entry',required=True);p.add_argument('--puppeteer-package-json',required=True);p.add_argument('--chrome',required=True)
    args=p.parse_args();root=Path(args.run).resolve();root.mkdir(parents=True,exist_ok=True)
    repo=root/'repo';repo.mkdir(exist_ok=True)
    inputs,plan=fixture(repo,1)
    source=Path(plan['sources'][0]['path']);source.write_text('설명용 fixture: 점 (0,0),(1,1),(2,2), 절편 0. w=0,1,2의 SSE는 5,0,5.')
    inputs,plan=fixture_reload(repo,plan)
    plan_path=root/'selection.json';atomic_json(plan_path,plan)
    env=root/'fake.env';env.write_text('GOOGLE_API_KEY=FAKE_SMOKE_KEY_ONLY\n');env.chmod(0o600)
    call(['plan-check','1001','--repo',repo,'--selection',plan_path])
    batch=Path(call(['prepare-set','1001','--repo',repo,'--selection',plan_path,'--env-file',env])['batch'])
    clip=plan['clips'][0];run=batch/'videos'/clip['id'];m=author(run,plan,clip)
    call(['check','--run',run])
    audio=pcm(root/'fake.wav')
    with wave.open(str(audio),'rb') as f:raw=f.readframes(f.getnframes())
    calls=[]
    def fake(payload):
        calls.append(payload)
        return {'candidates':[{'finishReason':'STOP','content':{'parts':[{'inlineData':{'mimeType':'audio/L16;rate=24000','data':base64.b64encode(raw).decode()}}]}}],'usageMetadata':{'promptTokenCount':1,'candidatesTokenCount':1}}
    with patch('urllib.request.urlopen',side_effect=AssertionError('paid API forbidden')),patch('video.live_transport',return_value=fake):
        call(['tts','--run',run,'--env-file',env]);first=len(calls)
        call(['tts','--run',run,'--env-file',env]);assert len(calls)==first==3
    call(['assemble','--run',run,'--pack',ROOT/'.agents/skills/ml-review-pack','--assets-from',args.assets])
    call(['render','--run',run,'--hyperframes-entry',args.hyperframes_entry])
    review_fixture(run,m,args)
    call(['publish-set','--batch',batch]);resume=call(['resume-set','--batch',batch])
    assert resume['status']=='verified'
    final=repo/'복습영상/1001'/('기울기와 잔차 제곱합.mp4')
    assert final.is_file() and (run/'review.mp4').is_symlink()
    assert not list(batch.rglob('*.env'))
    old_hash=file_hash(run/'review.mp4')
    new=Path(call(['prepare','--repo',repo,'--from-run',run,'--voice','Charon','--env-file',env])['run'])
    call(['check','--run',new])
    with patch('urllib.request.urlopen',side_effect=AssertionError('paid API forbidden')),patch('video.live_transport',return_value=fake):
        call(['tts','--run',new,'--env-file',env]);assert len(calls)==6
    call(['assemble','--run',new,'--pack',ROOT/'.agents/skills/ml-review-pack','--assets-from',args.assets])
    call(['revoice','--run',new,'--source-run',run,'--hyperframes-entry',args.hyperframes_entry])
    review_fixture(new,json.loads((new/'manifest.json').read_text()),args)
    assert (new/'review.mp4').is_symlink() and file_hash(run/'review.mp4')==old_hash
    assert final.is_file() and not list(new.rglob('*.env'))
    summary={'status':'passed','run':str(run),'final':str(final),'fake_requests':len(calls),'paid_requests':0,'resume':resume['status'],'revoice':'verified','revoice_run':str(new),'hyperframes_entry':args.hyperframes_entry}
    atomic_json(root/'summary.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2));return 0


def review_fixture(run,m,args):
    subprocess.run(['node',str(SKILL/'tests/browser_check.mjs'),str(run),args.puppeteer_package_json,args.chrome],check=True)
    browser=json.loads((run/'verification/browser.json').read_text())
    assert browser['status']=='passed'
    timeline=json.loads((run/'source/timeline.json').read_text())
    for seg in timeline['segments']:
        mid=(seg['start_sample']+seg['end_sample'])/48000
        row=next(r for r in browser['results'] if abs(r['time']-mid)<.001 and r['osTheme']=='dark')
        assert row['graphStates']==['scene-atp-'+seg['id'].removeprefix('seg-')]
    evidence=run/'verification/smoke-review.txt'
    evidence.write_text('Synthetic fixture only. SSE=5/0/5 oracle checked. Fake sine PCM, no speech or live authentication claim. Browser states and media are real.')
    key=review_fingerprint(run,m)
    reports={d:{'status':'passed','evidence':['verification/smoke-review.txt']+(['verification/browser.json'] if d=='visual' else []),'errors':[],'input_hash':key} for d in ['content','audio','visual']}
    atomic_json(run/'verification/reviews.json',reports)
    result=call(['verify','--run',run,'--hyperframes-entry',args.hyperframes_entry])
    assert result['status']=='passed'


def fixture_reload(repo,plan):
    from lib.sources import discover
    inputs=discover(repo,'1001');plan['sources']=inputs['files'];src=inputs['files'][0]
    plan['source_reviews']=[{'source_id':src['id'],'status':'reviewed','reason':'Synthetic fixture: slope 0/1/2, SSE 5/0/5; no preview topics'}]
    for row in plan['topics']:row['source_id']=src['id']
    plan['topics'][0].update(claim='절편 0인 직선의 기울기 0/1/2에서 잔차 제곱합 5/0/5',reason='직선과 잔차의 상태 변화')
    plan['clips'][0].update(title='기울기와 잔차 제곱합',learning_question='기울기를 바꾸면 잔차 제곱합이 어떻게 변하는가',visual_states=['w=0, SSE=5','w=1, SSE=0','w=2, SSE=5'])
    return inputs,plan

if __name__=='__main__':raise SystemExit(main())
