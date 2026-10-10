from fixtures import *
from solution_video.subtitles import write_srt,burn_subtitles
from solution_video.util import checked
class MediaTests(Sandbox):
    def test_white_pdf_renders_and_captions_stay_outside(self):
        self.check_caption_strip('원본 풀이를 확인합니다.')
    def test_two_line_caption_strip(self):
        self.check_caption_strip('따라서 Q₁은 이미터가 접지된 공통 이미터 증폭기로 볼 수 있습니다.',True)
    def check_caption_strip(self,text,two_lines=False):
        timeline=dict(rate=24000,segments=[dict(text=text,start_sample=0,end_sample=24000,voice_samples=24000)])
        srt=write_srt(timeline,self.run/'caption.srt'); self.assertIn(text.split()[0],srt.read_text())
        if two_lines:self.assertEqual(len(srt.read_text().strip().splitlines()[2:]),2)
        master=self.run/'master.mp4'
        checked(['ffmpeg','-y','-v','error','-f','lavfi','-i','color=white:s=1920x1080:r=30','-t','1','-c:v','libx264','-pix_fmt','yuv420p',master])
        font=S/'assets/fonts/Pretendard-Bold.ttf'
        final=burn_subtitles(master,srt,self.run/'최종.mp4',font)
        raw=checked(['ffmpeg','-v','error','-i',final,'-frames:v','1','-f','image2',self.run/'frame.png'])
        from PIL import Image,ImageChops
        image=Image.open(self.run/'frame.png').convert('RGB'); bbox=ImageChops.difference(image,Image.new('RGB',image.size,'white')).getbbox()
        self.assertIsNotNone(bbox); self.assertGreaterEqual(bbox[1],900)
    def test_two_line_background_is_one_uniform_rectangle(self):
        # Unequal lines must share one box; stacked per-line boxes create steps and overlaps.
        from PIL import Image
        from solution_video.media import ffmpeg
        master=self.run/'white.mp4'
        checked([ffmpeg(),'-y','-v','error','-f','lavfi','-i','color=white:s=1920x1080:r=30','-t','0.1','-c:v','libx264','-pix_fmt','yuv420p',master])
        srt=self.run/'two.srt';srt.write_text('1\n00:00:00,000 --> 00:00:00,100\nQ₁과 Q₃의 출력 저항까지 같은\n두 노드에 연결되므로 병렬입니다.\n')
        final=burn_subtitles(master,srt,self.run/'two.mp4',S/'assets/fonts/Pretendard-Bold.ttf')
        png=self.run/'two.png';checked([ffmpeg(),'-v','error','-i',final,'-frames:v','1',png])
        mask=Image.open(png).convert('L').crop((0,900,1920,1080)).point(lambda p:255 if p<200 else 0)
        box=mask.getbbox();self.assertIsNotNone(box)
        bounds=[mask.crop((0,y,1920,y+1)).getbbox() for y in range(box[1]+5,box[3]-5)]
        self.assertTrue(all(bounds),'one shared background has no horizontal gap')
        self.assertLessEqual(max(b[0] for b in bounds)-min(b[0] for b in bounds),4,'left box edge must be straight')
        self.assertLessEqual(max(b[2] for b in bounds)-min(b[2] for b in bounds),4,'right box edge must be straight')
        # Background beside the shorter line must not double-darken where line boxes overlap.
        gray=Image.open(png).convert('L');x=box[0]+8
        shades=[gray.getpixel((x,y+900)) for y in range(box[1]+5,box[3]-5)]
        self.assertLessEqual(max(shades)-min(shades),5,'background opacity is uniform between lines')
    def test_padded_segments_place_pcm_at_shifted_start(self):
        from solution_video.media import render_master
        from solution_video.util import file_hash
        from unittest.mock import patch
        from test_annotations import teaching_fixture,make_teaching_plan
        from solution_video.teaching import build_teaching_timeline
        from solution_video.review_adapter import default_config
        _,_,m,l=teaching_fixture();audio=[]
        for index,seg in enumerate(m['segments']):
            a=make_audio(seg['id'],800,self.run)
            with wave.open(str(self.run/a['path']),'wb') as f:f.setparams((1,2,24000,0,'NONE',''));f.writeframes((index+1).to_bytes(2,'little')*800)
            a['sha256']=file_hash(self.run/a['path']);audio.append(a)
        t=build_teaching_timeline(m,l,audio,default_config(),None,make_teaching_plan())
        entry=self.run/'cli.js';entry.write_text('');html=self.run/'composition/index.html';html.parent.mkdir();html.write_text('')
        def command(args,**kwargs):
            Path(args[args.index('--output')+1]).write_bytes(b'video');return __import__('types').SimpleNamespace(returncode=0,stdout='',stderr='')
        def checked(args,**kwargs):(self.run/'renders/master.pending.mp4').write_bytes(b'video')
        with patch('solution_video.media.source_checks'),patch('solution_video.media.command',side_effect=command),patch('solution_video.media.probe',return_value={'streams':[{'codec_type':'video','width':1920,'height':1080,'r_frame_rate':'30/1','nb_frames':t['total_frames']},{'codec_type':'audio','sample_rate':24000,'channels':1}]}),patch('solution_video.media.checked',side_effect=checked),patch('solution_video.media.ffmpeg',return_value='ffmpeg'):
            render_master([dict(entry='composition/index.html',key='solution',first_frame=0,last_frame=t['total_frames'])],t,audio,self.run,entry)
        with wave.open(str(self.run/'renders/narration.wav'),'rb') as f:raw=f.readframes(f.getnframes())
        self.assertEqual(raw[800*2:1600*2],b'\x02\x00'*800)
        self.assertEqual(raw[1600*2:64800*2],b'\x00\x00'*(64800-1600))
        self.assertEqual(raw[64800*2:65600*2],b'\x03\x00'*800)

class RenderOutputTests(Sandbox):
    def setUp(self):
        super().setUp()
        from test_render_options import OPTIONS
        from solution_video.util import write
        self.options=dict(OPTIONS);write(self.run/'source/render-options.json',self.options)
        self.entry=self.run/'cli.js';self.entry.write_text('')
        self.html=self.run/'composition/index.html';self.html.parent.mkdir();self.html.write_text('')
        self.parts=[dict(key='solution',entry='composition/index.html',first_frame=0,last_frame=30)]
        self.timeline=dict(total_frames=30,total_samples=24000,segments=[])
        self.work=self.run/'renders';self.work.mkdir()
        self.master=self.work/'master.mp4';self.master.write_bytes(b'old master')
        self.part=self.work/'solution.mp4';self.part.write_bytes(b'old part')
        self.receipt=self.run/'verification/render-receipt.json';write(self.receipt,dict(old=True))
        self.old_receipt=self.receipt.read_bytes();self.calls=[]
    def metadata(self,master=False):
        streams=[dict(codec_type='video',width=1920,height=1080,r_frame_rate='30/1',nb_frames=30)]
        if master:streams.append(dict(codec_type='audio',sample_rate='24000',channels=1))
        return dict(streams=streams)
    def command(self,args,**kwargs):
        from types import SimpleNamespace
        self.calls.append([str(a) for a in args])
        Path(args[args.index('--output')+1]).write_bytes(b'new part')
        return SimpleNamespace(returncode=0,stdout='rendered',stderr='')
    def checked(self,args,**kwargs):
        Path(args[-1]).write_bytes(b'new master')
    def invoke(self,command=None,probe=None):
        from unittest.mock import patch
        from solution_video.media import render_master
        with patch('solution_video.media.source_checks'),patch('solution_video.media.ffmpeg',return_value='ffmpeg'),patch('solution_video.media.command',side_effect=command or self.command),patch('solution_video.media.checked',side_effect=self.checked),patch('solution_video.media.probe',side_effect=probe or (lambda p:self.metadata('master' in p.name))):
            return render_master(self.parts,self.timeline,[],self.run,self.entry)
    def assert_preserved(self,part=True):
        if part:self.assertEqual(self.part.read_bytes(),b'old part')
        self.assertEqual(self.master.read_bytes(),b'old master');self.assertEqual(self.receipt.read_bytes(),self.old_receipt)
        self.assertFalse(list(self.work.glob('*.pending.mp4')))
        self.assertFalse(list(self.receipt.parent.glob('*.pending*')))
    def test_render_failure_preserves_previous_outputs(self):
        import subprocess
        from types import SimpleNamespace
        from solution_video.contracts import InputError
        for failure in ['nonzero','timeout']:
            def fail(args,**kwargs):
                self.command(args,**kwargs)
                if failure=='timeout':raise subprocess.TimeoutExpired(args,2,output=b'partial stdout',stderr=b'partial stderr')
                return SimpleNamespace(returncode=1,stdout='partial stdout',stderr='partial stderr')
            with self.subTest(failure=failure),self.assertRaises((InputError,subprocess.TimeoutExpired)):self.invoke(command=fail)
            self.assert_preserved();log=(self.work/'solution.log').read_text()
            self.assertIn('partial stdout',log);self.assertIn('partial stderr',log)
    def test_wrong_dimensions_or_fps_or_frames_cannot_replace_part(self):
        from solution_video.contracts import InputError
        cases=[dict(width=1280),dict(height=720),dict(r_frame_rate='24/1'),dict(nb_frames=29),dict(nb_frames='N/A'),dict(r_frame_rate='0/0')]
        for fields in cases:
            metadata=self.metadata();metadata['streams'][0].update(fields)
            with self.subTest(fields=fields),self.assertRaises(InputError):self.invoke(probe=lambda p:metadata)
            self.assert_preserved()
        with self.assertRaises(InputError):self.invoke(probe=lambda p:dict(streams=[]))
        self.assert_preserved()
    def test_later_part_failure_preserves_master_and_completed_part(self):
        from solution_video.contracts import InputError
        from types import SimpleNamespace
        self.parts.append(dict(self.parts[0],key='second',first_frame=30,last_frame=60))
        second=self.work/'second.mp4';second.write_bytes(b'old second')
        def fail_second(args,**kwargs):
            result=self.command(args,**kwargs)
            return SimpleNamespace(returncode=1,stdout='bad second',stderr='') if 'second.pending.mp4' in str(args[-1]) else result
        with self.assertRaises(InputError):self.invoke(command=fail_second)
        self.assert_preserved(part=False);self.assertEqual(self.part.read_bytes(),b'new part');self.assertEqual(second.read_bytes(),b'old second')
        self.assertEqual(len(self.calls),2)
    def test_invalid_master_cannot_replace_previous_master(self):
        from solution_video.contracts import InputError
        for fields in [dict(sample_rate='48000'),dict(channels=2)]:
            def probe(p):
                result=self.metadata('master' in p.name)
                if 'master' in p.name:result['streams'][1].update(fields)
                return result
            with self.subTest(fields=fields),self.assertRaises(InputError):self.invoke(probe=probe)
            self.assert_preserved(part=False)
    def test_receipt_write_or_replace_failure_rolls_back_master(self):
        import os
        from unittest.mock import patch
        from solution_video.media import _commit_master_and_receipt
        for failure in ['write','second_replace']:
            pending=self.work/'master.pending.mp4';pending.write_bytes(b'new master')
            real_replace=os.replace
            def replace(src,dest):
                if Path(src).name=='render-receipt.json.pending' and Path(dest).resolve()==self.receipt.resolve():raise OSError('receipt replace')
                return real_replace(src,dest)
            target=patch('solution_video.media.write',side_effect=OSError('receipt write')) if failure=='write' else patch('solution_video.media.os.replace',side_effect=replace)
            with self.subTest(failure=failure),target,self.assertRaises(OSError):
                _commit_master_and_receipt(pending,dict(new=True),self.master,self.receipt)
            self.assert_preserved()
    def test_saved_render_options_drive_execution_and_receipt(self):
        from solution_video.util import read,file_hash
        result=self.invoke();self.assertEqual(result,self.master.resolve())
        receipt=read(self.receipt);self.assertEqual(receipt['options'],self.options)
        args=self.calls[0];self.assertEqual(args[args.index('--workers')+1],'6');self.assertEqual(args[args.index('--quality')+1],'delivery')
        self.assertIn('--experimental-fast-capture=false',args);self.assertNotIn('--gpu',args)
        self.assertEqual(receipt['parts'][0]['command'],args);self.assertEqual(receipt['parts'][0]['frames'],30)
        self.assertEqual(receipt['parts'][0]['output_sha256'],file_hash(self.part));self.assertEqual(receipt['master_sha256'],file_hash(self.master))
        self.assertGreaterEqual(receipt['parts'][0]['elapsed_seconds'],0);self.assertFalse(list(self.work.glob('*.pending.mp4')))
    def test_invalid_options_are_rejected_before_source_checks(self):
        from unittest.mock import patch
        from solution_video.media import render_master
        from solution_video.contracts import InputError
        with patch('solution_video.media.source_checks',side_effect=AssertionError('renderer launched')):
            with self.assertRaises(InputError):render_master(self.parts,self.timeline,[],self.run,self.entry,render_options=dict(self.options,workers=True))
    def test_stale_pending_is_not_accepted_as_new_render(self):
        from types import SimpleNamespace
        from solution_video.contracts import InputError
        (self.work/'solution.pending.mp4').write_bytes(b'stale video')
        with self.assertRaises(InputError):self.invoke(command=lambda *a,**kw:SimpleNamespace(returncode=0,stdout='',stderr=''))
        self.assert_preserved()
    def test_failed_rollback_keeps_recovery_copies(self):
        import os
        from unittest.mock import patch
        from solution_video.media import _commit_master_and_receipt
        pending=self.work/'master.pending.mp4';pending.write_bytes(b'new master');real_replace=os.replace
        def fail(src,dest):
            if Path(src).name in ['render-receipt.json.pending','master.mp4.rollback']:raise OSError('injected commit/restore failure')
            return real_replace(src,dest)
        with patch('solution_video.media.os.replace',side_effect=fail),self.assertRaises(Exception) as caught:
            _commit_master_and_receipt(pending,dict(new=True),self.master,self.receipt)
        backup=self.master.with_name('master.mp4.rollback')
        self.assertTrue(backup.is_file(),'old master recovery copy must survive rollback failure')
        self.assertEqual(backup.read_bytes(),b'old master')
        self.assertIn(str(backup),str(caught.exception));self.assertEqual(self.receipt.read_bytes(),self.old_receipt)
        self.assertFalse(pending.exists())
    def test_interrupt_between_pair_replacements_restores_previous_pair(self):
        import os
        from unittest.mock import patch
        from solution_video.media import _commit_master_and_receipt
        pending=self.work/'master.pending.mp4';pending.write_bytes(b'new master');real_replace=os.replace
        def interrupt(src,dest):
            if Path(src).name=='render-receipt.json.pending':raise KeyboardInterrupt()
            return real_replace(src,dest)
        with patch('solution_video.media.os.replace',side_effect=interrupt),self.assertRaises(KeyboardInterrupt):
            _commit_master_and_receipt(pending,dict(new=True),self.master,self.receipt)
        self.assert_preserved();self.assertFalse(list(self.work.glob('*.rollback')))
    def test_retry_cannot_overwrite_unrestored_recovery_copy(self):
        from solution_video.media import _commit_master_and_receipt
        from solution_video.contracts import InputError
        backup=self.master.with_name('master.mp4.rollback');backup.write_bytes(b'only old master')
        pending=self.work/'master.pending.mp4';pending.write_bytes(b'new master')
        with self.assertRaisesRegex(InputError,'recovery'):
            _commit_master_and_receipt(pending,dict(new=True),self.master,self.receipt)
        self.assertEqual(backup.read_bytes(),b'only old master');self.assert_preserved()
