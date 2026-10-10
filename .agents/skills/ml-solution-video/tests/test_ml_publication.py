from fixtures import *
from solution_video.util import write,read
from solution_video.publication import output_filename,report_current,publish_batch
from solution_video.verify import verification_fingerprint
class MLPublication(Sandbox):
 def test_unlistened_audio_cannot_publish(self):
  run=self.run/'run';write(run/'source/manifest.json',dict(problem_id='P1',segments=[dict(id='a',chunks=[dict(id='c')])]))
  h=verification_fingerprint(run);write(run/'verification/audio-review.json',dict(mode='not-listened',status='passed',input_hash=h,notes='synthetic',evidence={'source/manifest.json':'fake'},chunk_checks=[]))
  report=dict(schema_version=2,complete=True,technical_complete=True,input_hash=h,live_audio='verified',checks={},review_hashes={})
  self.assertFalse(report_current(run,report))
 def test_range_and_pack_title_collisions(self):
  write(self.run/'source/manifest.json',dict(problem_id='P1',title='평균/분산: 비교'))
  a=output_filename(dict(id='P1',prefix='0930 — Basics — '),self.run);b=output_filename(dict(id='P1',prefix='1007 — Basics — '),self.run)
  self.assertNotEqual(a,b);self.assertNotIn('/',a)
 def test_partial_publish_and_rollback(self):
  from test_publication import PublicationTests
  for name in ('test_final_tamper_and_publish_rollback','test_move_failure_restores_previous'):
   result=unittest.TestResult();PublicationTests(name).run(result)
   self.assertTrue(result.wasSuccessful(),str(result.errors+result.failures))
 def test_title_id_and_invisible_characters_do_not_repeat(self):
  write(self.run/'source/manifest.json',dict(problem_id='P1',title='P1. 평균\u202e 비교'))
  name=output_filename(dict(id='P1',prefix=''),self.run)
  self.assertEqual(name,'P1 — 평균 비교.mp4')
