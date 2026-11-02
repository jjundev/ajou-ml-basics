from fixtures import *
from test_cli import cli
from test_manifest import example
from unittest.mock import patch
import contextlib,io
from solution_video.util import read,write
from solution_video import bundle_cli,media

class RenderCLITests(Sandbox):
 def test_single_and_bundle_override_reaches_renderer(self):
  m,l,c,r=example()
  for schema in (1,2):
   run=self.run/str(schema)
   for name,value in [('manifest',m),('coverage',c),('circuit-review',r),('math-review',r),('lesson',{}),('pair',dict(schema_version=schema,problem_id=m['problem_id'])),('parts',[]),('timeline',{}),('audio',dict(voices=[])),('config',cli.default_config())]:write(run/f'source/{name}.json',value)
   write(run/'layers/layers.json',l)
   def renderer(*args,**kwargs):
    self.assertEqual(kwargs['render_options']['workers'],4)
    p=run/'renders/master.mp4';p.parent.mkdir(exist_ok=True);p.write_bytes(b'master');write(run/'verification/render-receipt.json',dict(master_sha256='synthetic'));return p
   with patch.object(cli,'_gate'),patch.object(cli,'load_lesson'),patch.object(cli,'render_master',side_effect=renderer),patch.object(media,'render_master',side_effect=renderer),patch.object(bundle_cli,'check_content',return_value=(m,l,c,r,None,cli.default_writing())),contextlib.redirect_stdout(io.StringIO()) as output:
    self.assertEqual(cli.main(['render','--run',str(run),'--hyperframes-entry','cli.js','--render-workers','4']),0)
   result=__import__('json').loads(output.getvalue());self.assertEqual(result['render_options']['workers'],4)
   self.assertEqual(read(run/'source/render-options.json')['workers'],4)
   self.assertEqual(set(read(run/'state.json')['stages']['render']['outputs']),{'renders/master.mp4','verification/render-receipt.json'})
 def test_resume_does_not_create_options(self):
  batch=self.run/'batch';write(batch/'batch.json',dict(items=[dict(id='x',run='videos/x')]))
  cli.resume_batch(batch)
  self.assertFalse((batch/'videos/x/source/render-options.json').exists())
 def test_malformed_options_not_hidden_by_cli(self):
  m,l,c,r=example()
  for name,value in [('manifest',m),('coverage',c),('circuit-review',r),('pair',{}),('config',cli.default_config())]:write(self.run/f'source/{name}.json',value)
  write(self.run/'layers/layers.json',l);(self.run/'source/render-options.json').write_text('{broken')
  with patch.object(cli,'render_master',side_effect=AssertionError('renderer reached')),contextlib.redirect_stdout(io.StringIO()) as out:
   self.assertEqual(cli.main(['render','--run',str(self.run),'--hyperframes-entry','cli.js','--render-workers','4']),1)
  self.assertIn('invalid saved',out.getvalue())
 def test_prepare_bundle_saves_default(self):
  from ml_fixtures import make_ml_repo
  with patch.object(bundle_cli,'export_bundle'):
   batch=bundle_cli.prepare_batch(make_ml_repo(self.run),'1007')
  for item in read(batch/'batch.json')['items']:
   options=read(batch/item['run']/'source/render-options.json')
   self.assertIn(options['workers'],(2,6))
   self.assertEqual(options['encoder'],'cpu')
