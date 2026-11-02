import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from solution_video.bundle_cli import prepare_batch
class OutputLocationTests(unittest.TestCase):
 def test_new_batches_use_solution_video_root(self):
  with tempfile.TemporaryDirectory() as folder:
   repo=Path(folder).resolve()
   with patch('solution_video.bundle_cli.discover',return_value=[]),patch('solution_video.bundle_cli.freeze_sources',return_value=[]):
    batch=prepare_batch(repo,'과제1')
   self.assertEqual(batch.parent,repo/'문제풀이영상/과제1/과제1_제작자료/실행')
   self.assertFalse((repo/'복습영상').exists())
