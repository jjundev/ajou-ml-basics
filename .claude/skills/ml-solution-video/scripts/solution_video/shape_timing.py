"""Allocate one horizontal reveal budget per original PDF shape."""
import math
from .contracts import InputError


def allocate_shape_frames(units:list[dict],layers:dict,step_id:str,height:float,interval:int)->dict[tuple[str,int],int]:
    if type(height) not in (int,float) or not math.isfinite(height) or height<=0 or type(interval) is not int or interval<=0:
        raise InputError('invalid shape timing height/interval')
    shapes={s['id']:s for s in layers['shapes']};groups={};result={}
    for u in units:
        if u['step_id']!=step_id:continue
        for i,p in enumerate(u['pieces']):
            if p['kind']=='shape':groups.setdefault(p['id'],[]).append(((u['id'],i),p['clip_bbox'][2]-p['clip_bbox'][0]))
    for sid,parts in groups.items():
        if sid not in shapes:raise InputError('missing shape '+sid)
        width=shapes[sid]['bbox'][2]-shapes[sid]['bbox'][0]
        if not math.isfinite(width) or width<0 or any(not math.isfinite(w) or w<0 for _,w in parts):raise InputError('invalid shape width '+sid)
        budget=min(90,max(18,math.ceil(width/height*interval)))
        if len(parts)>budget:raise InputError(f'shape {sid}: {len(parts)} pieces exceed {budget} frames')
        if width==0:
            if len(parts)!=1:raise InputError('vertical shape must have one piece '+sid)
            result[parts[0][0]]=budget;continue
        if any(w<=0 for _,w in parts):raise InputError('empty shape clip '+sid)
        # Freeze quotas below one frame, then redistribute remaining budget.
        pending=list(range(len(parts)));quotas=[0.]*len(parts);remaining=budget
        while pending:
            scale=remaining/sum(parts[i][1] for i in pending)
            small=[i for i in pending if parts[i][1]*scale<1]
            if not small:
                for i in pending:quotas[i]=parts[i][1]*scale
                break
            for i in small:quotas[i]=1.;remaining-=1;pending.remove(i)
        frames=[math.floor(q) for q in quotas]
        for i in sorted(range(len(parts)),key=lambda i:(-(quotas[i]-frames[i]),i))[:budget-sum(frames)]:frames[i]+=1
        for (key,_),n in zip(parts,frames):result[key]=n
    return result
