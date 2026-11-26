#!/usr/bin/env python3
"""복습문제 구성이 출제 명세표(시험결과/출제명세표.json)의 요구 구조 목표를 채우는지 검사한다.

    python3 check_blueprint.py <RUN>/manifest.json <RUN>/blueprint.json <REPO>/시험결과/출제명세표.json \
        [--self-checks <RUN>/self-checks.json]

<RUN>/blueprint.json:
    {"problems": [{"id": "p1", "asks": 2, "last_ask": "읽기", "chained": false}, ...,
                  {"id": "p11", "asks": 2, "last_ask": "판정", "chained": false,
                   "fills": "non_calc_last", "uses": ["s1-mean"]}],
     "gaps": {"chained": "못 채운 이유"}}
목표를 못 채운 항목은 gaps에 같은 키로 이유를 적으면 통과한다. 태그가 카드 문장과 맞는지는 리뷰어가 본다.

자작 문제(manifest source "자작 pN")는 MML 문제만으로 못 채운 목표(fills)에만 쓴다.
팩당 targets.max_self_made개 이하, uses는 이번 팩에서 가르친 토픽 id, self-checks.json에 {"pN": {"status": "pass"}}.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

GAP_KEYS = {"levels", "multi_ask", "non_calc_last", "chained", "dates"}
FILL_KEYS = GAP_KEYS - {"levels"}  # 난이도 균형은 MML 문제로만 맞춘다


def exam_stats(exam: dict) -> dict:
    items = exam["items"]
    return {
        "items": len(items),
        "levels": [sum(i["level"] == k for i in items) for k in (1, 2, 3)],
        "chained": sum(bool(i["chained"]) for i in items),
        "non_calc_last": sum(i["last_ask"] != "계산" for i in items),
        "lost": sum(i["lost"] for i in items),
    }


def _int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def is_self_made(problem: dict) -> bool:
    return str(problem.get("source", "")).startswith("자작 ")


def _missed(t: dict, probs: list[dict], rows: dict, n: int, dates: list[str]) -> dict:
    """probs만 세었을 때 비는 목표. 비율은 팩 전체 문항 수 n으로 나눈다."""
    tagged = [rows[p["id"]] for p in probs]
    floor = t["per_date_min_level"]
    return {
        "multi_ask": (sum(r["asks"] >= 2 for r in tagged), n and sum(r["asks"] >= 2 for r in tagged) / n < t["min_multi_ask_share"]),
        "non_calc_last": (sum(r["last_ask"] != "계산" for r in tagged),
                          n and sum(r["last_ask"] != "계산" for r in tagged) / n < t["min_non_calc_last_share"]),
        "chained": (sum(r["chained"] for r in tagged), sum(r["chained"] for r in tagged) < t["min_chained"]),
        "dates": [d for d in dates if not any(p["date"] == d and p["level"] >= floor for p in probs)],
    }


def _check_self_made(manifest: dict, rows: dict, t: dict, self_checks: dict | None) -> list[str]:
    errors: list[str] = []
    probs = manifest.get("problems", [])
    own = [p for p in probs if is_self_made(p)]
    for p in probs:
        if not is_self_made(p) and ("fills" in rows[p["id"]] or "uses" in rows[p["id"]]):
            errors.append(f"{p['id']}.fills: MML 문제에는 fills/uses를 쓰지 않음")
    if not own:
        return errors
    if len(own) > t["max_self_made"]:
        errors.append(f"자작 문제 {len(own)}개, 팩당 최대 {t['max_self_made']}개")
    preview = manifest.get("preview_topic")
    taught = {tp["id"] for s in manifest.get("sections", []) for tp in s.get("topics", [])
              if tp["id"] != preview and not tp["id"].endswith("-links")}
    dates = sorted({s["date"] for s in manifest.get("sessions", [])})
    mml = [p for p in probs if not is_self_made(p)]
    missed = _missed(t, mml, rows, len(probs), dates)
    for p in own:
        pid, r = p["id"], rows[p["id"]]
        if p["source"] != f"자작 {pid}":
            errors.append(f"{pid}.source: '자작 {pid}'이어야 함 ({p['source']!r})")
        fills = r.get("fills")
        if fills not in FILL_KEYS:
            errors.append(f"{pid}.fills: {sorted(FILL_KEYS)} 중 하나 필요 (levels는 자작으로 채우지 않음)")
        elif fills == "dates":
            if p["date"] not in missed["dates"] or p["level"] < t["per_date_min_level"]:
                errors.append(f"{pid}: dates를 채우려면 MML 난이도 {t['per_date_min_level']}+ 문제가 없는 날짜의 "
                              f"난이도 {t['per_date_min_level']}+ 문제여야 함 (필요 없는 자작)")
        elif not missed[fills][1]:
            errors.append(f"{pid}: MML 문제만으로 {fills} 목표를 이미 채워 자작이 필요 없음")
        uses = r.get("uses")
        if not isinstance(uses, list) or not uses or any(u not in taught for u in uses):
            errors.append(f"{pid}.uses: 이번 팩에서 가르친 토픽 id 1개 이상 필요 (예고·links 제외): {uses!r}")
        status = (self_checks or {}).get(pid, {})
        if not isinstance(status, dict) or status.get("status") != "pass":
            errors.append(f"{pid}: self-checks.json에 sympy 검산 pass 없음")
    return errors


def check(manifest: dict, tags: dict, blueprint: dict, self_checks: dict | None = None) -> list[str]:
    errors: list[str] = []
    t = blueprint["targets"]
    kinds = set(blueprint["last_ask_kinds"])
    probs = manifest.get("problems", [])
    rows = {r.get("id"): r for r in tags.get("problems", []) if isinstance(r, dict)}
    gaps = tags.get("gaps", {})

    for key in sorted(set(gaps) - GAP_KEYS):
        errors.append(f"gaps.{key}: 알 수 없는 키 (허용: {', '.join(sorted(GAP_KEYS))})")
    excused = {k for k, v in gaps.items() if isinstance(v, str) and v.strip()}

    ids = [p["id"] for p in probs]
    for pid in ids:
        if pid not in rows:
            errors.append(f"{pid}: blueprint.json에 태그 없음")
    for pid in rows:
        if pid not in ids:
            errors.append(f"{pid}: manifest problems에 없는 id")

    for pid, r in rows.items():
        if not _int(r.get("asks")) or r["asks"] < 1:
            errors.append(f"{pid}.asks: 1 이상의 정수 필요")
        if r.get("last_ask") not in kinds:
            errors.append(f"{pid}.last_ask: {sorted(kinds)} 중 하나 필요")
        if not isinstance(r.get("chained"), bool):
            errors.append(f"{pid}.chained: true/false 필요")
        elif r["chained"] and not (_int(r.get("asks")) and r["asks"] >= 2):
            errors.append(f"{pid}.chained: 이어지는 카드는 요구가 2개 이상이어야 함")
    if errors:
        return errors
    errors += _check_self_made(manifest, rows, t, self_checks)

    def miss(key: str, msg: str) -> None:
        if key not in excused:
            errors.append(f"{key}: {msg}")

    n = len(probs)
    want = t["level_counts"].get(str(n))
    got = [sum(p["level"] == k for p in probs) for k in (1, 2, 3)]
    if want is None:
        miss("levels", f"문항 수 {n}에 대한 난이도 표 없음 ({', '.join(t['level_counts'])}문항만)")
    elif got != want:
        miss("levels", f"난이도 1:2:3 = {got[0]}:{got[1]}:{got[2]}, 목표 {want[0]}:{want[1]}:{want[2]}")

    tagged = [rows[pid] for pid in ids]
    multi = sum(r["asks"] >= 2 for r in tagged)
    if n and multi / n < t["min_multi_ask_share"]:
        miss("multi_ask", f"요구 2개 이상 {multi}/{n}, 목표 {t['min_multi_ask_share']:.0%} 이상")
    non_calc = sum(r["last_ask"] != "계산" for r in tagged)
    if n and non_calc / n < t["min_non_calc_last_share"]:
        miss("non_calc_last", f"마지막 요구가 계산이 아닌 문제 {non_calc}/{n}, 목표 {t['min_non_calc_last_share']:.0%} 이상")
    chained = sum(r["chained"] for r in tagged)
    if chained < t["min_chained"]:
        miss("chained", f"이어지는 카드 {chained}개, 목표 {t['min_chained']}개 이상")

    floor = t["per_date_min_level"]
    for d in sorted({s["date"] for s in manifest.get("sessions", [])}):
        if not any(p["date"] == d and p["level"] >= floor for p in probs):
            miss("dates", f"{d}: 난이도 {floor} 이상 문제 없음")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest")
    ap.add_argument("tags")
    ap.add_argument("blueprint")
    ap.add_argument("--self-checks", help="자작 문제가 있을 때 <RUN>/self-checks.json")
    a = ap.parse_args()
    load = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
    errors = check(load(a.manifest), load(a.tags), load(a.blueprint), load(a.self_checks) if a.self_checks else None)
    for e in errors:
        print(e)
    print("OK" if not errors else f"FAIL ({len(errors)})")
    return int(bool(errors))


if __name__ == "__main__":
    import sys
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
