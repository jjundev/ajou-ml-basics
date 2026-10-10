from pathlib import Path
import sys, wave
SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[2]
sys.path.insert(0, str(SKILL / 'scripts'))

def pcm(path, samples=24000):
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as f:
        f.setparams((1, 2, 24000, 0, 'NONE', 'not compressed'))
        import math, struct
        f.writeframes(b''.join(struct.pack('<h', int(3000*math.sin(i*.08))) for i in range(samples)))
    return path

def minimal_manifest():
    return {
        'schema_version':1, 'range':'0915',
        'sources':[{'id':'src-note','kind':'note-html','path':'note.html','sha256':'fixture'}],
        'topics':[{'id':'t-atp','requirements':[{'id':'r-atp','claim':'수업 기준 32 ATP','source_id':'src-note','locator':'#respiration','kind':'number','required':True}]}],
        'scenes':[{'id':'scene-atp','topic_ids':['t-atp'],'question_ids':[],'template_kind':'note','visual':'ATP 수량','motion':'수량 증가'}],
        'segments':[{'id':'seg-atp','scene_id':'scene-atp','text':'수업 기준 32 ATP입니다.','caption':'수업 기준 32 ATP','requirement_ids':['r-atp'],'source_ids':['src-note']}],
        'questions':[], 'notices':[], 'conflicts':[], 'exclusions':[],
        'coverage_reviews':[{'requirement_id':'r-atp','segment_ids':['seg-atp'],'status':'passed','reason':'수치와 기준 보존'}]}
