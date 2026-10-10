from fixtures import *
from solution_video.speech_tts import make_speech_payload,synthesize_speech,POLICY
from solution_video.review_adapter import default_config,_modules
import base64

def response(samples=2400):
    return {'candidates':[{'finishReason':'STOP','content':{'parts':[{'inlineData':{'mimeType':'audio/L16;rate=24000','data':base64.b64encode(b'\x01\x00'*samples).decode()}}]}}],
            'usageMetadata':dict(promptTokenCount=10,candidatesTokenCount=20)}

class SpeechTTSTests(Sandbox):
    def setUp(self):
        super().setUp();self.cfg=default_config();self.cfg.update(max_attempts=1,tts_concurrency=1)
        self.tts,bm=_modules();self.budget=bm.Budget(self.run/'ledger.json')
    def test_payload_contains_only_spoken_text(self):
        p=make_speech_payload('먼저 관계를 정리합니다.',self.cfg)
        self.assertEqual(p['contents'],[dict(role='user',parts=[dict(text='먼저 관계를 정리합니다.')])])
        self.assertNotIn(self.cfg['direction'],json.dumps(p,ensure_ascii=False))
        self.assertEqual(p['generationConfig']['responseModalities'],['AUDIO'])
        self.assertEqual(p['generationConfig']['speechConfig']['languageCode'],'ko-KR')
        self.assertEqual(p['generationConfig']['speechConfig']['voiceConfig']['prebuiltVoiceConfig']['voiceName'],'Aoede')
    def test_policy_invalidates_old_cache(self):
        old=self.tts.synthesize([dict(id='one',text='읽을 원고')],self.run,self.cfg,self.budget,lambda p:response())
        fresh=synthesize_speech([dict(id='one',text='읽을 원고')],self.run,self.cfg,self.budget,lambda p:response())
        self.assertNotEqual(old[0]['key'],fresh[0]['key'])
        self.assertEqual(fresh[0]['policy'],POLICY)
        self.assertEqual(len(json.loads((self.run/'ledger.json').read_text())['requests']),2)
    def test_caption_change_reuses_voice(self):
        calls=[]
        def transport(p):calls.append(p);return response()
        items=[dict(id='one',text='알 오 원',caption_text='r_O1')]
        a=synthesize_speech(items,self.run,self.cfg,self.budget,transport)
        items[0]['caption_text']='다른 r_O1';b=synthesize_speech(items,self.run,self.cfg,self.budget,transport)
        self.assertEqual(len(calls),1);self.assertEqual(a[0]['key'],b[0]['key'])
        self.assertEqual(calls[0]['contents'][0]['parts'][0]['text'],'알 오 원')
    def test_429_retry_and_partial_resume(self):
        self.cfg['max_attempts']=2;calls=[];fail=[True];throttle=[True];sleeps=[]
        def transport(p):
            text=p['contents'][0]['parts'][0]['text'];calls.append(text)
            if text=='첫 문장' and throttle[0]:throttle[0]=False;raise self.tts.VertexError(429)
            if text=='둘째 문장' and fail[0]:raise self.tts.VertexError(503)
            return response()
        items=[dict(id='one',text='첫 문장'),dict(id='two',text='둘째 문장')]
        with self.assertRaises(self.tts.VertexError):synthesize_speech(items,self.run,self.cfg,self.budget,transport,sleep=sleeps.append)
        fail[0]=False;out=synthesize_speech(items,self.run,self.cfg,self.budget,transport,sleep=sleeps.append)
        self.assertEqual(calls,['첫 문장','첫 문장','둘째 문장','둘째 문장','둘째 문장'])
        self.assertEqual([x['id'] for x in out],['one','two'])
        self.assertEqual(len(json.loads((self.run/'ledger.json').read_text())['requests']),5)
    def test_corrupt_cached_pcm_regenerates(self):
        items=[dict(id='one',text='첫 문장')];a=synthesize_speech(items,self.run,self.cfg,self.budget,lambda p:response())
        (self.run/a[0]['path']).write_bytes(b'corrupt')
        b=synthesize_speech(items,self.run,self.cfg,self.budget,lambda p:response())
        self.assertEqual(b[0]['samples'],2400)
        self.assertEqual(len(json.loads((self.run/'ledger.json').read_text())['requests']),2)
    def test_error_does_not_expose_secret(self):
        def transport(p):raise RuntimeError('private-token')
        with self.assertRaises(self.tts.VertexError) as caught:synthesize_speech([dict(id='one',text='원고')],self.run,self.cfg,self.budget,transport)
        self.assertNotIn('private-token',str(caught.exception))
    def test_malformed_receipt_regenerates(self):
        items=[dict(id='one',text='첫 문장')]
        for mutation in ['list','null','rate','bool_samples']:
            a=synthesize_speech(items,self.run,self.cfg,self.budget,lambda p:response())
            p=(self.run/a[0]['path']).with_suffix('.json');rec=json.loads(p.read_text())
            if mutation=='list':rec=[]
            elif mutation=='null':rec=None
            elif mutation=='rate':rec['rate']=1
            else:rec['samples']=True
            p.write_text(json.dumps(rec));before=len(json.loads((self.run/'ledger.json').read_text())['requests'])
            b=synthesize_speech(items,self.run,self.cfg,self.budget,lambda p:response())
            self.assertEqual(b[0]['rate'],24000)
            self.assertEqual(len(json.loads((self.run/'ledger.json').read_text())['requests']),before+1)
