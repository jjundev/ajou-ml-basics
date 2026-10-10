from fixtures import *
from solution_video.review_adapter import generate_voice,default_config
from solution_video.subtitles import write_srt
from solution_video.reveal import build_timeline
from solution_video.speech_chunks import MODE
from solution_video.speech_chunks import verify_chunk_sync,chunk_review_passed
from solution_video.contracts import InputError
from solution_video.util import read,write
from test_speech_tts import response
from test_manifest import example
import copy

class ChunkTimingTests(Sandbox):
    def make_run(self):
        m,l,_,_=example();m['caption_timing']=MODE
        for s in m['segments']:
            s['caption_text']=s['text'];s['chunks']=[dict(id='one',text=s['text'],caption_text=s['text'])]
        cfg=default_config();audio=generate_voice(m['segments'],self.run,cfg,self.run/'ledger.json',lambda p:response())
        t=build_timeline(m,l,audio,cfg)
        for name,data in [('source/manifest.json',m),('layers/layers.json',l),('source/timeline.json',t)]:write(self.run/name,data)
        write_srt(t,self.run/'renders/captions.srt')
        return m,t
    def test_modified_srt_or_chunk_pcm_fails_sync(self):
        m,t=self.make_run();self.assertEqual(verify_chunk_sync(self.run)['status'],'passed')
        p=self.run/'renders/captions.srt';p.write_text(p.read_text().replace('00:00:00,100','00:00:00,110',1))
        self.assertNotEqual(verify_chunk_sync(self.run)['status'],'passed')
        write_srt(t,p)
        a=read(self.run/'source/chunk-audio.json')['voices'][0];(self.run/a['path']).write_bytes(b'bad')
        self.assertNotEqual(verify_chunk_sync(self.run)['status'],'passed')
    def test_no_listening_or_incomplete_chunk_review_blocks_complete(self):
        m,_=self.make_run()
        rows=[dict(segment_id=s['id'],chunk_id='one',transcript_match=True,no_instruction_speech=True,natural_join=True,sync_passed=True,notes='reviewed') for s in m['segments']]
        good=dict(mode='live-listened',chunk_checks=rows)
        self.assertTrue(chunk_review_passed(good,m))
        self.assertFalse(chunk_review_passed(dict(good,mode='not-listened'),m))
        self.assertFalse(chunk_review_passed(dict(good,chunk_checks=rows[:-1]),m))
        self.assertFalse(chunk_review_passed(dict(good,chunk_checks=rows+[rows[0]]),m))
        for flag in ['transcript_match','no_instruction_speech','natural_join','sync_passed']:
            bad=copy.deepcopy(good);bad['chunk_checks'][0][flag]=False
            self.assertFalse(chunk_review_passed(bad,m))
    def test_synthetic_sync_does_not_approve_live_audio(self):
        m,_=self.make_run();self.assertEqual(verify_chunk_sync(self.run)['status'],'passed')
        self.assertFalse(chunk_review_passed(dict(mode='not-listened',chunk_checks=[]),m))
    def timeline(self):
        chunks=[dict(id='a',text='전류를 봅니다.',caption_text='I₀입니다.'),dict(id='b',text='변화를 봅니다.',caption_text='(I₀ + ΔI)/2입니다.')]
        seg=dict(id='write',text='전류를 봅니다. 변화를 봅니다.',caption_text='I₀입니다. (I₀ + ΔI)/2입니다.',chunks=chunks,start_sample=24000,end_sample=48000,voice_samples=9600)
        return dict(rate=24000,caption_timing=MODE,segments=[seg],caption_cues=[dict(segment_id='write',chunk_id='a',caption_text='I₀입니다.',start_sample=24000,end_sample=26400),dict(segment_id='write',chunk_id='b',caption_text='(I₀ + ΔI)/2입니다.',start_sample=26400,end_sample=33600)])
    def test_srt_uses_pcm_not_character_weights(self):
        t=self.timeline();dest=self.run/'a.srt';write_srt(t,dest);s=dest.read_text()
        self.assertIn('00:00:01,000 --> 00:00:01,100',s)
        self.assertIn('00:00:01,100 --> 00:00:01,400',s)
        t['caption_cues'][0]['caption_text']='변화 전 거울 전류는 I₀입니다.'
        t['segments'][0]['chunks'][0]['caption_text']=t['caption_cues'][0]['caption_text'];write_srt(t,dest)
        self.assertIn('00:00:01,000 --> 00:00:01,100',dest.read_text())
    def test_missing_or_reordered_chunk_boundaries_fail(self):
        for mutate in ['missing','order','offset']:
            t=self.timeline()
            if mutate=='missing':t['caption_cues'].pop()
            elif mutate=='order':t['caption_cues'].reverse()
            else:t['caption_cues'][1]['start_sample']=26000
            with self.subTest(mutate=mutate),self.assertRaises(InputError):write_srt(t,self.run/'bad.srt')
    def test_fake_transport_to_joined_timeline_and_hold(self):
        m,l,_,_=example();m['caption_timing']=MODE
        for s in m['segments']:
            s['caption_text']=s['text'];s['chunks']=[dict(id='one',text=s['text'],caption_text=s['text'])]
        s=m['segments'][1];s['text']='전류를 봅니다. 변화를 봅니다.';s['caption_text']='I₀입니다. ΔI입니다.'
        s['chunks']=[dict(id='one',text='전류를 봅니다.',caption_text='I₀입니다.'),dict(id='two',text='변화를 봅니다.',caption_text='ΔI입니다.')]
        cfg=default_config();cfg.update(max_attempts=1,tts_concurrency=1)
        def transport(p):return response(7200 if p['contents'][0]['parts'][0]['text']=='변화를 봅니다.' else 2400)
        audio=generate_voice(m['segments'],self.run,cfg,self.run/'ledger.json',transport)
        t=build_timeline(m,l,audio,cfg)
        self.assertEqual([(c['start_sample'],c['end_sample']) for c in t['caption_cues'][:3]],[(0,2400),(2400,4800),(4800,12000)])
        write_srt(t,self.run/'captions.srt');text=(self.run/'captions.srt').read_text()
        self.assertIn('00:00:00,200 --> 00:00:00,500',text)
        self.assertGreater(t['segments'][1]['end_sample'],12000)
        self.assertEqual(t['caption_cues'][2]['end_sample'],12000)
        self.assertEqual(len(read(self.run/'ledger.json')['requests']),4)
