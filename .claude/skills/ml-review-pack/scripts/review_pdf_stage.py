#!/usr/bin/env python3
"""Mirror read dependencies while keeping the current pack writable and isolated."""
from pathlib import Path
import argparse
import re
import shutil
from review_pdf_types import ReviewPdfError


def prepare_stage(run_dir: Path, repo_root: Path, range_: str) -> Path:
    if not re.fullmatch(r'\d{4}(?:-\d{4})?',range_):
        raise ReviewPdfError('invalid stage range')
    run_dir,repo_root=Path(run_dir).resolve(),Path(repo_root).resolve()
    root=run_dir/'work/stage'
    if root.is_symlink():raise ReviewPdfError('stage root must be a private directory')
    root.mkdir(parents=True,exist_ok=True)
    for name in ['강의노트','교과서','STT']:
        source=repo_root/name;target=root/name
        if source.exists() and not target.exists():target.symlink_to(source,target_is_directory=True)
    notes=root/'복습노트'
    if notes.is_symlink():raise ReviewPdfError('stage notes root must be private')
    notes.mkdir(exist_ok=True)
    source_notes=repo_root/'복습노트'
    if source_notes.exists():
        for source in source_notes.iterdir():
            if source.name==range_:continue
            target=notes/source.name
            if not target.exists():target.symlink_to(source,target_is_directory=source.is_dir())
    pack=notes/range_
    if pack.is_symlink():raise ReviewPdfError('current stage pack must be private')
    pack.mkdir(exist_ok=True)
    # Existing image assets may be reused, but stale HTML/MD/PDFs are never staged.
    old=source_notes/range_
    if old.exists():
        for image in old.rglob('*'):
            if image.is_file() and image.suffix.lower() in {'.png','.jpg','.jpeg','.gif','.svg','.webp'}:
                target=pack/image.relative_to(old)
                if not target.exists():
                    target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(image,target)
    return pack


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run',required=True,type=Path);ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--range',required=True)
    args=ap.parse_args()
    print(prepare_stage(args.run,args.repo,args.range))
if __name__=='__main__':main()
