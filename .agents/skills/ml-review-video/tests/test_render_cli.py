from test_cli import *

class RenderCliTest(unittest.TestCase):
    def test_render_workers_is_render_and_revoice_only(self):
        from video import parser
        self.assertIn('--render-workers',parser()._subparsers._group_actions[0].choices['render'].format_help())
        for mode in ('render','revoice'):
            extra=['--source-run','old'] if mode=='revoice' else []
            self.assertEqual(parser().parse_args([mode,'--run','run','--render-workers','6',*extra]).render_workers,6)
        for argv in (['render','--run','r','--render-workers','7'],['tts','--run','r','--render-workers','2']):
            with self.assertRaises(SystemExit):parser().parse_args(argv)
    def test_render_saves_policy_before_recovery_without_changing_voice_config(self):
        import json
        from video import parser
        self.assertIn('--render-workers',parser()._subparsers._group_actions[0].choices['render'].format_help())
        from lib.state import RunStore
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);seen=[]
            def recover(store):
                seen.append(json.loads((store.run/'source/render-options.json').read_text()))
            with patch.object(RunStore,'recover',recover):
                self.assertEqual(main(['render','--run',d,'--render-workers','3']),1)
            self.assertEqual(seen[0]['workers'],3)
            self.assertNotIn('render_workers',json.loads((run/'config.json').read_text()))

    def test_render_and_revoice_dispatch_cpu_policy_and_register_receipt(self):
        import json
        from _util import minimal_manifest
        from lib.cache import atomic_json
        from lib.timing import build_timeline
        from lib.state import RunStore
        for mode in ('render','revoice'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as d:
                run=Path(d)/'run';run.mkdir();old=Path(d)/'old';old.mkdir();m=minimal_manifest()
                audio=[dict(id='seg-atp',samples=24000,rate=24000,path='voice.wav')];timeline=build_timeline(m,audio)
                for base in (run,old):
                    atomic_json(base/'manifest.json',m);atomic_json(base/'source/theme.json',{})
                    atomic_json(base/'source/timeline.json',timeline);(base/'review.mp4').write_bytes(b'old')
                atomic_json(run/'source/audio.json',{'voices':audio});atomic_json(run/'source/parts.json',{'parts':[dict(id='scene-atp',entry='scene-atp.html',frames=78)]})
                capture=run/'renders/parts/scene-atp.mp4';capture.parent.mkdir(parents=True);capture.write_bytes(b'part')
                atomic_json(capture.with_suffix('.json'),{'args':['actual capture'],'frames':78})
                RunStore(run).save({'stages':{'composition':{'status':'passed'}}})
                seen=[]
                def render(parts,run,backend):seen.append(backend);return [capture]
                def fake_mux(parts,audio,t,destination):Path(destination).write_bytes(b'new-master')
                extra=['--source-run',str(old)] if mode=='revoice' else []
                with patch.object(RunStore,'recover',return_value='render'),patch('video.render_parts',side_effect=render),patch('lib.render.mux',side_effect=fake_mux),patch('video.probe_backends',side_effect=AssertionError('auto GPU probe forbidden')),patch('video.plan_revoice',return_value=[dict(scene_id='scene-atp',mode='rerender')]),patch('video.render_revoice',return_value=[capture]):
                    self.assertEqual(main([mode,'--run',str(run),'--hyperframes-entry','unused','--render-workers','6',*extra]),0)
                self.assertEqual(seen[0]['encoder'],'libx264');self.assertEqual(seen[0]['workers'],1);self.assertEqual(seen[0]['render_options']['workers'],6)
                state=RunStore(run).load();self.assertIn('verification/render-receipt.json',state['stages']['render']['output_hashes'])
                self.assertEqual(json.loads((run/'verification/render-receipt.json').read_text())['render_options']['workers'],6)

    def test_resume_legacy_run_does_not_create_options(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(main(['resume','--run',d]),0)
            self.assertFalse((Path(d)/'source/render-options.json').exists())

    def test_master_receipt_failure_preserves_previous_pair(self):
        from _util import minimal_manifest
        from lib.cache import atomic_json
        from lib.state import RunStore
        from lib.timing import build_timeline
        import lib.render as render
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);m=minimal_manifest();audio=[dict(id='seg-atp',samples=24000,rate=24000,path='voice.wav')]
            atomic_json(run/'manifest.json',m);atomic_json(run/'source/audio.json',{'voices':audio});atomic_json(run/'source/parts.json',{'parts':[]})
            atomic_json(run/'source/timeline.json',build_timeline(m,audio));RunStore(run).save({'stages':{'composition':{'status':'passed'}}});(run/'review.mp4').write_bytes(b'old');atomic_json(run/'verification/render-receipt.json',{'old':True})
            def fake_mux(parts,audio,t,destination):Path(destination).write_bytes(b'new')
            with patch.object(RunStore,'recover',return_value='render'),patch('video.render_parts',return_value=[]),patch('lib.render.mux',side_effect=fake_mux),patch('video.mux',side_effect=fake_mux),patch('lib.render.atomic_json',side_effect=OSError('receipt failed')):
                self.assertEqual(main(['render','--run',str(run),'--hyperframes-entry','unused']),1)
            self.assertEqual((run/'review.mp4').read_bytes(),b'old');self.assertEqual(__import__('json').loads((run/'verification/render-receipt.json').read_text()),{'old':True})

    def test_prepare_from_run_preserves_saved_workers(self):
        import json,contextlib,io
        from lib.cache import atomic_json
        with tempfile.TemporaryDirectory() as d:
            repo=Path(d);note=repo/'복습노트/0915';note.mkdir(parents=True);(note/'정리노트_0915_test.md').write_text('ML concept')
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(main(['prepare','--repo',str(repo),'0915']),0)
            old=Path(json.loads(out.getvalue())['run']);options=json.loads((old/'source/render-options.json').read_text());options['workers']=3;atomic_json(old/'source/render-options.json',options)
            atomic_json(old/'manifest.json',{'range':'0915','title':'test'})
            (old/'assets').mkdir()
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(main(['prepare','--repo',str(repo),'--from-run',str(old)]),0)
            new=Path(json.loads(out.getvalue())['run']);self.assertEqual(json.loads((new/'source/render-options.json').read_text()),options)
