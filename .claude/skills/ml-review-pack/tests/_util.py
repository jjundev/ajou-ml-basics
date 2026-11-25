"""스킬 테스트 공통 경로·도우미."""

from __future__ import annotations

import http.server
import os
import random
from pathlib import Path
import shutil
import sys
import unicodedata

TESTS = Path(__file__).resolve().parent
SKILL = TESTS.parent
SCRIPTS = SKILL / "scripts"
FIXTURES = TESTS / "fixtures"
MINI_RUN = FIXTURES / "mini-run"
REPO = SKILL.parents[2]  # <repo>/.claude/skills/ml-review-pack
sys.path.insert(0, str(SCRIPTS))


def find_nfc(directory: Path, name: str) -> Path | None:
    """macOS NFD 파일명을 NFC 이름으로 찾는다."""
    if not directory.is_dir():
        return None
    for entry in os.listdir(directory):
        if unicodedata.normalize("NFC", entry) == name:
            return directory / entry
    return None


def copy_nfc(src: Path, dst_dir: Path) -> Path:
    """파일을 NFC 이름으로 복사한다."""
    dst = dst_dir / unicodedata.normalize("NFC", src.name)
    shutil.copyfile(src, dst)
    return dst


class _Server(http.server.ThreadingHTTPServer):
    allow_reuse_address = False  # on Windows reuse would let two servers share one port


def local_server(handler):
    """Serve on a free port that Chrome accepts; it blocks several ports up to 10080."""
    for port in random.sample(range(20000, 60000), 50):
        try:
            return _Server(('127.0.0.1', port), handler)
        except OSError:
            continue
    raise RuntimeError('no free local port')
