"""ML graph-interpretation lesson, authored against the fixed 1007 P3 sources."""
from ml_authored import author_run
from solution_video.util import read
from video import run_stage
from types import SimpleNamespace
def author_guided(run):
 m=author_run(run);result=run_stage('extract',run,SimpleNamespace())
 if result['status']!='passed':raise ValueError(result)
 result=run_stage('check',run,SimpleNamespace())
 if result['status']!='passed':raise ValueError(result)
 return dict(core_step_ids=[s['step_id'] for s in read(run/'source/lesson.json')['steps']])
