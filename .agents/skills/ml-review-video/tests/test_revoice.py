import unittest
from _util import ROOT
from lib.revoice import plan_revoice

class RevoiceTest(unittest.TestCase):
    def test_extreme_zero_and_hash(self):
        old={'fps':30,'windows':[{'id':'a-1','scene_id':'a','first_frame':0,'last_frame':30}]}
        for finish in (0,90):
            new={'fps':30,'windows':[{'id':'a-1','scene_id':'a','first_frame':0,'last_frame':finish}]}
            self.assertEqual(plan_revoice(old,new,'hash',{'a'})[0]['mode'],'rerender')
        a=plan_revoice(old,old,'a',{'a'}); b=plan_revoice(old,old,'b',{'a'})
        self.assertNotEqual(a[0]['key'],b[0]['key'])
    def test_mismatch_and_overlap(self):
        old={'fps':30,'windows':[{'id':'a','scene_id':'a','first_frame':0,'last_frame':30}]}
        with self.assertRaises(ValueError): plan_revoice(old,{'fps':30,'windows':[]},'a',{'a'})
    def test_picture_dependency_change_invalidates_retime(self):
        import tempfile
        from pathlib import Path
        from lib.revoice import picture_fingerprint
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); p=root/'assets/diagram.svg'; p.parent.mkdir()
            p.write_text('<svg/>')
            a=picture_fingerprint(root,'scene-a')
            p.write_text('<svg><rect/></svg>')
            self.assertNotEqual(a,picture_fingerprint(root,'scene-a'))
