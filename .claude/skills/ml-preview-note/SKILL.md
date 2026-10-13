---
name: ml-preview-note
description: 머신러닝기초 다음 강의의 강의노트 PDF와 MML 교과서로, 수업 중 옆에 띄워 둘 짧은 예습노트 HTML(+MD, 그림)을 만들어 예습노트/<Lxx>/ 폴더에 저장한다. 문제는 만들지 않는다. "예습노트", "예습", "다음 강의 미리 보기", "L04 예습해줘"처럼 수업 전 준비를 요청하거나 /ml-preview-note [Lxx] [lite]로 부를 때 사용한다.
---

# 머신러닝기초 예습노트

강의노트 PDF와 MML 교과서로 Lecture 하나의 예습노트를 만든다. 수업을 들으면서 옆에 띄워 두는 용도라 **짧게** 쓰고, 토픽 순서는 **슬라이드 순서 그대로**다. 문제는 만들지 않는다. 양식은 `ml-review-pack` 정리노트와 같다(`assets/note-template.html`은 그 템플릿의 심링크). 중간에 사용자에게 묻지 않고 끝에 한 번 보고한다. 커밋은 제안만 한다.

**산출물** (`예습노트/<Lxx>/`): `예습노트_<Lxx>_<slug>.html`, 같은 이름 `.md`, `figures_<Lxx>/`

**인자**: `[Lxx] [lite]`
- `Lxx`가 없으면 번호가 가장 큰 Lecture PDF. 그 예습노트가 이미 있으면 멈추고 알린다. `l03`, `L3`, `3`도 `L03`으로 받는다.
- `lite`: 작성자와 6단계 리뷰어를 sonnet(GPT이면 luna)으로 돌린다. 리뷰는 생략하지 않는다(검사기가 못 잡는 사실 오류·문장 문제를 잡는 유일한 단계라서). 기계 검사와 브라우저 검사도 그대로 한다.

**진행 표시**: 단계마다 한 줄, `<단계 번호>/9`(단계는 0~9). 예: `3/9 작성 중: 섹션 4개 (병렬)`

**경로 약속**
- `SKILL` = 이 파일이 있는 폴더(`.claude/skills/ml-preview-note`)의 절대 경로
- `REPO` = 저장소 루트
- `RUN` = `<scratchpad>/preview-note/<Lxx>/`
- 셸 상태는 Bash 호출 사이에 이어지지 않는다. `$SKILL`, `$RUN`, `$REPO`, `$LEC`는 실행할 때마다 실제 값으로 바꿔 쓰거나 같은 명령 앞에 붙여 설정한다. `cd`는 쓰지 않는다.

## 절차

### 0. 준비
1. `REPO`에 `강의노트/`와 `교과서/Mathematics_for_Machine_Learning.pdf`가 있는지 확인한다. 없으면 "머신러닝기초 저장소에서만 동작합니다"라고 알리고 멈춘다.
2. Lecture를 고른다.
   ```bash
   python3 "$SKILL/scripts/preview_files.py" pick --repo "$REPO" [--lecture Lxx]
   ```
   출력은 `Lxx<TAB>PDF 경로<TAB>slug`. 종료 코드가 1이면 표준에러 메시지(사용 가능 목록, ajou-bb 안내)를 그대로 보여 주고 멈춘다.
3. 실행 폴더를 만든다. 서브에이전트에게는 `RUN`, `RUN/repo`, `SKILL` 경로만 넘긴다.
   ```bash
   rm -rf "$RUN/sections" "$RUN/work" && mkdir -p "$RUN"/{sections,work} && ln -sfn "$REPO" "$RUN/repo"
   ```
   같은 세션에서 다시 실행해도 이전 실행의 조각이 섞이지 않게 `sections/`와 `work/`를 비우고 시작한다(`RUN` 아래 scratch 폴더만 지운다). 에이전트는 `RUN` 밖에 쓰지 않는다. 임시 파일은 `RUN/work/`에만 둔다. `예습노트/`에는 메인 에이전트만 쓴다.

### 1. 자료 파악
1. 슬라이드 텍스트를 슬라이드 번호와 함께 `RUN/slides.txt`로 뽑는다.
   ```bash
   LEC=<Lxx> PDF=<PDF 경로> RUN=… python3 - <<'EOF'
   import fitz, os
   d = fitz.open(os.environ["PDF"])
   with open(os.path.join(os.environ["RUN"], "slides.txt"), "w", encoding="utf-8") as f:
       for i, page in enumerate(d, 1):
           f.write(f"=== {os.environ['LEC']} s{i} ===\n{page.get_text()}\n")
   print(len(d), "slides")
   EOF
   ```
   추출에 실패하면 PDF를 Read 도구로 직접 읽고, 보고서에 적는다.
2. `slides.txt`를 끝까지 읽고 슬라이드를 개념 단위(1~3장)로 묶는다.
3. MML에서 관련 장과 쪽을 찾는다. `keys`는 슬라이드 핵심어(영어 소문자)로 바꾼다. 출력 숫자가 링크 `#page=N`의 N이다.
   ```bash
   REPO=… python3 - <<'EOF'
   import fitz, os
   d = fitz.open(os.path.join(os.environ["REPO"], "교과서/Mathematics_for_Machine_Learning.pdf"))
   keys = ["linear regression", "least-squares", "maximum likelihood"]
   for i, p in enumerate(d):
       hit = [k for k in keys if k in p.get_text().lower()]
       if len(hit) >= 2:
           print(i + 1, hit)
   EOF
   ```
4. 이전 복습노트(`복습노트/*/.pack/정리노트_*.md`, MD는 날짜 폴더의 `.pack/` 아래에 있다)에서 이 강의가 기대는 개념을 찾아 둔다("미리 알아둘 것"과 링크에 쓴다).

### 2. manifest
- `RUN/manifest.json`을 쓴다. 규칙은 `references/manifest-guide.md`.
- 검증: `python3 "$SKILL/scripts/preview_manifest.py" "$RUN/manifest.json"` → `OK`

### 3. 작성
- 섹션마다 작성자 1명을 **한 메시지에서 병렬로** 띄운다. 브리프는 `references/content-rules.md`.
- 모델은 opus, `lite`이면 sonnet. GPT이면 opus 대신 sol, sonnet 대신 luna. 리뷰어도 같은 규칙이다.
- 브리프의 `<…>` 자리에 실제 경로, 섹션 id·제목, 그 섹션 토픽의 `links` 목록, MML 쪽 번호를 채운다.

### 4. 조립
- **처음 조립할 때만** 기존 예습노트를 백업한다(다시 조립할 때는 하지 않는다. 스킬이 만든 초안이 백업에 섞이기 때문이다).
  ```bash
  python3 "$SKILL/scripts/preview_files.py" backup --repo "$REPO" --lecture <Lxx> --run "$RUN"
  ```
  종료 코드가 1이면 조립하지 말고 원인을 고친다. 조립기가 "다른 slug의 예습노트가 남아 있어요" 경고를 내면 지우지 말고 보고서 "미해결"에 적는다(사용자가 정한다).
- 조립:
  ```bash
  python3 "$SKILL/scripts/preview_assemble.py" --run "$RUN" --out "$REPO/예습노트/<Lxx>"
  ```

### 5. 기계 검사
```bash
python3 "$SKILL/scripts/preview_check.py" --manifest "$RUN/manifest.json" --note "$REPO/예습노트/<Lxx>/<예습노트>.html"
```
- `FAIL`이면 Problem의 `where`(토픽·섹션 id)로 담당 작성자를 찾아 문제 목록을 보낸다(SendMessage, 안 되면 같은 브리프로 새 에이전트).
- `topic-long`·`eli5-long`·`listen-long`은 "줄여 주세요"로 보낸다. 내용을 다른 토픽으로 옮기지 말고 덜 중요한 문장을 뺀다.
- 고친 뒤 4단계(조립)부터 다시 한다. 최대 2회, 그래도 남으면 "미해결"로 보고한다.

### 6. 리뷰 (`lite`면 sonnet)
- 리뷰어 1명. 브리프는 `references/review-prompt.md`.
- Critical·Important는 모두, Minor는 쉬운 것만 고친다. 작성자별로 한 번에 모아 한 번만 수정 요청한다. 수정 후 4~5단계를 다시 한다.

### 7. 브라우저 검증
- `references/browser-check.md`대로 한다(KaTeX 오류 0, 남은 `$` 없음, 720px·375px 가로 넘침 없음, 720px에서 토픽 한 화면, 다크모드, 콘솔 오류).
- 결함은 5단계와 같은 방식으로 되돌린다(최대 2회 규칙에 포함). 끝나면 서버를 종료한다.

### 8. MD 변환
```bash
python3 "$SKILL/scripts/preview_md.py" "$REPO/예습노트/<Lxx>/<예습노트>.html" --check
```
`OK`가 나와야 한다. 누락은 대부분 조각의 마크업 문제다. 조각을 고치고 4단계부터 다시 한다.

### 9. 보고
```
## 예습노트 <Lxx> 완료
- 파일: 예습노트/<Lxx>/… (html 1, md 1, figures_<Lxx>/ N개)
- 범위: <PDF 이름> s1–sN, 토픽 M개
- 스킬이 정한 사항: slug, 섹션 구성, 교과서 보충으로 넣은 것과 이유, 뺀 슬라이드와 이유
- 미해결: … (없으면 "없음")
- 커밋 제안: git add 예습노트/<Lxx> && git commit -m "docs(notes): add preview note <Lxx>"
```
실행 폴더 경로(`RUN`)와 백업 경로(있으면)도 적는다.

## 오류 처리
| 상황 | 동작 |
|---|---|
| 저장소가 아님 | 알리고 멈춤 |
| Lecture PDF 없음 / 최신 Lecture 예습노트가 이미 있음 | `pick` 메시지를 보여 주고 멈춤 |
| PDF 텍스트 추출 실패 | Read 도구로 PDF를 읽고 보고서에 표시 |
| 포트 사용 중 | 다른 빈 포트 사용 |
| 백업 실패 | 조립하지 않고 원인을 고침 |
| 검사 2회 실패 | 멈추지 않고 나머지 단계를 끝낸 뒤 "미해결"로 보고 |
