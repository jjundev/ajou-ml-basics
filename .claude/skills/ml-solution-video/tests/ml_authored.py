"""Acceptance-only authoring inspected against the fixed 1007 PDFs; never runtime inference."""
from pathlib import Path
from fractions import Fraction
import hashlib
import shutil
import subprocess
from solution_video.util import read,write,local,file_hash
from solution_video.manifest import content_fingerprint
from solution_video.bundle_layers import extract_bundle,flatten_layers
from solution_video.contracts import InputError
from solution_video.ml_cards import source_markup
from review_sources import CardFragments
from test_writing_units import unit
# Authored semantic steps, column extents and physical row breaks (PDF points).
LAYOUTS={
 'P2':[(496,65,908,120,[85,101]),(496,120,908,240,[140,158,175,190,204,222]),(496,240,908,389,[260,287,302,330,352]),(496,389,908,535,[411,430,445,464,478,499]),(908,65,1287,195,[85,104,119,138,151,175]),(908,195,1287,270,[222,246]),(496,600,1287,657,[631])],
 'P3':[(496,249,1287,314,[272,291]),(496,314,1287,395,[338,354,372]),(496,395,1287,442,[418]),(496,442,1287,477,[]),(496,477,1287,511,[]),(496,600,1287,657,[631])],
 'P8':[(496,65,908,117,[86]),(496,117,908,227,[135,156,171,189,204]),(496,227,908,373,[247,264,283,298,318,333,352]),(496,373,908,517,[389,409,423,442,457,477,491]),(496,517,908,564,[535]),(908,65,1287,168,[85,100,117,132,145]),(908,168,1287,317,[190,220,242,270,294]),(496,566,1287,657,[594,611,628])]}
# The authored rectangles and row breaks were measured on these exact PDFs.
AUTHORED_REVISION = '2e09a745fd8eb71a106ce73782c54ac541b9f6f3'
AUTHORED_STEM = '복습문제_1007_Product_of_Gaussians'
PACKAGE = Path('복습노트/1007')

SOURCE_HASHES={'복습문제_1007_Product_of_Gaussians.cards.json': '589a0ecf14f90c615c0f4a45a859dbdacac83f39b93b40d7a721d1d27c7eb0c8', '복습문제_1007_Product_of_Gaussians-답안.pdf': '154f174733cb6829235d580736ca45b0d8daf5af5412825bdfdc3c95c76e4d2d', '복습문제_1007_Product_of_Gaussians.html': '46455ef75fa1c4f084f5fddfbf87864d4f5a66af8a62f8417f674c2e3d7b36c1', '복습문제_1007_Product_of_Gaussians-문제.pdf': '8783330c3aaef9dd3822f09ecb23be69746265ec30e0d1aae8ffdf1b1bb4bc92', '복습문제_1007_Product_of_Gaussians.md': '7da68168f9ff9f54e26a244a5daee8a27df8608856d2f20398a567a739152d1f'}
def stage_authored_fixture(repo, scratch):
    """Combine the equivalent published card archive with the pinned PDF geometry."""
    repo, scratch = Path(repo).resolve(), Path(scratch).resolve()
    if scratch == repo or scratch.is_relative_to(repo / '복습노트'):
        raise InputError('acceptance requires a separate scratch destination')
    archive_name = AUTHORED_STEM + '.cards.json'
    archive = repo / PACKAGE / '.pack' / archive_name
    if file_hash(archive) != SOURCE_HASHES[archive_name]:
        raise InputError('acceptance card archive changed; reinspect before authoring')

    def original(filename):
        try:
            data = subprocess.check_output(
                ['git', '-C', str(repo), 'show', f'{AUTHORED_REVISION}:{PACKAGE / filename}'],
                stderr=subprocess.DEVNULL,
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            raise InputError(f'authored acceptance requires the Git fixture at {AUTHORED_REVISION}') from exc
        if hashlib.sha256(data).hexdigest() != SOURCE_HASHES[filename]:
            raise InputError('historical acceptance fixture hash mismatch: ' + filename)
        return data

    historical = CardFragments(original(AUTHORED_STEM + '.html').decode('utf-8'))
    archived = CardFragments(source_markup(archive))
    if (archived.cards, archived.interaction) != (historical.cards, historical.interaction):
        raise InputError('archived card markup differs from the authored acceptance fixture')

    fixture = scratch / PACKAGE
    pdfs = {AUTHORED_STEM + suffix: original(AUTHORED_STEM + suffix)
            for suffix in ('-문제.pdf', '-답안.pdf')}
    if fixture.exists():
        for name in (archive_name, AUTHORED_STEM + '.md', *pdfs):
            path = fixture / '.pack' / name
            if not path.is_file() or file_hash(path) != SOURCE_HASHES[name]:
                raise InputError('choose a new scratch directory for the pinned acceptance fixture')
    else:
        shutil.copytree(repo / PACKAGE, fixture)
        for name, data in pdfs.items():
            (fixture / '.pack' / name).write_bytes(data)
    return fixture


SPEECH={
 'P2':[
  ('입력을 고정하면 특징 벡터는 상수가 됩니다.','φ(x*)는 6차원 특징 벡터입니다.','고정된 특징 벡터의 전치와 파라미터 벡터를 곱합니다.','f(x*) = φ(x*)ᵀθ입니다.'),
  ('파라미터의 사전 평균이 영벡터이므로 함수 평균도 영입니다.','E[θ] = 0이므로 평균은 0입니다.','아핀 변환의 평균 공식을 적용합니다.','E[f(x*)] = φ(x*)ᵀE[θ] = 0입니다.'),
  ('파라미터의 공분산으로 함수값의 분산을 계산합니다.','Σθ = (1/2)I를 사용합니다.','특징 벡터의 제곱 길이에 이분의 일을 곱합니다.','var[f(x*)] = (1/2)φ(x*)ᵀφ(x*)입니다.'),
  ('입력이 영이면 상수 특징만 일이 됩니다.','φ(0)는 첫 성분만 1입니다.','여섯 성분의 제곱을 더하면 일입니다.','var[f(0)] = 1/2입니다.'),
  ('입력이 일이면 여섯 특징이 모두 일이 됩니다.','φ(1)의 여섯 성분이 모두 1입니다.','제곱 길이가 육이므로 분산은 삼입니다.','var[f(1)] = (1/2) × 6 = 3입니다.'),
  ('가우시안의 아핀 변환도 가우시안입니다.','함수값도 가우시안 분포입니다.','두 입력에서 얻은 평균과 분산을 분포에 넣습니다.','f(0)는 N(0, 1/2)이고 f(1)은 N(0, 3)입니다.'),
  ('두 점의 평균은 같지만 분산은 다릅니다.','평균은 0이고 분산은 1/2와 3입니다.','원본 답안과 평균 및 분산을 대조합니다.','E[f(0)] = E[f(1)] = 0입니다.')],
 'P3':[
  ('가우시안 사후분포는 평균에서 가장 높습니다.','사후분포의 최빈값은 평균입니다.','맵 추정값을 사후 평균으로 적습니다.','θ_MAP = m_N입니다.'),
  ('고정된 특징 벡터에 사후 평균을 곱하면 평균 함수입니다.','평균 함수는 φ(x*)ᵀm_N입니다.','맵 함수와 사후 평균 함수가 같음을 확인합니다.','MAP 함수는 BLR 사후 평균 함수입니다.'),
  ('음영은 잡음 없는 함수값의 불확실성을 보여 줍니다.','교과서 표기는 67%와 95% 구간입니다.','데이터 주변에서 좁고 양 끝에서 넓은 음영을 읽습니다.','함수값의 불확실성이 음영으로 나타납니다.'),
  ('사후분포는 하나의 함수가 아닌 함수들의 분포입니다.','여러 곡선은 사후 함수 표본입니다.','각 곡선이 그럴듯한 함수 실현임을 적습니다.','함수 위의 사후분포에서 표본을 얻습니다.'),
  ('파라미터를 사후분포에서 뽑아 함수로 바꿉니다.','θ_i를 뽑고 φ(·)ᵀθ_i를 만듭니다.','데이터가 있는 곳에서 함수들이 가까워짐을 봅니다.','데이터 주변에서는 표본 곡선들이 가깝습니다.'),
  ('맵 함수와 음영 및 표본의 의미를 다시 확인합니다.','MAP 함수와 신뢰 구간 및 함수 표본을 구분합니다.','원문 정답의 세 가지 해석을 대조합니다.','음영과 표본은 서로 다른 표현입니다.')],
 'P8':[
  ('입력과 무관한 정규화 상수를 비례식에서 분리합니다.','x와 무관한 상수는 비례식에서 분리합니다.','두 가우시안의 지수를 더합니다.','밀도의 곱에서는 지수를 더합니다.'),
  ('공분산의 역행렬이 대칭이므로 교차항을 묶습니다.','A⁻¹와 B⁻¹의 대칭성을 사용합니다.','각 이차형식을 펼쳐 교차항 두 개를 합칩니다.','이차항과 교차항 및 상수항으로 펼칩니다.'),
  ('정밀도 합과 정밀도로 가중한 평균을 따로 둡니다.','Λ = A⁻¹ + B⁻¹입니다.','이차항과 일차항 및 상수항을 묶습니다.','η = A⁻¹a + B⁻¹b입니다.'),
  ('평균 후보를 정하면 같은 상수를 더하고 뺄 수 있습니다.','m = Λ⁻¹η로 놓습니다.','완전제곱식을 펼쳐 원래 이차형식과 대조합니다.','완전제곱식으로 원래 지수를 정리합니다.'),
  ('남은 상수는 입력과 무관합니다.','γ − ηᵀΛ⁻¹η는 x와 무관합니다.','상수를 비례 계수로 보내 가우시안 꼴을 남깁니다.','남은 지수는 가우시안의 이차형식입니다.'),
  ('정밀도는 공분산의 역행렬입니다.','C = (A⁻¹ + B⁻¹)⁻¹입니다.','가우시안 지수와 계수를 맞춰 평균을 읽습니다.','c = C(A⁻¹a + B⁻¹b)입니다.'),
  ('일차원에서는 행렬이 분산 스칼라가 됩니다.','1차원에서는 A와 B가 분산입니다.','공분산과 평균 식이 스칼라 곱 공식과 같음을 봅니다.','스칼라 곱 공식과 결과가 같습니다.'),
  ('평균과 공분산의 순서 및 역행렬을 점검합니다.','공분산은 정밀도 합의 역행렬입니다.','원본 정답의 공분산과 평균을 대조합니다.','평균은 정밀도로 가중한 평균입니다.')]}

def author_units(page,pid):
 gs={g['id']:g for g in page['glyphs']};ss={s['id']:s for s in page['shapes']}
 for si,(step,layout) in enumerate(zip(page['map']['steps'],LAYOUTS[pid])):
  breaks=layout[4];bins=[[] for _ in range(len(breaks)+1)]
  for kind,ids,objects in [('glyph',step['glyph_ids'],gs),('shape',step['shape_ids'],ss)]:
   for ident in ids:
    o=objects[ident];b=o['bbox'];row=sum((b[1]+b[3])/2>=edge for edge in breaks);bins[row].append((kind,o))
  units=[]
  for ri,targets in enumerate(bins):
   if not targets:continue
   intervals=sorted((o['bbox'][0],o['bbox'][2]) for kind,o in targets if kind=='glyph' and not o['text'].isspace() or kind=='shape' and o['bbox'][2]-o['bbox'][0]<30);merged=[]
   for lo,hi in intervals:
    if merged and lo<merged[-1][1]:merged[-1][1]=max(hi,merged[-1][1])
    else:merged.append([lo,hi])
   left=min(o['bbox'][0] for _,o in targets);right=max(o['bbox'][2] for _,o in targets);cuts=sorted(set([left,right]+[(a[1]+b[0])/2 for a,b in zip(merged,merged[1:])]+([900] if left<900<right else [])))
   if len(cuts)==1:cuts.append(cuts[0]+1)
   for bi,(lo,hi) in enumerate(zip(cuts,cuts[1:])):
    selected={kind:[] for kind in ('glyph','shape')}
    for kind,o in targets:
     b=o['bbox'];zero=b[2]==b[0] or kind=='glyph' and o['text'].isspace()
     if (zero and (lo<=b[0]<hi or bi==len(cuts)-2 and b[0]==hi)) or (not zero and b[0]<hi and b[2]>lo):selected[kind].append(o['id'])
    if not any(selected.values()):continue
    chunk=1 if lo>=900 and left<900 else 0;chunk_id=f'chunk_{si}_{ri}_{chunk}';line=f'line_{si}_{ri}';change=bool(units) and units[-1]['line_id']==line and units[-1]['chunk_id']!=chunk_id
    units.append(unit(f'u_{si}_{ri}_{bi}',[lo,hi],selected['glyph'],selected['shape'],line=line,chunk=chunk_id,column='right' if layout[0]>=908 else 'left',camera_break=change))
  step['writing_units']=units
 return page

def author_run(run):
 run=Path(run);bundle=read(run/'source/pair.json')
 for role in (('cards' if 'cards' in bundle['source_files'] else 'html'),'md','problem_pdf','answer_pdf'):
  path=local(run,bundle['source_files'][role]);expected=SOURCE_HASHES['복습문제_1007_Product_of_Gaussians'+({'cards':'.cards.json','html':'.html','md':'.md','problem_pdf':'-문제.pdf','answer_pdf':'-답안.pdf'}[role])]
  if file_hash(path)!=expected:raise InputError('acceptance fixture source changed; reinspect before authoring')
 pid=bundle['problem_id'];candidate=read(run/'layers/candidates.json')['pages']['answer-1'];layouts=LAYOUTS[pid];steps=[]
 from solution_video.pdf_pages import inside
 work=[496,249 if pid=='P3' else 65,1287,657];selected=[o for o in candidate['glyphs']+candidate['shapes'] if inside(o['bbox'],work)]
 for i,layout in enumerate(layouts):
  objects=[o for o in selected if layout[0]<=(o['bbox'][0]+o['bbox'][2])/2<layout[2] and layout[1]<=(o['bbox'][1]+o['bbox'][3])/2<layout[3]]
  steps.append(dict(id=f's{i+1}',glyph_ids=[o['id'] for o in objects if o in candidate['glyphs']],shape_ids=[o['id'] for o in objects if o in candidate['shapes']]))
 accounted=[j for s in steps for j in s['glyph_ids']+s['shape_ids']]
 if set(accounted)!={o['id'] for o in selected} or len(accounted)!=len(set(accounted)):raise InputError('acceptance authored rectangles do not cover PDF')
 page=dict(candidate,map=dict(work_bbox=work,steps=steps,answer_step_id=steps[-1]['id']),glyphs=[g for g in candidate['glyphs'] if g['id'] in accounted],shapes=[s for s in candidate['shapes'] if s['id'] in accounted]);author_units(page,pid)
 mp=dict(schema_version=2,pages={'answer-1':dict(work_bbox=work,steps=steps,terminal_step_id=steps[-1]['id'])},step_order=['answer-1::'+s['id'] for s in steps],answer_step_id='answer-1::'+steps[-1]['id']);write(run/'source/map.json',mp)
 layers=extract_bundle(read(run/'layers/candidates.json'),mp);flat=flatten_layers(layers)
 card_kind='cards' if 'cards' in bundle['source_files'] else 'html'
 refs=[card_kind+':'+bundle['source_files'][card_kind]+'#'+pid.lower(),'md:'+bundle['source_files']['md']+'#'+pid.lower(),'pdf:'+bundle['source_files']['answer_pdf']+'#page='+str(bundle['answer_pages'][0]['page_index']+1)]
 def segment(ident,kind,step,text,caption,page_id):return dict(id=ident,kind=kind,step_id=step,page_id=page_id,text=text,caption_text=caption,source_refs=refs,chunks=[dict(id='c1',text=text,caption_text=caption)])
 segments=[segment('problem','problem','', '원본 문제의 조건과 물음을 확인합니다.','원본 문제의 조건과 물음을 확인합니다.','problem-1')];lesson=[];coverage=[];math=[]
 for i,(step,speech) in enumerate(zip(flat['map']['steps'],SPEECH[pid])):
  sid=step['id'];reason,rc,spoken,caption=speech;segments.extend([segment(f'reason{i}','reason',sid,reason,rc,'answer-1'),segment(f'write{i}','write',sid,spoken,caption,'answer-1')]);lesson.append(dict(step_id=sid,mode='reasoned',meaning_notes=reason,source_refs=refs,reason_segment_ids=[f'reason{i}'],check_segment_ids=[],region_ids=[],annotation_ids=[]))
  glyphs={g['id']:g for g in flat['glyphs']};text=''.join(glyphs[g]['text'] for g in step['glyph_ids']);coverage.append(dict(step_id=sid,source_refs=refs,pdf_text=text,md_text=bundle['card']['steps'][min(i,len(bundle['card']['steps'])-1)],meaning_review='Directly compared fixed PDF step, HTML card and MD; PDF glyph paint order is preserved.'))
  details={
   'P2':dict(variables='θ and φ have 6 components; x* fixed scalar; f scalar',dimensions='φ, θ: (6,1); φᵀθ scalar; A=(1,6), Σθ=(6,6)',assumptions='Prior θ~N(0,(1/2)I), noiseless f, x*=0 or1',derivation='Affine Gaussian mean φᵀ0=0; variance φᵀΣθφ=(1/2)sum x^(2k), k=0..5',numeric_checks=f'E0=E1=0; var0={Fraction(1,2)}; var1={6*Fraction(1,2)}',visual_checks='Original transpose, covariance fraction and final means/variances compared; no invented graph'),
   'P3':dict(variables='θ_MAP=m_N, S_N posterior covariance, fixed φ(x*)',dimensions='θ,m_N,φ are 6-vectors; S_N 6x6; function mean scalar',assumptions='Gaussian posterior; noiseless latent function, fixed training data',derivation='Gaussian mode equals mean; E[φᵀθ|X,y]=φᵀm_N=φᵀθ_MAP',numeric_checks='Not applicable: this task interprets a posterior function figure, no numeric substitution',visual_checks='Compared original figure: dark67/light95 course labels, narrower near data and wider at edges; sampled curves are functions, not observed noise. 67% is source convention, not exact 1σ mass.'),
   'P8':dict(variables='x,a,b,c in R^d; A,B,C covariance; Λ precision, η information vector',dimensions='A,B,C,Λ dxd; η,c d-vector; quadratic form scalar',assumptions='A,B symmetric positive definite, inverses exist; proportionality drops only x-independent constants',derivation='Λ=A^-1+B^-1; η=A^-1a+B^-1b; m=Λ^-1η; complete square residual γ-ηᵀΛ^-1η; C=Λ^-1,c=Cη',numeric_checks='Internal check d=1, A=2,B=3,a=1,b=4: C=6/5,c=11/5; expansion constants agree. This check is not narrated as a new problem.',visual_checks='Compared all original minus signs, transposes, inverse order, fraction bars and scalar ν0/ν1 expressions')}
  math.append(dict(step_id=sid,source_refs=refs,meaning_review=reason,**{k:dict(applicable=not v.startswith('Not applicable'),evidence=v) for k,v in details[pid].items()}))
 if pid=='P3':
  source=candidate['metadata']['source_sha256'];region=dict(id='graph',page_id='answer-1',source_sha256=source,bbox=[750,60,1050,240])
  focus=dict(schema_version=2,regions=[region],cues=[dict(segment_id='reason2',target='graph')])
  annotations=dict(schema_version=2,items=[dict(id='band',region_id='graph',segment_id='reason2',chunk_id='c1',offset_frames=0,kind='ellipse',geometry=dict(bbox=[858,123,953,156]),duration_frames=18,stroke_width_px=6,color='#1565C0',source_refs=refs,meaning_notes='Mark the narrower latent-function uncertainty band around the training inputs.',hide_at=dict(segment_id='reason2',offset_frames=78))])
  write(run/'source/focus.json',focus);write(run/'source/annotations.json',annotations);lesson[2]['region_ids']=['graph'];lesson[2]['annotation_ids']=['band']
 m=dict(schema_version=2,key=bundle['key'],pack_id=bundle['pack_id'],problem_id=pid,title=bundle['title'],segments=segments,reveal_order=[g for step in flat['map']['steps'] for g in step['glyph_ids']],shape_anchors={shape:step['glyph_ids'][0] if next(o for o in flat['shapes'] if o['id']==shape)['kind']=='step_badge' else step['glyph_ids'][-1] for step in flat['map']['steps'] for shape in step['shape_ids']},cameras=[],caption_timing='pcm-chunks-v1');c=dict(status='passed',pdf_md_agree=True,rows=coverage);h=content_fingerprint(m,layers,c);c['input_hash']=h;r=dict(status='passed',input_hash=h,steps=math)
 for name,obj in [('manifest',m),('coverage',c),('math-review',r),('lesson',dict(schema_version=1,steps=lesson))]:write(run/'source'/(name+'.json'),obj)
 return m
