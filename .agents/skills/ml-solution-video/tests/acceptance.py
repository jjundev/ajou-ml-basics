"""ML source-bound scratch acceptance; synthetic output cannot publish."""
from ml_acceptance import run_acceptance,main
from ml_authored import author_run
IDS=['P2','P3','P8']
def author(run):
 from solution_video.util import read
 from solution_video.bundle_layers import extract_bundle
 m=author_run(run);l=extract_bundle(read(run/'layers/candidates.json'),read(run/'source/map.json'))
 return m,l
if __name__=='__main__':raise SystemExit(main())
