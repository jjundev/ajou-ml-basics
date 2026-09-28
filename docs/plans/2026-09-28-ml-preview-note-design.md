# 머신러닝기초 예습노트 스킬 (`ml-preview-note`) 설계

2026-09-28 · grill-yourself 세션에서 확정

## 의도
다음 강의의 **강의노트 PDF + MML 교과서**로, 수업을 들으면서 옆에 띄워 둘 **짧은 예습노트 HTML(+MD)**을 만드는 별도 스킬. 양식(한 화면 페이저, 좌우 패널, 다크모드, KaTeX)은 `ml-review-pack`과 같고 템플릿은 심링크로 공유한다. 문제는 만들지 않는다. `/ml-preview-note L04` → `예습노트/L04/예습노트_L04_<slug>.html`이 생기고, 토픽마다 슬라이드 번호가 붙어 수업 중 현재 슬라이드를 바로 찾을 수 있으면 완료.

분류: architectural — 새 스킬 진입점, 새 manifest 스키마, 조립·검사 래퍼, 공유 템플릿 인터페이스(슬롯) 추가.

## 완성 후 동작
- `/ml-preview-note [Lxx] [lite]`.
  - 인자가 있으면 그 Lecture.
  - 인자가 없으면 **번호가 가장 큰 Lecture PDF**. 그 Lecture의 예습노트가 이미 있으면 "새 강의노트가 올라왔는지 ajou-bb로 확인하세요"라고 알리고 멈춘다(지난 강의로 조용히 내려가지 않는다).
  - 같은 번호에 `_rev` PDF가 있으면 그것을 쓴다. slug는 `_rev`를 뺀 이름.
- 결과: `예습노트/<Lxx>/예습노트_<Lxx>_<slug>.html`, 같은 이름 `.md`, `figures_<Lxx>/`.
- 화면
  - 상단 브랜드 "예습노트", 페이지 제목 `머신러닝기초 예습노트 <Lxx>`.
  - 토픽 = 슬라이드 1~3장, 태그 `<Lxx> s12–14`, **슬라이드 순서 그대로**.
  - 레이어 3개: 쉽게 말하면(`eli5`, 2문장 이하, 그림은 필요할 때만) · 정확히 말하면(`formal`, 핵심 식 + 기호 뜻) · 들을 때 포인트(`listen`, 항목 2개 이하).
  - 교과서에서 보충한 내용은 `layer supp` + 배지 "교과서 보충".
  - 첫 섹션 `s0` "미리 알아둘 것"(선수지식, MML 쪽), 마지막 섹션 "한눈에 보기"(`-cheatsheet`, `-links`).
  - 분량: 토픽당 본문 600자 이하(공백·TeX·그림·레이어 제목·요약 패널 제외).
- 실패: Lecture PDF 없음 → 사용 가능 목록 + ajou-bb 안내 후 멈춤. 같은 Lecture 예습노트가 있으면 `RUN/previous-*`에 백업 후 덮어씀.

## 이번 라운드에서 제외
- 복습팩 → 예습노트 자동 링크(복습 스킬 변경이 커짐)
- ajou-bb 자동 다운로드(외부 로그인 작업)
- 위젯(0개 고정)
- 교수님 말씀/꼭 기억해요 레이어(STT 근거 없음)

## 접근: A — 템플릿 심링크 + 복습 스킬 모듈을 import하는 얇은 래퍼
- 공유: `assets/note-template.html`(상대 심링크), 복습 스킬 `scripts/`의 `manifest`(도우미), `assemble`(`fill`/`split_scripts`/`esc`), `check_html`(`check_common`/`check_note`), `html2md`(`convert`/`check_md`/`Ctx`).
- `html2md.py`는 심링크하지 않고 import한다. `NAME_RE`와 `convert_pack`이 정리노트·복습문제 쌍을 강제하기 때문(`html2md.py:26,614`).
- `assemble.read_fragment`는 쓰지 않는다. `review_name`을 부르기 때문(`assemble.py:54`).

## 공유 템플릿 변경(복습 스킬, 추가만)
1. `note-template.html:324` `<strong class="brand">정리노트</strong>` → `{{BRAND}}`, 복습 `build_note`가 `"BRAND": "정리노트"`를 넘긴다.
2. `.layer.listen`: `.layer.warn`과 같은 박스 스타일, 제목 색 `--accent-ink`.

## 확정 결정
| # | 결정 | 답 |
|---|---|---|
| 0 | 접근 | A |
| 1 | 스킬 이름 | `ml-preview-note` |
| 2 | 범위 단위 | Lecture 번호 `L\d{2}` |
| 3 | 브랜드 | `{{BRAND}}` 슬롯 |
| 4 | 조립 | 자체 조립, 공용 함수 import |
| 5 | MD | `convert`/`check_md` 직접 호출 |
| 6 | 레이어 | eli5 · formal · listen (+supp) |
| 7 | listen 스타일 | `.layer.warn` 규칙 공유 |
| 8 | 위젯 | 0개 |
| 9 | 토픽 순서 | 슬라이드 순서 |
| 10 | `.sum` 패널 | 유지 |
| 11 | 출력 위치 | `예습노트/<Lxx>/` [confirmed] |
| 12 | 분량 | 600자 / eli5 2문장 / listen 2항목 [confirmed] |
| 13 | 리뷰어 | 기본 켬, `lite`에서 끔 [confirmed] |
| 14 | MD 출력 | 만듦 [confirmed] |

## 구현 중 구체화한 점
- 기본 Lecture 선택 규칙: "예습노트가 없는 Lecture 중 가장 큰 번호" 대신 "가장 큰 번호, 이미 있으면 멈춤"으로 구체화했다. 전자는 최신 강의가 끝난 뒤 지난 강의를 고르게 된다.
- 스크립트는 `preview.py` 하나 대신 책임별 모듈로 나눈다: `preview_manifest.py`, `preview_files.py`(선택·백업), `preview_assemble.py`, `preview_check.py`, `preview_md.py`, `_review.py`(import 경로).
- 백업은 SKILL.md 스니펫 대신 `preview_files.py backup`으로 두어 테스트한다.
