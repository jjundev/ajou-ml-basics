"""Backed-up multi-file replacement with rollback and kernel-owned locks.

This is recoverable publication, not an OS-atomic multi-file transaction.
"""
from contextlib import contextmanager, ExitStack
from pathlib import Path
try:
    import fcntl
except ImportError:  # Windows: msvcrt byte-range lock, released when the handle closes
    fcntl=None
    import msvcrt
import hashlib
import os
import re
import shutil
import tempfile
import uuid
from urllib.parse import unquote, urlsplit
from review_pdf_types import ReviewPdfError
from manifest import PACK_DIR, note_name, pdf_names, review_name
from review_sources import archive_cards, html_name


def _try_lock(stream):
    if fcntl:fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB);return
    stream.seek(0)
    try:msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
    except OSError as e:raise BlockingIOError(str(e)) from e


@contextmanager
def publication_lock(destinations):
    lock_root=Path(tempfile.gettempdir())/'ml-review-pdf-locks';lock_root.mkdir(exist_ok=True)
    parents=sorted({str(Path(p).resolve().parent) for p in destinations})
    with ExitStack() as stack:
        for parent in parents:
            name=hashlib.sha256(parent.encode()).hexdigest()+'.lock'
            stream=stack.enter_context((lock_root/name).open('a+'))
            try:_try_lock(stream)
            except BlockingIOError as e:raise ReviewPdfError(f'publication locked: {parent}') from e
        yield
    # Closing the descriptors releases locks; never unlink a live lock inode.


def _replace_copy(source,destination):
    destination.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.review-pdf-',dir=destination.parent)
    temp=Path(name)
    try:
        with os.fdopen(fd,'wb') as stream:
            with source.open('rb') as src:shutil.copyfileobj(src,stream)
            stream.flush();os.fsync(stream.fileno())
        os.replace(temp,destination)
    finally:temp.unlink(missing_ok=True)


def publish_files(staged,backup_dir, *, remove=(), expected_hashes=None):
    mapping={Path(dst):Path(src) for dst,src in staged.items()}
    if not mapping:raise ReviewPdfError('no files to publish')
    for dst,src in mapping.items():
        if not src.is_file():raise ReviewPdfError(f'missing stage file: {src}')
        if dst.is_symlink() or (dst.exists() and not dst.is_file()):raise ReviewPdfError(f'invalid destination: {dst}')
        if dst.resolve()==src.resolve():raise ReviewPdfError(f'stage equals destination: {dst}')
    deletions = tuple(map(Path, remove))
    if set(deletions) & mapping.keys():
        raise ReviewPdfError("cannot replace and remove the same file")
    destinations = (*mapping, *deletions)
    expected_hashes = expected_hashes or {}
    with publication_lock((*destinations, *expected_hashes)):
        for path, expected in expected_hashes.items():
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ReviewPdfError(f'source changed before publication: {path}')
        for dst in deletions:
            if dst.is_symlink() or (dst.exists() and not dst.is_file()):
                raise ReviewPdfError(f"invalid deletion destination: {dst}")
        backup=Path(backup_dir)/uuid.uuid4().hex;backup.mkdir(parents=True,exist_ok=False)
        originals={};replaced=[]
        for i,dst in enumerate(destinations):
            if dst.exists():
                saved=backup/f'{i}-{dst.name}';shutil.copy2(dst,saved);originals[dst]=saved
            else:originals[dst]=None
        try:
            for dst,src in mapping.items():
                _replace_copy(src,dst);replaced.append(dst)
            for dst in deletions:
                if originals[dst] is not None:
                    dst.unlink();replaced.append(dst)
        except BaseException:
            for dst in reversed(replaced):
                if originals[dst] is None:dst.unlink(missing_ok=True)
                else:_replace_copy(originals[dst],dst)
            raise

def publish_pack(stage, destination, backup_dir, manifest):
    """Publish the approved PDF pair, note and authored sources together."""
    stage, destination = Path(stage), Path(destination)
    review = stage / review_name(manifest)
    note = stage / note_name(manifest)
    from review_pdf_cards import parse, read_cards
    old_links = [href for node in parse(note.read_text(encoding='utf-8')).find_all(lambda n: n.tag == 'a')
                 if (href := node.attrs.get('href')) and re.fullmatch(
                     r'복습문제_.*\.html', html_name(Path(unquote(urlsplit(href).path))))]
    if old_links:
        raise ReviewPdfError(f'review HTML links must be replaced with PDF links: {old_links}')
    original = read_cards(review).cards
    archived = archive_cards(review)
    if original != read_cards(archived).cards:
        raise ReviewPdfError('archived review cards differ')
    storage = stage / PACK_DIR
    required = [note, archived, storage / note.with_suffix('.md').name,
                storage / review.with_suffix('.md').name]
    required.extend(storage / name for name in pdf_names(manifest['range'], manifest['slug']))
    optional = [p for p in storage.rglob('*') if p.is_file() and p not in required
                and not re.fullmatch(r'복습문제_.*\.html', html_name(p))]
    mapping = {destination / p.relative_to(stage): p for p in [*required, *optional]}
    publish_files(mapping, backup_dir, remove=[destination / review.name])
