"""Bind every exported page and glyph label to its frozen PDF, before paid work."""
from pathlib import Path
import xml.etree.ElementTree as ET,unicodedata
from .contracts import ReviewError
from .util import read,local,file_hash
from .pdf_pages import _painted,image_proven_invisible

def validate_bundle_sources(bundle,layers,run):
 import fitz
 run=Path(run).resolve();inputs=read(run/'source/inputs.json')['files'];refs=bundle['problem_pages']+bundle['answer_pages']
 if layers['page_order']!=[r['id'] for r in refs] or set(layers['pages'])!={r['id'] for r in refs}:raise ReviewError('source page inventory differs from frozen bundle')
 for ref in refs:
  path=local(run,ref['snapshot']);page=layers['pages'][ref['id']];meta=page['metadata'];source=inputs.get(ref['snapshot'])
  if not source or file_hash(path)!=source['sha256'] or meta['source_sha256']!=source['sha256'] or meta['page_index']!=ref['page_index']:raise ReviewError('frozen PDF page identity mismatch')
  original=Path(page['original_svg']).resolve()
  if not original.is_relative_to(run):raise ReviewError('original SVG outside run')
  with fitz.open(path) as pdf:
   pg=pdf[ref['page_index']]
   if abs(pg.rect.width-ref['width_pt'])>.01 or abs(pg.rect.height-ref['height_pt'])>.01 or meta['width_pt']!=ref['width_pt'] or meta['height_pt']!=ref['height_pt']:raise ReviewError('source page dimensions changed')
   svg=pg.get_svg_image(text_as_path=True)
  if original.read_text()!=svg:raise ReviewError('original SVG differs from frozen PDF page; re-export')
  root=ET.fromstring(svg);nodes={'sv-'+str(i):node for i,node in enumerate(_painted(root))}
  from .util import browser
  inventory={i['id']:i for i in browser(['--mode','inventory','--svg',str(original)])}
  if {i['id'] for i in page.get('images',[])}!={i['id'] for i in inventory.values() if i['tag']=='image'}:raise ReviewError('source raster inventory differs from frozen PDF')
  for image in page.get('images',[]):
   sid=image['id'];native=inventory.get(sid)
   if not native or native['tag']!='image' or len(image['bbox'])!=4 or any(abs(a-b)>1e-6 for a,b in zip(image['bbox'],native['bbox'])) or bool(image.get('proven_invisible',False))!=image_proven_invisible(root,nodes[sid]):raise ReviewError('raster bounds/invisibility differs from frozen source')
  seen=set()
  for glyph in page['glyphs']:
   ids=glyph['svg_ids']
   if not ids or any(i not in nodes or nodes[i].get('data-text') is None or i in seen for i in ids):raise ReviewError('source glyph ID mismatch')
   text=''.join(nodes[i].get('data-text') for i in ids);seen.update(ids)
   if unicodedata.normalize('NFC',glyph['text'])!=unicodedata.normalize('NFC',text):raise ReviewError('glyph text differs from frozen PDF outline')
