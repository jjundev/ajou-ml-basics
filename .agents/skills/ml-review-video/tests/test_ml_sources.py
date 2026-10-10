import tempfile,unittest,unicodedata,json
from pathlib import Path
from _util import ROOT
from lib.sources import discover
from lib.selection import require_selection
from test_selection import fixture
class MlSourcesTests(unittest.TestCase):
 def test_no_chapter_audit_warning(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); folder=root/'복습노트/0930';folder.mkdir(parents=True)
   (folder/'정리노트_0930_test.md').write_text('노트')
   (folder/'복습문제_0930_test.md').write_text('문제')
   self.assertEqual(discover(root,'0930')['missing_optional'],[])
 def test_unicode_range_and_figures(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   for date in ['0928','0930']:
    folder=root/'복습노트'/date;folder.mkdir(parents=True)
    (folder/unicodedata.normalize('NFD',f'정리노트_{date}_test.md')).write_text('노트')
    (folder/f'복습문제_{date}_test.md').write_text('문제')
    (folder/'figure.svg').write_text('<svg/>')
   result=discover(root,'0928-0930')
   self.assertEqual(result['range'],'0928-0930');self.assertEqual(len(result['files']),6)
   self.assertTrue(all(len(f['sha256'])==64 for f in result['files']))
 def test_preview_selection_fixture(self):
  with tempfile.TemporaryDirectory() as d:
   inputs,plan=fixture(Path(d),1)
   plan['topics'][0].update(claim='사전분포가 사후분포로 갱신된다',reason='관측 전후 분포 변화')
   plan['topics'][1].update(claim='다음 수업 최적화',reason='예고: 아직 배우지 않은 범위',decision='text')
   source=plan['sources'][0]
   plan['topics'].append(dict(plan['topics'][0],id='r-prior',decision='context',claim='사전분포',reason='선수 개념'))
   plan['clips'][0]['prerequisite_ids']=['r-prior']
   require_selection(plan,inputs)
   self.assertEqual(plan['topics'][1]['decision'],'text')
   self.assertNotIn('r-text',plan['clips'][0]['requirement_ids'])
   self.assertEqual(plan['clips'][0]['prerequisite_ids'],['r-prior'])
