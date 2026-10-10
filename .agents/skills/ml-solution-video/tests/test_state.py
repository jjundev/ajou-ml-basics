from fixtures import *
from solution_video.state import finish_stage,recover_run,STAGES
from solution_video.util import write
class StateTests(Sandbox):
    def test_chunk_receipt_and_trim_invalidate_timing(self):
        for stage in STAGES[:5]:
            out=self.run/(stage+'.txt');out.write_text(stage);finish_stage(self.run,stage,[out])
        write(self.run/'source/chunk-audio.json',dict(voices=[]))
        self.assertEqual(recover_run(self.run),'timing')
        finish_stage(self.run,'timing',[self.run/'timing.txt'])
        write(self.run/'source/chunk-trims.json',dict(schema_version=1,rows=[]))
        self.assertEqual(recover_run(self.run),'timing')
    def test_lesson_edit_invalidates_script(self):
        from solution_video.state import stage_fingerprint
        before=stage_fingerprint(self.run,'script')
        write(self.run/'source/lesson.json',{'schema_version':1,'steps':[]})
        added=stage_fingerprint(self.run,'script');self.assertNotEqual(before,added)
        write(self.run/'source/lesson.json',{'schema_version':1,'steps':[{'exemption_reason':'changed'}]})
        self.assertNotEqual(added,stage_fingerprint(self.run,'script'))
        (self.run/'source/lesson.json').unlink();self.assertEqual(before,stage_fingerprint(self.run,'script'))
    def test_caption_edit_invalidates_script_preserving_pcm(self):
        from solution_video.state import stage_fingerprint
        from solution_video.util import file_hash
        a=make_audio('w',2400,self.run);sha=file_hash(self.run/a['path'])
        write(self.run/'source/manifest.json',dict(segments=[dict(id='w',text='알 오 원',caption_text='r_O1')]))
        before=stage_fingerprint(self.run,'script')
        write(self.run/'source/manifest.json',dict(segments=[dict(id='w',text='알 오 원',caption_text='저항 r_O1')]))
        self.assertNotEqual(before,stage_fingerprint(self.run,'script'));self.assertEqual(sha,file_hash(self.run/a['path']))
    def test_first_invalid_stage_and_voice_preservation(self):
        (self.run/'source').mkdir(); (self.run/'layers').mkdir(); write(self.run/'source/map.json',{'work_bbox':[1,2,3,4]}); write(self.run/'source/config.json',{'voice':'Aoede'})
        pub=self.run/'published.mp4';pub.write_bytes(b'published')
        from solution_video.util import file_hash
        write(self.run/'verification/publication.json',{'published':{str(pub):file_hash(pub)}})
        for stage in STAGES:
            out=self.run/(stage+'.txt'); out.write_text(stage); finish_stage(self.run,stage,[out])
        self.assertIsNone(recover_run(self.run))
        write(self.run/'source/config.json',{'voice':'Other'}); self.assertEqual(recover_run(self.run),'voice')
        write(self.run/'source/map.json',{'work_bbox':[1,2,30,40]}); self.assertEqual(recover_run(self.run),'layers'); self.assertEqual((self.run/'voice.txt').read_text(),'voice')
    def test_writing_and_asset_first_invalid_stage(self):
        import copy,shutil
        from unittest.mock import patch
        import solution_video.state as state
        from solution_video.writing import default_writing
        root=self.run/'tool';shutil.copytree(S,root,ignore=shutil.ignore_patterns('__pycache__'))
        c=default_writing();write(self.run/'source/writing.json',c)
        def finish():
            for stage in STAGES[:6]:
                out=self.run/(stage+'.txt');out.write_text(stage);finish_stage(self.run,stage,[out])
        with patch.object(state,'S',root):
            finish();c['chars_per_second']=4;write(self.run/'source/writing.json',c);self.assertEqual(recover_run(self.run),'timing')
            finish();c['pencil_length_px']=150;write(self.run/'source/writing.json',c);self.assertEqual(recover_run(self.run),'composition')
            finish();p=root/'assets/pencil/pencil-yellow-v1.json';meta=json.loads(p.read_text());meta['tip_px'][0]+=1;write(p,meta);self.assertEqual(recover_run(self.run),'composition')
            (self.run/'source/writing.json').unlink();finish();meta['tip_px'][0]+=1;write(p,meta);self.assertEqual(recover_run(self.run),'render')
    def test_teaching_visual_timing_add_delete(self):
        from test_annotations import teaching_fixture
        f,a,m,l=teaching_fixture();write(self.run/'source/manifest.json',m);write(self.run/'layers/layers.json',l)
        def finish():
            for stage in STAGES[:6]:
                out=self.run/(stage+'.txt');out.write_text(stage);finish_stage(self.run,stage,[out])
        finish();write(self.run/'source/focus.json',f);write(self.run/'source/annotations.json',a)
        self.assertEqual(recover_run(self.run),'timing')
        finish();a['items'][0]['color']='#FF0000';write(self.run/'source/annotations.json',a);self.assertEqual(recover_run(self.run),'composition')
        finish();a['items'][0]['offset_frames']=20;write(self.run/'source/annotations.json',a);self.assertEqual(recover_run(self.run),'timing')
        finish();(self.run/'source/annotations.json').unlink();(self.run/'source/focus.json').unlink();self.assertEqual(recover_run(self.run),'timing')
    def test_spatial_units_script_and_camera_invalidate_correct_stages(self):
        import shutil
        from unittest.mock import patch
        import solution_video.state as state
        root=self.run/'tool';shutil.copytree(S,root,ignore=shutil.ignore_patterns('__pycache__'))
        from solution_video.util import read,file_hash
        from solution_video.writing import default_writing
        write(self.run/'source/writing.json',default_writing());write(self.run/'source/map.json',dict(steps=[dict(writing_units=[])]))
        voice=make_audio('w',2400,self.run);before=file_hash(self.run/voice['path'])
        def finish():
            for stage in STAGES[:6]:
                out=self.run/(stage+'.txt');out.write_text(stage);finish_stage(self.run,stage,[out])
        with patch.object(state,'S',root):
            finish();mp=read(self.run/'source/map.json');mp['steps'][0]['writing_units']=[dict(id='changed')];write(self.run/'source/map.json',mp)
            self.assertEqual(recover_run(self.run),'layers')
            finish();write(self.run/'source/manifest.json',dict(segments=[dict(text='new explanation')]))
            self.assertEqual(recover_run(self.run),'script')
            finish();p=root/'scripts/solution_video/writing_camera.py';p.write_text(p.read_text()+'\n# camera edit\n')
            self.assertEqual(recover_run(self.run),'composition');self.assertEqual(file_hash(self.run/voice['path']),before)

    def test_shape_timing_invalidates_only_timing(self):
        import shutil
        from unittest.mock import patch
        import solution_video.state as state
        root=self.run/'tool';shutil.copytree(S,root,ignore=shutil.ignore_patterns('__pycache__'))
        a=make_audio('w',2400,self.run);before=(self.run/a['path']).read_bytes()
        with patch.object(state,'S',root):
            for stage in STAGES[:5]:
                out=self.run/(stage+'.txt');out.write_text(stage);finish_stage(self.run,stage,[out])
            p=root/'scripts/solution_video/shape_timing.py';p.write_text(p.read_text()+'\n# fingerprint change\n')
            self.assertEqual(recover_run(self.run),'timing')
            self.assertEqual((self.run/a['path']).read_bytes(),before)

    def test_chunk_and_style_invalidation(self):
        from test_annotations import teaching_fixture
        from solution_video.state import stage_fingerprint
        from solution_video.util import file_hash
        f,a,m,l=teaching_fixture();m['caption_timing']='pcm-chunks-v1';m['segments'][1]['chunks']=[dict(id='c1'),dict(id='c2')];a['items'][0].update(chunk_id='c1',offset_frames=0)
        write(self.run/'source/manifest.json',m);write(self.run/'layers/layers.json',l);write(self.run/'source/focus.json',f);write(self.run/'source/annotations.json',a)
        wav=make_audio('r',2400,self.run);sha=file_hash(self.run/wav['path']);voice=stage_fingerprint(self.run,'voice')
        def finish():
            for stage in STAGES[:6]:
                out=self.run/(stage+'.txt');out.write_text(stage);finish_stage(self.run,stage,[out])
        finish();a['items'][0]['chunk_id']='c2';write(self.run/'source/annotations.json',a);self.assertEqual(recover_run(self.run),'timing')
        finish();a['items'][0].update(stroke_width_px=8,color='#C45100');write(self.run/'source/annotations.json',a);self.assertEqual(recover_run(self.run),'composition')
        self.assertEqual(stage_fingerprint(self.run,'voice'),voice);self.assertEqual(file_hash(self.run/wav['path']),sha)

    def _finish_render_fixture(self):
        from solution_video.util import file_hash
        pub=self.run/'published.mp4';pub.write_bytes(b'published')
        write(self.run/'verification/publication.json',dict(published={str(pub):file_hash(pub)}))
        for stage in STAGES:
            out=self.run/(stage+'.txt');out.write_text(stage);finish_stage(self.run,stage,[out])
    def test_render_options_change_preserves_voice_and_timeline(self):
        from solution_video.state import stage_fingerprint
        from solution_video.util import file_hash
        from test_render_options import OPTIONS
        wav=make_audio('w',2400,self.run)
        write(self.run/'source/config.json',dict(voice='Aoede'))
        write(self.run/'source/timeline.json',dict(total_frames=30))
        path=self.run/'source/render-options.json';write(path,dict(OPTIONS,workers=2))
        self._finish_render_fixture()
        snapshots={s:stage_fingerprint(self.run,s) for s in STAGES[:6]}
        hashes={p:file_hash(self.run/p) for p in [wav['path'],'source/config.json','source/timeline.json']}
        for change in ['update','delete','add']:
            with self.subTest(change=change):
                if change=='delete':path.unlink()
                else:write(path,OPTIONS)
                self.assertEqual(recover_run(self.run),'render')
                self.assertEqual(snapshots,{s:stage_fingerprint(self.run,s) for s in STAGES[:6]})
                self.assertEqual(hashes,{p:file_hash(self.run/p) for p in hashes})
                self._finish_render_fixture()
    def test_missing_options_recovery_is_read_only(self):
        self._finish_render_fixture();self.assertIsNone(recover_run(self.run))
        self.assertFalse((self.run/'source/render-options.json').exists())

    def test_render_port_preserves_pre_port_input_fingerprint(self):
        import subprocess,shutil
        from unittest.mock import patch
        import solution_video.state as state
        old=subprocess.check_output(['git','show','642a17b:.agents/skills/ml-solution-video/scripts/solution_video/bundle_cli.py'],cwd=REPO)
        tool=self.run/'tool';shutil.copytree(S,tool,ignore=shutil.ignore_patterns('__pycache__'))
        module=tool/'scripts/solution_video/bundle_cli.py';new=module.read_bytes();module.write_bytes(old)
        with patch.object(state,'S',tool):
            before={stage:state.stage_fingerprint(self.run,stage) for stage in state.STAGES[:6]}
            module.write_bytes(new)
            self.assertEqual(before,{stage:state.stage_fingerprint(self.run,stage) for stage in state.STAGES[:6]})
            module.write_bytes(new+b'\n# unrelated input logic change\n')
            self.assertNotEqual(before['inputs'],state.stage_fingerprint(self.run,'inputs'))
