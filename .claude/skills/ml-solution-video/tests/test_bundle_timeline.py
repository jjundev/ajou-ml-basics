from fixtures import *
from solution_video.bundle_timeline import build_bundle_timeline,page_state
from solution_video.review_adapter import default_config
from solution_video.writing import default_writing
class BundleTiming(Sandbox):
 def test_page_boundaries_and_backward_state(self):
  pages={};order=[];segments=[];audio=[]
  for n in (1,2):
   pid=f'answer-{n}';sid=pid+'::s';order.append(sid)
   pages[pid]=dict(role='answer',metadata=dict(width_pt=1440,height_pt=810),glyphs=[dict(id='g',text='x',bbox=[400,100,410,118])],shapes=[],map=dict(work_bbox=[300,60,1400,600],steps=[dict(id='s',glyph_ids=['g'],shape_ids=[])],answer_step_id='s'))
   segments.append(dict(id=f'write{n}',page_id=pid,step_id=sid,kind='write',text='엑스를 씁니다.',caption_text='x를 씁니다.',source_refs=['source'],chunks=[dict(id='c',text='엑스를 씁니다.',caption_text='x를 씁니다.')]))
   a=make_audio(f'write{n}',24000,self.run);a['chunks']=[dict(id='c',start_sample=0,end_sample=24000)];audio.append(a)
  l=dict(schema_version=2,pages=pages,page_order=list(pages),step_order=order,answer_step_id=order[-1]);m=dict(caption_timing='pcm-chunks-v1',segments=segments,shape_anchors={},cameras=[])
  t=build_bundle_timeline(m,l,audio,default_config(),default_writing('typing'),None)
  self.assertEqual(page_state(t,0)['page_id'],'answer-1')
  end=t['page_spans'][0]['end_frame'];self.assertEqual(page_state(t,end)['page_id'],'answer-2')
  self.assertEqual(page_state(t,0)['visible_ids'],[])
  self.assertEqual(page_state(t,t['total_frames']-1)['visible_ids'],['answer-2::g'])
