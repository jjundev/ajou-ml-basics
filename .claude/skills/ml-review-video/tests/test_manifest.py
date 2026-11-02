import unittest
from _util import minimal_manifest
from lib.manifest import validate_manifest, require_ready, ManifestError

class ManifestTest(unittest.TestCase):
    def test_required_coverage(self):
        m=minimal_manifest(); self.assertEqual(validate_manifest(m),[])
        m['segments'][0]['requirement_ids']=[]
        self.assertIn('uncovered:r-atp',validate_manifest(m))
    def test_review_is_not_just_id_link(self):
        m=minimal_manifest(); m['coverage_reviews'][0]['status']='pending'
        self.assertIn('unreviewed:r-atp',validate_manifest(m))
    def test_conflicts_and_bad_references(self):
        m=minimal_manifest(); m['conflicts']=[{'id':'c1','status':'open'}]
        self.assertIn('conflict:c1',validate_manifest(m))
        m=minimal_manifest(); m['segments'][0]['scene_id']='missing'
        with self.assertRaises(ManifestError): require_ready(m)
    def test_malformed_never_crashes(self):
        for m in (None,{}, {'sources':7}, {'schema_version':1,'topics':[None]}):
            self.assertTrue(validate_manifest(m))
    def test_missing_question_requirement_and_duplicate(self):
        m=minimal_manifest()
        m['questions']=[{'id':'q1','source_id':'src-note','locator':'#q1','requirement_ids':[]}]
        self.assertTrue(validate_manifest(m))
        m=minimal_manifest(); m['segments']*=2
        self.assertTrue(validate_manifest(m))
