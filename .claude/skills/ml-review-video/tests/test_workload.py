import importlib.util,json,tempfile,unittest
from pathlib import Path
from _util import ROOT
from lib.cache import atomic_json

M5=dict(platform='darwin',chip='Apple M5',cpu_cores=10,memory_bytes=16*1024**3)
AUTO=dict(schema_version=2,workers='auto',encoder='cpu',browser_gpu='auto',fast_capture=False)
def fixture(run,duration=.6,frames=900):
    part=dict(id='scene-a',entry='scene-a.html',frames=frames)
    length=frames*800
    atomic_json(run/'source/timeline.json',dict(rate=24000,fps=30,scenes=[dict(id='scene-a',start_sample=0,end_sample=length,first_frame=0,last_frame=frames)],segments=[dict(id='seg-a',scene_id='scene-a',start_sample=0,end_sample=length)]))
    atomic_json(run/'source/scene-fragments/scene-a.motion.json',[dict(segment_id='seg-a',target='#x',kind='move',duration_s=duration,**{'from':{'x':0},'to':{'x':100}})])
    return part

class WorkloadTest(unittest.TestCase):
    def resolver(self):
        from lib import render_options
        self.assertTrue(hasattr(render_options,'resolve_scene_workers'),'automatic selector missing')
        return render_options.resolve_scene_workers
    def test_static_dynamic_threshold_and_short_scene(self):
        resolve=self.resolver()
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)
            for duration,frames,expected in [(.6,900,2),(24,900,6),(15,900,2),(15.01,900,6),(2,60,2)]:
                part=fixture(run,duration,frames);decision=resolve(run,part,AUTO,hardware=M5)
                self.assertEqual(decision['workers'],expected)
                self.assertAlmostEqual(decision['motion_ratio'],duration/(frames/30))
    def test_overlap_is_not_counted_twice_and_clips_to_scene(self):
        resolve=self.resolver()
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);part=fixture(run,12);path=run/'source/scene-fragments/scene-a.motion.json';one=json.loads(path.read_text())[0];atomic_json(path,[one,dict(one,target='#y')])
            decision=resolve(run,part,AUTO,hardware=M5);self.assertEqual(decision['workers'],2);self.assertEqual(decision['animated_seconds'],12)
    def test_unchanged_properties_do_not_count_as_motion(self):
        resolve=self.resolver()
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);part=fixture(run,24);path=run/'source/scene-fragments/scene-a.motion.json';motions=json.loads(path.read_text());motions[0]['to']=motions[0]['from'];atomic_json(path,motions)
            self.assertEqual(resolve(run,part,AUTO,hardware=M5)['motion_ratio'],0)
    def test_unknown_hardware_missing_metadata_and_manual_override(self):
        resolve=self.resolver()
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);part=fixture(run,24)
            self.assertEqual(resolve(run,part,AUTO,hardware={})['workers'],2)
            self.assertEqual(resolve(run,part,dict(AUTO,workers=4),hardware={})['workers'],4)
            (run/'source/scene-fragments/scene-a.motion.json').unlink()
            self.assertEqual(resolve(run,part,AUTO,hardware=M5)['workers'],2)
    def test_invalid_metadata_rejected_and_read_only(self):
        resolve=self.resolver()
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);part=fixture(run,24);paths=list((run/'source').rglob('*.json'));before={p:p.read_bytes() for p in paths}
            resolve(run,part,AUTO,hardware=M5);self.assertEqual(before,{p:p.read_bytes() for p in paths})
            path=run/'source/scene-fragments/scene-a.motion.json'
            for bad in ('{bad','{}','[{"segment_id":"seg-a","duration_s":NaN}]'):
                path.write_text(bad)
                with self.assertRaises(ValueError):resolve(run,part,AUTO,hardware=M5)
    def test_partial_properties_only_destination_changes_count(self):
        resolve=self.resolver()
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);part=fixture(run,24);path=run/'source/scene-fragments/scene-a.motion.json';m=json.loads(path.read_text())[0]
            m['from']={'x':0,'opacity':1};m['to']={'opacity':1};atomic_json(path,[m])
            decision=resolve(run,part,AUTO,hardware=M5);self.assertEqual(decision['workers'],2);self.assertEqual(decision['motion_ratio'],0)
            m['to']={};atomic_json(path,[m]);self.assertEqual(resolve(run,part,AUTO,hardware=M5)['motion_ratio'],0)
            m['to']={'opacity':0};atomic_json(path,[m]);self.assertEqual(resolve(run,part,AUTO,hardware=M5)['workers'],6)
    def test_missing_metadata_does_not_hide_present_corruption(self):
        resolve=self.resolver()
        for missing in ('timeline','motion'):
            with self.subTest(missing=missing),tempfile.TemporaryDirectory() as d:
                run=Path(d);part=fixture(run,24);timeline=run/'source/timeline.json';motion=run/'source/scene-fragments/scene-a.motion.json'
                (timeline if missing=='timeline' else motion).unlink();(motion if missing=='timeline' else timeline).write_text('{bad')
                with self.assertRaises(ValueError):resolve(run,part,AUTO,hardware=M5)
