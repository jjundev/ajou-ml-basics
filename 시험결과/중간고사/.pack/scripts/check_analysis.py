"""Validate 중간고사_오답분석.md: 20 per-part rows, lost points sum to 21 and match transcript, typed + evidenced."""
import json, re, sys
from pathlib import Path

TYPES = {'계산 실수', '요구사항 누락', '개념 오해', '표기·관례', '미완성', '전파'}

def check(md_path):
    md_path = Path(md_path)
    text = md_path.read_text(encoding='utf-8')
    transcript = json.loads((md_path.parent / '.pack/transcript.json').read_text(encoding='utf-8'))
    scores = {f"Q{q['n']}{p['label']}": p['score'] for q in transcript['questions'] for p in q['parts']}
    rows = [r for r in text.splitlines() if re.match(r'\|\s*Q\d+[ab]\s*\|', r)]
    errors = []
    if len(rows) != 20:
        errors.append(f'rows {len(rows)} != 20')
    lost_total = 0
    for r in rows:
        cells = [c.strip() for c in r.strip('|').split('|')]
        key, got, lost, kind = cells[0], cells[1], cells[2], cells[5]
        if key not in scores or int(got) != scores[key]:
            errors.append(f'{key}: 득점 {got} != transcript {scores.get(key)}')
        if int(lost) != 5 - int(got):
            errors.append(f'{key}: 감점 {lost} != 5-{got}')
        lost_total += int(lost)
        if int(lost) > 0:
            kinds = [k.strip().replace('(추정)', '').strip() for k in kind.split('+')]
            if not kinds or any(k not in TYPES for k in kinds):
                errors.append(f'{key}: 오류 유형 {kind!r}')
            if '.pack/scan/' not in r:
                errors.append(f'{key}: 근거 crop 링크 없음')
    if lost_total != 21:
        errors.append(f'감점 합 {lost_total} != 21')
    if errors:
        print('FAIL\n' + '\n'.join(errors)); return 1
    print(f'OK {len(rows)} rows, lost {lost_total}'); return 0

if __name__ == '__main__':
    sys.exit(check(sys.argv[1]))
