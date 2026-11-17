"""Validated choice/diagnostic mapping and self-contained review enhancement."""
from __future__ import annotations
import hashlib
import json
import re

from quiz_sources import SKILL
from html2md import Builder, Node

LABEL = re.compile(r'^\s*(?:\((\d+)\)|([A-Z])[.)])\s*')
ANSWER = re.compile(r'^\s*정답:\s*(?:\((\d+)\)|([A-Z]))\s*$')
CAUTION = re.compile(r'모호|모두 가능|단일 정답|엄밀한.*정답|복수.?정답|답이 하나|성립할 여지|해석에 따라|옳은 설명으로 볼 여지|완전히 옳다고 보기 어려|같은 뜻이 되지만|자료도 있으니')


def find(node, cls):
    return list(node.find_all(lambda n: cls in n.classes))


def children(node, tag):
    return [n for n in node.children if isinstance(n, Node) and n.tag == tag]


def label(node, attr):
    explicit = node.attrs.get(attr)
    if explicit:
        if not re.fullmatch(r'\d+|[A-Z]', explicit):
            raise ValueError('보기 식별자 형식 오류')
        return explicit
    match = LABEL.match(node.text())
    if not match:
        return None
    return next(g for g in match.groups() if g is not None)


def snapshot(node):
    if isinstance(node, str):
        return node
    return [node.tag, sorted(node.attrs.items()), [snapshot(n) for n in node.children]]


def build_model(source: str, document_id: str) -> dict:
    tree = Builder()
    tree.feed(source)
    result = dict(schema=1, documentId=document_id, cards={}, skipped=[], errors=[])
    seen = set()
    for card in find(tree.root, 'card'):
        cid = card.attrs.get('id', '')
        try:
            if not cid or cid in seen:
                raise ValueError('문항 id 누락 또는 중복')
            seen.add(cid)
            if card.attrs.get('data-format') == 'short':
                answer = json.loads(card.attrs.get('data-short-answer', '{}'))
                if (not isinstance(answer, dict) or not isinstance(answer.get('canonical'), str)
                    or not answer['canonical'].strip() or not isinstance(answer.get('accepted'), list)
                    or not all(isinstance(x, str) and x.strip() for x in answer['accepted'])
                    or type(answer.get('case_sensitive')) is not bool):
                    raise ValueError('단답형 정답/허용답 형식 오류')
                if len(find(card, 'solution')) != 1:
                    raise ValueError('단답형 풀이 누락 또는 중복')
                result['cards'][cid] = dict(format='short', answer=answer,
                    version=hashlib.sha256(json.dumps(snapshot(card), ensure_ascii=False).encode()).hexdigest())
                continue
            lists = find(card, 'choices')
            if not lists:
                result['skipped'].append(cid)
                continue
            if len(lists) != 1:
                raise ValueError('보기 목록은 하나여야 함')
            choices = children(lists[0], 'li')
            solutions = find(card, 'solution')
            answers = find(card, 'answer')
            if len(solutions) != 1 or len(answers) != 1:
                raise ValueError('풀이 또는 정답이 없거나 중복됨')
            steps = find(solutions[0], 'steps')
            if len(steps) != 1:
                raise ValueError('보기별 해설 목록이 없거나 중복됨')
            diagnostics = children(steps[0], 'li')
            match = ANSWER.fullmatch(answers[0].text())
            if not match:
                raise ValueError('명시 정답 형식을 해석할 수 없음')
            answer = next(g for g in match.groups() if g is not None)
            ids = [label(n, 'data-choice') for n in choices]
            if len(ids) < 2 or None in ids or len(set(ids)) != len(ids) or answer not in ids:
                raise ValueError('보기 식별자 누락/중복 또는 정답이 보기에 없음')
            mapping = {}
            for i, n in enumerate(diagnostics):
                key = label(n, 'data-explains')
                if key is not None:
                    if key in mapping:
                        raise ValueError('보기별 해설 식별자 중복')
                    mapping[key] = i
            positions = [mapping.get(key) for key in ids]
            if any(type(i) is not int or not 0 <= i < len(diagnostics) for i in positions):
                raise ValueError('보기별 해설 연결 누락 또는 범위 오류')
            if len(set(positions)) != len(positions):
                raise ValueError('여러 보기에 동일 해설 연결')
            if CAUTION.search(solutions[0].text()):
                raise ValueError('모호성 문구 수동 검토 필요')
            model = dict(answer=answer, mode='single', notice='',
                         options=[dict(id=key, index=i, diagnostic=mapping[key]) for i, key in enumerate(ids)])
            payload = json.dumps([snapshot(card), model], ensure_ascii=False, sort_keys=True)
            model['version'] = hashlib.sha256(payload.encode('utf-8')).hexdigest()
            result['cards'][cid] = model
        except ValueError as exc:
            result['cards'].pop(cid, None)
            result['errors'].append(dict(cardId=cid, reason=str(exc)))
    return result


START = '<!-- review-interaction:start -->'
END = '<!-- review-interaction:end -->'
ANSWER_EVENT = """        document.addEventListener('od:answer', ({detail}) => {
          if (!cards.some(c => c.id === detail.id)) return;
          if (detail.restored && detail.selected !== null) return;
          if (detail.selected === null) solved.delete(detail.id);
          else solved.add(detail.id);
          // 저장하지 않는다: 새로고침하면 진행이 초기화된다(ds-review-pack 템플릿엔 tabStore 가 없다).
          if (curId) paintBtn();
          markToc(solved, cards.length, '푼 문제');
        });
"""


LEAVE_ANCHOR = "          if (cur >= 0) screens[cur].classList.remove('is-current', 'enter-next', 'enter-prev');\n"
LEAVE_LINE = ("          if (cur >= 0) document.dispatchEvent(new CustomEvent('od:leave', "
              "{ detail: { index: cur, screen: screens[cur] } }));\n")


def patch_pager_shell(source: str) -> str:
    if '<script id="pager-ui">' not in source or "detail: { index: cur, screen: screens[cur] }" in source:
        return source
    if source.count(LEAVE_ANCHOR) != 1:
        raise ValueError('pager 화면 전환 구조 불일치')
    return source.replace(LEAVE_ANCHOR, LEAVE_LINE + LEAVE_ANCHOR)


def patch_review_shell(source: str) -> str:
    if 'function setupReview()' not in source:
        return source
    begin = source.index('function setupReview()')
    end = source.index('function setupNote()', begin)
    section = source[begin:end]
    if "g.dataset.cardId = card.id;" not in section:
        needle = "g.className = 'aid';"
        if section.count(needle) != 1:
            raise ValueError('setupReview aid 구조 불일치')
        section = section.replace(needle, needle + '\n          g.dataset.cardId = card.id;')
    if "if (detail.selected === null) solved.delete(detail.id);" not in section:
        needle = "        document.addEventListener('od:screen', (e) => {"
        if section.count(needle) != 1:
            raise ValueError('setupReview 이벤트 구조 불일치')
        section = section.replace(needle, ANSWER_EVENT + needle)
    elif 'if (detail.restored && detail.selected !== null) return;' not in section:
        needle = "          if (!cards.some(c => c.id === detail.id)) return;"
        if section.count(needle) != 1:
            raise ValueError('setupReview 완료 상태 연결 구조 불일치')
        section = section.replace(needle, needle + '\n          if (detail.restored && detail.selected !== null) return;')
    section = drop_solved_persistence(section)
    return source[:begin] + section + source[end:]


SOLVED_LOAD = "new Set(store.get(KEY, []).filter("
SOLVED_SAVE = "          store.set(KEY, Array.from(solved));\n"
SOLVED_MARK = "// concept-check: 푼 문제 기록은 저장하지 않는다"


def drop_solved_persistence(section: str) -> str:
    """setupReview 의 '푼 문제' 기록을 메모리에만 둔다(새로고침하면 진행 초기화). 테마 저장은 그대로."""
    if SOLVED_MARK in section:
        return section
    if section.count(SOLVED_LOAD) != 1 or section.count(SOLVED_SAVE) != 1:
        raise ValueError('setupReview 푼 문제 저장 구조 불일치')
    section = section.replace(SOLVED_LOAD, "new Set([].filter(")
    return section.replace(SOLVED_SAVE, "          " + SOLVED_MARK + "\n")


def install(source: str, document_id: str) -> str:
    source = patch_review_shell(source)
    source = patch_pager_shell(source)
    model = build_model(source, document_id)
    if model['errors']:
        raise ValueError(json.dumps(model['errors'], ensure_ascii=False))
    if source.count('</body>') != 1:
        raise ValueError('body 종료 태그는 하나여야 함')
    payload = json.dumps(model, ensure_ascii=False, sort_keys=True).replace('<', '\\u003c')
    css = (SKILL / 'assets/review-interaction.css').read_text(encoding='utf-8')
    js = ((SKILL / 'assets/review-prompt.js').read_text(encoding='utf-8') + '\n'
          + (SKILL / 'assets/review-interaction.js').read_text(encoding='utf-8'))
    boot = """(function () {
      const prompt = ReviewPrompt;
      const openDialog = prompt.openPromptDialog;
      prompt.openPromptDialog = (doc, record, onCopied) => {
        openDialog(doc, record, onCopied);
        const dialog = doc.querySelector('dialog.review-prompt-dialog[open]');
        const button = dialog.querySelector('.review-prompt-actions .btn-primary');
        button.addEventListener('click', async event => {
          event.stopImmediatePropagation();
          const text = prompt.buildReviewPrompt(record)
            .replace('# 생명과학 복기 요청', '# 머신러닝기초 복기 요청')
            .replace('너는 내 생명과학 튜터야.', '너는 내 머신러닝기초 튜터야.')
            .replace('내가 방금 푼 복습문제(', '내가 방금 푼 확인문제(');
          button.disabled = true;
          const copied = await prompt.copyText(doc.defaultView, text, dialog);
          button.disabled = false;
          if (copied) {
            dialog.close();
            onCopied();
          } else if (dialog.open) {
            dialog.querySelector('[role="status"]').textContent =
              'Ctrl+C(⌘C)로 복사해 AI 채팅에 붙여 넣으세요.';
            const area = dialog.querySelector('textarea');
            area.hidden = false;
            area.value = text;
            area.focus();
            area.select();
          }
        }, {capture: true});
      };
      function start() {
        try {
          const storage = null;
          ReviewInteraction.mount(document, JSON.parse(document.getElementById('review-interaction-model').textContent), storage);
        } catch (error) { console.warn('복습문제 상호작용 초기화 실패:', error); }
      }
      if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once:true});
      else start();
    })();"""
    block = (START + '\n<style>\n' + css + '\n</style>\n'
             + '<script id="review-interaction-model" type="application/json">' + payload + '</script>\n'
             + '<script>\n' + js + '\n</script>\n<script>' + boot + '</script>\n' + END + '\n')
    return source.replace('</body>', block + '</body>')
