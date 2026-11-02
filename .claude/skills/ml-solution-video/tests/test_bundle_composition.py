from fixtures import *
from solution_video.bundle_layers import export_bundle,extract_bundle
from solution_video.bundle_timeline import build_bundle_timeline
from solution_video.composition import assemble
from solution_video.review_adapter import default_config
from solution_video.writing import default_writing
from solution_video.util import write,checked,browser_config
class BundleComposition(Sandbox):
 def test_seek_across_pages_and_visible_equation_focus(self):
  pdf=math_pdf(self.run/'a.pdf');refs=[dict(id=f'answer-{n}',role='answer',snapshot=str(pdf),page_index=0) for n in (1,2)];bundle=dict(problem_pages=[dict(id='problem-1',role='problem',snapshot=str(pdf),page_index=0)],answer_pages=refs)
  pages=export_bundle(bundle,self.run);maps={pid:dict(mapping(p),terminal_step_id='solution') for pid,p in pages.items() if pid.startswith('answer')};order=[pid+'::solution' for pid in maps];l=extract_bundle(pages,dict(schema_version=2,pages=maps,step_order=order,answer_step_id=order[-1]));segments=[];audio=[]
  for i,pid in enumerate(pages):
   sid=f's{i}';text='식의 조건을 확인합니다.';step=pid+'::solution' if pid.startswith('answer') else '';segments.append(dict(id=sid,page_id=pid,step_id=step,kind='write' if step else 'problem',text=text,caption_text=text,source_refs=['source'],chunks=[dict(id='c',text=text,caption_text=text)]));a=make_audio(sid,24000,self.run);a['chunks']=[dict(id='c',start_sample=0,end_sample=24000)];audio.append(a)
  m=dict(schema_version=2,segments=segments,cameras=[],shape_anchors={pid+'::'+s:pid+'::'+mp['steps'][0]['glyph_ids'][-1] for pid,mp in maps.items() for s in mp['steps'][0]['shape_ids']},caption_timing='pcm-chunks-v1');t=build_bundle_timeline(m,l,audio,default_config(),default_writing('typing'));write(self.run/'source/timeline.json',t);assemble(bundle,l,m,t,self.run,S/'assets/runtime/vendor/gsap.min.js')
  r=checked(['node',S/'tests/bundle_check.mjs','--entry',self.run/'composition/index.html','--timeline',self.run/'source/timeline.json','--views',self.run/'composition/bundle-views.json',*browser_config()]);result=json.loads(r.stdout)
  self.assertEqual(result['first_page_svg_height'],900);self.assertEqual(result['forward_backward_diff'],0);self.assertEqual(result['future_leaks'],0);self.assertEqual(result['final_pencil'],'0');self.assertEqual(result['parent_reference_diff'],0)
  entry=self.run/'composition/index.html';original=entry.read_text();entry.write_text(original.replace('</head>', '<style>.bundle-page[data-page-id="answer-2"]{opacity:0}</style></head>'))
  mutant=json.loads(checked(['node',S/'tests/bundle_check.mjs','--entry',entry,'--timeline',self.run/'source/timeline.json','--views',self.run/'composition/bundle-views.json',*browser_config()]).stdout)
  self.assertGreater(mutant['parent_reference_diff'],0)
