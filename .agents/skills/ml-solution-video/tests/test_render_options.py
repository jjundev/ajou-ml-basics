from fixtures import *
from unittest.mock import patch
from solution_video.contracts import InputError
from solution_video.util import write
from solution_video.render_options import default_render_options, load_render_options, validate_render_options, detect_hardware

M5=dict(platform='darwin',chip='Apple M5',cpu_cores=10,memory_bytes=16*1024**3)
OPTIONS=dict(schema_version=1,workers=6,encoder='cpu',browser_gpu='auto',fast_capture=False)
class RenderOptionsTests(Sandbox):
    def test_host_defaults(self):
        self.assertEqual(default_render_options(M5),OPTIONS)
        for host in [dict(M5,chip='Apple M4'),dict(M5,memory_bytes=8*1024**3),dict(M5,cpu_cores=8),dict(platform='linux'),{}]:
            self.assertEqual(default_render_options(host)['workers'],2)
    def test_missing_options_is_read_only(self):
        self.assertEqual(load_render_options(self.run,hardware=M5),OPTIONS)
        self.assertFalse((self.run/'source/render-options.json').exists())
    def test_saved_override_survives_host_change(self):
        path=self.run/'source/render-options.json';write(path,dict(OPTIONS,workers=4));before=path.read_bytes()
        for host in [M5,{},dict(platform='linux')]:
            self.assertEqual(load_render_options(self.run,hardware=host)['workers'],4)
            self.assertEqual(load_render_options(self.run,2,hardware=host)['workers'],2)
        self.assertEqual(path.read_bytes(),before)
    def test_invalid_options_fail_without_rewrite(self):
        path=self.run/'source/render-options.json'
        bad=[dict(OPTIONS,workers=v) for v in [True,0,-1,7,2.5,'6']]
        bad += [dict(OPTIONS,**kv) for kv in [dict(extra=1),dict(schema_version=2),dict(schema_version=True),dict(encoder='gpu'),dict(browser_gpu='hardware'),dict(fast_capture=True),dict(fast_capture=0)]]
        bad += [[],None,dict(workers=2)]
        for value in bad:
            with self.subTest(value=value):
                write(path,value);before=path.read_bytes()
                with self.assertRaises(InputError):load_render_options(self.run,2,hardware=M5)
                self.assertEqual(path.read_bytes(),before)
        path.write_text('{broken');before=path.read_bytes()
        with self.assertRaises(InputError):load_render_options(self.run,2,hardware=M5)
        self.assertEqual(path.read_bytes(),before)
        path.unlink()
        for value in [True,0,-1,7,2.5,'6']:
            with self.assertRaises(InputError):load_render_options(self.run,value,hardware=M5)
    def test_detection_failure_uses_legacy_workers(self):
        with patch('solution_video.render_options.sys.platform','darwin'),patch('solution_video.render_options.subprocess.run',side_effect=OSError('unavailable')):
            self.assertEqual(default_render_options()['workers'],2)
        with patch('solution_video.render_options.sys.platform','darwin'),patch('solution_video.render_options.subprocess.run',side_effect=__import__('subprocess').TimeoutExpired('sysctl',2)):
            self.assertEqual(default_render_options()['workers'],2)
    def test_validation_returns_copy(self):
        result=validate_render_options(OPTIONS);result['workers']=2
        self.assertEqual(OPTIONS['workers'],6)
