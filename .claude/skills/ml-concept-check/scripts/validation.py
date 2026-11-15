"""Validate course scope, item shape, and exact arithmetic before rendering."""
from __future__ import annotations

import re
from collections import Counter
from fractions import Fraction
from html import unescape
from pathlib import Path

from quiz_sources import load_items, parse_html

NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)(?:/[0-9]+)?")
CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
NEGATIVES = re.compile(r"않은|아닌|틀린|옳지")
ALLOWED_STEM = re.compile(r"</?(?:p|em|strong|b|i|br|sub|sup)\s*/?>", re.I)


def number(value):
    if not isinstance(value, str) or not NUMBER.fullmatch(value):
        raise ValueError("숫자·유한소수·분수 중 하나를 문자열로 입력하세요")
    return Fraction(value)


def computed(spec):
    match spec:
        case {"op": "responsibility", "contributions": values, "component": component}:
            terms = list(map(number, values))
            if type(component) is not int or not 1 <= component <= len(terms) or min(terms) < 0:
                raise ValueError("0 이상의 기여량과 1부터 시작하는 성분 번호가 필요합니다")
            return terms[component - 1] / sum(terms)
        case {"op": "sum" | "product" | "difference" | "ratio", "values": values}:
            a, b = map(number, values)
            op = spec["op"]
            if op == "sum":
                return a + b
            if op == "product":
                return a * b
            if op == "difference":
                return a - b
            return a / b
        case _:
            raise ValueError("지원하는 계산을 compute에 지정하세요")


def plain_text(html):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]*>", " ", html))).strip()


def check_short(item):
    if not isinstance(item.get("solution"), list) or not item["solution"] or any(
            not isinstance(step, str) or not step.strip() for step in item["solution"]):
        return ["단답의 풀이 단계가 필요합니다"]
    try:
        answer = item["answer"]
        canonical = number(answer["canonical"])
        accepted = answer.get("accepted", [])
        if not isinstance(accepted, list) or any(number(value) != canonical for value in accepted):
            return ["허용값은 대표 정답과 정확히 동치여야 합니다"]
        if computed(item["compute"]) != canonical:
            return ["검산 결과가 대표 정답과 다릅니다"]
    except (TypeError, KeyError, ValueError, ZeroDivisionError) as exc:
        return [f"단답 검산 실패: {exc}"]
    return []


def check_mcq(item, scope):
    options = item.get("options")
    if (not isinstance(options, list) or any(not isinstance(opt, dict) for opt in options)
            or [opt.get("id") for opt in options] != list("ABCD") or item.get("answer") not in list("ABCD")):
        return ["A~D 보기와 정답 글자 하나가 필요합니다"]
    errors = []
    seen = set()
    sources = {f"note:{topic}" for topic in scope["topics"]}
    stt_prefixes = tuple(f"stt:{day}#" for day in scope["stt"])
    for opt in options:
        text, why = opt.get("text"), opt.get("why")
        if not all(isinstance(value, str) and value.strip() for value in (text, why)):
            errors.append(f"{opt['id']}: 보기 문구와 설명이 필요합니다")
            continue
        cleaned = re.sub(r"\s+", "", text).casefold()
        if cleaned in seen:
            errors.append(f"{opt['id']}: 보기 문구가 중복됩니다")
        seen.add(cleaned)
        if opt["id"] == item["answer"]:
            if len(cleaned) >= 2 and cleaned in re.sub(r"\s+", "", item["title"]).casefold():
                errors.append("제목에 정답 보기 문구가 들어 있습니다")
        else:
            ref = opt.get("source", "")
            if not isinstance(opt.get("misconception"), str) or not opt["misconception"].strip():
                errors.append(f"{opt['id']}: 오개념 설명이 필요합니다")
            if not isinstance(ref, str) or (ref not in sources and not (
                    ref.startswith(stt_prefixes) and ref.partition("#")[2].strip())):
                errors.append(f"{opt['id']}: 수업 근거가 필요합니다")
    return errors


def check(src, scope):
    doc, items = load_items(src)
    if (doc.get("range"), doc.get("slug")) != (scope["range"], scope["slug"]):
        return ["정리노트와 objectives.json의 range·slug가 다릅니다"]
    objectives = doc["objectives"]
    errors = []
    known = set()
    for obj in objectives:
        if not isinstance(obj, dict):
            errors.append("목표는 JSON 객체여야 합니다")
            continue
        key = obj.get("id")
        if not isinstance(key, str) or not re.fullmatch(r"o[1-9][0-9]*", key) or key in known:
            errors.append(f"{key}: 고유한 목표 ID가 필요합니다")
            continue
        known.add(key)
        if obj.get("topic_id") not in scope["topics"]:
            errors.append(f"{key}: 수업 토픽 앵커가 없습니다")
        source = obj.get("source")
        if (not isinstance(source, dict) or source.get("date") not in scope["stt"]
                or not isinstance(source.get("locator"), str) or not source["locator"].strip()
                or not isinstance(obj.get("concept"), str) or not obj["concept"].strip()):
            errors.append(f"{key}: 개념, STT 날짜와 근거 위치가 필요합니다")

    if not 1 <= len(items) <= 16:
        errors.append("문항은 1~16개여야 합니다")
    review = parse_html(Path(scope["review"]), review=True)
    review_stems = ["".join(node.text().split()) for node in
                    review.find_all(lambda node: "problem" in node.classes)]
    review_windows = {stem[i:i+20] for stem in review_stems for i in range(len(stem) - 19)}
    objective_counts, answers = Counter(), Counter()
    negatives = 0
    for index, item in enumerate(items, 1):
        key = f"q{index}"
        if not isinstance(item, dict):
            errors.append(f"{key}: 문항은 JSON 객체여야 합니다")
            continue
        objective = item.get("objective")
        if item.get("id") != key or not isinstance(objective, str) or objective not in known:
            errors.append(f"{key}: 문항 순번과 확인 목표를 확인하세요")
            continue
        objective_counts[objective] += 1
        stem, hint, title = (item.get(name) for name in ("stem_html", "hint", "title"))
        if not all(isinstance(value, str) and value.strip() for value in (stem, hint, title)):
            errors.append(f"{key}: 발문·제목·힌트가 필요합니다")
            continue
        if hint.splitlines() != [hint]:
            errors.append(f"{key}: 힌트는 한 문장으로 작성하세요")
        if "<" in ALLOWED_STEM.sub("", stem):
            errors.append(f"{key}: 발문 HTML에 허용되지 않은 태그나 속성이 있습니다")
        text = plain_text(stem)
        compact = "".join(text.split())
        if any(compact[i:i+20] in review_windows for i in range(len(compact) - 19)):
            errors.append(f"{key}: 기존 복습문제 발문과 20자 이상 연속으로 겹칩니다")
        negatives += bool(NEGATIVES.search(title + text))
        if item.get("format") == "short":
            problems = check_short(item)
        elif item.get("format") == "mcq" and isinstance(item.get("answer"), str):
            problems = check_mcq(item, scope)
            answers[item["answer"]] += 1
        else:
            problems = ["문항 형식은 mcq 또는 short여야 합니다"]
        errors.extend(f"{key}: {problem}" for problem in problems)
        extras = []
        if isinstance(item.get("solution"), list):
            extras.extend(item["solution"])
        if isinstance(item.get("options"), list):
            extras.extend(opt.get(field, "") for opt in item["options"] if isinstance(opt, dict)
                          for field in ("text", "why", "misconception"))
        learner_text = " ".join(str(value) for value in (title, stem, hint, *extras)).casefold()
        if CONTROL.search(learner_text):
            errors.append(f"{key}: 발문·힌트·보기 또는 풀이에 제어 문자가 있습니다")
        for word in scope["forbidden"]:
            if word.casefold() in learner_text:
                errors.append(f"{key}: 예고 전용 범위가 포함됩니다 ({word})")
    for key in sorted(known):
        if not 1 <= objective_counts[key] <= 2:
            errors.append(f"{key}: 목표마다 1~2문항이 필요합니다")
    if sum(answers.values()) >= 4:
        counts = [answers[key] for key in "ABCD"]
        if max(counts) - min(counts) > 1:
            errors.append(f"객관식 정답 위치가 고르지 않습니다: A~D {counts}")
    if negatives * 4 > len(items):
        errors.append("부정형 발문은 전체 문항의 4분의 1 이하여야 합니다")
    return errors
