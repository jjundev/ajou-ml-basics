import copy,json,tempfile,unittest
from pathlib import Path
from _util import minimal_manifest
from lib.cache import atomic_json,file_hash
from lib.verify import review_fingerprint,verify_run,DOMAINS
from lib.math_evidence import validate_math_evidence,math_evidence_files

def write_evidence(run,m,numeric=False):
    rows=[]; hashes={}
    for scene in m['scenes']:
        row={'scene_id':scene['id'],'mode':'qualitative','formula_refs':['definition'],
             'conditions':['given model'],'axes':['not applicable'], 'units':['dimensionless'],
             'dimensions':['scalar'],'reason':'This scene explains a qualitative relationship without numeric claims.'}
        if numeric:
            row.update(mode='numeric',calculation_script='source/calculation.py',calculation_result='source/result.json',
                states=[{'label':x,'figure_path':f'source/{x}.svg','values':{'slope':i,'sse':[5,0,5][i]}} for i,x in enumerate(['start','middle','end'])])
            for relative,text in [('source/calculation.py','print([5,0,5])'),('source/result.json','[5,0,5]')]+[(f'source/{x}.svg','<svg/>') for x in ['start','middle','end']]:
                p=run/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);hashes[relative]=file_hash(p)
        rows.append(row)
    e={'schema_version':1,'scenes':rows,'file_hashes':hashes}
    atomic_json(run/'source/math-evidence.json',e);return e

class MathEvidenceTests(unittest.TestCase):
 def setUp(self):
    self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
    self.run=Path(self.tmp.name);self.m=minimal_manifest()
 def test_numeric_evidence_complete(self):
    write_evidence(self.run,self.m,True)
    self.assertEqual(validate_math_evidence(self.run,self.m),[])
    self.assertEqual(len(math_evidence_files(self.run)),6)
 def test_qualitative_reason_required(self):
    e=write_evidence(self.run,self.m);self.assertEqual(validate_math_evidence(self.run,self.m),[])
    e['scenes'][0]['reason']='';atomic_json(self.run/'source/math-evidence.json',e)
    self.assertTrue(validate_math_evidence(self.run,self.m))
 def test_missing_scene_or_axes(self):
    self.assertTrue(validate_math_evidence(self.run,self.m))
    for change in ['missing','axes','duplicate','unknown']:
      e=write_evidence(self.run,self.m,True)
      if change=='missing':e['scenes']=[]
      if change=='axes':del e['scenes'][0]['axes']
      if change=='duplicate':e['scenes'].append(copy.deepcopy(e['scenes'][0]))
      if change=='unknown':e['scenes'][0]['scene_id']='unknown'
      atomic_json(self.run/'source/math-evidence.json',e)
      self.assertTrue(validate_math_evidence(self.run,self.m),change)
 def test_unsafe_evidence_path(self):
    e=write_evidence(self.run,self.m,True)
    e['scenes'][0]['calculation_script']='../external.py'
    atomic_json(self.run/'source/math-evidence.json',e)
    self.assertTrue(validate_math_evidence(self.run,self.m))
    with tempfile.TemporaryDirectory() as d:
      external=Path(d)/'result';external.write_text('external')
      p=self.run/'source/result.json';p.unlink();p.symlink_to(external)
      e=write_evidence(self.run,self.m)
      e['file_hashes']={'source/result.json':file_hash(external)}
      atomic_json(self.run/'source/math-evidence.json',e)
      self.assertTrue(validate_math_evidence(self.run,self.m))
 def test_modified_result_invalidates_review(self):
    write_evidence(self.run,self.m,True)
    evidence=self.run/'verification/review.txt';evidence.parent.mkdir();evidence.write_text('reviewed')
    key=review_fingerprint(self.run,self.m)
    reports={d:{'status':'passed','evidence':['verification/review.txt'],'input_hash':key} for d in DOMAINS}
    self.assertTrue(verify_run(self.run,self.m,reports)['complete'])
    (self.run/'source/result.json').write_text('[0,0,0]')
    self.assertNotEqual(review_fingerprint(self.run,self.m),key)
    self.assertFalse(verify_run(self.run,self.m,reports)['complete'])
    self.assertTrue(validate_math_evidence(self.run,self.m))
 def test_invalid_schema_is_reported(self):
    for value in [[],None,{'schema_version':1,'scenes':[None]}, {'schema_version':1,'scenes':[],'file_hashes':[]}]:
      atomic_json(self.run/'source/math-evidence.json',value)
      self.assertTrue(validate_math_evidence(self.run,self.m))
