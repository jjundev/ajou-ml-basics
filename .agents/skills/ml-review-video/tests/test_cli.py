import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from _util import ROOT
from video import main

class CliTest(unittest.TestCase):
    def test_prepare_free_invalid_range_nonzero(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); p=root/'복습노트/0915'; p.mkdir(parents=True)
            (p/'정리노트_0915_test.md').write_text('수업 기준 32 ATP',encoding='utf-8')
            with patch('urllib.request.urlopen',side_effect=AssertionError('network forbidden')):
                self.assertEqual(main(['prepare','--repo',str(root),'0915']),0)
                self.assertNotEqual(main(['prepare','--repo',str(root),'0931']),0)
            runs=list((root/'복습영상/0915/0915_제작자료/실행').iterdir())
            self.assertEqual(len(runs),1); self.assertTrue((runs[0]/'source/inputs.json').is_file())
    def test_resume_reports_next_step(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(main(['resume','--run',d]),0)
    def test_render_cannot_skip_changed_voice_stage(self):
        from _util import minimal_manifest
        from lib.cache import atomic_json
        from video import finish
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)
            atomic_json(run/'manifest.json',minimal_manifest())
            atomic_json(run/'source/audio.json',{'voices':[]})
            atomic_json(run/'config.json',{'voice':'Aoede'})
            finish(run,'voice',[run/'source/audio.json'])
            atomic_json(run/'source/parts.json',{'parts':[]})
            finish(run,'composition',[run/'source/parts.json'])
            atomic_json(run/'config.json',{'voice':'Charon'})
            with patch('video.probe_backends',side_effect=AssertionError('stale render')):
                self.assertEqual(main(['render','--run',str(run),'--hyperframes-entry','unused']),1)
    def test_check_rejects_missing_math_evidence(self):
        from _util import minimal_manifest
        from lib.cache import atomic_json
        from video import finish
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);atomic_json(run/'source/inputs.json',{})
            atomic_json(run/'manifest.json',minimal_manifest())
            finish(run,'inputs',[run/'source/inputs.json'])
            self.assertEqual(main(['check','--run',str(run)]),1)

    def test_revoice_preparation_from_batch_is_independent(self):
        import json
        from test_selection import fixture,manifest_for
        from test_math_evidence import write_evidence
        from lib.batch import prepare_set,budget_path
        from lib.cache import atomic_json
        with tempfile.TemporaryDirectory() as d:
            repo=Path(d);inputs,plan=fixture(repo,1)
            batch=prepare_set(repo,'1001',plan,{})
            old=batch/'videos/clip-0';m=manifest_for(plan,plan['clips'][0])
            atomic_json(old/'manifest.json',m);write_evidence(old,m)
            (old/'assets').mkdir()
            self.assertEqual(main(['prepare','--repo',str(repo),'--from-run',str(old),'--voice','Charon']),0)
            new=next(p for p in (repo/'복습영상/1001/1001_제작자료/실행').iterdir() if p!=batch)
            self.assertFalse((new/'source/clip-scope.json').exists())
            self.assertEqual(budget_path(new),new.resolve()/'cost-ledger.json')
