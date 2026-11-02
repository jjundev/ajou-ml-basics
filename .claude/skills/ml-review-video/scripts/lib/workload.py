"""Estimate authored motion coverage; no browser sampling or source mutation."""
from fractions import Fraction
from pathlib import Path
import json,math


def _integer(value):
    if type(value) is not int:raise ValueError('motion metadata requires integer samples/frames')
    return value


def scene_motion_profile(run,part):
    run=Path(run);frames=_integer(part['frames'])
    if frames<=0:raise ValueError('scene frames must be positive')
    timeline_path=run/'source/timeline.json'
    motion_path=run/'source/scene-fragments'/(part['id']+'.motion.json')
    try:
        timeline=json.loads(timeline_path.read_text(encoding='utf-8-sig')) if timeline_path.is_file() else None
        motions=json.loads(motion_path.read_text(encoding='utf-8-sig')) if motion_path.is_file() else None
        if timeline_path.is_file() and (not isinstance(timeline,dict) or timeline.get('rate')!=24000 or timeline.get('fps')!=30):
            raise ValueError('motion timeline requires 24kHz/30fps')
        if motion_path.is_file() and not isinstance(motions,list):raise ValueError('motions must be a list')
        if timeline is None or motions is None:
            return dict(status='unknown',scene_frames=frames,animated_seconds=None,motion_ratio=None)
        matches=[s for s in timeline['scenes'] if s['id']==part['id']]
        if len(matches)!=1:raise ValueError('scene metadata missing or repeated')
        scene=matches[0];start=_integer(scene['start_sample']);end=_integer(scene['end_sample'])
        if start<0 or end<=start or _integer(scene['last_frame'])-_integer(scene['first_frame'])!=frames:
            raise ValueError('scene metadata does not match render part')
        duration=Fraction(frames,30);segments={}
        for seg in timeline['segments']:
            if seg['scene_id']==part['id']:
                if seg['id'] in segments:raise ValueError('duplicate segment metadata')
                left=_integer(seg['start_sample']);right=_integer(seg['end_sample'])
                if not start<=left<right<=end:raise ValueError('speech outside scene')
                segments[seg['id']]=seg
        intervals=[]
        for motion in motions:
            if not isinstance(motion,dict):raise ValueError('motion must be an object')
            seg=segments[motion['segment_id']];seconds=motion['duration_s']
            if type(seconds) not in (int,float) or not math.isfinite(seconds) or seconds<=0:
                raise ValueError('motion duration must be finite positive')
            span=Fraction(str(seconds))
            if span>Fraction(seg['end_sample']-seg['start_sample'],24000):raise ValueError('motion exceeds speech')
            if not isinstance(motion['from'],dict) or not isinstance(motion['to'],dict):raise ValueError('motion properties must be objects')
            if not any(key not in motion['from'] or motion['from'][key]!=value
                       for key,value in motion['to'].items()):continue
            left=Fraction(seg['start_sample']-start,24000);right=min(duration,left+span)
            if right>left:intervals.append((max(Fraction(0),left),right))
        merged=[]
        for left,right in sorted(intervals):
            if merged and left<=merged[-1][1]:merged[-1]=(merged[-1][0],max(merged[-1][1],right))
            else:merged.append((left,right))
        active=sum((right-left for left,right in merged),Fraction(0))
        return dict(status='known',scene_frames=frames,animated_seconds=float(active),motion_ratio=float(active/duration))
    except (KeyError,TypeError,OverflowError) as ex:
        raise ValueError('invalid motion metadata: '+str(ex)) from ex
