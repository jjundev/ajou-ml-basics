import importlib.util,json,tempfile,unittest
from pathlib import Path
from _util import ROOT

class RenderOptionsTest(unittest.TestCase):
    def policy(self):
        self.assertIsNotNone(importlib.util.find_spec('lib.render_options'), 'render policy missing')
        from lib import render_options
        return render_options
    def test_defaults_and_unknown_hardware(self):
        p=self.policy();host=dict(platform='darwin',chip='Apple M5',cpu_cores=10,memory_bytes=16*1024**3)
        self.assertEqual(p.default_render_options(host),dict(schema_version=1,workers=6,encoder='cpu',browser_gpu='auto',fast_capture=False))
        for h in ({},dict(host,chip='Apple M4'),dict(host,memory_bytes=8*1024**3),dict(host,cpu_cores=True)):
            self.assertEqual(p.default_render_options(h)['workers'],2)
    def test_precedence_and_read_only(self):
        p=self.policy()
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);self.assertEqual(p.load_render_options(run,hardware={})['workers'],2)
            self.assertFalse((run/'source').exists())
            path=run/'source/render-options.json';path.parent.mkdir();o=p.default_render_options({});o['workers']=3;path.write_text(json.dumps(o))
            before=path.read_bytes();self.assertEqual(p.load_render_options(run)['workers'],3)
            self.assertEqual(p.load_render_options(run,6)['workers'],6);self.assertEqual(path.read_bytes(),before)
    def test_invalid_saved_policy_not_hidden_by_override(self):
        p=self.policy()
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);path=run/'source/render-options.json';path.parent.mkdir();path.write_text('{bad')
            with self.assertRaises(ValueError):p.load_render_options(run,6)
    def test_strict_workers_and_fixed_flags(self):
        p=self.policy();base=p.default_render_options({})
        for field,values in {'workers':[True,1.0,'6',0,7], 'schema_version':[True,2], 'encoder':['gpu'], 'browser_gpu':['off'], 'fast_capture':[True,0]}.items():
            for value in values:
                with self.subTest(field=field,value=value),self.assertRaises(ValueError):p.validate_render_options(dict(base,**{field:value}))
        with self.assertRaises(ValueError):p.validate_render_options(dict(base,extra=1))

    def test_matches_solution_policy_for_shared_hardware(self):
        import sys
        sys.path.insert(0,str(ROOT/'.agents/skills/ml-solution-video/scripts'))
        from solution_video.render_options import default_render_options as solution_defaults
        p=self.policy()
        for host in ({},dict(platform='darwin',chip='Apple M5',cpu_cores=10,memory_bytes=16*1024**3),dict(platform='linux',chip='unknown',cpu_cores=32,memory_bytes=64*1024**3)):
            self.assertEqual(p.default_render_options(host),solution_defaults(host))
