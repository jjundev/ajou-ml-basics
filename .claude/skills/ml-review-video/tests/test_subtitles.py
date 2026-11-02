import tempfile,unittest,subprocess,shutil
from pathlib import Path
from _util import SKILL
from lib.subtitles import split_srt,burn_subtitles,STYLE

SRT='1\n00:00:00,000 --> 00:00:10,000\n첫 문장입니다. 두 번째 문장은 조금 더 길어서 쉼표를 만나면, 여기서 한 번 끊어야 합니다. 마지막 문장.\n'

class SubtitleTest(unittest.TestCase):
    def test_split_keeps_span_and_short_lines(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'n.srt'; p.write_text(SRT,encoding='utf-8'); out=split_srt(p)
        cues=out.strip().split('\n\n'); self.assertGreater(len(cues),1)
        self.assertTrue(cues[0].split('\n')[1].startswith('00:00:00,000'))
        self.assertTrue(cues[-1].split('\n')[1].endswith('00:00:10,000'))
        for c in cues: self.assertTrue(all(len(l)<=40 for l in c.split('\n')[2:]))
    def test_style_is_fixed(self):
        for token in ('FontName=Pretendard','FontSize=14','Bold=1','Alignment=2','MarginV=22','BorderStyle=3','Outline=4','OutlineColour=&H4D0E0B0B','BackColour=&H4D0E0B0B'): self.assertIn(token,STYLE)
    @unittest.skipUnless(shutil.which('ffmpeg'),'FFmpeg required')
    def test_burn_korean_path_keeps_source(self):
        with tempfile.TemporaryDirectory(prefix='머러기 자막 ') as d:
            d=Path(d); src=d/'in.mp4'; (d/'n.srt').write_text(SRT,encoding='utf-8')
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=black:s=1920x1080:r=30','-f','lavfi','-i','anullsrc=r=24000:cl=mono',
              '-t','2','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(src)],check=True)
            out=burn_subtitles(src,d/'n.srt',d/'out 자막.mp4'); self.assertTrue(out.is_file())
            with self.assertRaises(ValueError): burn_subtitles(src,d/'n.srt',src)
            self.assertFalse((d/'out 자막.subwork').exists())
if __name__=='__main__': unittest.main()

class DarkGuardTest(unittest.TestCase):
    def _video(self,d,color):
        v=Path(d)/(color+'.mp4')
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',f'color=c={color}:s=320x180:r=30','-t','2','-c:v','libx264','-pix_fmt','yuv420p',str(v)],check=True)
        return v
    @unittest.skipUnless(shutil.which('ffmpeg'),'FFmpeg required')
    def test_light_video_is_rejected_everywhere(self):
        from lib.render import dark_failures
        with tempfile.TemporaryDirectory() as d:
            dark,light=self._video(d,'0x17171c'),self._video(d,'white')
            self.assertEqual(dark_failures(dark),[])
            self.assertTrue(dark_failures(light))
            (Path(d)/'n.srt').write_text(SRT,encoding='utf-8')
            with self.assertRaises(ValueError): burn_subtitles(light,Path(d)/'n.srt',Path(d)/'o.mp4')
    def test_entries_must_be_dark_scene_files(self):
        from lib.render import require_dark_entries
        with tempfile.TemporaryDirectory() as d:
            d=Path(d); (d/'scene-01.html').write_text('<!doctype html><html lang="ko" data-theme="dark"><head>',encoding='utf-8')
            (d/'scene-02.html').write_text('<!doctype html><html lang="ko"><head>',encoding='utf-8')
            require_dark_entries([{'entry':'scene-01.html'}],d)
            for entry in ('scene-02.html','index.html'):
                with self.assertRaises(ValueError): require_dark_entries([{'entry':entry}],d)

class SubtitleToolTests(unittest.TestCase):
    def test_selects_build_with_subtitle_filter(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        from lib.subtitles import _subtitle_ffmpeg
        with patch('lib.subtitles.subprocess.run',side_effect=[SimpleNamespace(returncode=0,stdout=' .a scale V->V',stderr=''),SimpleNamespace(returncode=0,stdout=' ... subtitles V->V Render subtitles',stderr='')]):
            self.assertEqual(_subtitle_ffmpeg(['minimal-ffmpeg','full-ffmpeg']),'full-ffmpeg')
    def test_no_capable_build_is_actionable(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        from lib.subtitles import _subtitle_ffmpeg
        with patch('lib.subtitles.subprocess.run',return_value=SimpleNamespace(returncode=0,stdout='',stderr='')):
            with self.assertRaisesRegex(RuntimeError,'libass'):_subtitle_ffmpeg(['minimal-ffmpeg'])

class FinalDarkMediaTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('ffmpeg'),'FFmpeg required')
    def test_mux_and_media_reject_light_output(self):
        from _util import pcm
        from lib.render import mux
        from lib.verify import verify_media
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);light=run/'light.mp4'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=white:s=1920x1080:r=30','-f','lavfi','-i','anullsrc=r=24000:cl=mono','-t','2','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(light)],check=True)
            self.assertIn('not-dark',verify_media(light,{'total_frames':60})['errors'])
            pcm(run/'voice.wav',48000)
            timeline={'total_samples':48000,'total_frames':60,'segments':[{'id':'s','start_sample':0,'end_sample':48000}]}
            with self.assertRaisesRegex(RuntimeError,'not dark'):
                mux([light],[{'id':'s','path':'voice.wav','samples':48000}],timeline,run/'output.mp4')
            self.assertFalse((run/'output.mp4').exists())
