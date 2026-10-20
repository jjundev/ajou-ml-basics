import json,pathlib,hashlib,collections
out=pathlib.Path(__file__).parent
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
current=json.loads((out/'current-read-evidence.json').read_text())
# Written after reading the actual current source cards, original excerpts, all seven layers and summaries.
# These are academic content judgments, not a blind derivation or a test suite.
reasons={
'0909':[
 ['At x=10 the three products are -10,5,20; division by the nonzero input restores the three slopes.', 'Absolute slopes are 1,1/2,2, so theta=2 is steepest. Retained signed-slope shorthand is valid only with the explicit absolute-value correction in solve/verify/pitfall/sum.'],
 ['A is 3x2 and B is 3x3: inner dimensions 2 and 3 do not match, so the product is undefined, not zero.'],
 ['For AB, columns are sums of the selected columns of A: rows [4,3,5],[10,9,11],[16,15,17]. Every column-major TeX entry matches these rows.', 'For BA, selected row sums give [5,7,9],[11,13,15],[8,10,12]. Same shape does not imply AB=BA.'],
 ['(2x4)(4x2) gives 2x2. Four row-column sums give [14,6],[-21,2]; last entry 12-1-1-8=2 checks the negative signs.'],
 ['(4x2)(2x4) gives 4x4, with rows [12,3,-3,-12],[-3,1,2,6],[6,5,1,0],[13,12,3,2]. This is not a transpose of the previous 2x2 product.']
],
'0914':[
 ['Appending the unit feature to (2,-1) gives [1,2,-1]^T, length D+1=3, matching the coefficient length.', 'The ordered inner product is 1/2+6-2=9/2; the affine form produces the same scalar.'],
 ['Each data point is one row: X=[[1,0],[1,1],[1,2]], y=[1,4,4]^T; X is 3x2.', 'A predicts [1,3,5] with squared residual sum 2; B predicts [3/2,3,9/2] with sum 3/2; division by N=3 gives 2/3 and 1/2.', 'B is the better of these candidates because 2/3-1/2=1/6>0. The text correctly avoids asserting that this candidate comparison alone proves a global optimum.'],
 ['At lambda=0, A has loss 0 and B 5/3, so A wins.', 'Including the bias in the specified penalty gives norms squared 5 and 2: at lambda=1 scores are 5 and 11/3, so B wins. The crossover is lambda=5/9.'],
 ['Conditioning on fixed x and theta, x^T theta=5 shifts zero-mean noise and leaves its variance 1: the result is N(5,1).'],
 ['For independent common fixed variance Gaussian noise, -log likelihood=SSE/(2 sigma^2)+N log(2 pi sigma^2)/2; sigma^2=1,N=3 gives the constant 3 log(2pi)/2.', 'Using SSE 2 and 3/2 gives NLLs 3.7568156... and 3.5068156..., correctly rounded to 3.757 and 3.507.', 'A-B=1/4>0; identical positive scale and additive constant preserve SSE candidate ordering, so B wins.'],
 ['x-y=[2,3,3]^T; its squared Euclidean norm is 4+9+9=22, so distance is sqrt(22), not 22. Reversing the difference leaves the result unchanged.'],
 ['Derivative 3x^2+12x-3 has roots -2±sqrt5; second derivative at those roots is ±6sqrt5. Thus the minus root is a local maximum, plus root a local minimum; values are 17±10sqrt5. The cubic is unbounded in both directions, so these are not global extrema.']
],
'0916':[
 ['Taking the negative log of the explicitly displayed Gaussian prior yields D log(2pi)/2+log|Sigma|/2+theta^T Sigma^-1 theta/2. This ordinary density needs a fixed positive definite covariance; singular covariance does not support this determinant/inverse formula.', 'Bayes evidence does not depend on theta, so MAP minimizes NLL plus the prior quadratic term. Fixed nonsingular covariance and optimization over theta only are essential; Sigma-dependent constants cannot be dropped when Sigma is optimized.'],
 ['Column sums of the visually checked 3x5 joint table are [16,17,11,22,34]/100; the total is 1. Marginalization sums over Y, rather than normalizing each column.'],
 ['Row sums are [26,47,27]/100; top row is y1, as specified in both the current card and MML table. The total is 1.'],
 ['The y1 row masses [1,2,3,10,10]/100 divided by its positive marginal 26/100 give [1,2,3,10,10]/26. The displayed reduced fractions sum to 1 and multiply back to the original row.'],
 ['Column x3 masses [3,5,3]/100 divided by 11/100 give [3,5,3]/11, in y1,y2,y3 order. These sum to 1 and recover the source column on multiplication.'],
 ['The i.i.d. Bernoulli likelihood has exponents k and N-k; multiplying a proper Beta(alpha,beta) prior adds alpha-1,beta-1, giving Beta(alpha+k,beta+N-k). For N=10,k=2,alpha=beta=4, mode=5/16 and mean=1/3 differ as disclosed.']
],
'0921':[
 ['The represented factor p(c|a,b) assigns c the graphical parents a,b. It does not prove every distribution has nonzero statistical dependence on each parent.', 'The represented p(b|a) assigns a as the graphical parent of b. This is a factorization reading, not a causal claim.', 'The factor p(a) has no conditioning parents. It does not imply marginal independence of a from descendants b,c; the retained reference answer is explicitly restricted in verify and pitfall.'],
 ['The three parent-to-child arrows are a→b,a→c,b→c, matching the inspected Figure 8.9(a).', 'There is one edge for each of the three unordered pairs; topological order a,b,c excludes a directed cycle. Fully connected here describes the skeleton.'],
 ['Five nodes require five node factors, including root marginal factors.', 'The source SVG arrowheads, visually re-rendered here, give Pa(x1)=Pa(x5)=empty, Pa(x2)={x5}, Pa(x3)={x1,x2}, Pa(x4)={x2}; these agree with MML Figure 8.9(b).', 'Only x2→x4 enters x4, hence its factor is p(x4|x2). x5 is an ancestor rather than an extra direct parent.'],
 ['The exact five-factor product is p(x1)p(x5)p(x2|x5)p(x3|x1,x2)p(x4|x2), matching MML (8.30). Every node is the target of exactly one factor; reverse topological integration/summation gives normalization 1.'],
 ['Joint mango masses are (3/5)(2/3)=2/5 for bag1 and (2/5)(1/2)=1/5 for bag2. Evidence is 3/5, so P(bag2|mango)=1/3; posterior odds 2:1 give the same result.'],
 ['For E|X|<infinity, substitute p(x|y)p(y)=p(x,y), apply Fubini, and marginalize y to obtain integral x p(x) dx=E[X]. Conditional values on p(y)=0 sets do not change the outer expectation. The nonintegrable case is not unconditionally approved.']
],
'0923':[
 ['The scalar Gram term is 1+4+16=21>0, so the scalar inverse exists.', 'The input-label product sum is 2+10+28=40.', 'SSE=21 theta^2-80 theta+78 has unique minimum theta=40/21 and value 38/21 because its second derivative is 42>0. ML attribution assumes independent common positive Gaussian noise; source gives the estimator and marginal Gaussian setting, not a fully specified joint likelihood.'],
 ['Counting repeated x=1 observations separately gives X^T X=6 and X^T y=12.', 'The scalar normal equation 6 theta=12 gives theta=2; residual [-1,1,0] is orthogonal to X and SSE=2. This is an exact least-squares solution. Calling it ML requires the intended independent common-variance Gaussian model, which this card does not specify separately.'],
 ['K=4 means powers 0 through 3, so phi(2)=[1,2,4,8]^T.', 'The dot product is 1-4+0+8=5, matching direct substitution in 1-2x+x^3. Linear refers to coefficients.'],
 ['K=3 gives phi(3)=[1,3,9]^T; the zero linear coefficient does not remove the middle feature.', 'The ordered dot product is 2+0-9=-7, matching 2-x^2 at x=3.'],
 ['The stated row eliminations are arithmetically consistent and end at [0,0,0,0|1]; coefficient rank 3 versus augmented rank 4 proves S is empty. This does not deny the existence of a least-squares approximation.'],
 ['R3=2R2-R1 shows row dependence; first two rows are independent, so rank=2. Determinant -2+6-4=0 and null vector [1,-2,1] give separate singularity criteria.'],
 ['Gauss–Jordan operations are applied to both halves of [A|I]. The proposed inverse rows [0,-1,0,1],[-1,0,0,1],[1,1,0,-1],[1,1,1,-2] give identity in both multiplication orders, as also established by the frozen controller comparison.']
],
'0928':[
 ['Putting one transposed feature vector in each row gives [1,-1,1],[1,1,1],[1,2,4]. The design matrix is 3x3 and Phi theta is 3x1; squaring -1 gives +1.'],
 ['The current authoritative adaptation uses degree 3, hence four features [1,x,x^2,x^3]. MML Example 9.5 instead used degree 4; its historical quotation is not the current numerical question.', 'For the current N=8, degree3 adaptation, Phi is 8x4. The original book figure uses N=10, degree4 and must not overwrite the stated current values.', 'For fixed positive Gaussian noise variance and full column rank 4, the normal equation yields (Phi^T Phi)^-1 Phi^T y. At least four distinct inputs suffice for these monomial columns; in rank-deficient cases the inverse formula and uniqueness fail, as disclosed.'],
 ['Noise variance is (0.2)^2=1/25 and prior variance is 1/4, so lambda=(1/25)/(1/4)=4/25=0.16. The adapted prior is I/4, whereas the inspected MML example uses I.', 'Figure9.7 illustrates greater regularization visibility for the historical degree8 fit than degree6. No realized design/labels or quantitative effect criterion is supplied for this adapted prior, so a universal ordering is underdetermined. y=0 gives zero estimates at both degrees. Current solve/verify/pitfall and summary disclose this; approve only the example-specific interpretation.'],
 ['On real x≠0, product and chain rules give (4/x)sin(x^3)+3x^2 log(x^4)cos(x^3). The identity log(x^4)=4log|x| preserves negative x; replacing it by 4log x requires x>0.'],
 ['With fixed mu and sigma≠0, the inner derivative is -(x-mu)/sigma^2, multiplying the original exponential. Its sign changes from positive to negative at mu because sigma^2>0; sigma=0 in the overly broad original R condition is excluded explicitly.'],
 ['For z=x^T x, df/dz is 1x1 and dz/dx=2x^T is 1xD; multiplying gives 2x^T/(1+x^T x). The logarithm is defined for all real x vectors because z≥0.', 'For componentwise sine, df/dz=diag(cos z) is ExE and dz/dx=A is ExD; product is ExD. Component differentiation gives cos(z_i)A_ij, confirming orientation.'],
 ['For componentwise tanh, df/dz=diag(1-tanh^2 z) is MxM, dz/dx=A is MxN, and the product is MxN with entries (1-tanh^2 z_i)A_ij. Bias is fixed and has zero derivative.'],
 ['Two chain-rule negatives cancel: fprime=e^-x/(1+e^-x)^2=f(1-f)>0. At x=0, f=1/2 and derivative=1/4; the domain is all real x.']
]
}
source_notes={
'0909':[
 ([297],'Example9.1 is the real scalar theta x model. Current theta=-1,1/2,2 and x=10 are adapted practice values, not claims about book figure coordinates.'),
 ([70,71],'Exercise2.4(a) matrices visually match the card, including 3x2 then 3x3 dimensions.'),
 ([70,71],'Exercise2.4(b,c) matrix entries and order visually match; card subparts deliberately retain book labels b,c.'),
 ([70,71],'Exercise2.4(d) 2x4 and 4x2 matrices including -1,-4 entries visually match.'),
 ([70,71],'Exercise2.4(e) is the reversed rectangular product, visually matched entry by entry.')],
'0914':[
 ([265],'Example8.1 unit-feature convention and D+1 dimensional predictor match; supplied feature/coefficient numbers are current adaptations.'),
 ([266,267],'Example8.2 and (8.9) use mean squared Euclidean error; current three points/two candidate vectors are adapted and authoritative.'),
 ([268,269],'Example8.3 continues onto269 with N^-1 SSE+lambda||theta||^2. Current candidate values and inclusion of bias follow the displayed current objective.'),
 ([272],'Example8.4 specifies zero-mean independent Gaussian noise and conditional mean x^T theta; current numeric x,theta,sigma^2 are adapted.'),
 ([273],'Example8.5 displays the NLL expansion and fixed-sigma condition; current dataset/candidates remain authoritative.'),
 ([102],'Exercise3.3(a) vectors [1,2,3],[-1,-1,0] and standard inner product match exactly. Book subpart(b) weighted inner product is intentionally not asked.'),
 ([253],'Exercise7.1 polynomial x^3+6x^2-3x-5 and stationary-point classification ask match exactly.')],
'0916':[
 ([204,275],'Example8.6 gives zero-mean multivariate Gaussian prior; actual density formula (6.63) on204 confirms determinant, inverse and half factor. Current density with ordinary inverse requires a nonsingular covariance.'),
 ([228],'Exercise6.1 table visually checked: y1 top row, columns x1..x5, all15 decimals match; p(x) is the selected ask.'),
 ([228],'Same actual table: all15 entries and axis orientation match; p(y) is the selected ask.'),
 ([228],'Same actual table: y1 row and conditional p(x|Y=y1) selection match.'),
 ([228],'Same actual table: x3 column and conditional p(y|X=x3) selection match.'),
 ([228],'Exercise6.3 compiler Bernoulli model matches. Current card explicitly supplies Beta(alpha,beta) and i.i.d. observations; book asks to choose a conjugate prior.')],
'0921':[
 ([285,286],'Example8.7 factors and Figure8.9(a) arrow structure match; book wording about direct dependence is interpreted as graphical parents.'),
 ([285,286],'Figure8.9(a) visually gives a→b,a→c,b→c, all three pairs linked.'),
 ([285,286],'Figure8.9(b) and Example8.8 have five nodes, with arrows x5→x2,x1→x3,x2→x3,x2→x4. Current source SVG was separately rendered and inspected.'),
 ([285,286],'Current source SVG geometry is identical to p3 except ID and was separately captured; it matches Figure8.9(b) and (8.30) five-factor product.'),
 ([228],'Exercise6.4 bag1 4mango/2apple, bag2 4/4, biased coin0.6/0.4 and posterior bag2 ask match exactly.'),
 ([229],'Exercise6.11 total expectation identity and conditioning notation match. Current card specializes to continuous variables; integrability is supplied in the explanation, not presumed unconditional.')],
'0923':[
 ([300,301],'Example9.2 provides fitting-through-origin theory; inspected (9.12) gives estimator/rank condition. Current points (1,2),(2,5),(4,7) are authoritative adaptations, not the plotted book sample.'),
 ([300,301],'Same normal-equation theory. Current repeated x=1 observations and y=(1,3,4) are authoritative; their likelihood assumptions are incompletely stated and retained as a qualification.'),
 ([301,302],'Example9.3 monomial feature convention K and degree K-1 match; current K4,theta=(1,-2,0,1),x2 are adaptations.'),
 ([301,302],'Same feature convention; current K3,theta=(2,0,-1),x3 are adaptations.'),
 ([71],'Exercise2.5(a) all16 matrix entries and b=(1,-2,4,6) visually match.'),
 ([72],'Exercise2.8(a) 3x3 entries visually match, including diagonal2,4,6.'),
 ([72],'Exercise2.8(b) all16 binary matrix entries visually match.')],
'0928':[
 ([302],'Example9.4 design-matrix arrangement matches. Current inputs -1,1,2 are explicit numerical adaptations.'),
 ([302,303],'Example9.5 original figure uses N10 and degree4; current question explicitly changes to N8 and degree3. The noise model/function matches, and current adapted values control all answers.'),
 ([307,308],'Actual (9.31), Example9.6, Figure9.7 degree6/8 plots inspected. Original prior is I; current prior I/4 changes lambda to0.16. Figure supports historical qualitative comparison, not a universal adapted-data ranking.'),
 ([176],'Exercise5.1 function log(x^4)sin(x^3) matches; real-domain x≠0 qualification is necessary.'),
 ([176],'Exercise5.3 exponent -(x-mu)^2/(2sigma^2) matches; book/card broad sigma∈R includes undefined0, explicitly qualified by explanation.'),
 ([177],'Exercise5.7(a,b) functions, dimensions ExD and componentwise sin agree exactly.'),
 ([177],'Exercise5.8(c) tanh composition input N, output M and A of size MxN and explicit permission not to multiply Jacobians agree; the selected current problem retains its full conditions.'),
 ([176],'Exercise5.2 logistic sigmoid matches. Rewriting the derivative using f(x) is an explicit current additional ask and is answered.')]
}
results={'schema_version':1,'role':'academic source_visual/content review','reviewer':'ml_source_content_a','independence':'Not blind: current reference explanations were read. Frozen controller-reference results are supplementary comparison evidence only; no independent approval is asserted.','review_policy_version':'problem-explain-2026-10-15','current_read_evidence':{'path':str(out/'current-read-evidence.json'),'sha256':sha(out/'current-read-evidence.json')},'methodology':'Manually read current source conditions/asks/original excerpts and all seven active fragment sections plus summary. Independently inspect actual rendered MML page pixels against those current questions. SourcePack/DOM collection verifies exact preservation, not semantic approval. Mathematical reasoning below was assessed against source, actual fragments, and disclosed frozen controller comparison.','packs':[],'limitations':['No browser-layout, navigation, grading, or runtime release approval is given by this academic role. Graph-only captures are source figure evidence, not full page/browser validation.','Dated explanation HTML has no inline data-original-problem/original tabs in either current or pre-change version. Original textbook excerpts remain in source cards accessible via the preserved 원 문제 보기 link; this role read those actual source excerpts.','Source MML is the local Draft2024-01-15 PDF displayed in the page footer; textbook examples and current adapted numerical cards are deliberately distinguished.','Qualified items remain conditional; mathematical consistency within stated assumptions is not an unconditional product approval.']}
for pack in current:
 date=pack['date'];compare_path=out.parent/'dated-controller-comparison'/f'{date}.json';compare=json.loads(compare_path.read_text());cmpqs={q['id']:q for q in compare['questions']}
 content_items={};source_qs=[]
 for qi,q in enumerate(pack['questions']):
  pid=q['id'];cq=cmpqs[pid];rs=reasons[date][qi];assert len(rs)==len(q['subparts'])
  ns=source_notes[date][qi];imgs=[{'pdf_page':n,'printed_page':n-6,'path':str(out/f'mml-{n}.png'),'sha256':sha(out/f'mml-{n}.png'),'actually_visually_inspected':True} for n in ns[0]]
  source_qs.append({'id':pid,'status':'pass','source_label':q['source_label'],'comparison':ns[1],'source_link':q['source_link'],'source_link_target_verified':q['source_link_target_verified'],'source_fields':{'conditions':q['source_fields']['conditions']['exact_canonical_match'],'ask':q['source_fields']['ask']['exact_canonical_match']},'original_excerpt_read':q['source_original_html'],'original_access':q['original_access'],'figure_records':q['figures'],'MML_page_images':imgs,'current_source_sha256':pack['source_sha256'],'current_fragment_sha256':q['fragment_sha256']})
  for si,sub in enumerate(q['subparts']):
   cs=next(v for v in cq['subparts'] if v['subpart_id']==sub)
   key=pid+':'+sub
   content_items[key]={'status':'pass','verdict':cs['verdict'],'reviewer':'ml_source_content_a','source_visual_question':pid,'current_source_sha256':pack['source_sha256'],'current_fragment_path':q['fragment'],'current_fragment_sha256':q['fragment_sha256'],'conclusion_and_reasoning':rs[si],'qualification':cs.get('source_qualification'),'frozen_unresolved_retained':cs.get('frozen_unresolved_retained',[]),'current_recall_covariance_disclosure':q['sections']['recall']['text'] if date=='0916' and pid=='p1' else None,'comparison_disclosure_scope_note':'The supplementary comparator only protected solve/verify/pitfall; current recall also explicitly states fixed positive definite covariance. Its summary-only wording must not be applied to all seven layers.' if date=='0916' and pid=='p1' else None,'comparison_reason':cs['comparison_reason'],'seven_sections_reviewed':{k:{'sha256':v['sha256'],'published_fragment_match':v['published_fragment_match']} for k,v in q['sections'].items()},'summary_sha256':q['summary']['sha256'],'summary_matches_published':q['summary']['published_match'],'content_criteria':{'understand':'Names the requested current problem and includes every listed source subpart; prose is generic but does not change the task.','recall':'Read the actual conceptual cue, formula/definition, symbol roles and application assumptions; it is more than a title and is shorter than the full solution.','start':'The stated first calculation/setup is valid for current values and matches the full solution.','solve_verify':rs[si],'pitfall':'The current warning identifies a concrete incorrect inference and is consistent with the reasoning and qualifications.','retry':'Reuses the valid first action and warning without adding a new mathematical claim.','sum':'Read its actual current formula, first line, check and condition/distinction text; each claim is present in the same fragment body and no source qualification is erased.'},'evidence':[str(out/'current-read-evidence.json')+f' pack {date} question {pid}',str(compare_path)+f' question {pid} subpart {sub} (supplementary, nonblind)',*map(lambda im:im['path'],imgs)]}
 counts=collections.Counter(i['verdict'] for i in content_items.values())
 results['packs'].append({k:pack[k] for k in ['pack_id','date','source','source_sha256','html','html_sha256','manifest','manifest_sha256','inline_original_current_count','inline_original_prechange_count','MML_pdf']}|{'source_visual':{'status':'pass','reviewer':'ml_source_content_a','evidence':source_qs},'content':{'status':'pass','reviewer':'ml_source_content_a','meaning_of_pass':'Current mathematical claims are consistent subject to every retained item qualification; this does not remove underdetermination or supply unstated likelihood assumptions.','verdict_counts':dict(counts),'items':content_items},'supplementary_controller_comparison':{'path':str(compare_path),'sha256':sha(compare_path)}})
results['counts']={'packs':len(results['packs']),'questions':sum(len(x['source_visual']['evidence']) for x in results['packs']),'subparts':sum(len(x['content']['items']) for x in results['packs']),'verdicts':dict(collections.Counter(i['verdict'] for x in results['packs'] for i in x['content']['items'].values())),'MML_rendered_inspected_pages':len(list(out.glob('mml-*.png')))}
(out/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
lines=['# Current academic source/content review A','',f"Reviewed {results['counts']['packs']} packs / {results['counts']['questions']} questions / {results['counts']['subparts']} subparts; {results['counts']['MML_rendered_inspected_pages']} actual local MML pages rendered and visually inspected.",'','This is a source/content review, not a code review or blind derivation. I read current source cards and explanations, then used the disclosed frozen controller-reference comparison as supplementary mathematical evidence. No product file, release approval, commit, or independent-review record was changed.','',f"Verdicts: {results['counts']['verdicts']}. Every qualified_consistent item below retains its assumptions; pass means consistent under those conditions, not unconditional approval.",'','## Exact binding','',f"Detailed section HTML/text and source fields: `current-read-evidence.json`, SHA256 `{results['current_read_evidence']['sha256']}`. `results.json` carries per-pack live HTML/source/manifest/MML hashes, per-question source_visual comparisons and page-image hashes, and all 62 per-subpart content records with seven section hashes. Figures are normalized only for scoped SVG IDs before geometry comparison.",'','## Limits','']+[f'- {x}' for x in results['limitations']]
lines+=['','0916/p1 current recall explicitly states fixed positive definite covariance and theta-only optimization. Supplementary comparison disclosure labels describing only solve/verify/pitfall are retained as historical comparison scope, not as a claim that the full seven-section body lacks this statement. Conditional covariance-domain approval remains in place.']
for pack in results['packs']:
 lines+=['',f"## {pack['date']} / {pack['pack_id']}",'',f"- Current source SHA256: `{pack['source_sha256']}`",f"- Current explanation HTML SHA256: `{pack['html_sha256']}`",f"- MML SHA256: `{pack['MML_pdf']['sha256']}`",f"- source_visual: pass. content: pass with item qualifications. {pack['content']['verdict_counts']}",'']
 for sq in pack['source_visual']['evidence']:
  lines += [f"### {sq['id']} source and figure comparison",'',f"{sq['comparison']} Pages: {', '.join(str(v['pdf_page']) for v in sq['MML_page_images'])}. Conditions and ask match the actual current extraction. Original excerpt was read in the source card. Fragment SHA256: `{sq['current_fragment_sha256']}`.",'']
  for key,it in pack['content']['items'].items():
   if key.startswith(sq['id']+':'):
    lines += [f"- **{key}: {it['verdict']}** — {it['conclusion_and_reasoning']}"]
    if it['qualification']:lines += [f"  Retained qualification: {it['qualification'].get('issue','')}"]
    if it['frozen_unresolved_retained']:lines += [f"  Retained unresolved scope: {'; '.join(it['frozen_unresolved_retained'])}"]
lines+=['','## Figure evidence','', 'The separately rendered current 0921/p3 and p4 SVGs show x1→x3, x2→x3, x5→x2, x2→x4. Both raster captures are byte-identical (same geometry, different source SVG IDs): SHA256 `'+sha(out/'current-0921-p3-graph.png')+'`. These were compared visually to actual MML285 Figure8.9(b), then against MML286 (8.30).','', 'Page continuation/theory locators were expanded beyond historical page pointers: MML267 for (8.9),269 for (8.12),300 for (9.12),307 for (9.31),204 for the actual multivariate Gaussian density. Historical reports supplied locators only and were not accepted as current approval.','']
(out/'report.md').write_text('\n'.join(lines))
print(json.dumps(results['counts'],ensure_ascii=False))
