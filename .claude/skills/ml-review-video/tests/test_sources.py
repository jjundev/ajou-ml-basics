import tempfile, unittest, unicodedata
from pathlib import Path
from unittest.mock import patch
from _util import ROOT
from lib.sources import discover, asset_path, SourceError

class SourcesTest(unittest.TestCase):
    def test_paths_range_and_invalid_date(self):
        with tempfile.TemporaryDirectory(prefix="생명 O'Brien ") as d:
            root=Path(d)
            for date in ('0915','0917'):
                p=root/'복습노트'/date
                p.mkdir(parents=True)
                (p/f'정리노트_{date}_호흡.html').write_text('ATP',encoding='utf-8')
            self.assertEqual(len(discover(root,'0915-0917')['files']),2)
            self.assertEqual(discover(root,'0915')['range'],'0915')
            for bad in ('0931','0917-0915','091'):
                with self.assertRaises(SourceError): discover(root,bad)
            with self.assertRaises(SourceError): asset_path(root,'../outside.svg')
    def test_unicode_duplicates_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'복습노트'/'0915'; p.mkdir(parents=True)
            name='정리노트_0915_호흡.html'
            names=(name,unicodedata.normalize('NFD',name))
            for n in names:
                (p/n).write_text('ATP',encoding='utf-8')
            if len(list(p.iterdir()))==1:
                # APFS treats NFC/NFD spellings as the same file. Simulate an
                # enumerator reporting both aliases so the collision rule is
                # tested here too, without requiring a case-sensitive volume.
                with patch.object(Path,'rglob',return_value=iter(p.resolve()/n for n in names)):
                    with self.assertRaises(SourceError): discover(Path(d),'0915')
            else:
                with self.assertRaises(SourceError): discover(Path(d),'0915')
    def test_partial_range_overlap_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for date in ('0915-0917','0917-0919'):
                p=Path(d)/'복습노트'/date; p.mkdir(parents=True)
                (p/f'정리노트_{date}_test.md').write_text('ATP')
            with self.assertRaises(SourceError): discover(Path(d),'0915-0919')
