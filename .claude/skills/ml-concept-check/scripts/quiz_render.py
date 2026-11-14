"""문항(item) → 카드 HTML. 생명과학 review_interaction.build_model 이 읽는 마크업을 따른다."""
from __future__ import annotations

import html
import json

def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def _problem(item: dict, choices: str) -> str:
    body = item["stem_html"]
    # 보기 목록은 .problem 안에 둔다(review-prompt.js problemText 가 .problem 안의 .choices 를 지운다).
    return f'<div class="problem">{body}{choices}</div>'


def _mcq(item: dict) -> tuple[str, str, str, str]:
    choices = "".join(f'<li data-choice="{esc(o["id"])}">{esc(o["text"])}</li>' for o in item["options"])
    steps = []
    for o in item["options"]:
        if o["id"] == item["answer"]:
            text = esc(o["why"])
        else:
            text = f'"{esc(o["misconception"])}" — {esc(o["why"])}'
        steps.append(f'<li data-explains="{esc(o["id"])}">{text}</li>')
    return ("", f'<ol class="choices">{choices}</ol>', "",
            f'<ol class="steps">{"".join(steps)}</ol><p class="answer">정답: {esc(item["answer"])}</p>')


def _short(item: dict) -> tuple[str, str, str, str]:
    canonical = item["answer"]["canonical"]
    accepted: list[str] = []
    for a in item["answer"].get("accepted", []):
        if a != canonical and a not in accepted:
            accepted.append(a)
    data = json.dumps(dict(canonical=canonical, accepted=accepted, case_sensitive=False), ensure_ascii=False)
    cid = esc(item["id"])
    attrs = f' data-format="short" data-short-answer="{esc(data)}"'
    inputs = (f'<div class="short-input"><label for="answer-{cid}">답</label>'
              f'<input type="text" id="answer-{cid}" autocomplete="off">'
              '<button class="btn btn-primary check-answer" type="button">답 확인</button></div>')
    steps = "".join(f"<li>{esc(s)}</li>" for s in item["solution"])
    return attrs, "", inputs, f'<ol class="steps">{steps}</ol><p class="answer">정답: {esc(canonical)}</p>'


NOTE_LINK_TEXT = "정리노트에서 이 개념 다시 보기 →"


def note_link(note_name: str, topic_id: str) -> str:
    """그 목표의 정리노트 토픽으로 가는 링크. 풀이 안에 두어 채점 뒤에만 보인다. 같은 창에서 연다(사용자 결정, 2026-11-13)."""
    href = f"{note_name}#{topic_id}"
    return (f'<p class="note-link"><a href="{esc(href)}">'
            f'{esc(NOTE_LINK_TEXT)}</a></p>')


def card_html(item: dict, objective: dict, number: int, note_name: str) -> str:
    attrs, choices, after, solution = _short(item) if item["format"] == "short" else _mcq(item)
    hint = item.get("hint")
    hint_block = (f'<details class="hint" open><summary>힌트 보기</summary><p>{esc(hint)}</p></details>'
                  if hint else "")
    solution += note_link(note_name, objective["topic_id"])
    return (f'<article class="card" id="{esc(item["id"])}" data-objective="{esc(objective["id"])}"{attrs}>'
            f'<h3>Q{number}. {esc(item["title"])}</h3>'
            + _problem(item, choices) + after + hint_block
            + f'<details class="solution"><summary>풀이 보기</summary>{solution}</details></article>')
