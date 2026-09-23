#!/usr/bin/env python3
"""
복습팩 manifest.json 로더·검증기 (표준 라이브러리만 사용).

manifest는 한 번의 실행(기간 하나)에 대한 계약이다. assemble.py와 check_html.py가 읽는다.
CLI: manifest.py RUN/manifest.json   (검증만, 오류가 있으면 목록 출력 후 종료 코드 1)
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

LAYER_NAMES = {"eli5", "formal", "prof", "warn"}
TOP_LEVEL_TYPES = {
    "course": str, "range": str, "slug": str,
    "note_title": str, "note_subtitle": str, "review_title": str, "review_intro": str,
    "footer_note": str, "footer_review": str,
    "sessions": list, "sections": list, "preview_topic": str, "forbidden_outside_preview": list,
    "parts": list, "problems": list, "links": list,
}
RANGE_RE = re.compile(r"\d{4}(-\d{4})?")
SLUG_RE = re.compile(r"[A-Za-z0-9_]+")
ID_RE = re.compile(r"[A-Za-z][A-Za-z0-9-]*")


class ManifestError(ValueError):
    pass


def _need(obj: dict, key: str, typ: type, where: str, errors: list[str]) -> bool:
    if not isinstance(obj.get(key), typ):
        errors.append(f"{where}.{key}: {typ.__name__} 필요")
        return False
    return True


def validate(m: dict) -> list[str]:
    errors: list[str] = []
    for key, typ in TOP_LEVEL_TYPES.items():
        _need(m, key, typ, "manifest", errors)
    if errors:
        return errors
    if not RANGE_RE.fullmatch(m["range"]):
        errors.append(f"manifest.range: MMDD 또는 MMDD-MMDD 형식이어야 함: {m['range']}")
    if not SLUG_RE.fullmatch(m["slug"]):
        errors.append(f"manifest.slug: 영문·숫자·밑줄만: {m['slug']}")

    seen: set[str] = set()

    def new_id(value: str, where: str) -> None:
        if not ID_RE.fullmatch(value):
            errors.append(f"{where}: id 형식 오류: {value}")
        if value in seen:
            errors.append(f"{where}: 중복 id: {value}")
        seen.add(value)

    for i, s in enumerate(m["sessions"]):
        for key in ("date", "stt", "summary", "slides"):
            _need(s, key, str, f"sessions[{i}]", errors)

    topic_ids: set[str] = set()
    for i, sec in enumerate(m["sections"]):
        where = f"sections[{i}]"
        if not all([_need(sec, "id", str, where, errors), _need(sec, "title", str, where, errors),
                    _need(sec, "short", str, where, errors), _need(sec, "topics", list, where, errors)]):
            continue
        new_id(sec["id"], where)
        for j, t in enumerate(sec["topics"]):
            tw = f"{where}.topics[{j}]"
            ok = all([_need(t, "id", str, tw, errors), _need(t, "title", str, tw, errors),
                      _need(t, "required_terms", list, tw, errors), _need(t, "layers", list, tw, errors),
                      _need(t, "supp", bool, tw, errors)])
            if not ok:
                continue
            new_id(t["id"], tw)
            topic_ids.add(t["id"])
            unknown = set(t["layers"]) - LAYER_NAMES
            if unknown:
                errors.append(f"{tw}.layers: 알 수 없는 레이어 {sorted(unknown)}")

    if m["preview_topic"] not in topic_ids:
        errors.append(f"preview_topic: 토픽 id가 아님: {m['preview_topic']}")

    part_ids: set[str] = set()
    for i, p in enumerate(m["parts"]):
        where = f"parts[{i}]"
        if all([_need(p, "id", str, where, errors), _need(p, "title", str, where, errors),
                _need(p, "short", str, where, errors)]):
            new_id(p["id"], where)
            part_ids.add(p["id"])

    for i, q in enumerate(m["problems"]):
        where = f"problems[{i}]"
        ok = all([_need(q, key, typ, where, errors) for key, typ in (
            ("id", str), ("part", str), ("source", str), ("variant", bool), ("anchor", str),
            ("level", int), ("date", str), ("terms", list), ("answer", str))])
        if not ok:
            continue
        new_id(q["id"], where)
        if q["part"] not in part_ids:
            errors.append(f"{where}.part: 없는 part: {q['part']}")
        if q["anchor"] not in topic_ids:
            errors.append(f"{where}.anchor: 없는 토픽: {q['anchor']}")
        if not 1 <= q["level"] <= 3:
            errors.append(f"{where}.level: 1~3이어야 함")

    for i, link in enumerate(m["links"]):
        where = f"links[{i}]"
        if _need(link, "topic", str, where, errors) and link["topic"] not in topic_ids:
            errors.append(f"{where}.topic: 없는 토픽: {link['topic']}")
        _need(link, "href", str, where, errors)
    return errors


def load(path: Path | str) -> dict:
    m = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate(m)
    if errors:
        raise ManifestError("\n".join(errors))
    return m


def note_name(m: dict) -> str:
    return f"정리노트_{m['range']}_{m['slug']}.html"


def review_name(m: dict) -> str:
    return f"복습문제_{m['range']}_{m['slug']}.html"


def fig_dir_name(range_: str) -> str:
    return f"figures_{range_}"


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("사용법: manifest.py RUN/manifest.json", file=sys.stderr)
        return 2
    try:
        load(argv[0])
    except ManifestError as e:
        print(e)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
