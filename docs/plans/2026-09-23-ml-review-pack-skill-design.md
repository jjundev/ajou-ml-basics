# 머신러닝기초 복습팩 스킬 `ml-review-pack` — 설계

> 2026-09-23 grill-yourself 세션 산출물. Needs-you #1, #16, #17, #18은 사용자가 확정했다.
> 선례: 0909~0916 복습팩(`docs/plans/2026-09-21-lecture-notes-review-html*.md`, 결과물 `복습노트/`).

## Intent
머신러닝기초 저장소 전용 프로젝트 스킬이다. 지정한 기간의 수업 자료를 읽고 복습팩을 호출 한 번으로 만든다.
- 입력: `STT/MMDD 머러기.md`, `강의노트/Lecture*.pdf`, MML 교과서(`교과서/Mathematics_for_Machine_Learning.pdf`, `교과서/연습문제/`)
- 출력: ELI5 정리노트 HTML, 교과서 기반 복습문제 HTML, 두 파일의 MD 버전, `figures_<range>/`의 SVG. 모두 `복습노트/`에 저장한다.

0909~0916 팩과 같은 품질이 나오고, 매주 grill → plan → SDD를 반복할 필요가 없어지면 완료다.

Classification: architectural. 스킬, 도구, 템플릿을 모두 새로 만든다.

## Behavior when done
- 호출 방법: `/ml-review-pack [MMDD | MMDD-MMDD] [lite]` 또는 "0921~0923 정리노트랑 복습문제 만들어줘".
- 기간을 생략하면 `복습노트/`에 있는 마지막 팩의 끝 날짜 이후 STT를 모두 쓴다. 해당 STT가 없으면 사용 가능한 날짜를 보여 주고 멈춘다.
- 진행 중에는 단계마다 한 줄 상태만 보여 준다. 중간에 사용자에게 확인을 받지 않는다(#18).
- 끝나면 다음을 보고한다.
  - 생성된 파일
  - 수업 범위: 배운 슬라이드와 예고만 한 슬라이드
  - 문제 목록과 각 출처
  - 스킬이 직접 정한 사항
  - 미해결 항목
- 커밋은 하지 않고 제안만 한다. 두 번 수정해도 검증에 실패한 항목은 "미해결"로 보고한다.
- 저장소가 아닌 곳에서 호출하면 오류를 내고 멈춘다.

## Not in this round
- 다른 과목 지원(#1)과 교과서가 없을 때의 문제 출처 대체 규칙(#16)
- 머신러닝기초 저장소의 잔여 문제: 기존 팩의 추가강의 링크, `tests/test_notes_html.py` 경로
- STT 생성: `audio-stt` 스킬이 담당한다.
- 결정론적 렌더러(C안), 블랙보드 업로드, PDF 인쇄

## Approaches
| Option | Approach | Pro | Con | Chosen |
|---|---|---|---|---|
| A | SKILL.md만 두고 도구는 매번 새로 만듦 | 가볍다 | 매번 검사기와 변환기를 다시 만들고 품질이 흔들린다 | — |
| B | 절차 + 범용 스크립트 + 템플릿·규칙. 본문은 에이전트가 작성 | 검증된 도구를 재사용하고 내용은 자유롭게 쓴다 | 작성 품질은 여전히 에이전트에 달려 있다 | ✔ |
| C | JSON 콘텐츠 모델 + 결정론적 렌더러 | 형식이 완벽히 일정하다 | 그림·유도·비유를 JSON으로 표현하기 어렵다 | — |

## Implementation spec
위치: `.claude/skills/ml-review-pack/` (프로젝트 스킬, git으로 관리)

```
SKILL.md                      절차(0~9단계), 인자, 오류 처리, 보고 형식
references/
  stt-summary-prompt.md       STT 요약 에이전트 지시문
  manifest-guide.md           manifest.json 작성 규칙과 스키마
  content-rules.md            섹션 작성자 브리프 + 토픽 4층 마크업 + 문체 + SVG 규칙
  widget-rules.md             위젯 마크업 + .widget-static 정적 대체물 필수
  problem-selection.md        MML 문제 선별 규칙과 위치 찾기
  card-rules.md               문제 작성자 브리프 + 카드 마크업
  review-prompt.md            리뷰어 지시문
  browser-check.md            브라우저 검증 스크립트
assets/note-template.html, review-template.html   0909~0916 CSS·뼈대 + 슬롯
scripts/manifest.py           manifest 로드·검증 (CLI)
scripts/assemble.py           manifest + 조각 → HTML 2개
scripts/check_html.py         공통 검사 + manifest 계약 검사
scripts/html2md.py            HTML 2개 → MD 2개 + figures, --check로 누락 검사
tests/                        unittest, 미니 픽스처, 0909~0916 회귀
```

**실행 폴더**: `<scratchpad>/review-pack/<range>/`
- `repo`: 저장소를 가리키는 ASCII 심볼릭 링크
- `manifest.json`, `summaries/stt-MMDD.md`, `sections/<sid>.html`, `cards/<pid>.html`

과목 저장소에는 결과물만 남는다.

**파이프라인**
0. 준비: 저장소를 확인하고, NFC로 STT 목록을 만들어 기간을 정한 뒤 실행 폴더를 만든다.
1. 범위 파악: STT마다 요약 에이전트를 병렬로 돌린다. 메인 에이전트는 슬라이드 텍스트와 MML 위치를 추출한다.
2. manifest 작성: 메인 에이전트가 쓴다. 정답은 Python `fractions`로 계산하고 `manifest.py`로 검증한다.
3. 작성: 섹션 작성자를 병렬로 돌리고, 문제 작성자 1명이 카드를 쓴다. 품질 모드는 opus, `lite`는 sonnet(#17).
4. `assemble.py`로 두 HTML을 조립한다.
5. `check_html.py --manifest`로 검사한다. 실패하면 해당 작성자에게 되돌리며 최대 2회까지 한다.
6. 리뷰어 1명이 검토하고 수정은 한 번에 모아서 한다. `lite`에서는 생략한다.
7. 메인 에이전트가 브라우저로 검증한다.
   - http.server를 빈 포트에 띄운다.
   - KaTeX 오류 0, 남은 `$` 없음, 375px에서 가로 스크롤 없음
   - 다크모드, 위젯, 링크
8. `html2md.py --check`를 실행한다.
9. 보고한다.

**테스트**
- 스크립트 단위 테스트
- 0909~0916 회귀 테스트: 계약 검사와 MD 누락 0
- 압력 테스트: 예고 내용 미포함, 자작 문제 금지
- 인수 실행: 0921 STT로 실제 팩 생성

## Decisions
### Confident
| # | Decision | Answer |
|---|---|---|
| 0 | 접근 | B |
| 2 | 스킬 개수 | 한 스킬에 노트, 문제, MD를 모두 포함 |
| 3 | 위치와 이름 | 프로젝트 스킬 `.claude/skills/ml-review-pack/` |
| 4 | 입력 | 고정 경로. 기간을 생략하면 마지막 팩 이후 |
| 5 | 출력 | `복습노트/{정리노트,복습문제}_<range>_<slug>.{html,md}`, `복습노트/figures_<range>/` |
| 6 | 범위 | STT로 확인된 범위만 본문에 넣고, 예고는 제목만 |
| 7 | 문제 출처 | MML만 사용. Part II 장은 Example 변형 + 관련 Part I 연습문제. 자작 금지 |
| 8 | 작성 방식 | 조각 파일 병렬 작성 → assemble |
| 9 | 파일 배치 | 도구는 스킬에, manifest와 조각은 실행 폴더에 |
| 10 | 검증 계층 | 기계 검사 → 리뷰 1회 → 브라우저 → MD 검사 |
| 11 | MD 생성 | 항상 생성. 위젯은 `.widget-static`으로 대체 |
| 12 | 템플릿 | 0909~0916의 CSS와 뼈대 |
| 13 | 커밋 | 자동 커밋 없음 |
| 14 | 경로 처리 | ASCII 링크와 NFC 비교 |
| 15 | 테스트 | 스킬 자체 테스트 |

### Needs you (확정됨)
| # | Decision | Value |
|---|---|---|
| 1 | 적용 범위 | [confirmed] 머신러닝기초 전용 |
| 16 | 교과서 없을 때 | [confirmed] 해당 없음(머신러닝기초만 사용) |
| 17 | 품질·비용 | [confirmed] 품질 우선 + `lite` 옵션 |
| 18 | 중간 확인 | [confirmed] 없음, 끝에 보고 |
