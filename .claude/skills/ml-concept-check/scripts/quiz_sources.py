"""Read matching ML notes and transcripts by their NFC file names."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
REVIEW_SCRIPTS = SKILL.parent / "ml-review-pack" / "scripts"
if str(REVIEW_SCRIPTS) not in sys.path:
    sys.path.append(str(REVIEW_SCRIPTS))

from html2md import Builder

RANGE = re.compile(r"[0-9]{4}(?:-[0-9]{4})?")
SLUG = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
TRANSCRIPT = re.compile(r"([0-9]{4}) 머러기\.md")


class QuizError(ValueError):
    pass


def nfc(value):
    return unicodedata.normalize("NFC", str(value))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise QuizError(f"{path}: {exc}") from exc
    if not isinstance(data, dict):
        raise QuizError(f"{path}: JSON 객체가 필요합니다")
    return data


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_items(src):
    objectives = read_json(src / "objectives.json")
    items = read_json(src / "items.json").get("items")
    if not isinstance(objectives.get("objectives"), list) or not isinstance(items, list):
        raise QuizError("objectives와 items는 목록이어야 합니다")
    return objectives, items


def parse_html(path):
    parser = Builder()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser.root


def source_scope(repo, range_, manifest_path=None):
    if not RANGE.fullmatch(range_):
        raise QuizError("범위는 MMDD 또는 MMDD-MMDD로 입력하세요")
    dates = range_.split("-")
    first, last = dates[0], dates[-1]
    if last < first:
        raise QuizError("범위의 끝 날짜가 시작 날짜보다 앞섭니다")

    day = repo / "복습노트" / range_
    if not day.is_dir():
        raise QuizError(f"복습팩 폴더가 없습니다: {day}")
    prefix = f"정리노트_{range_}_"
    notes = [path for path in day.iterdir() if path.is_file()
             and nfc(path.name).startswith(prefix) and path.suffix == ".html"]
    if len(notes) != 1:
        raise QuizError(f"{day}: 정리노트 HTML을 하나로 특정할 수 없습니다 ({len(notes)}개)")
    note = notes[0]
    slug = nfc(note.stem)[len(prefix):]
    if not SLUG.fullmatch(slug):
        raise QuizError(f"정리노트 slug가 유효하지 않습니다: {slug}")
    md = day / ".pack" / f"{prefix}{slug}.md"
    review = day / f"복습문제_{range_}_{slug}.html"
    for path in (md, review):
        if not path.is_file():
            raise QuizError(f"복습팩 근거가 없습니다: {path}")

    stt_dir = repo / "STT"
    stt = {}
    if stt_dir.is_dir():
        for path in sorted(stt_dir.iterdir()):
            name = TRANSCRIPT.fullmatch(nfc(path.name))
            if name and path.is_file() and first <= name[1] <= last:
                stt[name[1]] = path
    if any(date not in stt for date in dates):
        raise QuizError(f"범위의 시작·끝 날짜 STT가 필요합니다: {range_}")

    if manifest_path is None:
        manifests = [path for path in (day / ".pack").glob("*/manifest.json")
                     if nfc(path.parent.name) in {"자료_복습팩", f"자료_복습팩_{range_}"}]
        if len(manifests) > 1:
            raise QuizError(f"{day}: 확인할 복습팩 manifest를 --manifest로 지정하세요")
        manifest_path = next(iter(manifests), None)
    manifest = read_json(manifest_path) if manifest_path else {}
    if manifest_path and (manifest.get("range"), manifest.get("slug")) != (range_, slug):
        raise QuizError("복습팩 manifest의 range·slug가 정리노트와 일치하지 않습니다")
    listed = {topic["id"]: topic for section in manifest.get("sections", [])
              for topic in section["topics"]}
    preview = manifest.get("preview_topic")
    topics = []
    for node in parse_html(note).find_all(lambda node: node.tag == "article" and "topic" in node.classes):
        topic = node.attrs.get("id", "")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", topic):
            continue
        if topic == preview or topic.endswith(("-next", "-preview", "-links", "-cheatsheet")):
            continue
        if listed and (topic not in listed or listed[topic].get("supp")):
            continue
        topics.append(topic)
    if not topics or len(set(topics)) != len(topics):
        raise QuizError("정리노트에서 고유한 수업 토픽을 찾지 못했습니다")
    files = [note, md, review, *stt.values()]
    if manifest_path:
        files.append(manifest_path)
    return {
        "range": range_, "slug": slug, "note": str(note), "note_md": str(md), "review": str(review),
        "stt": {day_: str(path) for day_, path in stt.items()}, "topics": topics,
        "forbidden": manifest.get("forbidden_outside_preview", []),
        "hashes": {str(path): digest(path) for path in files},
    }
