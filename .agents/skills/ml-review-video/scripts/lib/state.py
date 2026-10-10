from pathlib import Path
import json
from .math_evidence import math_evidence_files
from .cache import atomic_json,file_lock,file_hash,digest

STAGES=('inputs','coverage','script','voice','timing','composition','render','verify','publish')

def stage_fingerprint(run,stage):
    run=Path(run)
    patterns={
      'inputs':['source/inputs.json','source/inputs/*'],
      'coverage':['manifest.json','source/inputs.json','source/inputs/*'],
      'script':['manifest.json','source/scene-fragments/*','source/math-evidence.json','source/calculations/**/*'],
      'voice':['manifest.json'],
      'timing':['manifest.json','source/audio.json'],
      'composition':['manifest.json','source/timeline.json','source/theme.json','source/*.css','source/scene-fragments/*','assets/**/*'],
      'render':['*.html','source/compositions/*','source/*.css','source/parts.json','source/timeline.json','source/render-options.json','assets/**/*'],
      'verify':['review.mp4','manifest.json','*.html','source/**/*','assets/**/*'],
      'publish':['review.mp4','verification/report.json']}
    files={}
    for pattern in patterns[stage]:
        for p in run.glob(pattern):
            if p.is_file(): files[p.relative_to(run).as_posix()]=file_hash(p)
    if stage in ('script','composition') and (run/'source/math-evidence.json').exists():
        try:
            for p in math_evidence_files(run): files[p.relative_to(run.resolve()).as_posix()]=file_hash(p)
        except (OSError,ValueError,TypeError,KeyError):
            files['invalid-math-evidence']='invalid'
    config={}
    if stage=='voice' and (run/'config.json').exists():
        c=json.loads((run/'config.json').read_text(encoding='utf-8'))
        config={k:c.get(k) for k in ('provider','model','voice','language','direction','pronunciation','max_output_tokens')}
    if stage=='composition':
        files['renderer/composition.py']=file_hash(Path(__file__).with_name('composition.py'))
    if stage in ('render','verify','publish'):
        for name in ('render_options.py','render.py'):
            files['renderer/'+name]=file_hash(Path(__file__).with_name(name))
    return digest({'files':files,'config':config})

class RunStore:
    def __init__(self,run): self.run=Path(run)
    def lock(self): return file_lock(self.run/'work/run.lock')
    def load(self):
        p=self.run/'run.json'
        return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'schema_version':1,'stages':{}}
    def save(self,state): atomic_json(self.run/'run.json',state)
    def invalidate(self,stage):
        state=self.load()
        for name in STAGES[STAGES.index(stage):]:
            state.setdefault('stages',{})[name]={'status':'pending'}
        self.save(state)
    def recover(self):
        state=self.load()
        for name in STAGES:
            item=state.setdefault('stages',{}).get(name,{})
            if item.get('status') not in ('passed','running'): continue
            outputs=item.get('output_hashes',{})
            valid=bool(outputs) and item.get('input_hash')==stage_fingerprint(self.run,name)
            for relative,h in outputs.items():
                p=self.run/relative
                valid=valid and p.is_file() and file_hash(p)==h
            if not valid:
                self.invalidate(name); return name
            item['status']='passed'
        self.save(state)
        return next((s for s in STAGES if state['stages'].get(s,{}).get('status')!='passed'),None)
