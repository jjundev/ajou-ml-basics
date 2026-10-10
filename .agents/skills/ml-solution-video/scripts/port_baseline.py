"""Reproducible, credential-free import of a fixed Git tree."""
from pathlib import Path
import hashlib,json,subprocess
COMMIT='eeec3d56513fe9e8a34f45edb05ae1118b08cf62'
PREFIX='.agents/skills/ec2-solution-video/'
def sha(b):return hashlib.sha256(b).hexdigest()
def port_baseline(source_repo:Path,dest:Path,commit:str=COMMIT)->dict:
 if commit!=COMMIT:raise ValueError('unsupported baseline')
 dest=Path(dest)
 if dest.exists() and any(dest.iterdir()):raise ValueError('destination must be empty')
 files=subprocess.check_output(['git','ls-tree','-r','--name-only',commit,PREFIX],cwd=source_repo,text=True).splitlines()
 extras=['.agents/skills/ec2-review-video/scripts/lib/'+n+'.py' for n in ('__init__','cache','budget','vertex_tts')]+['.agents/skills/ec2-review-video/assets/fonts/Pretendard-Bold.ttf','.agents/skills/ec2-review-video/assets/runtime/vendor/gsap.min.js']
 rows=[]
 for source in files+extras:
  relative=source.removeprefix(PREFIX) if source.startswith(PREFIX) else ('scripts/solution_video/vendor_tts/'+Path(source).name if '/scripts/lib/' in source else source.split('ec2-review-video/')[1])
  b=subprocess.check_output(['git','show',commit+':'+source],cwd=source_repo);target=dest/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
  rows.append(dict(source=source,destination=relative,source_sha256=sha(b),initial_copy_sha256=sha(b),ported_sha256=sha(b),disposition='copied',test_evidence=['inherited regression']))
 result=dict(commit=commit,baseline_files=files,files=rows)
 (dest/'assets/port-provenance.json').write_text(json.dumps(result,indent=2)+'\n');return result

def refresh_manifest(skill:Path)->None:
 p=Path(skill)/'assets/port-provenance.json';m=json.loads(p.read_text())
 for row in m['files']:
  current=sha((Path(skill)/row['destination']).read_bytes());row['ported_sha256']=current
  if current!=row['initial_copy_sha256'] and row.get('disposition')!='replaced':row['disposition']='adapted'
 p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

def validate_port_manifest(skill:Path)->dict:
 m=json.loads((Path(skill)/'assets/port-provenance.json').read_text());rows=m['files'];sources=[r['source'] for r in rows]
 valid=m['commit']==COMMIT and len(m['baseline_files'])==84 and set(m['baseline_files'])=={s for s in sources if s.startswith(PREFIX)} and len(sources)==len(set(sources))
 for r in rows:
  p=(Path(skill)/r['destination']).resolve()
  valid=valid and p.is_relative_to(Path(skill).resolve()) and p.is_file() and sha(p.read_bytes())==r['ported_sha256'] and r['source_sha256']==r['initial_copy_sha256'] and bool(r['test_evidence'])
 return dict(commit=m['commit'],files=rows,valid=bool(valid))
