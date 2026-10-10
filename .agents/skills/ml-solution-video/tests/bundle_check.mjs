import fs from 'node:fs';import {createRequire} from 'node:module';import {pathToFileURL} from 'node:url';
const args=Object.fromEntries(process.argv.slice(2).reduce((a,v,i,x)=>i%2===0?[...a,[v,x[i+1]]]:a,[]));
const require=createRequire(args['--puppeteer-package']);const puppeteer=require('puppeteer-core');const browser=await puppeteer.launch({executablePath:args['--chrome'],headless:true,args:['--allow-file-access-from-files','--no-sandbox','--disable-gpu','--disable-partial-raster','--disable-backgrounding-occluded-windows','--disable-background-timer-throttling','--disable-renderer-backgrounding']});
try{const page=await browser.newPage();await page.setViewport({width:1920,height:1080});await page.goto(pathToFileURL(args['--entry']).href,{waitUntil:'load'});await page.evaluate(()=>window.solutionReady);
const first_page_svg_height=await page.evaluate(()=>{const p=Array.from(document.querySelectorAll('.bundle-page')).find(p=>p.style.visibility==='visible');return p.querySelector('svg').getBoundingClientRect().height;});
const timeline=JSON.parse(fs.readFileSync(args['--timeline'],'utf8'));let leaks=0,diff=0;const frames=[0,...timeline.page_spans.flatMap(s=>[s.start_frame,Math.max(s.start_frame,s.end_frame-1)]),...timeline.events.flatMap(e=>[Math.max(0,e.frame-1),e.frame])];
async function state(frame,gsap=false){return page.evaluate(({frame,gsap})=>{if(gsap)window.__timelines.solution.seek(frame/30,false);else window.renderSolutionFrame(frame);const p=Array.from(document.querySelectorAll('.bundle-page')).find(p=>p.style.visibility==='visible');const w=window.solutionPageRenderers[p?.dataset.pageId];return {page_id:window.solutionPageId,visible:Array.from(p?.querySelectorAll('[data-reveal]')||[]).filter(n=>getComputedStyle(n).opacity!=='0').map(n=>n.dataset.reveal),writing:w?.solutionWriting?.snapshot()||null,pencil:p?.querySelector('[data-local-name="pencil"]')?.style.opacity||'0'};},{frame,gsap});}
if(!args['--reference-only']){
 const states=await page.evaluate(({timeline,frames})=>{
  function snapshot(f,gsap=false){if(gsap)window.__timelines.solution.seek(f/30,false);else window.renderSolutionFrame(f);const p=Array.from(document.querySelectorAll('.bundle-page')).find(p=>p.style.visibility==='visible'),w=window.solutionPageRenderers[p?.dataset.pageId];return {page_id:window.solutionPageId,visible:Array.from(p?.querySelectorAll('[data-reveal]')||[]).filter(n=>getComputedStyle(n).opacity!=='0').map(n=>n.dataset.reveal),writing:w?.solutionWriting?.snapshot()||null,pencil:p?.querySelector('[data-local-name="pencil"]')?.style.opacity||'0'};}
  const snapshots=new Map();let leaks=0,diff=0;for(const f of frames){const s=snapshot(f);snapshots.set(f,JSON.stringify(s));const expected=timeline.page_spans.find(p=>p.start_frame<=f&&f<p.end_frame).page_id;if(s.page_id!==expected)leaks++;if(timeline.writing?.mode!=='pencil'){const visible=new Set(timeline.events.filter(e=>e.frame<=f&&e.page_id===s.page_id).map(e=>e.id));if(s.visible.some(id=>!visible.has(id)))leaks++;}}
  for(const f of frames.slice().reverse()){if(JSON.stringify(snapshot(f))!==snapshots.get(f))diff++;if(JSON.stringify(snapshot(f,true))!==snapshots.get(f))diff++;}return {leaks,diff};
 },{timeline,frames});leaks=states.leaks;diff=states.diff;
}
let parent_reference_diff=0,oracle_probes=0,oracle_total_probes=0,mismatch_frames=[];
if(args['--views']){
 const views=JSON.parse(fs.readFileSync(args['--views'],'utf8')),ref=await browser.newPage();await ref.setViewport({width:1920,height:1080});
 const probeFrames=[...frames,...(timeline.writing_spans||[]).flatMap(s=>[s.start_frame,Math.floor((s.start_frame+s.end_frame-1)/2),s.end_frame-1]),...(timeline.writing_unit_spans||[]).map(s=>s.end_frame),...(timeline.teaching?.spans||[]).flatMap(s=>[s.start_frame,Math.floor((s.start_frame+s.end_frame-1)/2),s.end_frame])];
 const tasks=[];for(const pid of Object.keys(views))for(const f of [...new Set(probeFrames)].sort((a,b)=>a-b)){if(f<timeline.total_frames&&timeline.page_spans.find(s=>s.start_frame<=f&&f<s.end_frame)?.page_id===pid)tasks.push({pid,f});}oracle_total_probes=tasks.length;const wanted=tasks.slice(Number(args['--frame-start']||0),Number(args['--frame-start']||0)+Number(args['--frame-count']||tasks.length));
 for(const [pid,view] of Object.entries(views)){
  if(!wanted.some(t=>t.pid===pid))continue;
  const entry=new URL(view.entry,pathToFileURL(args['--entry'])).href;await ref.goto(entry,{waitUntil:'load'});await ref.evaluate(async()=>{for(const im of document.images)await im.decode();});
  const warm=timeline.page_spans.filter(s=>s.page_id===pid).at(-1).end_frame-1;await state(warm);await ref.evaluate(f=>window.renderSolutionFrame(f),warm);for(const target of [page,ref]){await target.bringToFront();await target.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));await target.screenshot();}
  for(const {f} of wanted.filter(t=>t.pid===pid)){
   if(f>=timeline.total_frames||timeline.page_spans.find(s=>s.start_frame<=f&&f<s.end_frame)?.page_id!==pid)continue;
   await state(f);await ref.evaluate(f=>window.renderSolutionFrame(f),f);await page.bringToFront();await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));const actual=await page.screenshot();
   await ref.bringToFront();await ref.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));const expected=await ref.screenshot();if(!Buffer.from(actual).equals(Buffer.from(expected))){
 const delta=await page.evaluate(async({a,b})=>{
  async function pixels(value){const bytes=Uint8Array.from(atob(value),c=>c.charCodeAt(0)),image=await createImageBitmap(new Blob([bytes],{type:'image/png'})),canvas=document.createElement('canvas');canvas.width=image.width;canvas.height=image.height;const ctx=canvas.getContext('2d');ctx.drawImage(image,0,0);const data=ctx.getImageData(0,0,canvas.width,canvas.height).data;image.close();return {data,width:canvas.width,height:canvas.height};}
  const aa=await pixels(a),bb=await pixels(b);if(aa.width!==bb.width||aa.height!==bb.height)return {pixels:-1};let count=0,max=0,x0=aa.width,y0=aa.height,x1=0,y1=0;for(let k=0;k<aa.data.length;k+=4){let changed=false;for(let c=0;c<4;c++){const d=Math.abs(aa.data[k+c]-bb.data[k+c]);max=Math.max(max,d);changed||=d!==0;}if(changed){count++;const x=(k/4)%aa.width,y=Math.floor(k/4/aa.width);x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);}}return {pixels:count,max_channel_diff:max,bbox:count?[x0,y0,x1,y1]:null};
 },{a:Buffer.from(actual).toString('base64'),b:Buffer.from(expected).toString('base64')});
 if(delta.pixels!==0){parent_reference_diff++;mismatch_frames.push({page_id:pid,frame:f,...delta});if(args['--dest']){fs.mkdirSync(args['--dest'],{recursive:true});fs.writeFileSync(args['--dest']+'/'+pid+'-'+f+'-actual.png',actual);fs.writeFileSync(args['--dest']+'/'+pid+'-'+f+'-expected.png',expected);}}
 }oracle_probes++;
  }
 }await ref.close();
}
const final=await state(timeline.total_frames-1);console.log(JSON.stringify({forward_backward_diff:diff,future_leaks:leaks,final_pencil:final.pencil,page_count:timeline.page_spans.length,parent_reference_diff,oracle_probes,oracle_total_probes,first_page_svg_height,mismatch_frames,forward_backward_checked:!args['--reference-only']}));
}finally{await browser.close();}
