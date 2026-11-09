"""Validate the midterm scan transcript: 10 questions x 2 parts, scores sum to total, crops exist and are small."""
import json, sys
from pathlib import Path

def check(path):
    path = Path(path)
    data = json.loads(path.read_text(encoding='utf-8'))
    errors = []
    qs = data.get('questions', [])
    if len(qs) != 10:
        errors.append(f'questions: {len(qs)} != 10')
    parts = [p for q in qs for p in q.get('parts', [])]
    for q in qs:
        if [p.get('label') for p in q.get('parts', [])] != ['a', 'b']:
            errors.append(f"Q{q.get('n')}: parts must be a,b")
        crop = path.parent / q.get('crop', '')
        if not crop.is_file():
            errors.append(f"Q{q.get('n')}: missing crop {crop}")
        elif crop.stat().st_size > 600_000:
            errors.append(f"Q{q.get('n')}: crop too large {crop.stat().st_size}")
        for p in q.get('parts', []):
            for key in ('statement_tex', 'my_answer_tex'):
                if not str(p.get(key, '')).strip():
                    errors.append(f"Q{q.get('n')}{p.get('label')}: empty {key}")
            if not (0 <= p.get('score', -1) <= p.get('max', 0) == 5):
                errors.append(f"Q{q.get('n')}{p.get('label')}: bad score")
            if p.get('confidence') not in ('high', 'low'):
                errors.append(f"Q{q.get('n')}{p.get('label')}: confidence")
    total = sum(p.get('score', 0) for p in parts)
    if total != data.get('total') or total != 79:
        errors.append(f'score sum {total} vs total {data.get("total")} (expected 79)')
    if errors:
        print('FAIL\n' + '\n'.join(errors)); return 1
    print(f'OK {len(qs)} questions, {len(parts)} parts, {total} points'); return 0

if __name__ == '__main__':
    sys.exit(check(sys.argv[1]))
