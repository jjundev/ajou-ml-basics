"""ml-review-pack의 scripts/를 import 경로에 넣는다. 양식·검사 로직을 복습 스킬과 공유하기 위해서다."""

from pathlib import Path
import sys

REVIEW_SCRIPTS = Path(__file__).resolve().parents[2] / "ml-review-pack" / "scripts"
if not REVIEW_SCRIPTS.is_dir():
    raise ImportError(f"ml-review-pack 스킬 없음: {REVIEW_SCRIPTS}")
if str(REVIEW_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(REVIEW_SCRIPTS))
