from .bundle_layers import flatten_layers
from .teaching import build_teaching_timeline
from .contracts import InputError

def build_bundle_timeline(manifest,layers,audio,config,writing,teaching=None):
 flat=flatten_layers(layers);t=build_teaching_timeline(manifest,flat,audio,config,writing,teaching);t['schema_version']=2
 spans=[]
 for seg in t['segments']:
  pid=seg.get('page_id')
  if pid not in layers['pages']:raise InputError('timeline segment page missing')
  start,end=seg['start_sample']//800,seg['end_sample']//800
  if spans and spans[-1]['page_id']==pid:spans[-1]['end_frame']=end
  else:spans.append(dict(page_id=pid,start_frame=start,end_frame=end))
 spans[-1]['end_frame']=t['total_frames'];t['page_spans']=spans
 for field in ('events','writing_spans','writing_unit_spans'):
  for row in t.get(field,[]):row['page_id']=row.get('step_id',row.get('id','')).split('::',1)[0]
 if t.get('teaching') and teaching:
  page_of={i['id']:i.get('page_id') for i in teaching['items']}
  for span in t['teaching']['spans']:span['page_id']=page_of[span['id']]
 reset_page_entry_moves(t)
 return t

def page_state(timeline,frame):
 frame=max(0,min(timeline['total_frames']-1,int(frame)));span=next(s for s in timeline['page_spans'] if s['start_frame']<=frame<s['end_frame']);pid=span['page_id']
 return dict(page_id=pid,visible_ids=[e['id'] for e in timeline['events'] if e.get('page_id')==pid and e['frame']<=frame])


def reset_page_entry_moves(timeline):
 # A new PDF page has no visible pen continuity with the previous sheet.
 # Keep the measured move interval, but start it at the current target.
 for span in timeline.get('writing_spans',[]):
  source=span.get('from_id') or ''
  if span.get('kind')=='move' and '::' in source and source.split('::',1)[0]!=span.get('page_id'):
   span['from_id']=span['id']
   span['from_bbox']=list(span['clip_bbox'])
 return timeline
