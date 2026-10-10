import unittest,tempfile
from pathlib import Path
from _util import ROOT
from render_performance_acceptance import run_acceptance
class AcceptanceInputTests(unittest.TestCase):
 def test_invalid_path_and_motion_write_nothing(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);entry=root/'cli.js';entry.write_text('')
   for value in (-1,0,1,30):
    with self.assertRaises(ValueError):run_acceptance(root/'out',entry,motion_duration=value)
    self.assertFalse((root/'out').exists())
   with self.assertRaises(ValueError):run_acceptance(root/'out',root/'missing')
   self.assertFalse((root/'out').exists())
 def test_destination_nonempty(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);entry=root/'cli.js';entry.write_text('');out=root/'out';out.mkdir();(out/'keep').write_text('keep')
   with self.assertRaises(ValueError):run_acceptance(out,entry)
   self.assertEqual((out/'keep').read_text(),'keep')

 def test_frame_or_source_difference_is_not_complete(self):
  from render_performance_acceptance import compare_outputs
  a=dict(frame_hash='A',pcm_hash='P',aac_hash='C',frames=30)
  self.assertFalse(compare_outputs([a,dict(a,frame_hash='B')],30,True)['technical_complete'])
  self.assertFalse(compare_outputs([a,a],30,False)['technical_complete'])
  self.assertTrue(compare_outputs([a,a],30,True)['technical_complete'])
