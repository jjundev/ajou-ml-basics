import tempfile, unittest, json
from pathlib import Path
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from _util import ROOT
from lib.cache import digest,file_hash,cache_valid,atomic_json
from lib.state import RunStore
from lib.budget import Budget

class StateTest(unittest.TestCase):
    def test_cache_content_and_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'part.mp4'; p.write_bytes(b'old')
            k=digest({'frames':90,'text':'32 ATP'})
            receipt={'key':k,'output_sha256':file_hash(p)}
            self.assertTrue(cache_valid(p,receipt,k))
            self.assertFalse(cache_valid(p,receipt,digest({'frames':90,'text':'30 ATP'})))
            p.write_bytes(b'corrupt'); self.assertFalse(cache_valid(p,receipt,k))
    def test_atomic_failure_preserves_state(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'run.json'; atomic_json(p,{'stage':'voice'})
            with patch('lib.cache.os.replace',side_effect=OSError('interrupted')):
                with self.assertRaises(OSError): atomic_json(p,{'stage':'render'})
            self.assertEqual(json.loads(p.read_text())['stage'],'voice')
    def test_concurrent_budget_and_unknown_charge(self):
        with tempfile.TemporaryDirectory() as d:
            b=Budget(Path(d)/'ledger.json',Decimal('2'))
            with ThreadPoolExecutor(max_workers=2) as pool:
                r=list(pool.map(lambda i:b.reserve(str(i),Decimal('1.2')),range(2)))
            self.assertEqual(sorted(r),[False,True])
            b.settle(str(r.index(True)),None)
            self.assertEqual(b.remaining(),Decimal('.8'))
            self.assertFalse(b.reserve('retry',Decimal('.9')))
    def test_invalidate_and_lock(self):
        with tempfile.TemporaryDirectory() as d:
            store=RunStore(Path(d)); store.save({'stages':{'voice':{'status':'passed'},'render':{'status':'passed'}}})
            store.invalidate('voice')
            self.assertEqual(store.load()['stages']['render']['status'],'pending')
            with store.lock():
                with self.assertRaises(RuntimeError):
                    with RunStore(Path(d)).lock(): pass
    def test_resume_detects_changed_voice_config(self):
        from video import finish
        with tempfile.TemporaryDirectory() as d:
            run=Path(d); atomic_json(run/'config.json',{'voice':'Aoede'})
            atomic_json(run/'manifest.json',{'segments':[]})
            atomic_json(run/'source/audio.json',{'voices':[]})
            finish(run,'voice',[run/'source/audio.json'])
            atomic_json(run/'config.json',{'voice':'Charon'})
            self.assertEqual(RunStore(run).recover(),'voice')

    def test_render_options_only_invalidate_render_onwards(self):
        from lib.state import stage_fingerprint
        from video import finish
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);atomic_json(run/'manifest.json',{'segments':[]});atomic_json(run/'source/parts.json',{'parts':[]})
            atomic_json(run/'source/render-options.json',{'workers':2});(run/'review.mp4').write_bytes(b'previous')
            finish(run,'voice',[run/'manifest.json']);finish(run,'composition',[run/'source/parts.json']);finish(run,'render',[run/'review.mp4'])
            fingerprints={s:stage_fingerprint(run,s) for s in ('voice','timing','composition','render')}
            atomic_json(run/'source/render-options.json',{'workers':6})
            for s in ('voice','timing','composition'):self.assertEqual(fingerprints[s],stage_fingerprint(run,s))
            self.assertNotEqual(fingerprints['render'],stage_fingerprint(run,'render'))
            self.assertEqual(RunStore(run).recover(),'render');self.assertEqual(RunStore(run).load()['stages']['voice']['status'],'passed')
    def test_composition_code_change_requires_reassemble_keeps_voice(self):
        from video import finish
        from lib.cache import file_hash as original
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);atomic_json(run/'manifest.json',{'segments':[]});atomic_json(run/'source/parts.json',{'parts':[]});(run/'review.mp4').write_bytes(b'previous')
            finish(run,'voice',[run/'manifest.json']);finish(run,'composition',[run/'source/parts.json']);finish(run,'render',[run/'review.mp4'])
            def changed(path):return 'changed-composition-code' if Path(path).name=='composition.py' else original(path)
            with patch('lib.state.file_hash',side_effect=changed):self.assertEqual(RunStore(run).recover(),'composition')
            self.assertEqual(RunStore(run).load()['stages']['voice']['status'],'passed')
