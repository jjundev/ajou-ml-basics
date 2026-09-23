---
name: ml-review-pack
description: 머신러닝기초 수업의 STT·강의노트·MML 교과서로 ELI5 정리노트 HTML과 교과서 기반 복습문제 HTML(+MD, 그림)을 만들어 복습노트/에 저장한다. "정리노트", "복습문제", "복습팩", "0921~0923 정리해줘"처럼 머신러닝기초 수업 정리를 요청하거나 /ml-review-pack [MMDD|MMDD-MMDD] [lite]로 부를 때 사용한다.
---

# 머신러닝기초 복습팩

수업 녹음 전사(STT)와 강의자료, MML 교과서로 한 기간의 복습팩을 만든다. 중간에 사용자에게 묻지 않고 끝에 한 번 보고한다. 커밋은 제안만 한다.

**산출물** (`복습노트/`):
`정리노트_<range>_<slug>.html`, `복습문제_<range>_<slug>.html`, 같은 이름의 `.md` 두 개, `figures_<range>/`

**인자**: `[MMDD | MMDD-MMDD] [lite]`
- `lite`: 작성자·요약 에이전트를 sonnet으로, 6단계 리뷰를 생략한다. 기계 검사와 브라우저 검사는 그대로 한다.

**진행 표시**: 단계마다 한 줄만 쓴다. 예: `3/9 작성 중: 섹션 5개 + 카드 10개 (병렬)`

**경로 약속**
- `SKILL` = 이 파일이 있는 폴더(`.claude/skills/ml-review-pack`)의 절대 경로
- `REPO` = 저장소 루트
- `RUN` = `<scratchpad>/review-pack/<range>/`
- 셸 상태는 Bash 호출 사이에 이어지지 않는다. 아래 명령의 `$SKILL`, `$RUN`, `$REPO`는 실행할 때마다 실제 절대 경로로 바꿔 쓰거나, 같은 명령 앞에 `SKILL=… RUN=… REPO=…`를 붙여 설정한다. `cd`는 쓰지 않고 파일도 절대 경로로 넘긴다.

## 절차

### 0. 준비
1. `REPO`에 `STT/`, `강의노트/`, `교과서/Mathematics_for_Machine_Learning.pdf`가 모두 있는지 확인한다. 하나라도 없으면 "머신러닝기초 저장소에서만 동작합니다"라고 알리고 멈춘다.
2. STT 목록은 NFC로 읽는다. macOS에는 NFD 파일명이 섞여 있다.
   ```bash
   python3 -c "import os,unicodedata as u,re;n=[u.normalize('NFC',f) for f in os.listdir('$REPO/STT')];print(sorted(m.group(1) for f in n if f.endswith('머러기.md') and (m:=re.match(r'(\d{4})',f))))"
   ```
3. 기간을 정한다.
   - 인자가 있으면 그 기간을 쓴다.
   - 인자가 없으면 `복습노트/정리노트_<range>_*.html` 중 가장 늦은 끝 날짜를 찾고, 그 뒤의 STT를 모두 쓴다. `정리노트_*`가 하나도 없으면 STT 전부를 쓴다.
   - 해당 STT가 하나도 없으면 사용 가능한 날짜를 보여 주고 멈춘다.
   - `range`는 첫 STT 날짜 하나이거나 `첫-끝` 형식이다.
4. 실행 폴더를 만든다. 서브에이전트에게는 `RUN`, `RUN/repo`, `SKILL` 경로만 넘긴다.
   ```bash
   mkdir -p "$RUN"/{summaries,sections,cards} && ln -sfn "$REPO" "$RUN/repo"
   ```
   에이전트는 `RUN` 밖에 쓰지 않는다. `복습노트/`에는 메인 에이전트만 쓴다.

### 1. 범위 파악
1. **먼저** 관련 `강의노트/Lecture*.pdf` 텍스트를 슬라이드 번호와 함께 `RUN/slides.txt`에 추출한다(PyMuPDF, 쪽마다 `=== LXX sN ===`, 몇 초면 끝난다). 요약 에이전트는 이 파일이 있다고 보고 시작하므로 추출이 끝난 뒤에 띄운다.
   - 관련 PDF: 이전 팩(`복습노트/정리노트_*`)이 끝까지 다루지 않은 Lecture PDF 전부. 확실하지 않으면 넉넉히 넣는다.
   - 추출에 실패하면 STT만으로 진행하고 보고서에 적는다(브리프의 `slides.txt` 줄은 "없음"으로 바꿔 넘긴다).
2. 그다음 STT 날짜마다 요약 에이전트 1명을 **병렬로** 띄운다. 브리프는 `references/stt-summary-prompt.md`에 있다.
   - `<LectureXX_*.pdf>`: 그 날짜가 다룬 슬라이드가 들어 있는 PDF(`slides.txt`와 이전 팩의 범위로 판단). 확실하지 않으면 1의 관련 PDF를 모두 적는다.
   - `<YYYY-MM-DD>`: 연도는 이번 학기 연도(오늘 날짜 기준), 월·일은 `<MMDD>`.
3. 에이전트가 도는 동안 메인 에이전트는 MML에서 관련 장과 Example·연습문제 위치를 찾는다(`references/problem-selection.md`의 스니펫).

### 2. manifest
- 요약들의 슬라이드 대조표와 용어·식 목록으로 `RUN/manifest.json`을 쓴다. 규칙은 `references/manifest-guide.md`에 있다.
- 문제 선별은 `references/problem-selection.md`를 따른다.
  - 정답은 `RUN/answers.py`(`fractions`)로 계산한다.
  - 문제별 교과서 쪽은 `RUN/problem-pages.txt`에 적는다.
- 검증: `python3 "$SKILL/scripts/manifest.py" "$RUN/manifest.json"` 결과가 `OK`여야 한다.

### 3. 작성
- 섹션마다 작성자 1명을 띄운다. 브리프는 `references/content-rules.md`, 위젯 규칙은 `references/widget-rules.md`에 있다.
- 문제 작성자 1명이 모든 카드를 쓴다. 브리프는 `references/card-rules.md`에 있다.
- 모두 **한 메시지에서 병렬로** 띄운다. 모델은 opus, `lite`이면 sonnet이다.
- 브리프의 `<…>` 자리는 실제 경로, id, 금지어 목록(`<forbidden 목록>`), 예고 토픽 id(`<preview_topic>`), 그리고 섹션 작성자에게는 manifest `links` 중 그 섹션 토픽에 속한 것만(`<이 섹션의 links 목록>`) 채워 넣는다.

### 4. 조립
- **처음 조립할 때만**: `복습노트/`에 이번 `range`의 산출물(`정리노트_<range>_*`, `복습문제_<range>_*`의 `.html`·`.md`, `figures_<range>/`)이 하나라도 있으면 먼저 백업한다. 다시 조립할 때(5~8단계에서 돌아온 경우)는 백업하지 않는다. 이미 스킬이 만든 초안이 백업을 덮어쓰기 때문이다.
  ```bash
  mkdir -p "$RUN/previous" && find "$REPO/복습노트" -maxdepth 1 \( -name '정리노트_<range>_*' -o -name '복습문제_<range>_*' -o -name 'figures_<range>' \) -exec cp -R {} "$RUN/previous/" \; && ls "$RUN/previous"
  ```
```bash
python3 "$SKILL/scripts/assemble.py" --run "$RUN" --out "$REPO/복습노트"
```

### 5. 기계 검사
```bash
python3 "$SKILL/scripts/check_html.py" --manifest "$RUN/manifest.json" --note "$REPO/복습노트/<정리노트>.html" --review "$REPO/복습노트/<복습문제>.html"
```
- `FAIL`이면 Problem의 `where`(토픽 id, 카드 id, 섹션 id)로 담당 작성자를 찾는다.
- 그 작성자에게 문제 목록을 보내 조각을 고치게 한다(SendMessage, 안 되면 같은 브리프로 새 에이전트).
- 고친 뒤 4단계부터 다시 한다. 최대 2회까지이며, 그래도 남으면 "미해결"로 보고한다.

### 6. 리뷰 (`lite`면 생략)
- 리뷰어 1명을 띄운다. 브리프는 `references/review-prompt.md`에 있다.
- Critical과 Important는 모두, Minor는 쉬운 것만 고친다.
- 담당 작성자별로 **한 번에 모아서** 수정을 요청한다. 수정은 한 번만 한다.
- 수정 후 4~5단계를 다시 한다. 반영하지 않은 항목은 보고서에 적는다.

### 7. 브라우저 검증
- `references/browser-check.md`대로 한다.
  - http.server를 빈 포트에 띄운다.
  - 확인: KaTeX 오류 0, 남은 `$` 없음, 375px에서 가로 스크롤 없음, 다크모드, 위젯, 링크, 콘솔 오류
- 결함은 5단계와 같은 방식으로 작성자에게 되돌린다. 이것도 최대 2회 규칙에 포함된다.
- 끝나면 서버를 종료한다.

### 8. MD 변환
```bash
python3 "$SKILL/scripts/html2md.py" "$REPO/복습노트/<정리노트>.html" "$REPO/복습노트/<복습문제>.html" --check
```
- `OK`가 나와야 한다.
- 누락이 나오면 대부분 HTML 조각의 마크업 문제다(수식이 `svg`나 `.controls` 안에 있는 경우 등). 조각을 고치고 4단계부터 다시 한다.

### 9. 보고
다음 형식으로 끝낸다.
```
## 복습팩 <range> 완료
- 파일: 복습노트/… (html 2, md 2, figures_<range>/ N개)
- 범위: 배운 슬라이드 … / 예고만: …
- 문제: P1 MML Example 9.1 변형(★) … (정답은 RUN/answers.py로 검증)
- 스킬이 정한 사항: slug, 섹션 구성, 위젯, 뺀 내용과 이유
- 미해결: … (없으면 "없음")
- 커밋 제안: git add 복습노트/<파일들> && git commit -m "docs(notes): add review pack <range>"
```
실행 폴더 경로(`RUN`)도 적는다. 수정이 필요하면 조각을 고쳐 4단계부터 다시 돌리면 된다.

## 오류 처리
| 상황 | 동작 |
|---|---|
| 저장소가 아님 | 알리고 멈춤 |
| 기간에 해당하는 STT 없음 | 사용 가능한 날짜를 보여 주고 멈춤 |
| PDF 텍스트 추출 실패 | STT만으로 진행하고 보고서에 표시 |
| 포트 사용 중 | 다른 빈 포트 사용 |
| 같은 range의 팩이 이미 있음 | 4단계 첫 조립 전에 기존 html·md·`figures_<range>/`를 `RUN/previous/`에 복사하고(다시 조립할 때는 복사하지 않음) 보고서에 적음 |
| 검사 2회 실패 | 멈추지 않고 나머지 단계를 끝낸 뒤 "미해결"로 보고 |
