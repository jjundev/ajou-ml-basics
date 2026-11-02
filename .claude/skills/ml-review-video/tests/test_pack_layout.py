import tempfile,unittest
from pathlib import Path
from _util import ROOT
from lib.sources import discover
class PackLayoutTests(unittest.TestCase):
 def test_pack_subfolder_layout(self):
  # 복습노트/<날짜>/에는 HTML만, MD·그림은 .pack/ 아래에 있다.
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); folder=root/'복습노트/1012'; figures=folder/'.pack/figures_1012'; figures.mkdir(parents=True)
   (folder/'정리노트_1012_test.html').write_text('<html></html>')
   (folder/'.pack/정리노트_1012_test.md').write_text('노트')
   (folder/'.pack/복습문제_1012_test.md').write_text('문제')
   (figures/'a.svg').write_text('<svg/>')
   for selector in ('1012',str(folder)):
    kinds=sorted(f['kind'] for f in discover(root,selector)['files'])
    self.assertEqual(kinds,['figure','note-html','note-md','questions-md'])
