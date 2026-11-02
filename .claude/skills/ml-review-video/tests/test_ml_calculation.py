import json,tempfile,unittest
from pathlib import Path
from integration_smoke import author,fixture_reload
from test_selection import fixture
class MlCalculationTests(unittest.TestCase):
 def test_slope_residual_oracle_and_recorded_states(self):
  with tempfile.TemporaryDirectory() as d:
   repo=Path(d);_,plan=fixture(repo,1);_,plan=fixture_reload(repo,plan)
   run=repo/'run';run.mkdir();author(run,plan,plan['clips'][0])
   rows=json.loads((run/'source/calculations/result.json').read_text())
   self.assertEqual(rows,[{'w':0,'sse':5},{'w':1,'sse':0},{'w':2,'sse':5}])
   evidence=json.loads((run/'source/math-evidence.json').read_text())
   self.assertEqual([s['values'] for s in evidence['scenes'][0]['states']],rows)
   self.assertIn('L350 60',(run/'assets/end.svg').read_text())
