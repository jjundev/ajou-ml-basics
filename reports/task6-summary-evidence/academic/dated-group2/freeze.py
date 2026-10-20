from pathlib import Path
import json,hashlib,datetime
OUT=Path(__file__).parent
names=['0930','1007','1012','1014','1019','hw1']
packs=[json.loads((OUT/f'{n}.results.json').read_text()) for n in names]
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
unresolved=[]
for p in packs:
 for q in p['results']:
  for z in q['subparts']:
   for item in z['unresolved']:unresolved.append(dict(pack_id=p['pack_id'],id=q['id'],subpart_id=z['subpart_id'],issue=item))
result=dict(schema_version=1,review_kind='independent_source_only_academic_derivation',status='frozen_before_any_reference_comparison',frozen_at_utc=now,reviewer=packs[0]['reviewer'],source_scope='Exactly six assigned group-2 README.md/questions.json packets; all figure resources arrays were empty; supplied inline SVG markup was read in questions.json.',original_prompt_theory_use='Optional original_question_html was read as supplied source prompt. The derivations use the explicit conditions and self-contained mathematical arguments, without consulting authored hints or references. The I/2 versus I/4 difference in 1007/p2 is resolved by the actual question conditions, and noted in that result.',counts=dict(packs=len(packs),questions=sum(len(p['results']) for p in packs),subparts=sum(len(q['subparts']) for p in packs for q in p['results']),unresolved_subparts=len(set((u['pack_id'],u['id'],u['subpart_id']) for u in unresolved))),packs=packs,unresolved=unresolved,own_calculation_checks=json.loads((OUT/'calculation-checks.json').read_text()),approval_status='No reference comparison or approval has been performed or asserted.')
(OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
lines=['# Frozen independent mathematical derivations','',f'Frozen at {now}. Source-only, before any reference comparison.','',result['reviewer']['context_isolation'],'',result['original_prompt_theory_use'],'',f"Coverage: {result['counts']['packs']} packs, {result['counts']['questions']} questions, {result['counts']['subparts']} subparts.",'']
for p in packs:
 lines.extend([f"## Pack {p['pack_id']}",'',f"Packet payload SHA-256: `{p['packet_payload_sha256']}`",f"Question payload SHA-256: `{p['question_payload_sha256']}`",f"Raw packet SHA-256: `{p['packet_file_sha256']}`",''])
 for q in p['results']:
  lines.extend([f"### {q['id']}",'',f"Input SHA-256: `{q['input_sha256']}`",''])
  for z in q['subparts']:
   lines.extend([f"#### Subpart {z['subpart_id']} ({z['method']})",'',z['derivation'],'',f"Conclusion: {z['conclusion']}",'',f"Checks: {z['checks']}",''])
   if z['assumptions']:lines.extend(['Assumptions: '+'; '.join(z['assumptions']),''])
   if z['unresolved']:lines.extend(['Unresolved: '+'; '.join(z['unresolved']),''])
lines.extend(['## Own calculation log','','30 exact matrix/derivative/stationarity calculations and 6 concrete density normalization integrals were evaluated by calculation_checks.py. The numeric integrals use a finite, positive absolute tolerance 1e-25; the largest observed absolute residual was approximately 1.3364e-51. These support the detailed algebra and do not replace proofs.','','No reference answers have been compared and no academic approval is asserted.',''])
(OUT/'derivations.md').write_text('\n'.join(lines))
files=['results.json','derivations.md','derive.py','calculation_checks.py','calculation-checks.json','calculation-checks.log','freeze.py']+[f'{n}.results.json' for n in names]
manifest=dict(schema_version=1,status='frozen_before_reference_comparison',frozen_at_utc=now,files={name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in files})
(OUT/'frozen-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(counts=result['counts'],results_sha256=manifest['files']['results.json'],unresolved=[f"{x['pack_id']}/{x['id']}/{x['subpart_id']}" for x in unresolved]),ensure_ascii=False,indent=2))
