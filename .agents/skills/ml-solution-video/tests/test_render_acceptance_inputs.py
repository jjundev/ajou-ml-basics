from fixtures import *
from unittest.mock import patch
from render_performance_acceptance import run_acceptance
class AcceptanceInputTests(Sandbox):
 def test_missing_input_fails_before_render(self):
  entry=self.run/'cli.js';entry.write_text('')
  with self.assertRaises(ValueError):run_acceptance(self.run/'missing',self.run/'out',entry)
  self.assertFalse((self.run/'out').exists())
 def test_destination_overlap_is_rejected(self):
  entry=self.run/'cli.js';entry.write_text('')
  with self.assertRaises(ValueError):run_acceptance(self.run,self.run/'out',entry)
  self.assertFalse((self.run/'out').exists())
 def test_nonempty_destination_preserved(self):
  out=self.run/'out';out.mkdir();(out/'keep').write_text('keep')
  with self.assertRaises(ValueError):run_acceptance(self.run/'fixture',out,self.run/'cli.js')
  self.assertEqual((out/'keep').read_text(),'keep')

 def test_frame_or_source_difference_is_not_complete(self):
  from render_performance_acceptance import compare_outputs
  a=dict(frame_hash='A',pcm_hash='P',aac_hash='C',frames=30)
  self.assertFalse(compare_outputs([a,dict(a,frame_hash='B')],30,True)['technical_complete'])
  self.assertFalse(compare_outputs([a,a],30,False)['technical_complete'])
  self.assertTrue(compare_outputs([a,a],30,True)['technical_complete'])
