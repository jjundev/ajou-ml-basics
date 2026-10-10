from fixtures import *
import unittest
from pathlib import Path
from port_baseline import validate_port_manifest
from solution_video.review_adapter import default_config, _modules
from solution_video.writing import default_writing
from solution_video.speech_tts import make_speech_payload
class PortTests(unittest.TestCase):
 def test_frozen_port_runs_without_ec2_checkout(self):
  skill=Path(__file__).resolve().parents[1]
  result=validate_port_manifest(skill)
  self.assertTrue(result['valid'])
  self.assertEqual(result['commit'],'eeec3d56513fe9e8a34f45edb05ae1118b08cf62')
  self.assertEqual(default_writing()['chars_per_second'],7.5)
  self.assertEqual(default_config()['voice'],'Aoede')
  self.assertNotIn('direction',str(make_speech_payload('평균을 구해요.',default_config())))
  self.assertTrue(all(str(skill) in str(m.__file__) for m in _modules()))

 def test_render_port_hashes(self):
  import json,hashlib
  skill=Path(__file__).resolve().parents[1]
  port=json.loads((skill/'assets/render-port-provenance.json').read_text())
  self.assertEqual(port['source_commit'],'75a6a581d7b66651d361856fa1bfa35bc85f20b8')
  for row in port['files']+port['ml_changes']:
   self.assertEqual(hashlib.sha256((skill/row['destination']).read_bytes()).hexdigest(),row['ported_sha256'])
