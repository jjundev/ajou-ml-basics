import pathlib,json,subprocess,hashlib,concurrent.futures
from PIL import Image,ImageDraw
out=pathlib.Path(__file__).parent;packs=json.loads((out/'assigned-packs.json').read_text());pdf=pathlib.Path(packs[0]['MML_pdf']['path']);pages=[46,47,87,88,89,153,155,156,159,194,196,198,205,208,230,298,299,302,307,309,317,319];dest=out/'source-pages'
def render(page):
 prefix=dest/f'mml-{page:03}';subprocess.run(['pdftoppm','-f',str(page),'-singlefile','-scale-to','1400','-png',str(pdf),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);png=pathlib.Path(str(prefix)+'.png');return {'pdf':str(pdf),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'page':page,'image':str(png),'image_sha256':hashlib.sha256(png.read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as x: rows=list(x.map(render,pages))
(out/'extra-source-page-bindings.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for start in range(0,len(rows),4):
 sheet=Image.new('RGB',(2800,2880),'#ddd');draw=ImageDraw.Draw(sheet)
 for n,row in enumerate(rows[start:start+4]):
  im=Image.open(row['image']);im.thumbnail((1400,1400));x=(n%2)*1400;y=(n//2)*1440;sheet.paste(im,(x,y+40));draw.text((x+10,y+10),pathlib.Path(row['image']).name,fill='black')
 sheet.save(dest/f'extra-{start//4+1:02}.jpg',quality=92)
print('rendered',len(rows))
