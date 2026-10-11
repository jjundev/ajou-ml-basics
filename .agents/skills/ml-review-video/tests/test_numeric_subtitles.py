import json,tempfile,unittest
from pathlib import Path
from _util import minimal_manifest
from lib.timing import build_timeline,write_subtitles
from lib.manifest import require_ready
from lib.subtitles import split_srt
from lib.vertex_tts import synthesize
from lib.budget import Budget
from test_tts import config,response

class NumericSubtitleTest(unittest.TestCase):
    def test_full_display_text_not_summary_and_legacy_fallback(self):
        m=minimal_manifest();s=m['segments'][0]
        s['text']='마이너스 영 점 오, 삼분의 일, 십이 점 오 퍼센트, 이 밀리초입니다. 일과 이 단어는 그대로입니다.'
        display='-0.5, 1/3, 12.5%, 2 ms입니다. 일과 이 단어는 그대로입니다.'
        s['subtitle_text']=display
        audio=[dict(id=s['id'],rate=24000,samples=240000)]
        with tempfile.TemporaryDirectory() as d:
            t=build_timeline(m,audio);write_subtitles(t,d);p=Path(d)/'narration.srt'
            self.assertIn(display,p.read_text());self.assertNotIn(s['caption'],p.read_text())
            self.assertEqual(t['segments'][0]['text'],s['text'])
            del s['subtitle_text'];write_subtitles(build_timeline(m,audio),d)
            self.assertIn(s['text'],p.read_text())
    def test_bad_display_text_rejected_before_tts(self):
        for bad in ('', '  ', None, 0, '0.5\n\n2\n00:00:00,000 --> 00:00:02,000'):
            m=minimal_manifest();m['segments'][0]['subtitle_text']=bad
            with self.subTest(bad=bad),self.assertRaises(ValueError):require_ready(m)
    def test_tts_uses_spoken_text_and_reuses_pcm_after_display_edit(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);item=dict(id='seg-x',text='영 점 오입니다.',subtitle_text='0.5입니다.');calls=[]
            def transport(payload):calls.append(payload);return response()
            budget=Budget(run/'ledger.json');cfg=config();cfg.pop('price',None)
            first=synthesize([item],run,cfg,budget,transport)
            item['subtitle_text']='0.50입니다.'
            second=synthesize([item],run,cfg,budget,transport)
            self.assertEqual(len(calls),1);self.assertEqual(first,second)
            self.assertIn('영 점 오입니다.',calls[0]['contents'][0]['parts'][0]['text'])
            self.assertNotIn('0.5입니다.',calls[0]['contents'][0]['parts'][0]['text'])
    def test_wrap_preserves_numeric_unit_atoms_and_timing(self):
        for atom in ('-0.5 ms','1/3 V','12.5 %','1.2e-3 A','1,000 Hz','2–3 초','(-0.5 ms)','2 ms입니다.'):
            text='가'*19+' '+atom+' '+'나'*19
            with self.subTest(atom=atom),tempfile.TemporaryDirectory() as d:
                p=Path(d)/'n.srt';p.write_text('1\n00:00:00,000 --> 00:00:10,000\n'+text+'\n')
                out=split_srt(p)
                self.assertIn(atom,out);self.assertIn('00:00:00,000',out);self.assertIn('00:00:10,000',out)
                contents=' '.join(' '.join(b.splitlines()[2:]) for b in out.strip().split('\n\n'))
                self.assertEqual(contents,text)

    def test_ordinary_word_starting_with_unit_letter_is_not_a_unit(self):
        text='가'*19+' 2 machine '+'나'*19
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'n.srt';p.write_text('1\n00:00:00,000 --> 00:00:10,000\n'+text+'\n')
            self.assertIn('2\nmachine',split_srt(p))
