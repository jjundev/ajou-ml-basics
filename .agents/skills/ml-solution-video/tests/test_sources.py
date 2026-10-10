from fixtures import *
from ml_fixtures import make_ml_repo
from solution_video.sources import discover,freeze_sources,validate_pairs
from solution_video.contracts import InputError
class SourceTests(Sandbox):
 def test_badge_can_share_text_line_with_title(self):
  self.assertEqual(len(discover(make_ml_repo(self.run),'1007')),2)
 def test_wide_conditions_compare_entire_panel(self):
  import fitz
  refs=[]
  for i in range(2):
   p=self.run/f'wide{i}.pdf';d=fitz.open();pg=d.new_page(width=1440,height=810);pg.draw_rect((36,61,487,657),fill=(246/255,246/255,243/255),color=None);pg.insert_text((400,160),'I = '+str(i+1));d.save(p);refs.append(dict(snapshot=str(p),page_index=0,width_pt=1440,height_pt=810))
  with self.assertRaisesRegex(InputError,'conditions differ'):validate_pairs([dict(problem_id='P1',problem=refs[0],answer=refs[1])])
 def test_pairs_skip_hint(self):
  b=discover(make_ml_repo(self.run),'1007');self.assertEqual(len(b),2);self.assertTrue(all(p['source_files']['md'] for p in b));self.assertEqual(b[1]['answer_pages'][0]['page_index'],1)
 def test_ambiguous_pair_and_duplicate_conflict(self):
  repo=make_ml_repo(self.run)
  for selector in ('0931','1007-0911','bad'):
   with self.assertRaises(InputError):discover(repo,selector)
  with self.assertRaises(InputError):discover(repo,'1007',['P99'])
  b=discover(repo,'1007',['P1']);self.assertEqual(len(b),1)
  src=next((repo/'복습노트/1007').glob('*답안.pdf'));shutil=__import__('shutil');shutil.copy(src,src.with_name(src.name.replace('Basics','Other')))
  # Exact stem pairing ignores an unrelated PDF.
  self.assertEqual(len(discover(repo,'1007',['P1'])),1)
 def test_zero_padded_dates_and_selected_only(self):
  repo=make_ml_repo(self.run,dates=('0923','0930'));self.assertTrue(discover(repo,'0923'));self.assertEqual(len(discover(repo,'0930',['p01'])),1)
 def test_pagination_does_not_alias_dates(self):
  b=discover(make_ml_repo(self.run,dates=('1001','1002')),'1001-1002');self.assertEqual(len(b),4);self.assertEqual(len({x['key'] for x in b}),4)
 def test_preserves_all_frozen_correspondences(self):
  b=discover(make_ml_repo(self.run,continuations=True),'1007');f=freeze_sources(b,self.run/'frozen')
  self.assertTrue(all((self.run/'frozen'/p['snapshot']).is_file() for x in f for p in x['problem_pages']+x['answer_pages']))
 def test_malformed_pdf_isolated_in_batch_discovery(self):
  repo=make_ml_repo(self.run,dates=('1001','1002'))
  next((repo/'복습노트/1001').glob('*답안.pdf')).write_bytes(b'not a pdf')
  errors=[];b=discover(repo,'1001-1002',failures=errors);self.assertEqual([p['range'] for p in b],['1002','1002']);self.assertEqual(len(errors),2)
