import tempfile,unittest,subprocess,json,shutil
from pathlib import Path
from _util import pcm
from lib.render import choose_backend,mux,probe_backends
from lib.cache import file_hash

class RenderTest(unittest.TestCase):
    def test_cpu_fallback(self):
        b=choose_backend([{'encoder':'h264_nvenc','ok':False,'seconds':0,'workers':1},
                          {'encoder':'libx264','ok':True,'seconds':2,'workers':1}])
        self.assertEqual(b['encoder'],'libx264')
    def test_probe_duration_not_part_of_render_key(self):
        from lib.render import stable_backend
        a={'encoder':'h264_nvenc','seconds':1,'workers':1,'ok':True}
        b=dict(a,seconds=2,workers=2)
        self.assertEqual(stable_backend(a),stable_backend(b))
    @unittest.skipUnless(shutil.which('ffmpeg'),'FFmpeg required')
    def test_mux_korean_quote_path_and_decode(self):
        with tempfile.TemporaryDirectory(prefix="생명 O'Brien ") as d:
            run=Path(d); video=run/'original.mp4'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=black:s=1920x1080:r=30',
              '-frames:v','60','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',str(video)],check=True)
            before=file_hash(video); pcm(run/'voice.wav',48000)
            t={'rate':24000,'total_samples':48000,'total_frames':60,'segments':[{'id':'s','start_sample':0,'end_sample':48000}]}
            mux([video],[{'id':'s','path':'voice.wav','samples':48000}],t,run/'review.mp4')
            subprocess.run(['ffmpeg','-v','error','-i',str(run/'review.mp4'),'-f','null','-'],check=True)
            self.assertEqual(before,file_hash(video))
            data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(run/'review.mp4')]))
            self.assertEqual(sum(s['codec_type']=='audio' for s in data['streams']),1)


class CapturePolicyTest(unittest.TestCase):
    def setup_run(self,run):
        from lib.cache import atomic_json
        entry=run/'cli.js';entry.write_text('test')
        parts=[dict(id='scene-a',entry='scene-a.html',frames=30),dict(id='scene-b',entry='scene-b.html',frames=30)]
        for p in parts:(run/p['entry']).write_text('<html data-theme="dark"></html>')
        options=dict(schema_version=1,workers=6,encoder='cpu',browser_gpu='auto',fast_capture=False)
        atomic_json(run/'source/render-options.json',options)
        return parts,dict(encoder='libx264',workers=2,hyperframes_entry=str(entry),render_options=options,capture_gpu=True)
    def test_settings_receipts_cache_and_changed_workers(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        from lib.render import render_parts
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);parts,backend=self.setup_run(run);seen=[]
            def tool(args,cwd=None,timeout=300):
                if 'render' in args:
                    seen.append(list(map(str,args)));Path(args[args.index('--output')+1]).write_bytes(b'new')
                return SimpleNamespace(returncode=0,stdout='0.8.137',stderr='')
            with patch('lib.render.command',side_effect=tool),patch('lib.render.frames_ok',return_value=True):
                outputs=render_parts(parts,run,backend)
                self.assertEqual([a[a.index('--composition')+1] for a in seen],['scene-a.html','scene-b.html'])
                self.assertTrue(all(str(a[a.index('--workers')+1])=='6' for a in seen))
                self.assertTrue(all('--experimental-fast-capture=false' in a and '--gpu' not in a and '--browser-gpu' not in a for a in seen))
                receipt=json.loads(outputs[0].with_suffix('.json').read_text())
                self.assertEqual(receipt['render_options'],backend['render_options']);self.assertEqual(receipt['args'],seen[0]);self.assertGreaterEqual(receipt['elapsed_seconds'],0)
                render_parts(parts,run,backend);self.assertEqual(len(seen),2)
                backend['render_options']['workers']=2;render_parts(parts,run,backend);self.assertEqual(len(seen),4)
    def test_failed_render_keeps_old_outputs_and_removes_stale_pending(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        from lib.render import render_parts
        for failure in ('nonzero','stale','timeout'):
            with self.subTest(failure=failure),tempfile.TemporaryDirectory() as d:
                run=Path(d);parts,backend=self.setup_run(run);dest=run/'renders/parts';dest.mkdir(parents=True)
                out=dest/'scene-a.mp4';out.write_bytes(b'old');receipt=out.with_suffix('.json');receipt.write_text('{}');pending=dest/'scene-a.pending.mp4';pending.write_bytes(b'stale')
                def tool(args,cwd=None,timeout=300):
                    if 'render' not in args:return SimpleNamespace(returncode=0,stdout='v',stderr='')
                    if failure=='timeout':raise subprocess.TimeoutExpired(args,1,output='partial output',stderr='timeout detail')
                    return SimpleNamespace(returncode=1 if failure=='nonzero' else 0,stdout='partial output',stderr='detail')
                with patch('lib.render.command',side_effect=tool),patch('lib.render.frames_ok',side_effect=lambda p,n:Path(p).is_file()):
                    with self.assertRaises((RuntimeError,subprocess.TimeoutExpired)):render_parts(parts[:1],run,backend)
                self.assertEqual(out.read_bytes(),b'old');self.assertEqual(receipt.read_text(),'{}');self.assertFalse(pending.exists())
                self.assertIn('partial output',out.with_suffix('.log').read_text())
    def test_frames_require_30fps(self):
        from unittest.mock import patch
        from lib.render import frames_ok
        with patch('lib.render.probe_media',return_value={'streams':[dict(codec_type='video',nb_frames='30',width=1920,height=1080,r_frame_rate='60/1')]}):
            self.assertFalse(frames_ok('unused',30))

    def test_renderer_code_change_invalidates_part_cache(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        from lib.render import render_parts
        from lib.cache import file_hash as original
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);parts,backend=self.setup_run(run);seen=[]
            def tool(args,cwd=None,timeout=300):
                if 'render' in args:seen.append(args);Path(args[args.index('--output')+1]).write_bytes(b'new')
                return SimpleNamespace(returncode=0,stdout='v',stderr='')
            with patch('lib.render.command',side_effect=tool),patch('lib.render.frames_ok',return_value=True):
                render_parts(parts[:1],run,backend)
                def changed(path):return 'changed-policy-code' if Path(path).name=='render_options.py' else original(path)
                with patch('lib.render.file_hash',side_effect=changed):render_parts(parts[:1],run,backend)
            self.assertEqual(len(seen),2)


class FailureSafetyTest(unittest.TestCase):
    def test_part_receipt_write_failure_preserves_previous_pair(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        from lib.render import render_parts
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);parts,backend=CapturePolicyTest().setup_run(run);out=run/'renders/parts/scene-a.mp4';out.parent.mkdir(parents=True);out.write_bytes(b'old');receipt=out.with_suffix('.json');receipt.write_text('{}')
            def tool(args,cwd=None,timeout=300):
                if 'render' in args:Path(args[args.index('--output')+1]).write_bytes(b'new')
                return SimpleNamespace(returncode=0,stdout='v',stderr='')
            with patch('lib.render.command',side_effect=tool),patch('lib.render.frames_ok',return_value=True),patch('lib.render.atomic_json',side_effect=OSError('receipt failed')):
                with self.assertRaises(OSError):render_parts(parts[:1],run,backend)
            self.assertEqual(out.read_bytes(),b'old');self.assertEqual(receipt.read_text(),'{}')
    def transaction(self):
        import lib.render as render
        self.assertTrue(hasattr(render,'commit_media_receipt'),'transaction missing')
        return render.commit_media_receipt
    def test_pair_replace_failure_and_interrupt_restore_previous_pair(self):
        from unittest.mock import patch
        import os
        commit=self.transaction()
        for error in [OSError('rename failed'),KeyboardInterrupt()]:
            with self.subTest(error=type(error).__name__),tempfile.TemporaryDirectory() as d:
                run=Path(d);master=run/'review.mp4';receipt=run/'receipt.json';pending=run/'new.mp4'
                master.write_bytes(b'old');receipt.write_text('{}');pending.write_bytes(b'new');original=os.replace
                def replace(a,b):
                    if Path(b)==receipt and '.rollback' not in Path(a).name:raise error
                    return original(a,b)
                with patch('lib.render.os.replace',side_effect=replace),self.assertRaises(type(error)):commit(pending,{'new':True},master,receipt)
                self.assertEqual(master.read_bytes(),b'old');self.assertEqual(receipt.read_text(),'{}')
    def test_failed_restore_keeps_backup_and_blocks_retry(self):
        from unittest.mock import patch
        import os
        commit=self.transaction()
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);master=run/'review.mp4';receipt=run/'receipt.json';pending=run/'new.mp4'
            master.write_bytes(b'old');receipt.write_text('{}');pending.write_bytes(b'new');original=os.replace
            def replace(a,b):
                if Path(b)==receipt or '.rollback' in Path(a).name:raise OSError('rename failed')
                return original(a,b)
            with patch('lib.render.os.replace',side_effect=replace),self.assertRaises(RuntimeError):commit(pending,{'new':True},master,receipt)
            backup=master.with_name(master.name+'.rollback');self.assertEqual(backup.read_bytes(),b'old')
            pending.write_bytes(b'retry')
            with self.assertRaises(RuntimeError):commit(pending,{'retry':True},master,receipt)
            self.assertEqual(backup.read_bytes(),b'old')
    @unittest.skipIf(__import__('os').name=='nt','POSIX process-tree probe')
    def test_timeout_kills_detached_descendant_before_pending_cleanup(self):
        import sys,time,os
        from lib.render import command
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);pidfile=run/'pid.txt';late=run/'late.mp4'
            child="import time;from pathlib import Path;time.sleep(.8);Path("+repr(str(late))+").write_bytes(b'orphan')"
            parent="import subprocess,sys,time;from pathlib import Path;p=subprocess.Popen([sys.executable,'-c',"+repr(child)+"],start_new_session=True);Path("+repr(str(pidfile))+").write_text(str(p.pid));print('parent ready',flush=True);time.sleep(10)"
            try:
                with self.assertRaises(subprocess.TimeoutExpired) as caught:command([sys.executable,'-c',parent],timeout=.4)
                output=caught.exception.stdout
                self.assertIn('parent ready',output.decode() if isinstance(output,bytes) else output)
                time.sleep(.7);self.assertFalse(late.exists(),'orphan wrote after timeout cleanup')
            finally:
                if pidfile.exists():
                    try:os.kill(int(pidfile.read_text()),9)
                    except ProcessLookupError:pass

class MuxPendingCleanupTest(unittest.TestCase):
    def test_failed_mux_removes_inner_pending(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        from lib.render import mux_with_receipt,cpu_backend
        from lib.render_options import default_render_options
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);part=run/'part.mp4';part.write_bytes(b'part');pcm(run/'voice.wav',24000)
            timeline=dict(rate=24000,total_samples=24000,total_frames=30,segments=[dict(id='s',start_sample=0,end_sample=24000)])
            def fail(args,**kwargs):
                if 'concat' in args:
                    Path(args[-1]).write_bytes(b'failed pending');return SimpleNamespace(returncode=1,stdout='',stderr='failed')
                Path(args[-1]).write_bytes(b'copied part');return SimpleNamespace(returncode=0,stdout='',stderr='')
            with patch('lib.render.command',side_effect=fail),self.assertRaises(RuntimeError):
                mux_with_receipt([part],[dict(id='s',path='voice.wav',samples=24000)],timeline,run/'review.mp4',cpu_backend(run/'cli.js',default_render_options({})))
            self.assertFalse(list(run.glob('*.pending*.mp4')))
