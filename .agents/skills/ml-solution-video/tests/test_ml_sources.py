from fixtures import *
from ml_fixtures import make_ml_repo
from solution_video.sources import discover,freeze_sources
from solution_video.contracts import InputError
class MLSources(Sandbox):
 def test_unicode_pack_identity_and_ambiguity(self):
  repo=make_ml_repo(self.run,dates=('0930','1007'),continuations=True)
  bundles=discover(repo,'0930-1007',['0930:P1','1007:P1'])
  self.assertEqual(len({b['key'] for b in bundles}),2)
  with self.assertRaisesRegex(InputError,'ambiguous'):discover(repo,'0930-1007',['P1'])
  make_ml_repo(repo,ambiguous=True)
  with self.assertRaisesRegex(InputError,'ambiguous'):discover(repo,'1007')
  self.assertEqual(len(discover(repo,'1007',pack='Basics')),2)
 def test_continuation_and_hint_mapping(self):
  bundles=discover(make_ml_repo(self.run,continuations=True),'1007',['p01'])
  self.assertEqual([p['continuation'] for p in bundles[0]['answer_pages']],[1,2])
  self.assertEqual(len(bundles[0]['problem_pages']),1)
 def test_selected_only_and_frozen_assets(self):
  repo=make_ml_repo(self.run);b=discover(repo,'1007',['P1'])
  f=freeze_sources(b,self.run/'batch')
  self.assertFalse(Path(f[0]['source_files']['html']).is_absolute())
  self.assertTrue((self.run/'batch'/f[0]['source_files']['html']).is_file())
 def test_real_current_pack(self):
  b=discover(REPO,'1007');self.assertEqual(len(b),8)
  self.assertEqual(b[1]['mml_source'],'MML Example 9.7')
  self.assertEqual(b[-1]['answer_pages'][0]['page_index'],7)
 def test_selected_card_isolated_from_unselected_bad_markup(self):
  repo=make_ml_repo(self.run);p=next((repo/'복습노트/1007').glob('*.html'));t=p.read_text();split=t.index('<article class="card" id="p2"');p.write_text(t[:split]+t[split:].replace('class="ask"','class="broken"'))
  self.assertEqual(len(discover(repo,'1007',['P1'])),1)
 def test_conditions_disagreement_blocks_selected_problem(self):
  import fitz
  repo=make_ml_repo(self.run);folder=repo/'복습노트/1007'
  for role in ('문제','답안'):
   path=next(folder.glob('*-'+role+'.pdf'));doc=fitz.open(path);p=doc[0];p.draw_rect((18,80,250,150),fill=(246/255,246/255,243/255),color=None);p.insert_text((30,115),'condition='+('1' if role=='문제' else '2'));temp=path.with_suffix('.pending.pdf');doc.save(temp);doc.close();temp.replace(path)
  with self.assertRaisesRegex(InputError,'conditions differ'):discover(repo,'1007',['P1'])
 def test_all_current_packs_preserve_legacy_statement(self):
  sizes={'0909':5,'0914':7,'0916':6,'0921':6,'0923':7,'0928':8,'0930':8,'1007':8}
  for date,count in sizes.items():
   b=discover(REPO,date);self.assertEqual(len(b),count)
   if date!='1007':self.assertTrue(all(x['card'].get('statement_html') and x['card']['partition_status']=='author-required' for x in b))
