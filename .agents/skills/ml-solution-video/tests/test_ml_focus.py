from fixtures import *
from ml_fixtures import make_bundle_run
from solution_video.util import read
from solution_video.bundle_layers import extract_bundle
from solution_video.annotations import validate_teaching
from solution_video.contracts import InputError
class MLFocus(Sandbox):
 def test_visible_equation_allowed_future_equation_blocked(self):
  run=make_bundle_run(self.run);m=read(run/'source/manifest.json');l=extract_bundle(read(run/'layers/candidates.json'),read(run/'source/map.json'));page=l['pages']['answer-1'];source=page['metadata']['source_sha256'];focus=dict(schema_version=2,regions=[dict(id='equation',page_id='answer-1',source_sha256=source,bbox=[310,150,650,200])],cues=[dict(segment_id='reason0',target='equation')])
  with self.assertRaisesRegex(InputError,'future'):validate_teaching(focus,None,m,l)
  check=dict(m['segments'][1],id='check',kind='check');m['segments'].append(check);focus['cues'][0]['segment_id']='check';self.assertIsNotNone(validate_teaching(focus,None,m,l))
  focus['regions'][0]['source_sha256']='other'
  with self.assertRaisesRegex(InputError,'source hash'):validate_teaching(focus,None,m,l)
