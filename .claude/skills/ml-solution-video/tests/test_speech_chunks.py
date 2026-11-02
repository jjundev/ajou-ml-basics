from fixtures import *
from solution_video.speech_chunks import validate_speech_chunks,speech_items
from solution_video.contracts import InputError
from solution_video.subtitles import caption_notation_warnings
import copy
from solution_video.speech_chunks import join_segment_audio,validate_chunk_audio
from solution_video.util import write,read

def paired_segment():
    return dict(id='write_one',text='전류를 봅니다. 이로 나눕니다.',
                caption_text='I₀를 봅니다. (I₀ + ΔI)/2입니다.',chunks=[
                    dict(id='current',text='전류를 봅니다.',caption_text='I₀를 봅니다.'),
                    dict(id='half',text='이로 나눕니다.',caption_text='(I₀ + ΔI)/2입니다.')])

class ChunkContractTests(Sandbox):
    def test_requires_every_segment_in_chunk_mode(self):
        with self.assertRaises(InputError):validate_speech_chunks([paired_segment(),dict(id='intro',text='문제입니다.')],required=True)
    def test_legacy_unchanged(self):
        segments=[dict(id='intro',text='문제입니다.',caption_text='문제 1입니다.')]
        validate_speech_chunks(segments,required=False)
        self.assertEqual(speech_items(segments),[dict(id='intro',text='문제입니다.')])
    def test_valid_pair_and_safe_identity(self):
        seg=paired_segment();validate_speech_chunks([seg],required=True)
        items=speech_items([seg])
        self.assertEqual([i['id'] for i in items],['write_one__current','write_one__half'])
        self.assertEqual(items[1]['text'],'이로 나눕니다.')
        self.assertNotIn('caption_text',items[1])
    def test_comma_clause_is_one_chunk_without_added_period(self):
        seg=paired_segment();seg['chunks'][0].update(text='분자는 전류이고,',caption_text='분자는 I₀이고,')
        seg['text']=' '.join(c['text'] for c in seg['chunks']);seg['caption_text']=' '.join(c['caption_text'] for c in seg['chunks'])
        validate_speech_chunks([seg],required=True)
    def test_parent_reconstruction_and_atomic_caption(self):
        cases=[]
        for key in ['text','caption_text']:
            s=paired_segment();s[key]='다른 원고입니다.';cases.append(s)
        s=paired_segment();s['chunks'][1]['id']='current';cases.append(s)
        s=paired_segment();s['chunks'][0]['text']='';cases.append(s)
        s=paired_segment();s['chunks'][0]['caption_text']='첫 문장입니다. 둘째 문장입니다.';s['caption_text']=' '.join(c['caption_text'] for c in s['chunks']);cases.append(s)
        s=paired_segment();s['chunks'][0]['id']='../bad';cases.append(s)
        for seg in cases:
            with self.subTest(seg=seg),self.assertRaises(InputError):validate_speech_chunks([seg],required=True)
    def test_synthesized_identity_collision(self):
        a=dict(id='a__b',text='문장.',caption_text='문장.',chunks=[dict(id='c',text='문장.',caption_text='문장.')])
        b=dict(id='a',text='문장.',caption_text='문장.',chunks=[dict(id='b__c',text='문장.',caption_text='문장.')])
        with self.assertRaises(InputError):validate_speech_chunks([a,b],required=True)
    def test_caption_warnings_include_chunk_id(self):
        seg=paired_segment();seg['chunks'][0]['caption_text']='이 R_L을 봅니다.'
        seg['caption_text']=' '.join(c['caption_text'] for c in seg['chunks'])
        warnings=caption_notation_warnings([seg])
        self.assertEqual(len(warnings),1)
        self.assertEqual((warnings[0]['segment_id'],warnings[0]['chunk_id']),('write_one','current'))

class ChunkPCMTests(Sandbox):
    def make_chunks(self):
        seg=paired_segment()
        audio=[make_audio('write_one__current',2400,self.run),make_audio('write_one__half',7200,self.run)]
        write(self.run/'source/chunk-audio.json',dict(voices=audio))
        return [seg],audio
    def test_join_measured_pcm(self):
        segs,audio=self.make_chunks();voices=join_segment_audio(segs,audio,self.run)
        self.assertEqual(voices[0]['samples'],9600)
        self.assertEqual([(c['start_sample'],c['end_sample']) for c in voices[0]['chunks']],[(0,2400),(2400,9600)])
        with wave.open(str(self.run/voices[0]['path'])) as w:self.assertEqual(w.readframes(9600),b'\0\0'*9600)
        validate_chunk_audio(segs,voices,self.run)
    def test_no_automatic_trim_of_quiet_speech(self):
        segs,audio=self.make_chunks();p=self.run/audio[0]['path']
        with wave.open(str(p),'wb') as w:w.setparams((1,2,24000,0,'NONE',''));w.writeframes(b'\x01\x00'*2400)
        audio[0]['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        voices=join_segment_audio(segs,audio,self.run)
        self.assertEqual(voices[0]['chunks'][0]['trim_start_sample'],0)
        self.assertEqual(voices[0]['samples'],9600)
    def test_explicit_trim_preserves_raw(self):
        segs,audio=self.make_chunks();raw_hash=audio[0]['sha256']
        trims=dict(schema_version=1,rows=[dict(segment_id='write_one',chunk_id='current',raw_sha256=raw_hash,start_sample=100,end_sample=2300,reason='reviewed silence')])
        voices=join_segment_audio(segs,audio,self.run,trims)
        self.assertEqual(voices[0]['samples'],9400)
        self.assertEqual(voices[0]['chunks'][0]['end_sample'],2200)
        self.assertEqual(hashlib.sha256((self.run/audio[0]['path']).read_bytes()).hexdigest(),raw_hash)
        write(self.run/'source/chunk-trims.json',trims);validate_chunk_audio(segs,voices,self.run)
    def test_reject_bad_trim_and_provenance(self):
        segs,audio=self.make_chunks()
        base=dict(segment_id='write_one',chunk_id='current',raw_sha256=audio[0]['sha256'],start_sample=100,end_sample=2300,reason='reviewed')
        cases=[dict(base,start_sample=-1),dict(base,end_sample=2401),dict(base,start_sample=True),dict(base,raw_sha256='stale'),dict(base,chunk_id='unknown')]
        for row in cases:
            with self.subTest(row=row),self.assertRaises(InputError):join_segment_audio(segs,audio,self.run,dict(schema_version=1,rows=[row]))
        with self.assertRaises(InputError):join_segment_audio(segs,audio,self.run,dict(schema_version=1,rows=[base,base]))
        (self.run/audio[0]['path']).write_bytes(b'corrupt')
        with self.assertRaises(InputError):join_segment_audio(segs,audio,self.run)
    def test_tampered_join_and_offsets_rejected(self):
        segs,audio=self.make_chunks();voices=join_segment_audio(segs,audio,self.run)
        bad=copy.deepcopy(voices);bad[0]['chunks'][0]['end_sample']=2000
        with self.assertRaises(InputError):validate_chunk_audio(segs,bad,self.run)
        p=self.run/voices[0]['path'];p.write_bytes(b'corrupt')
        with self.assertRaises(InputError):validate_chunk_audio(segs,voices,self.run)
