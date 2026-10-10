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
