import sys,json,pathlib,datetime,math,statistics,collections
sys.dont_write_bytecode=True
from compare import *
from adjudication_notes import REASONS,QUAL
ML=BASE/'머신러닝기초'
sys.path.insert(0,str(ML/'.agents/skills/ml-problem-explain/scripts'))
from mpe_source import load_source
EXPECTED={1:'a6daca0a50213c1975944399623d8e03c3962d1896f983aa48969d511f960368',2:'11508b6219a0c23906a1971b780e970131a87b12001e0ea05a6ee8835d351030'}
def sections(raw):
 rt=Parser(raw).root; result={}
 for sec in ['solve','verify','pitfall']:
  found=rt.all(lambda n:n.attrs.get('data-explanation')==sec)
  assert len(found)==1,(sec,len(found));result[sec]=found[0]
 found=rt.all(lambda n:'sum' in n.attrs.get('class','').split());assert len(found)==1
 result['summary']=found[0]
 return result
def mathpayload(raw):
 ss=sections(raw);return [{'section':sec,'html':raw[ss[sec].start:ss[sec].end]} for sec in ['solve','verify','pitfall']]
def mask_summary(raw):
 n=sections(raw)['summary'];start=raw.find('>',n.start)+1;end=raw.rfind('</div>',n.start,n.end)
 assert start>n.start and end>start
 return raw[:start]+'[SUMMARY_CONTENT]'+raw[end:]
def evidence(raw,node,path,section):
 quote=raw[node.start:node.end]
 return {'section':section,'path':str(path),'line_start':raw.count('\n',0,node.start)+1,'line_end':raw.count('\n',0,node.end)+1,'quote_html':quote,'quote_text':text(quote),'sha256':sha(quote)}
def perpart_evidence(raw,ss,path,sid):
 out=[]
 for sec,n in ss.items():
  ns=n.all(lambda n:n.attrs.get('data-subpart')==sid) if sid!='main' else []
  out.append(evidence(raw,ns[0] if ns else n,path,sec))
 return out
packs=[]; integrity=[]; findings=[]
for g,fp,pk,m,pp,pq in data():
 key=pk['pack_id']; frozen_file_sha=sha(fp.read_bytes());assert frozen_file_sha==EXPECTED[g],(g,frozen_file_sha)
 assert pq['pack_id']==key
 packet_file_sha=sha(pp.read_bytes());declared=pk.get('source_packet_file_sha256',pk.get('packet_file_sha256'))
 assert packet_file_sha==declared,(key,'file')
 assert sha(canon({k:v for k,v in pq.items() if k!='packet_payload_sha256'}))==pq['packet_payload_sha256']==pk['packet_payload_sha256']
 assert sha(canon(pq['questions']))==pq['question_payload_sha256']==pk['question_payload_sha256']
 sp=load_source(pathlib.Path(m['source']),ML); current={q.id:q for q in sp.problems}
 assert {q['id'] for q in pq['questions']}==set(current)=={q['id'] for q in pk['results']}
 source_file_sha=sha(pathlib.Path(m['source']).read_bytes());assert source_file_sha==m['source_sha256']
 generatedpath=pathlib.Path(m['html']);generatedraw=generatedpath.read_text();generatedroot=Parser(generatedraw).root
 topics={n.attrs.get('id'):n for n in generatedroot.all(lambda n:n.tag=='article' and 'topic' in n.attrs.get('class','').split())}
 rows=[]
 for q in pq['questions']:
  qid=q['id'];r=next(r for r in pk['results'] if r['id']==qid);aq=current[qid]
  assert sha(canon({k:v for k,v in q.items() if k!='input_sha256'}))==q['input_sha256']==r['input_sha256']
  current_q={f:(list(getattr(aq,{'original_question_html':'original_html','subpart_ids':'subparts'}.get(f,f))) if isinstance(getattr(aq,{'original_question_html':'original_html','subpart_ids':'subparts'}.get(f,f)),tuple) else getattr(aq,{'original_question_html':'original_html','subpart_ids':'subparts'}.get(f,f))) for f in q if f!='input_sha256'}
  assert sha(canon(current_q))==q['input_sha256'],(key,qid,'current question differs')
  sids=q['subpart_ids'];assert set(sids)=={s['subpart_id'] for s in r['subparts']};assert len(sids)==len(r['subparts'])
  reasons=REASONS[key][qid];assert len(reasons)==len(sids),(key,qid,'manual coverage')
  path=pathlib.Path(m['active_fragment_directory'])/(qid+'.html');raw=path.read_text();ss=sections(raw)
  oldpath=ML/'.task6-run-ml-01/before'/path.relative_to(ML);oldraw=oldpath.read_text()
  current_math_sha=sha(canon(mathpayload(raw)));old_math_sha=sha(canon(mathpayload(oldraw)))
  assert current_math_sha==old_math_sha,(key,qid,'protected math changed')
  masked_equal=mask_summary(raw)==mask_summary(oldraw);assert masked_equal,(key,qid,'non-summary bytes changed')
  non_summary_sha=sha(mask_summary(raw)); sumhash=sha(raw[ss['summary'].start:ss['summary'].end])
  # Bind the active fragment bodies to the actual published explanation, too.
  topic=topics[qid];pubmath=[]
  for sec in ['solve','verify','pitfall']:
   ns=topic.all(lambda n:n.attrs.get('data-explanation')==sec);assert len(ns)==1
   pubmath.append({'section':sec,'html':generatedraw[ns[0].start:ns[0].end]})
  # Rendered HTML can normalize relative image references; text/equation identity is the comparison required here.
  pubmath_equal=[re.sub(r'\s+','',text(v['html'])) for v in pubmath]==[re.sub(r'\s+','',text(v['html'])) for v in mathpayload(raw)]
  assert pubmath_equal,(key,qid,'published math differs')
  ev={sec:evidence(raw,n,path,sec) for sec,n in ss.items()}
  row={'id':qid,'source_question':q,'current_sourcepack_input_sha256':sha(canon(current_q)),'frozen_input_sha256':r['input_sha256'],'current_fragment':str(path),'current_fragment_sha256':sha(raw),'current_math_sha256':current_math_sha,'math_sha_definition':'SHA256 of canonical UTF-8 JSON array [{section,html}] for exact solve, verify, pitfall outer HTML, in that order.','current_non_summary_sha256':non_summary_sha,'current_summary_sha256':sumhash,'baseline_protection':{'baseline_fragment':str(oldpath),'baseline_math_sha256':old_math_sha,'math_bytes_identical':True,'all_non_summary_bytes_identical_after_mask_only_summary_inner_content':masked_equal,'baseline_non_summary_sha256':sha(mask_summary(oldraw)),'current_generated_html':str(generatedpath),'generated_math_text_equations_equal_active_fragment':pubmath_equal},'current_reference_evidence':ev,'frozen_question_unresolved':r.get('unresolved',[]),'subparts':[]}
  for i,sid in enumerate(sids):
   s=next(s for s in r['subparts'] if s['subpart_id']==sid);verdict,qualification,disclosure=QUAL.get((key,qid,sid),('consistent',None,'not_applicable_no_unresolved_source_qualification'))
   item={'pack_id':key,'question_id':qid,'subpart_id':sid,'frozen_input_sha256':r['input_sha256'],'current_sourcepack_input_sha256':sha(canon(current_q)),'current_math_sha256':current_math_sha,'current_fragment_sha256':sha(raw),'verdict':verdict,'comparison_reason':reasons[i],'frozen_independent_result':s,'frozen_unresolved_retained':s.get('unresolved',[]),'current_reference_evidence':perpart_evidence(raw,ss,path,sid),'source_qualification':{'issue':qualification,'disclosed_status':disclosure,'limitation_fully_explicit_in_non_summary_baseline':disclosure in ['explicit_non_summary','explicit_current_adaptation'],'related_condition_or_caveat_in_non_summary_baseline':disclosure in ['explicit_non_summary','partial_non_summary','partial_non_summary_no_exact_sigma_warning','explicit_current_adaptation','partial_source_gaussian_setting','implicit_formula_only_summary_explicit'],'preservation_proof':'Current exact solve/verify/pitfall bytes and masked non-summary fragment bytes compared directly to .task6-run-ml-01/before; this is not inferred from old approval metadata.','scope_note':'consistent means agreement within the actual stated mathematical object and source conventions; it is not a product approval.'}}
   row['subparts'].append(item)
   if verdict!='consistent':findings.append({'pack_id':key,'question_id':qid,'subpart_id':sid,'verdict':verdict,'issue':qualification,'disclosed_status':disclosure,'comparison_reason':reasons[i],'evidence_path':str(path),'evidence_lines':{sec:[e['line_start'],e['line_end']] for sec,e in ev.items()}})
  rows.append(row)
 pack={'pack_id':key,'current_pack_id':m['pack_id'],'frozen_results_path':str(fp),'frozen_results_file_sha256':frozen_file_sha,'source_packet_path':str(pp),'source_packet_file_sha256':packet_file_sha,'packet_payload_sha256':pq['packet_payload_sha256'],'question_payload_sha256':pq['question_payload_sha256'],'current_source_path':m['source'],'current_source_sha256':source_file_sha,'active_fragment_directory':m['active_fragment_directory'],'identity_and_coverage':'Verified canonical per-question, question-array, packet, and frozen file hashes; exact question ID and subpart sets; actual current SourcePack question fields byte-for-byte canonical identity.','questions':rows,'counts':{'questions':len(rows),'subparts':sum(len(q['subparts']) for q in rows)},'frozen_pack_unresolved_retained':pk.get('unresolved',[]),'status':'comparison_complete_no_product_approval'}
 packs.append(pack)
 (OUT/(key+'.json')).write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n')
 integrity.append({'pack_id':key,**pack['counts'],'frozen_input_and_actual_current_source_identity':True,'all_question_subpart_sets_exact':True,'all_protected_math_and_non_summary_bytes_equal_baseline':True,'all_current_generated_math_matches_active_fragment':True})
 print(key,pack['counts'])
counts=collections.Counter(s['verdict'] for p in packs for q in p['questions'] for s in q['subparts'])
normal=statistics.NormalDist()
focused={'kind':'controller authored focused checks; not a full-suite rerun','gaussian_interval_coverage':{'central_mass_plus_minus_1_sigma':math.erf(1/math.sqrt(2)),'central_mass_plus_minus_2_sigma':math.erf(2/math.sqrt(2)),'halfwidth_sigma_for_exact_67_percent':normal.inv_cdf((1+.67)/2),'halfwidth_sigma_for_exact_95_percent':normal.inv_cdf((1+.95)/2),'conclusion':'67% is not exactly ±1σ and 95% is not exactly ±2σ. No plot provenance was inferred from this calculation.'},'0930_p3_source_gap_counterexample':{'construction':'X,W,Z independent N(0,1); V=(1/2)W+sqrt(3)/2 Z; A=C=1, Q=R=1, H=Y=X+V, Xnext=X+W. Both W and V are independent of state X, as the source says. The source does not say W,V mutually independent.','current_state_conditional':'X|Y ~ N(Y/2,1/2)','actual_next_conditional':'Xnext|Y ~ N(3Y/4,7/8)','claimed_formula_if_only_state_independence':'N(Y/2,3/2)','calculation':'Cov(Xnext,Y)=1+1/2=3/2 and Var(Y)=2, hence mean 3Y/4; conditional variance 2-(3/2)^2/2=7/8.','conclusion':'Marginal state independence alone is insufficient; fresh-noise/conditional independence is substantive.'}}
(OUT/'focused-math-checks.json').write_text(json.dumps(focused,ensure_ascii=False,indent=2)+'\n')
pdf=ML/'교과서/Mathematics_for_Machine_Learning.pdf'
authentic={'path':str(pdf),'sha256':sha(pdf.read_bytes()),'page_308':{'printed_page':302,'render':str(OUT/'mml-308.png'),'text':str(OUT/'mml-308.txt'),'visual_inspection':'Full rendered page inspected. Figure9.7 compares degree6 left/degree8 right, MLE and MAP; paragraph gives original prior N(0,I), not current adapted I/4. Source confirms a historical example tendency only.'},'pages_315_316':{'printed_pages':[309,310],'render':str(OUT/'mml-316.png'),'text':str(OUT/'mml-315-316.txt'),'visual_inspection':'Full rendered PDF316 inspected. Figure9.10(b) caption gives 67% and95%; (c) caption explicitly says functions are induced by parameter posterior samples. It does not equate those levels to exactly1σ/2σ. PDF315 distinguishes latent function variance phi^T SN phi from observation variance plus sigma².'},'blind_packet_gaps':[{'pack_id':'1007','question_id':'p3','subpart_id':'b','missing':'Original Figure9.10(b) numerical coverage labels/caption','status':'Resolved at controller reference comparison by authentic current PDF316; remains absent from frozen source-only packet.'},{'pack_id':'1007','question_id':'p3','subpart_id':'c','missing':'Original Figure9.10(c) panel and sampling caption','status':'Resolved at controller reference comparison by authentic current PDF316; remains absent from frozen source-only packet.'}],'unresolved_authentic_source_requests':[]}
result={'schema_version':1,'review_kind':'controller_current_reference_comparison_after_frozen_independent_derivation','reviewer':'/root/ml_compare_dated','status':'all_assigned_comparisons_complete_root_adjudication_required','approval_status':'no_product_approval_set','scope':{'question_count':sum(p['counts']['questions'] for p in packs),'subpart_count':sum(p['counts']['subparts'] for p in packs),'packs':[p['pack_id'] for p in packs],'excluded':'86 exam questions: outside this delegate scope'},'snapshot_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'counts':dict(counts),'verification_integrity':integrity,'method':'Read all actual current solve/verify/pitfall and summary bodies, current source questions/inline figures, and all frozen independent calculations. Compare mathematical derivations, exact results, dimensions, domain/rank/independence conditions and normalizers. Use old preservation snapshots only for exact byte comparison, never old pass metadata. Two focused authentic PDF pages were inspected to resolve figure provenance. No product/index/branch writes, commits, subagents, or full-suite reruns.','current_reference_map_sha256':sha((ML/'.task6c-run-ml-01/current-pack-reference-map.json').read_bytes()),'authentic_source_supplement':authentic,'focused_math_checks':focused,'all_non_consistent_findings':findings,'packs':packs}
assert result['scope']['question_count']==98 and result['scope']['subpart_count']==177
(OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
lines=['# Dated/HW controller reference comparison','',f"Completed all 98 questions / 177 subparts in 12 packs. Verdicts: {dict(counts)}.",'','These are reference-comparison observations. No product approval has been set; final adjudication belongs to the root controller.','',
'## Evidence and preservation','',
'Both frozen result file SHA256 identities match the assigned hashes. Every packet file, canonical packet payload, canonical question array, per-question input digest, ID set and subpart set was checked. All 98 question payloads also match the actual current SourcePack produced from the current source HTML, including conditions, asks, original quotations and inline figures.','',
'For every question, exact current solve/verify/pitfall HTML was hashed and compared to the actual `.task6-run-ml-01/before` fragment. All 98 mathematical bodies are byte-identical. Masking only the inner summary content also leaves byte-identical fragments. The published current HTML mathematical text/equations match the active regeneration fragments. These checks establish preexistence of the quoted non-summary disclosures without relying on historical approval records.','',
'`results.json` contains every per-part verdict, frozen calculation, exact current HTML/text quotations with line locations, current fragment hash, protected mathematical-body hash, source qualification and disclosure status. The twelve per-pack JSON files preserve independent continuation boundaries.','',
'## Disagreements, qualifications and packet gaps','',
'The exact 67%/95% ↔ ±1σ/±2σ wording in 1007/p3(b) is the sole mathematical wording disagreement. Standard Gaussian central masses are 68.268949% and 95.449974%; exact 67%/95% half-widths are approximately 0.9741139σ and 1.9599640σ. The book’s 67%/95% caption does not justify an exact 1σ/2σ equivalence. That statement is in protected preexisting solve text, so it is reported rather than edited.','',
'Authentic MML PDF316 (printed310), Figure9.10(b)/(c), was rendered and inspected. Its caption resolves the blind packet’s missing coverage labels and missing panel(c) sample provenance. Those omissions remain documented as limitations of what the independent worker could verify. No authentic-source request remains unresolved in this comparison. MML PDF308 (printed302), Figure9.7, confirms the historical degree6/8 illustration and original prior I; it does not establish a universal ranking for the current adapted prior I/4 and unspecified dataset.','']
for f in findings:
 lines.append(f"- **{f['pack_id']}/{f['question_id']}/{f['subpart_id']} — {f['verdict']}**: {f['issue']} Disclosure: `{f['disclosed_status']}`. {f['evidence_path']} (solve lines {f['evidence_lines']['solve'][0]}–{f['evidence_lines']['solve'][1]}, verify {f['evidence_lines']['verify'][0]}–{f['evidence_lines']['verify'][1]}, pitfall {f['evidence_lines']['pitfall'][0]}–{f['evidence_lines']['pitfall'][1]}).")
lines+=['','## Per-pack coverage','','| Pack | Questions | Subparts | Verdict counts |','|---|---:|---:|---|']
for p in packs:
 c=collections.Counter(s['verdict'] for q in p['questions'] for s in q['subparts']);lines.append(f"| {p['pack_id']} | {p['counts']['questions']} | {p['counts']['subparts']} | {dict(c)} |")
lines+=['','## All subpart comparisons','']
for p in packs:
 lines+=['',f"### {p['pack_id']}",'']
 for q in p['questions']:
  for s in q['subparts']:lines.append(f"- {q['id']}/{s['subpart_id']}: **{s['verdict']}** — {s['comparison_reason']}")
(OUT/'report.md').write_text('\n'.join(lines)+'\n')
(OUT/'findings.json').write_text(json.dumps({'counts':dict(counts),'findings':findings,'packet_gaps':authentic['blind_packet_gaps'],'unresolved_authentic_source_requests':[]},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'scope':result['scope'],'counts':dict(counts)},ensure_ascii=False))
