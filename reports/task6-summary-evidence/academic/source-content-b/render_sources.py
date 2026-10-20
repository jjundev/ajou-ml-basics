import pathlib,json,subprocess,hashlib,concurrent.futures
from PIL import Image,ImageOps,ImageDraw
out=pathlib.Path(__file__).parent;packs=json.loads((out/'assigned-packs.json').read_text()); mml=pathlib.Path(packs[0]['MML_pdf']['path']);hw=pathlib.Path(packs[-1]['primary_source_pdf']['path']);lecture=next(pathlib.Path(r['path']) for r in packs[-1]['current_references'] if 'Lecture04' in r['path'])
tasks=[('mml',mml,p) for p in [106,107,188,189,200,206,207,218,225,226,228,229,300,308,311,312,314,315,316,318,320]]+[('hw',hw,p) for p in range(3,10)]+[('lecture4',lecture,p) for p in [14,17,23]]
renders=out/'source-pages';renders.mkdir(exist_ok=True)
def render(t):
 label,pdf,page=t;dest=renders/f'{label}-{page:03}';subprocess.run(['pdftoppm','-f',str(page),'-singlefile','-scale-to','1400','-png',str(pdf),str(dest)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);return {'pdf':str(pdf),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'page':page,'image':str(dest)+'.png','image_sha256':hashlib.sha256((pathlib.Path(str(dest)+'.png')).read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as x: rows=list(x.map(render,tasks))
(out/'source-page-bindings.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for start in range(0,len(rows),4):
 part=rows[start:start+4];sheet=Image.new('RGB',(2800,2880),'#ddd');d=ImageDraw.Draw(sheet)
 for n,row in enumerate(part):
  im=Image.open(row['image']);im.thumbnail((1400,1400));x=(n%2)*1400;y=(n//2)*1440;sheet.paste(im,(x,y+40));d.text((x+10,y+10),pathlib.Path(row['image']).name,fill='black')
 sheet.save(renders/f'contact-{start//4+1:02}.jpg',quality=92)
print('rendered',len(rows),'authentic source pages, contacts', (len(rows)+3)//4)
