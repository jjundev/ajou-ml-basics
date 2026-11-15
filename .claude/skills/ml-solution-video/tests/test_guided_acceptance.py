from fixtures import *
import importlib
from solution_video.util import read,write
class GuidedAcceptanceTests(Sandbox):
 def guided(self):
  try:from guided_acceptance import author_guided
  except ImportError:self.fail('guided author missing')
  import video
  from ml_authored import stage_authored_fixture
  stage_authored_fixture(REPO, self.run)
  batch=video.prepare_batch(self.run,'1007',['P3'],False)
  run=batch/read(batch/'batch.json')['items'][0]['run'];result=author_guided(run)
  return run,result
 def test_four_core_connections_and_exact_source_preservation(self):
  run,result=self.guided()
  self.assertEqual(len(result['core_step_ids']),6)
  lesson=read(run/'source/lesson.json');m=read(run/'source/manifest.json')
  from solution_video.bundle_layers import flatten_layers
  l=flatten_layers(read(run/'layers/layers.json'))
  self.assertEqual([r['step_id'] for r in lesson['steps'] if r['mode']=='reasoned'],result['core_step_ids'])
  for key,objects in [('glyph_ids',l['glyphs']),('shape_ids',l['shapes'])]:
   ids=[v for s in l['map']['steps'] for v in s[key]]
   self.assertEqual(len(ids),len(set(ids)));self.assertEqual(set(ids),{o['id'] for o in objects})
  self.assertTrue(all(s['text'].strip() and s['caption_text'].strip() for s in m['segments']))
  self.assertIn('맵',' '.join(s['text'] for s in m['segments']));self.assertIn('θ_MAP',' '.join(s['caption_text'] for s in m['segments']))
  self.assertNotIn('맵',' '.join(s['caption_text'] for s in m['segments']))
  from solution_video.annotations import load_teaching
  from solution_video.lesson import load_lesson
  bundle=read(run/'layers/layers.json')
  self.assertIsNotNone(load_lesson(run,m,bundle,load_teaching(run,m,bundle)))

 def test_fake_audio_never_approves(self):
  run,_=self.guided();m=read(run/'source/manifest.json');l=read(run/'layers/layers.json')
  from solution_video.annotations import load_teaching
  from solution_video.bundle_timeline import build_bundle_timeline
  from solution_video.writing import default_writing
  from solution_video.review_adapter import default_config
  from solution_video.narration_pacing import analyze_narration_pacing
  audio=[dict(make_audio(s['id'],24000 if s['kind']=='write' else 72000,run),chunks=[dict(id='c1',start_sample=0,end_sample=24000 if s['kind']=='write' else 72000)]) for s in m['segments']]
  t=build_bundle_timeline(m,l,audio,default_config(),default_writing(),load_teaching(run,m,l))
  self.assertEqual(analyze_narration_pacing(t,audio,run)['status'],'review-required')
  self.assertFalse((run/'verification/audio-review.json').exists())
 def test_guided_caption_semantic_coverage(self):
  from solution_video.subtitles import split_caption,caption_units
  run,_=self.guided();segments=read(run/'source/manifest.json')['segments']
  self.assertEqual(len(segments),13)
  output=[]
  for seg in segments:
   with self.subTest(segment=seg['id']):
    text=seg['caption_text'];chunks=split_caption(text)
    self.assertEqual(' '.join(' '.join(c.split()) for c in chunks),text)
    self.assertTrue(all(len(c.splitlines())<=2 and all(len(line)<=34 for line in c.splitlines()) for c in chunks))
    self.assertEqual(len(chunks),len(caption_units(text)))
    self.assertTrue(all(c.endswith((',', '.')) for c in chunks))
    output.extend(chunks)
  for symbol in ['θ_MAP','m_N','φ']:self.assertIn(symbol,' '.join(output))

 def test_repeated_original_svg_gate_stays_exact(self):
  # Rebuilding identical static SVG must not capture compositor intermediate frames.
  for attempt in range(8):
   with self.subTest(attempt=attempt):
    run,_=self.guided();gate=read(run/'verification/gate.json')
    self.assertEqual([gate['pages']['answer-1'][k] for k in ['pixel_diff','non_target_diff','hidden_leaks']],[0,0,0])
