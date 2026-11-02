import tempfile,unittest,base64,json
from pathlib import Path
from decimal import Decimal
from _util import ROOT
from lib.vertex_tts import synthesize,VertexError
from lib.budget import Budget

def config():
    return {'model':'gemini-2.5-flash-tts','voice':'Aoede','language':'ko-KR',
      'direction':'원고만 읽으세요.','pronunciation':{},'max_output_tokens':2048,
      'max_attempts':4,'tts_concurrency':1,
      'price':{'input_per_million':'1','output_per_million':'20','verified_at':'2026-09-29','source':'test-fixture'}}
def response():
    return {'candidates':[{'finishReason':'STOP','content':{'parts':[{'inlineData':{
      'mimeType':'audio/L16;rate=24000','data':base64.b64encode(b'\x10\x00'*24000).decode()}}]}}],
      'usageMetadata':{'promptTokenCount':10,'candidatesTokenCount':25}}

class TtsTest(unittest.TestCase):
    def test_retry_and_resume(self):
        calls=[]
        def fake(p):
            calls.append(p)
            if len(calls)==1: raise VertexError(429)
            return response()
        with tempfile.TemporaryDirectory() as d:
            run=Path(d); b=Budget(run/'ledger.json',Decimal('2'))
            items=[{'id':'seg-1','text':'ATP가 만들어집니다.'}]
            a=synthesize(items,run,config(),b,fake,lambda _:None)
            c=synthesize(items,run,config(),b,fake,lambda _:None)
            self.assertEqual(len(calls),2); self.assertEqual(a,c)
            self.assertEqual(a[0]['samples'],24000)
            changed=config(); changed['voice']='Charon'
            synthesize(items,run,changed,b,fake,lambda _:None)
            self.assertEqual(len(calls),3)
    def test_bad_mime_and_truncation_are_not_cached(self):
        for mode in ('mime','truncation'):
            with tempfile.TemporaryDirectory() as d:
                r=response()
                if mode=='mime': r['candidates'][0]['content']['parts'][0]['inlineData']['mimeType']='text/plain'
                else: r['candidates'][0]['finishReason']='MAX_TOKENS'
                with self.assertRaises(VertexError):
                    synthesize([{'id':'x','text':'말'}],Path(d),config(),Budget(Path(d)/'ledger.json',Decimal('2')),lambda _:r,lambda _:None)
                self.assertFalse(list(Path(d).rglob('*.wav')))
    def test_key_cannot_escape_error(self):
        with tempfile.TemporaryDirectory() as d:
            def bad(_): raise RuntimeError('SECRET_TEST_VALUE')
            with self.assertRaises(VertexError) as ex:
                synthesize([{'id':'x','text':'말'}],Path(d),config(),Budget(Path(d)/'ledger.json',Decimal('2')),bad,lambda _:None)
            self.assertNotIn('SECRET_TEST_VALUE',str(ex.exception))
            self.assertNotIn('SECRET_TEST_VALUE',(Path(d)/'ledger.json').read_text())

    def test_no_default_cap_or_price_requirement_and_usage_kept(self):
        cfg=config(); cfg.pop('price')
        with tempfile.TemporaryDirectory() as d:
            run=Path(d); budget=Budget(run/'ledger.json')
            result=synthesize([{'id':'x','text':'말'}],run,cfg,budget,lambda _:response(),lambda _:None)
            self.assertEqual(result[0]['usage']['promptTokenCount'],10)
            row=next(iter(json.loads((run/'ledger.json').read_text())['requests'].values()))
            self.assertIsNone(row['actual'])
            self.assertEqual(row['usage']['candidatesTokenCount'],25)
            self.assertIsNone(budget.remaining())

    def test_optional_limit_still_blocks_without_sufficient_budget(self):
        cfg=config(); cfg['price'].pop('verified_at'); cfg['price'].pop('source')
        with tempfile.TemporaryDirectory() as d:
            run=Path(d); calls=[]
            with self.assertRaises(VertexError):
                synthesize([{'id':'x','text':'말'}],run,cfg,Budget(run/'ledger.json',Decimal('0')),lambda p:calls.append(p),lambda _:None)
            self.assertEqual(calls,[])

    def test_explicit_limit_requires_rates_not_verification(self):
        cfg=config(); cfg['price'].pop('verified_at'); cfg['price'].pop('source')
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)
            result=synthesize([{'id':'x','text':'말'}],run,cfg,Budget(run/'ledger.json',Decimal('2')),lambda _:response(),lambda _:None)
            self.assertEqual(len(result),1)
