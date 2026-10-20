from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
import fitz
R=Path.cwd();RUN=R/'tmp/ml-midterm/round02-easier-20261020';OUT=R/'중간고사대비/예상문제_2회'
english=next(RUN.glob('english-*/english-pdf-validation.json'))
epdf=next(english.parent.glob('*.pdf'))
(RUN/'english-result.json').write_text(json.dumps({'problems_pdf':str(epdf),'report':str(english)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[('problems',next(OUT.glob('*-문제.pdf'))),('answers',next(OUT.glob('*-답안.pdf'))),('english',epdf)]
records=[]
for tag,pdf in files:
 dest=RUN/'pdf-shots'/tag;dest.mkdir(parents=True,exist_ok=True)
 subprocess.run(['pdftoppm','-png','-scale-to','1440',str(pdf),str(dest/'page')],check=True,capture_output=True)
 pages=sorted(dest.glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1]));doc=fitz.open(pdf)
 for n,(page,png) in enumerate(zip(doc,pages),1):
  im=Image.open(png).convert('RGB');bottom=im.crop((0,int(im.height*675/810),im.width,im.height))
  assert bottom.getextrema()==((255,255),(255,255),(255,255)),(tag,n,'bottom band not white')
  assert tuple(page.rect)==(0.0,0.0,1440.0,810.0)
  text=page.get_text();assert '\ufffd' not in text
  records.append({'file':pdf.name,'page':n,'size_pt':[1440,810],'white_bottom_pt':135,'png':str(png.relative_to(R)),'text_characters':len(text)})
 for j in range(0,len(pages),2):
  pair=pages[j:j+2];canvas=Image.new('RGB',(1440,840*len(pair)),'#dddddd');draw=ImageDraw.Draw(canvas)
  for k,p in enumerate(pair):
   im=Image.open(p).convert('RGB');canvas.paste(im,(0,840*k+30));draw.text((15,840*k+8),f'{tag} physical page {j+k+1}',fill='black')
  canvas.save(dest/f'contact-{j//2+1}.png')
(RUN/'pdf-render-results.json').write_text(json.dumps({'status':'rendered_pending_visual_review','pages':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print([(tag,len(fitz.open(pdf))) for tag,pdf in files]);print(len(records),'pages rendered')
