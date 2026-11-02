from fixtures import *
from solution_video.util import read,write,file_hash
from solution_video.contracts import InputError,ReviewError,ExtractionError
from ml_fixtures import make_ml_repo,make_bundle_run
from unittest.mock import patch
class FinalReview(Sandbox):
 def test_duplicate_pack_identity_rejected_even_with_pack(self):
  from solution_video.sources import discover
  import shutil
  repo=make_ml_repo(self.run);shutil.copytree(repo/'복습노트/1007',repo/'복습노트/duplicate')
  with self.assertRaisesRegex(InputError,'duplicate'):discover(repo,'1007',pack='Basics')
 def test_straddling_raster_solution_rejected(self):
  from solution_video.pdf_pages import export_page,extract_layers
  from PIL import Image
  import fitz
  pdf=self.run/'hybrid.pdf';d=fitz.open();p=d.new_page(width=400,height=300);p.insert_text((110,120),'x = 2');Image.new('RGB',(100,100),'black').save(self.run/'scan.png');p.insert_image((0,0,400,300),filename=str(self.run/'scan.png'));d.save(pdf)
  page=export_page(pdf,0,self.run/'page')
  with self.assertRaisesRegex(ExtractionError,'image|raster'):extract_layers(page,dict(work_bbox=[100,80,300,240],steps=[dict(id='s',glyph_ids=[g['id'] for g in page['glyphs']],shape_ids=[])],answer_step_id='s'))
 def test_named_meaning_reviews_allow_pacing_review(self):
  from solution_video.publication import report_current
  from solution_video.verify import verification_fingerprint
  run=self.run;write(run/'source/manifest.json',dict(segments=[]));required={'content','original_svg','hyperframes','final_media','captions','audio_meaning','visual_meaning'}
  paths={}
  for kind in ('audio','visual','pacing'):
   p=run/'verification'/f'{kind}-review.json';write(p,dict(status='passed'));paths[p.relative_to(run).as_posix()]=file_hash(p)
  report=dict(input_hash=verification_fingerprint(run),live_audio='verified',checks={k:dict(status='passed') for k in required},review_hashes=paths)
  self.assertTrue(report_current(run,report))
 def test_problem_roles_and_all_continued_conditions_required(self):
  from solution_video.bundle_layers import extract_bundle
  from solution_video.manifest import validate_manifest,content_fingerprint
  run=make_bundle_run(self.run);l=extract_bundle(read(run/'layers/candidates.json'),read(run/'source/map.json'));m=read(run/'source/manifest.json');c=read(run/'source/coverage.json');r=read(run/'source/math-review.json');l['pages']['problem-2']=dict(l['pages']['problem-1']);l['page_order'].insert(1,'problem-2');h=content_fingerprint(m,l,c);c['input_hash']=r['input_hash']=h
  with self.assertRaisesRegex(ReviewError,'problem page'):validate_manifest(m,l,c,r)
  l['pages'].pop('problem-2');l['page_order'].remove('problem-2');m['segments'][0]['page_id']='answer-1';h=content_fingerprint(m,l,c);c['input_hash']=r['input_hash']=h
  with self.assertRaisesRegex(ReviewError,'problem.*role|problem page'):validate_manifest(m,l,c,r)
 def test_failed_export_excluded_from_hash_bound_batch_review(self):
  import video
  from types import SimpleNamespace
  run=make_bundle_run(self.run);meta=read(run/'run.json');batch=Path(meta['batch']);meta['review']=True;write(run/'run.json',meta);data=read(batch/'batch.json');bad=batch/'videos/bad';write(bad/'source/pair.json',dict(schema_version=2));write(bad/'source/prepare-error.json',dict(reason='unsupported'));data['items'].append(dict(id='P2',key='1007:Basics:P2',run='videos/bad'));write(batch/'batch.json',data)
  self.assertEqual(video.run_stage('extract',run,SimpleNamespace())['status'],'passed');self.assertEqual(video.run_stage('check',run,SimpleNamespace())['status'],'passed');args=SimpleNamespace(config=None,approve_review=False,env_file=None);calls=[]
  result=video.run_stage('tts',run,args,lambda p:calls.append(p));self.assertEqual(result['status'],'awaiting-review');self.assertFalse(calls)
 def test_verification_dependency_invalidates_resume(self):
  import shutil
  from solution_video import state,review_adapter
  root=self.run/'skill';shutil.copytree(S,root,ignore=shutil.ignore_patterns('__pycache__'))
  run=self.run/'run';run.mkdir()
  with patch.object(state,'S',root),patch.object(review_adapter,'S',root):
   for stage in state.STAGES[:-1]:
    p=run/(stage+'.txt');p.write_text(stage);state.finish_stage(run,stage,[p])
   self.assertEqual(state.recover_run(run),'publish')
   p=root/'scripts/solution_video/bundle_verify.py';p.write_text(p.read_text()+'\n# changed verifier\n')
   self.assertEqual(state.recover_run(run),'verify')
