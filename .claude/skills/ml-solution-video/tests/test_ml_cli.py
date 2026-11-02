from fixtures import *
from ml_fixtures import make_ml_repo
import video,argparse
from solution_video.util import read,write
class MLCLI(Sandbox):
 def test_cli_prepare_selection_and_zero_paid_requests(self):
  batch=video.prepare_batch(make_ml_repo(self.run),'1007',['P1'],False,'typing');data=read(batch/'batch.json');self.assertEqual(len(data['items']),1);run=batch/data['items'][0]['run']
  self.assertEqual(read(run/'source/pair.json')['schema_version'],2)
  calls=[];r=video.run_stage('check',run,argparse.Namespace(),lambda *a:calls.append(a))
  self.assertEqual(r['paid_requests'],0);self.assertEqual(r['status'],'author-required');self.assertFalse(calls)
 def test_partial_prepare_resumes_same_frozen_inputs(self):
  batch=video.prepare_batch(make_ml_repo(self.run),'1007',['P1'],False,'typing');before=read(batch/'batch.json')['items'][0]['run'];self.assertEqual(video.resume_batch(batch)['items'][0]['run'],before)
 def test_caption_retime_trim_and_stage_invalidation(self):
  from ml_fixtures import make_bundle_run
  from solution_video.manifest import content_fingerprint
  from test_speech_tts import response
  from solution_video.state import recover_run
  from types import SimpleNamespace
  run=make_bundle_run(self.run);args=SimpleNamespace(config=None,env_file=None,approve_review=False,writing_config=None);calls=[]
  def transport(payload):calls.append(payload);return response(72000)
  for action in ('extract','check','tts'):self.assertEqual(video.run_stage(action,run,args,transport)['status'],'passed')
  before=len(calls);raw=read(run/'source/chunk-audio.json');m=read(run/'source/manifest.json');m['segments'][-1]['caption_text']='y = 2로 확인합니다.';m['segments'][-1]['chunks'][0]['caption_text']=m['segments'][-1]['caption_text'];write(run/'source/manifest.json',m)
  self.assertEqual(recover_run(run),'script')
  coverage=read(run/'source/coverage.json');review=read(run/'source/math-review.json');h=content_fingerprint(m,read(run/'layers/layers.json'),coverage);coverage['input_hash']=review['input_hash']=h;write(run/'source/coverage.json',coverage);write(run/'source/math-review.json',review)
  self.assertEqual(video.run_stage('check',run,args)['status'],'passed');self.assertEqual(video.run_stage('tts',run,args,transport)['status'],'passed');self.assertEqual(len(calls),before);self.assertEqual([r['sha256'] for r in read(run/'source/chunk-audio.json')['voices']],[r['sha256'] for r in raw['voices']])
  self.assertEqual(video.run_stage('retime',run,args)['status'],'passed')
 def test_pdf_md_conflict_blocks_paid_work(self):
  from ml_fixtures import make_bundle_run
  from types import SimpleNamespace
  run=make_bundle_run(self.run);args=SimpleNamespace();self.assertEqual(video.run_stage('extract',run,args)['status'],'passed');c=read(run/'source/coverage.json');c['pdf_md_agree']=False;write(run/'source/coverage.json',c);calls=[];r=video.run_stage('tts',run,args,lambda *a:calls.append(a));self.assertEqual(r['status'],'failed');self.assertEqual(r['paid_requests'],0);self.assertFalse(calls)
 def test_bundle_chunk_sync_uses_all_pages(self):
  from ml_fixtures import make_bundle_run
  from test_speech_tts import response
  from solution_video.speech_chunks import verify_chunk_sync
  from solution_video.subtitles import write_srt
  from types import SimpleNamespace
  run=make_bundle_run(self.run,answer_pages=2);args=SimpleNamespace(config=None,env_file=None,approve_review=False)
  for action in ('extract','check','tts'):self.assertEqual(video.run_stage(action,run,args,lambda p:response(72000))['status'],'passed')
  write_srt(read(run/'source/timeline.json'),run/'renders/captions.srt');r=verify_chunk_sync(run);self.assertEqual(r['status'],'passed',str(r))
