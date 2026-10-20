"""Explicit author/build/review/publish workflow; never authors exam questions."""
from pathlib import Path
import argparse
import json
import sys
from exam_config import config_for_round, config_for_output

def emit(value):
    print(json.dumps(value,ensure_ascii=False,indent=2))

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('init','base','english','explain','publish','check'))
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--run',type=Path)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--round',type=int)
    args=parser.parse_args(argv)
    run=None
    try:
        repo=args.repo.resolve()
        if args.command!='check' and args.run is None:raise ValueError('--run required')
        if args.run is not None:
            run=(repo/args.run).resolve()
            if not run.is_relative_to(repo) or run==repo:raise ValueError('run outside repository or repository root')
        if args.command=='init':
            cfg=config_for_round(repo,args.round)
            if cfg.output.exists():raise ValueError('existing round: '+str(cfg.output))
            run.mkdir(parents=True,exist_ok=False)
            value={'repo':str(repo),'out':str(cfg.output),'round':cfg.round_number,
                   'range':cfg.range_,'slug':cfg.slug,'stem':cfg.stem,'mode':'create','status':'initialized'}
            (run/'run.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            emit(value);return 0
        if args.out is None:raise ValueError('--out required')
        cfg=config_for_output(repo,args.out)
        if run is not None:
            run.mkdir(parents=True,exist_ok=True)
            metadata=run/'run.json'
            if metadata.exists():
                old=json.loads(metadata.read_text(encoding='utf-8'))
                if Path(old['repo']).resolve()!=repo or Path(old['out']).resolve()!=cfg.output:
                    raise ValueError('run target mismatch')
        if args.command=='check':
            from check_exam import check_delivery
            errors=check_delivery(cfg.output,repo)
            emit({'status':'fail' if errors else 'pass','errors':errors})
            return int(bool(errors))
        import build_exam
        if args.command=='english':
            from english_pdf import build_english_pdf
            result=build_english_pdf(repo,cfg.output,run)
            status='english_awaiting_visual_review'
        elif args.command=='publish':
            result={'files':list(build_exam.publish_explain(repo,cfg.output,run))}
            status='explanation_published'
        elif args.command=='explain':
            result=build_exam.build_explain(repo,cfg.output,run)
            result={k:v for k,v in result.items() if k not in ('pack','artifacts')}
            status='explanation_awaiting_reviews'
        else:
            result=build_exam.build_base(repo,cfg.output,run)
            status='base_ready'
        state={'repo':str(repo),'out':str(cfg.output),'round':cfg.round_number,'status':status}
        (run/'state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        emit({'status':status,**{k:[str(p) for p in v] if isinstance(v,list) else str(v) for k,v in result.items()}})
        return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        error={'status':'fail','step':args.command,'errors':[str(exc)]}
        if run is not None and run.exists():
            error['backups']=[str(p) for p in run.glob('*backup*')]
            (run/'failure.json').write_text(json.dumps(error,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        emit(error);return 1

if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
