"""Exercise generated GSAP in real Chrome; future hide must not reveal a graph."""
import unittest,tempfile,json,subprocess,shutil
from pathlib import Path
from _util import SKILL,ROOT,minimal_manifest
from lib.composition import assemble,stage_assets
from lib.theme import snapshot_theme
from lib.timing import build_timeline
from lib.cache import atomic_json
class SeekInitialStateTest(unittest.TestCase):
 def test_future_hide_does_not_reveal_middle_graph(self):
  pkg=Path('/Users/hyunjun_macbook_pro/.npm/_npx/702923228c2ce1e6/node_modules/puppeteer-core/package.json')
  chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
  if not pkg.is_file() or not chrome.is_file():self.skipTest('local Chrome/puppeteer required')
  with tempfile.TemporaryDirectory() as d:
   run=Path(d);m=minimal_manifest();base=m['segments'][0];sid=m['scenes'][0]['id'];m['segments']=[dict(base,id='s'+str(i)) for i in range(3)]
   stage_assets(SKILL/'assets/runtime',run);theme=snapshot_theme(ROOT/'.agents/skills/ml-review-pack',run);frag=run/'source/scene-fragments';frag.mkdir();(frag/(sid+'.html')).write_text('<section class="topic">'+''.join(f'<p id="{sid}-g{i}">graph{i}</p>' for i in range(3))+'</section>')
   motions=[]
   for i in range(3):
    motions.append(dict(target=f'#{sid}-g{i}',segment_id='s'+str(i),kind='reveal',**{'from':dict(opacity=0),'to':dict(opacity=1)},duration_s=.1))
    if i:motions.append(dict(target=f'#{sid}-g{i-1}',segment_id='s'+str(i),kind='reveal',**{'from':dict(opacity=1),'to':dict(opacity=0)},duration_s=.1))
   atomic_json(frag/(sid+'.motion.json'),motions);timeline=build_timeline(m,[dict(id=s['id'],samples=24000,rate=24000) for s in m['segments']]);assemble(m,timeline,theme,run)
   html=(run/(sid+'.html')).read_text();body=html.split('<body',1)[1].split('>',1)[1].split('<script>',1)[0];script=html.rsplit('<script>',1)[1].split('</script>',1)[0]
   code="const {createRequire}=require('module');const pp=createRequire(process.argv[1])('puppeteer-core');(async()=>{let browser=await pp.launch({executablePath:process.argv[2],headless:true,args:['--no-sandbox']});try{let page=await browser.newPage();await page.setContent(process.argv[3]);await page.addScriptTag({path:process.argv[4]});await page.evaluate(process.argv[5]);await page.waitForFunction(()=>window.__timelines);let values=await page.evaluate(()=>{window.__timelines['scene-atp'].seek(.8,false);return [0,1,2].map(i=>Number(getComputedStyle(document.querySelector('#scene-atp-g'+i)).opacity));});console.log(JSON.stringify(values));}finally{await browser.close();}})();"
   r=subprocess.run(['node','-e',code,str(pkg),str(chrome),body,str(SKILL/'assets/runtime/vendor/gsap.min.js'),script],capture_output=True,text=True,timeout=30,check=True)
   self.assertEqual(json.loads(r.stdout.strip()),[1,0,0])
