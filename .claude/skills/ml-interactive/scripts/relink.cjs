// Restore contextual links from portable per-artifact metadata.
const fs=require('node:fs'),path=require('node:path');
const {resolve}=require('./resolve.cjs'),{linkNotes}=require('./link-notes.cjs');
function repoPath(repo,relative){
 if(typeof relative!=='string'||path.isAbsolute(relative)||/^[a-z]:|^\\/i.test(relative))throw new Error('relative path required');
 const result=path.resolve(repo,relative),rel=path.relative(path.resolve(repo),result);
 if(rel==='..'||rel.startsWith('..'+path.sep)||path.isAbsolute(rel))throw new Error('path outside repo');return result;
}
function list(d){try{return fs.readdirSync(d,{withFileTypes:true});}catch{return [];}}
// macOS names are often NFD while metadata is NFC: compare folder keys in NFC.
const folderKey=f=>path.resolve(f).normalize('NFC').toLowerCase();
function relink({repo,arg,dryRun=false}){
 repo=path.resolve(repo);const actual=list(repo).find(d=>d.isDirectory()&&d.name.normalize('NFC')==='복습노트');
 const root=path.join(repo,actual?actual.name:'복습노트');
 const sourceFolders=list(root).filter(d=>d.isDirectory()).map(d=>path.join(root,d.name));
 let folders=[];
 if(arg==='전체'||arg==='all')folders=sourceFolders;
 else{try{folders=[resolve({repo,arg}).folder];}catch(e){if(e.code==='NO_TARGET')return {notes:[],skipped:[]};throw e;}}
 const selected=new Set(folders.map(folderKey));
 const grouped=new Map(),skipped=[];
 // Metadata belongs to the artifact; the requested target belongs to the note.
 for(const folder of sourceFolders)for(const d of list(path.join(folder,'.pack'))){
  if(!d.isDirectory()||!/^자료_인터렉티브_/.test(d.name.normalize('NFC')))continue;
  const file=path.join(folder,'.pack',d.name,'note-links.json');
  if(!fs.existsSync(file)){skipped.push({file,reason:'NO_LINK_METADATA'});continue;}
  try{
   const data=JSON.parse(fs.readFileSync(file,'utf8').replace(/^\uFEFF/,''));
   if(data.v!==1||!Array.isArray(data.links))throw new Error('invalid metadata schema');
   const links=data.links.map(l=>({...l,note:repoPath(repo,l.note),html:repoPath(repo,l.html)}));
   for(const l of links){if(!selected.has(folderKey(path.dirname(l.note))))continue;
    if(!grouped.has(l.note))grouped.set(l.note,[]);grouped.get(l.note).push(l);
   }
  }catch(e){skipped.push({file,reason:'METADATA_INVALID',message:e.message});}
 }
 return {notes:[...grouped].map(([note,links])=>linkNotes({note,links,dryRun})),skipped};
}
if(require.main===module){const [repo,...rest]=process.argv.slice(2);try{console.log(JSON.stringify(relink({repo:repo||'.',arg:rest.filter(a=>a!=='--dry-run').join(' '),dryRun:rest.includes('--dry-run')}),null,2));}catch(e){console.error(e.message);process.exitCode=1;}}
module.exports={relink,repoPath};
