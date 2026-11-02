from fixtures import *
from solution_video.bundle_layers import export_bundle,extract_bundle,verify_bundle_layers
from solution_video.contracts import ExtractionError
class BundleTests(Sandbox):
 def fixture(self):
  pdf=math_pdf(self.run/'a.pdf');b=dict(problem_pages=[dict(id='problem-1',snapshot=str(pdf),page_index=0)],answer_pages=[dict(id='answer-1',snapshot=str(pdf),page_index=0),dict(id='answer-2',snapshot=str(pdf),page_index=0)])
  pages=export_bundle(b,self.run);maps={pid:dict(mapping(p),terminal_step_id='solution') for pid,p in pages.items() if pid.startswith('answer')}
  return pages,dict(schema_version=2,pages=maps,step_order=['answer-1::solution','answer-2::solution'],answer_step_id='answer-2::solution')
 def test_all_pages_and_final_answer_coverage(self):
  pages,m=self.fixture();layers=extract_bundle(pages,m)
  self.assertEqual(len(layers['page_order']),3);self.assertEqual(layers['answer_step_id'],'answer-2::solution')
  m['answer_step_id']='answer-1::solution'
  with self.assertRaises(ExtractionError):extract_bundle(pages,m)
 def test_scan_and_unclassified_shape_block_only_that_run(self):
  pages,m=self.fixture();m['pages']['answer-2']['steps'][0]['glyph_ids'].pop()
  with self.assertRaises(ExtractionError):extract_bundle(pages,m)
 def test_static_gate_preserves_exact_zero(self):
  pages,m=self.fixture();layers=extract_bundle(pages,m);r=verify_bundle_layers(layers,self.run/'evidence');self.assertTrue(r['passed'])
  self.assertTrue(all(p['pixel_diff']==p['non_target_diff']==p['hidden_leaks']==0 for p in r['pages'].values()))
 def test_global_writing_unit_targets_are_page_scoped(self):
  from solution_video.bundle_layers import flatten_layers
  from solution_video.writing_units import compile_writing_units
  from test_writing_units import unit
  pages,m=self.fixture()
  for pid,mp in m['pages'].items():
   step=mp['steps'][0];mp['steps'][0]['writing_units']=[unit('u',[100,300],step['glyph_ids'],step['shape_ids'])]
  l=extract_bundle(pages,m);flat=flatten_layers(l);units=compile_writing_units(flat)
  self.assertTrue(all(p['id'].startswith('answer-') for u in units for p in u['pieces']))
