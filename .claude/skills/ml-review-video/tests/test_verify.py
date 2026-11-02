import tempfile,unittest
from pathlib import Path
from _util import minimal_manifest
from lib.verify import verify_run,publish_latest

class VerifyTest(unittest.TestCase):
    def test_wrapper_pass_cannot_replace_source_check(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)/'0915'/'run-1'; run.mkdir(parents=True)
            reports={k:{'status':'passed','evidence':[],'errors':[]} for k in ('content','audio','visual','media','sync')}
            reports['source']={'status':'unverified','evidence':['wrapper passed'],'errors':[]}
            result=verify_run(run,minimal_manifest(),reports)
            self.assertFalse(result['complete'])
            with self.assertRaises(ValueError): publish_latest(run,result)
            self.assertFalse((run.parent/'latest.json').exists())
    def test_failed_run_preserves_latest(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)/'r'; run.mkdir(); latest=run.parent/'latest.json'
            latest.write_text('previous')
            with self.assertRaises(ValueError): publish_latest(run,{'complete':False})
            self.assertEqual(latest.read_text(),'previous')
    def test_forged_complete_cannot_publish(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): publish_latest(Path(d),{'complete':True})
    def test_source_timeout_is_unverified(self):
        from unittest.mock import patch
        import subprocess
        from lib.cache import atomic_json
        from lib.verify import check_sources
        with tempfile.TemporaryDirectory() as d:
            run=Path(d); (run/'assets').mkdir(); (run/'source/compositions').mkdir(parents=True)
            (run/'index.html').write_text('<html></html>')
            atomic_json(run/'source/parts.json',{'parts':[]})
            with patch('lib.verify.command',side_effect=subprocess.TimeoutExpired('node',1)):
                result=check_sources(run,'entry',1)
            self.assertEqual(result['status'],'unverified')
    def test_sync_rejects_different_audio_same_duration(self):
        import subprocess,wave,math,struct
        from _util import pcm
        from lib.render import mux
        from lib.verify import verify_sync
        with tempfile.TemporaryDirectory() as d:
            run=Path(d); video=run/'v.mp4'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=black:s=1920x1080:r=30',
              '-frames:v','30','-c:v','libx264','-preset','ultrafast',str(video)],check=True)
            path=pcm(run/'voice.wav')
            t={'rate':24000,'total_samples':24000,'total_frames':30,'segments':[{'id':'s','start_sample':0,'end_sample':24000}]}
            audio=[{'id':'s','path':'voice.wav','samples':24000}]
            mux([video],audio,t,run/'review.mp4')
            self.assertEqual(verify_sync(run,audio,t)['status'],'passed')
            with wave.open(str(path),'wb') as f:
                f.setparams((1,2,24000,0,'NONE','not compressed'))
                f.writeframes(b''.join(struct.pack('<h',int(3000*math.sin(i*.17))) for i in range(24000)))
            self.assertEqual(verify_sync(run,audio,t)['status'],'failed')
