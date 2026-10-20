---
name: ml-review-pack
description: 머신러닝기초 수업의 STT·강의노트·MML 교과서로 ELI5 정리노트 HTML과 교과서 기반 복습문제 HTML(+MD, 그림)을 만들어 복습노트/<날짜>/ 폴더에 저장한다. "정리노트", "복습문제", "복습팩", "0921~0923 정리해줘"처럼 머신러닝기초 수업 정리를 요청하거나 /ml-review-pack [MMDD|MMDD-MMDD] [lite]로 부를 때 사용한다.
---

# 머신러닝기초 복습팩

수업 녹음 전사(STT)와 강의자료, MML 교과서로 한 기간의 복습팩을 만든다. 중간에 사용자에게 묻지 않고 끝에 한 번 보고한다. 커밋은 제안만 한다.

**산출물** (`복습노트/<range>/`, 수업 날짜마다 폴더 하나):
날짜 폴더 바로 아래에는 HTML만 둔다: `정리노트_<range>_<slug>.html`, `복습문제_<range>_<slug>.html`, `문제설명_<range>_<slug>.html`. 나머지는 모두 `.pack/` 하위 폴더에 둔다: 같은 이름의 `.md` 세 개, `figures_<range>/`, 문제설명 소유 자료, **`복습문제_<range>_<slug>-문제.pdf`와 `-답안.pdf`**. HTML은 `.pack/…`을 상대 경로로 링크하고, `.pack/` 안의 MD는 HTML을 `../`로 링크한다. 문제지/해설지는 동봉된 전자회로2 고정 템플릿으로 16:9 PDF를 만든다.

**인자**: `[MMDD | MMDD-MMDD] [lite]`
- `lite`: 작성자·요약 에이전트를 sonnet(GPT이면 luna)으로, 6단계 리뷰를 생략한다. 기계 검사와 브라우저 검사, PDF 쌍 생성·전체 페이지 검수는 그대로 한다. 배포 뒤 문제설명 전체 저작과 네 실제 검토도 생략하지 않는다.

**진행 표시**: 단계마다 한 줄만 쓴다. 예: `3/9 작성 중: 섹션 5개 + 카드 10개 (병렬)`

**경로 약속**
- `SKILL` = 이 파일이 있는 폴더(`.claude/skills/ml-review-pack`)의 절대 경로
- `REPO` = 저장소 루트
- `RUN` = `<scratchpad>/review-pack/<range>/`
- 셸 상태는 Bash 호출 사이에 이어지지 않는다. 아래 명령의 `$SKILL`, `$RUN`, `$REPO`는 실행할 때마다 실제 절대 경로로 바꿔 쓰거나, 같은 명령 앞에 `SKILL=… RUN=… REPO=…`를 붙여 설정한다. `cd`는 쓰지 않고 파일도 절대 경로로 넘긴다.

## 기존 정리노트 설명만 개선하는 경우
사용자가 큰 그림·개념 연결·기호 설명 등 기존 정리노트의 설명 개선을 요청하면 이 경로를 쓴다. 복습문제·답안 PDF·문제설명·영상의 내용이 바뀌지 않으면 전체 복습팩을 재생성하지 않는다.
1. `references/big-picture-first.md`를 읽고 대상 HTML·MD·기존 첫 토픽·연결을 확인한다. 기존 ID, 수식, 위젯, PDF·인터랙티브 링크를 보존한다.
2. 원자료와 기존 설명을 대조해 도입·유도 연결을 작성한다. `big-picture-first.md`의 전체 연결·출발식·변경점·단계별 연산·결과 재사용·복원 요약을 필요한 개념 묶음에 적용한다. 일반 공식의 실제 대입과 수업 관례를 보이고 수업 공식·동치 재표현·보충을 구분한다. 대상 HTML과 모든 대응 MD를 RUN에 백업하고 stage에서 수정한다. 큰 그림이 이미 있으면 중복 토픽 대신 기존 도입을 보강한다.
3. `python3 SKILL/scripts/check_learning_map.py <정리노트 HTML...>`와 `check_html.py`를 실행한다. MD의 새 설명·수식·링크가 HTML과 대응하는지 확인한다. 첫 도입과 수정한 유도를 실제로 읽고 레퍼런스의 검토 질문에 답한다.
4. 375px·데스크톱, 두 테마에서 도입의 실제 가시성·수식·줄바꿈·목차·화면 이동·기존 링크를 확인하고 검증된 HTML·MD만 함께 반영한다. 실패하면 해당 노트는 기존 파일을 보존한다.
5. 변경 날짜, 설명의 차이, 검사 결과, 백업·RUN과 미해결을 보고한다. PDF와 문제의 재검증을 이번 설명 수정의 검증인 것처럼 보고하지 않는다.

## 절차

### 0. 준비
1. `REPO`에 `STT/`, `강의노트/`, `교과서/Mathematics_for_Machine_Learning.pdf`가 모두 있는지 확인한다. 하나라도 없으면 "머신러닝기초 저장소에서만 동작합니다"라고 알리고 멈춘다.
   형제 `ml-problem-explain/SKILL.md`와 형제 설명 스킬의 실행기 `mpe_cli.py`도 시작 전에 확인한다. 없으면 경로와 원인을 보고하고 시작하지 않는다.
2. STT 목록은 NFC로 읽는다. macOS에는 NFD 파일명이 섞여 있다.
   ```bash
   python3 -c "import os,unicodedata as u,re;n=[u.normalize('NFC',f) for f in os.listdir('$REPO/STT')];print(sorted(m.group(1) for f in n if f.endswith('머러기.md') and (m:=re.match(r'(\d{4})',f))))"
   ```
3. 기간을 정한다.
   - 인자가 있으면 그 기간을 쓴다.
   - 인자가 없으면 `복습노트/*/정리노트_<range>_*.html`(예전 형식인 `복습노트/정리노트_*`도 포함) 중 가장 늦은 끝 날짜를 찾고, 그 뒤의 STT를 모두 쓴다. `정리노트_*`가 하나도 없으면 STT 전부를 쓴다.
   - 해당 STT가 하나도 없으면 사용 가능한 날짜를 보여 주고 멈춘다.
   - `range`는 첫 STT 날짜 하나이거나 `첫-끝` 형식이다.
4. 실행 폴더를 만든다. 서브에이전트에게는 `RUN`, `RUN/repo`, `SKILL` 경로만 넘긴다.
   ```bash
   mkdir -p "$RUN"/{summaries,sections,cards,work} && ln -sfn "$REPO" "$RUN/repo"
   ```
   에이전트는 `RUN` 밖에 쓰지 않는다. 임시·보조 파일(그림 생성 스크립트, 초안, 복사본)은 `RUN/work/`에만 둔다. 저장소(`STT/`, `강의노트/`, `교과서/`)에는 아무도 쓰지 않고, `복습노트/`에는 메인 에이전트만 쓴다.

### 1. 범위 파악
1. **먼저** 관련 `강의노트/Lecture*.pdf` 텍스트를 슬라이드 번호와 함께 `RUN/slides.txt`에 추출한다(PyMuPDF, 쪽마다 `=== LXX sN ===`, 몇 초면 끝난다). 요약 에이전트는 이 파일이 있다고 보고 시작하므로 추출이 끝난 뒤에 띄운다.
   - 관련 PDF: 이전 팩(`복습노트/*/정리노트_*`)이 끝까지 다루지 않은 Lecture PDF 전부. 확실하지 않으면 넉넉히 넣는다.
   - 추출에 실패하면 STT만으로 진행하고 보고서에 적는다(브리프의 `slides.txt` 줄은 "없음"으로 바꿔 넘긴다).
2. 그다음 STT 날짜마다 요약 에이전트 1명을 **병렬로** 띄운다. 브리프는 `references/stt-summary-prompt.md`에 있다.
   - `<LectureXX_*.pdf>`: 그 날짜가 다룬 슬라이드가 들어 있는 PDF(`slides.txt`와 이전 팩의 범위로 판단). 확실하지 않으면 1의 관련 PDF를 모두 적는다.
   - `<YYYY-MM-DD>`: 연도는 이번 학기 연도(오늘 날짜 기준), 월·일은 `<MMDD>`.
3. 에이전트가 도는 동안 메인 에이전트는 MML에서 관련 장과 Example·연습문제 위치를 찾는다(`references/problem-selection.md`의 스니펫).
4. 요약이 끝나면 **학습 레퍼런스 적용 여부**를 정한다. 요약·슬라이드에서 이번에 "다룸/일부"인 토픽에 벡터/교차 공분산, 공분산 행렬, 또는 확률벡터의 선형·아핀 변환에 따른 공분산 계산이 있으면 메인은 `references/scalar-to-vector-covariance.md`를 **전체 읽는다**. 키워드가 예고·안 다룸에만 있거나, 선형변환이 공분산과 무관하면 적용하지 않는다.
   - 이 파일은 학습자 배경과 설명 전략이다. 수업 범위·식·교수님 발언의 근거는 STT·강의자료·MML로 유지한다. 설명됨을 숙달로, 미확인을 지식 부족으로 판정하지 않는다.
   - 관련 토픽과 사용할 설명 연결·미확인 지점을 정하고, 2단계 manifest에서 확정한 토픽 id로 3단계의 해당 섹션 작성자와 6단계 리뷰어 브리프에 전달한다. 파일이 없거나 읽을 수 없으면 일반 규칙으로 진행하고 9단계에 참고 누락을 보고한다. `lite`에서도 읽기와 작성자 전달을 생략하지 않는다.

### 2. manifest
- **큰 그림 먼저**: `references/big-picture-first.md`를 전체 읽고 `RUN/learning-map.json`에 질문·개념 관계·결과·유도 목적·예상 혼동과 근거를 정한다. 첫 학습 토픽은 이 큰 그림으로 계획한다. 위젯·비유·상세 유도보다 먼저 이 목표를 확정한다. 주요 결과를 다음 계산에 재사용하는 연결, 필요한 기존 공식과 실제 대입, 수업의 미분 관례와 보충 경계를 브리프에 함께 적는다. 기존 `learning-map.json` 브리프 안에 기록하며 manifest 스키마나 필수 HTML 속성을 추가하지 않는다.
- 요약들의 슬라이드 대조표와 용어·식 목록으로 `RUN/manifest.json`을 쓴다. 규칙은 `references/manifest-guide.md`에 있다.
- 문제 선별은 `references/problem-selection.md`를 따른다.
  - 정답은 `RUN/answers.py`(`fractions`)로 계산한다.
  - 문제별 교과서 쪽은 `RUN/problem-pages.txt`에 적는다.
- 검증: `python3 "$SKILL/scripts/manifest.py" "$RUN/manifest.json"` 결과가 `OK`여야 한다.

### 3. 작성
- 모든 정리노트 작성자에게 큰 그림 브리프와 `references/big-picture-first.md`를 전달한다. 첫 토픽 작성자는 도입을 작성하고, 다른 작성자는 자기 유도의 목적과 처음 등장하는 기호를 설명한다. 관련 본문은 기억할 출발식에서 변경점·한 단계 연산·다음 결과의 대입까지 연결하고 짧은 복원 요약으로 마친다. 수업 공식과 재표현을 구별하며 같은 설명을 반복하지 않는다. lite도 동일하다.
- 섹션마다 작성자 1명을 띄운다. 브리프는 `references/content-rules.md`, 위젯 규칙은 `references/widget-rules.md`에 있다.
- 문제 작성자 1명이 모든 카드를 쓴다. 브리프는 `references/card-rules.md`에 있다.
- 모두 **한 메시지에서 병렬로** 띄운다. 모델은 opus, `lite`이면 sonnet이다. Claude가 아닌 경우(GPT)에는 opus 대신 sol, sonnet 대신 luna를 쓴다.
- 브리프의 `<…>` 자리는 실제 경로, id, 금지어 목록(`<forbidden 목록>`), 예고 토픽 id(`<preview_topic>`), 섹션 작성자에게 필요한 MML 쪽 번호(`<쪽>`, 1단계 3에서 찾은 PDF 쪽), 그리고 섹션 작성자에게는 manifest `links` 중 그 섹션 토픽에 속한 것만(`<이 섹션의 links 목록>`) 채워 넣는다.
- 섹션 작성자 브리프의 `<학습 레퍼런스>`는 관련 토픽이 있는 섹션에만 `필수 읽기: <SKILL>/references/scalar-to-vector-covariance.md 전체; 적용 토픽: <id 목록>; 설명 연결: <가중합/성분 계산/정의/차원 중 필요한 것>; 미확인 지점: <이번 섹션에서 확인할 것>`으로 채운다. 무관한 섹션에는 `적용 없음`, 파일을 읽지 못한 관련 섹션에는 `참고 누락: <원인>; 일반 작성 규칙 적용`으로 채운다. 레퍼런스 예제를 근거 없이 새 문제 카드로 추가하지 않는다.
- 위젯은 팩 전체에 0~2개다. 병렬 작성자끼리는 서로를 모르므로 **메인 에이전트가 띄우기 전에** 위젯을 둘 토픽(0~2개)을 정하고, 그 토픽의 섹션 작성자 브리프에만 `<위젯>` 자리에 "토픽 `<토픽 id>`에 위젯 1개: <무엇을 움직이면 무엇이 보이는지>"를 적는다. 나머지 작성자의 `<위젯>` 자리에는 "위젯 없음"이라고 적는다. 정한 토픽과 이유는 보고서 "스킬이 정한 사항"에 적는다.

### 4. 조립
- `review_pdf_stage.py`는 stage 루트에 과목의 상대 경로 구조와 기존 노트/강의자료 읽기 연결을 준비한다. 현재 날짜 폴더는 일반 디렉터리이므로 공개 폴더에 초안이 쓰이지 않는다.
- 모든 초안과 수정은 `RUN/work/stage/복습노트/<range>/`에서 만든다. 8단계에서 HTML/MD/PDF 쌍과 그림을 모두 검증한 후에만 공개 폴더에 반영한다. 실패한 초안으로 기존 산출물을 덮어쓰지 않는다.
- **처음 조립할 때만**: `복습노트/<range>/`(그 아래 `.pack/` 포함, 또는 예전 형식인 `복습노트/` 바로 아래)에 이번 `range`의 산출물(`정리노트_<range>_*`, `복습문제_<range>_*`의 `.html`·`.md`·PDF, `figures_<range>/`)이 하나라도 있으면 먼저 백업한다. 다시 조립할 때(5~8단계에서 돌아온 경우)는 백업하지 않는다. 이미 스킬이 만든 초안이 백업에 섞이기 때문이다.
  - `RANGE`, `REPO`, `RUN`을 모두 실제 값으로 바꿔 한 명령으로 실행한다. 파일명은 NFC로 비교하므로 NFD 파일명도 잡힌다.
  - 백업은 매번 새 폴더 `RUN/previous-<시각>-<임의>/`에 만든다(이전 백업을 덮어쓰지 않음). `RANGE`가 형식에 안 맞거나, 대상이 있는데 복사된 파일 수가 다르면 종료 코드 1로 멈춘다. 이때는 조립하지 말고 원인을 고친다.
```bash
RANGE=<range> REPO=… RUN=… python3 - <<'EOF'
import os, re, shutil, sys, tempfile, time, unicodedata as u
r, run = os.environ["RANGE"], os.environ["RUN"]
notes = os.path.join(os.environ["REPO"], "복습노트")
if not re.fullmatch(r"\d{4}(-\d{4})?", r) or not os.path.isdir(run):
    sys.exit(f"백업 중단: RANGE={r!r} 또는 RUN={run!r} 잘못됨")
def want(n):
    n = u.normalize("NFC", n)
    return n.startswith((f"정리노트_{r}_", f"복습문제_{r}_")) or n == f"figures_{r}"
def listdir_nfc(d):  # NFD 폴더명도 찾는다
    return {u.normalize("NFC", n): os.path.join(d, n) for n in os.listdir(d)} if os.path.isdir(d) else {}
day = listdir_nfc(notes).get(r)
srcs = [day, day and listdir_nfc(day).get(".pack"), notes]  # 날짜 폴더, 그 아래 .pack/, 예전 형식(바로 아래)
hits = sorted({n: p for d in srcs if d and os.path.isdir(d) for n, p in listdir_nfc(d).items() if want(n)}.items())
if not hits:
    print("백업할 기존 팩 없음"); sys.exit(0)
def count(p):
    return sum(len(f) for _, _, f in os.walk(p)) if os.path.isdir(p) else 1
dst = tempfile.mkdtemp(prefix=time.strftime("previous-%Y%m%d-%H%M%S-"), dir=run)  # 항상 새 폴더
for n, a in hits:
    b = os.path.join(dst, n)
    shutil.copytree(a, b) if os.path.isdir(a) else shutil.copy2(a, b)
want_n, got_n = sum(count(a) for _, a in hits), count(dst)
if got_n != want_n:
    sys.exit(f"백업 실패: 파일 {want_n}개 중 {got_n}개만 복사됨 → {dst}")
print(f"백업 {len(hits)}항목(파일 {got_n}개): {dst}", *(a for _, a in hits), sep="\n")
EOF
```
```bash
python3 "$SKILL/scripts/review_pdf_stage.py" --run "$RUN" --repo "$REPO" --range "<range>"
python3 "$SKILL/scripts/assemble.py" --run "$RUN" --out "$RUN/work/stage/복습노트/<range>"
```

### 5. 기계 검사
- 정리노트에는 추가로 `python3 SKILL/scripts/check_learning_map.py <stage의 정리노트 HTML>`을 실행한다. 구조 검사는 의미 검토를 대체하지 않는다.
```bash
python3 "$SKILL/scripts/check_html.py" --manifest "$RUN/manifest.json" --note "$RUN/work/stage/복습노트/<range>/<정리노트>.html" --review "$RUN/work/stage/복습노트/<range>/<복습문제>.html"
```
- `FAIL`이면 Problem의 `where`(토픽 id, 카드 id, 섹션 id)로 담당 작성자를 찾는다.
- 그 작성자에게 문제 목록을 보내 조각을 고치게 한다(SendMessage, 안 되면 같은 브리프로 새 에이전트).
- 고친 뒤 4단계부터 다시 한다. 최대 2회까지이며, 그래도 남으면 "미해결"로 보고한다.

### 6. 리뷰 (`lite`면 생략)
- 리뷰어에게 `RUN/learning-map.json`과 `references/big-picture-first.md`를 전달해, 도입만으로 학습 목표·비교 축·결과를 설명할 수 있는지 검토하게 한다. 본문에서 기존 결과 재사용·일반 공식의 대입·복원 요약이 이어지는지, 미분 관례·임시 기호 스케일·출처 경계가 일관되는지도 확인한다. lite에서는 작성자가 같은 질문으로 자기 검토한다.
- 리뷰어 1명을 띄운다. 브리프는 `references/review-prompt.md`에 있다.
- 리뷰어 브리프의 `<학습 레퍼런스>`에는 3단계에서 전달한 적용 토픽 id와 필수 읽기 경로를 넣는다. 적용 대상이 없으면 `적용 없음`, 읽지 못했으면 `참고 누락: <원인>`으로 채운다. `lite`에서는 해당 섹션 작성자의 자기 검사로 공분산 설명을 확인한다.
- Critical과 Important는 모두, Minor는 쉬운 것만 고친다.
- 담당 작성자별로 **한 번에 모아서** 수정을 요청한다. 수정은 한 번만 한다.
- 수정 후 4~5단계를 다시 한다. 반영하지 않은 항목은 보고서에 적는다.

### 7. 브라우저 검증
- `references/browser-check.md`대로 한다.
  - http.server를 빈 포트에 띄운다.
  - 확인: KaTeX 오류 0, 남은 `$` 없음, 375px에서 가로 스크롤 없음, 다크모드, 위젯, 링크, 콘솔 오류
- 결함은 5단계와 같은 방식으로 작성자에게 되돌린다. 이것도 최대 2회 규칙에 포함된다.
- 끝나면 서버를 종료한다.

### 8. PDF 쌍·링크·MD 검증과 배포
- `references/pdf-workflow.md`의 명령을 그대로 따른다. HTML은 stage에서 검사하고, 저장된 원시 카드로 PDF 쌍을 만든다. 미래 카드에는 `.problem` 직계 `.conditions`와 `.ask`가 필수다.
- 기본은 1920×1080 CSS px(1440×810pt)의 `video-16x9`이며 하단 180px은 흰 자막 여백이다. A4 문항별 본문·풀이·수식 배율을 먼저 측정해 화면 글자 크기를 보존한다. 인쇄용 A4가 명시적으로 필요하면 `--layout a4`를 사용한다.
- `build_review_pdf.py --stage-only`가 성공한 PDF 둘만 stage에 복사한다. `add_pdf_links`로 노트에 문제지/해설지 링크를 넣고 실제 카드 수를 안내한다. manifest의 links 토픽에 두 PDF 링크를 추가한 후 다시 HTML 검사한다.
- `html2md.py --check`로 MD 두 개와 그림을 `.pack/`에 만들고 PDF href가 유지되는지 확인한다. PDF 전체 페이지를 PNG로 렌더링하여 표·화살표·수식·필기 공간·Hint·계속 페이지를 모두 눈으로 확인한다.
- PDF skill을 사용할 때 첫 PDF 작성 직전 authoring marker를 한 번 수행한다. 실행 중 두 템플릿과 video CSS는 변경하지 않는다. EC2 `757fa081521008d46542e23d5a1a53112391aed2`에서 고정 복사한 세 파일의 `pdf-template-provenance.json` 해시를 확인한다.
- 두 PDF, HTML 두 개, MD 두 개, 모든 참조 그림이 준비된 후 `publish_files`로 함께 배포한다. 백업은 `RUN/work/backups/`다. 교체 실패 시 기존 파일을 복구한다.
- KaTeX·폰트·이미지 로드 실패, 넘침, 정답 검증 실패 또는 PDF 둘 중 하나의 실패는 해당 팩 배포 실패다. 이미 있는 파일을 보존하고 원인/문제 id를 보고한다. HTML/MD만으로 완료라고 보고하지 않는다. `lite`도 이 규칙을 생략하지 않는다.

- 기본 팩 배포 성공 직후 [문제설명 공통 절차](references/problem-explain.md)를 최종 복습문제의 정확한 절대 HTML 경로로 실행한다. 신규·기존 팩 갱신·lite 모두 전체 문항·소문항을 처리한다. 설명 실패는 기본 팩을 보존하고 별도로 보고한다.

- 기본 팩 배포와 문제설명 처리 뒤 [기존 인터랙티브 연결 복원](references/interactive-links.md)을 적용한다. 기존 자료가 있을 때만 재연결하며 새 자료는 자동 생성하지 않는다. 연결 오류는 기본 팩·문제설명 결과와 분리해 보고한다.

### 9. 보고
다음 형식으로 끝낸다.
```
## 복습팩 <range> 완료
- 파일: 복습노트/<range>/… (html 2 + .pack/: md 2, PDF 2, figures_<range>/ N개)
- 범위: 배운 슬라이드 … / 예고만: …
- 문제: P1 MML Example 9.1 변형(level 1) … (정답은 RUN/answers.py로 검증)
- 스킬이 정한 사항: slug, 섹션 구성, 위젯, 뺀 내용과 이유
- 학습 레퍼런스: 적용 토픽 id / 적용 없음 / 참고 누락과 원인
- PDF 검증: 논리 문항 수, 모드별 페이지 수, 전체 페이지 시각 검수, validation.json, 템플릿 SHA
- 문제설명: published/withheld, 전체 문항·소문항 수, 네 실제 검토, HTML/MD 링크, RUN·백업; 실패하면 “복습팩 생성됨 / 문제설명 보류”, 이유. 이전 설명을 현재 입력 검증으로 보고하지 않음
- 인터랙티브 연결: added/updated/unchanged/skipped·노트 절·실제 링크; 자료 없음/스킬 미설치면 생략
- 백업: …
- 미해결: … (없으면 "없음")
- 커밋 제안: git add 복습노트/<range> && git commit -m "docs(notes): add review pack <range>"
```
실행 폴더 경로(`RUN`)도 적는다. 수정이 필요하면 조각을 고쳐 4단계부터 다시 돌리면 된다.

## 오류 처리
| 상황 | 동작 |
|---|---|
| 저장소가 아님 | 알리고 멈춤 |
| 기간에 해당하는 STT 없음 | 사용 가능한 날짜를 보여 주고 멈춤 |
| PDF 텍스트 추출 실패 | STT만으로 진행하고 보고서에 표시 |
| 포트 사용 중 | 다른 빈 포트 사용 |
| 같은 range의 팩이 이미 있음 | 4단계 첫 조립 전에 기존 html·md·`figures_<range>/`를 새 폴더 `RUN/previous-<시각>-<임의>/`에 복사하고(다시 조립할 때는 복사하지 않음) 백업 경로를 보고서에 적음. 백업 명령이 실패하면 조립하지 않고 원인을 고친다 |
| 검사 2회 실패 | 초안 검사를 끝내고 "미해결"로 보고; 검증된 산출물 쌍이 없으면 배포/완료하지 않음 |
| PDF 생성·검증 실패 | 해당 날짜 배포 보류, 기존 PDF/노트 보존, 날짜·문제 id·실패 원인과 stage/보고 경로를 알림 |
| 문제설명 검토·발행 실패 | 기본 팩과 이전 설명 보존; “복습팩 생성됨 / 문제설명 보류”, 이유·RUN·백업 보고. 현재 입력 승인으로 표시하지 않음 |

## 본문과 우측 패널 표시 계약

중앙 주제·문항 제목과 패널의 고정 제목은 유지한다. 우측에는 중앙 제목을 복사하지 않는다. `sum-for`는 제목이 아닌 유일한 `.sums` 컨테이너 ID로 보존한다. `.sum` 전환, 문제·원문 탭, 힌트·풀이, 앵커, read/solved 저장 키와 payload를 유지한다. 예습·과제·시험도 같은 표시 계약을 따른다.

요약은 같은 토픽 본문의 핵심 개념·작동 원리·성립 조건·혼동 구분을 압축한다. 식·용어·항목 수에 고정 상한을 두지 않는다. 본문에 없는 사실을 요약에만 추가하지 않으며 보충의 범위·출처·불확실성을 보존한다. 문제설명은 풀이의 판단 조건·결론·단서를 압축하고 문제 데이터와 풀이 본문을 바꾸지 않는다.

검토 시 자료·토픽별로 일반·강조·주의·보충의 서로 다른 핵심을 별도 행으로 기록하고 본문 주장, 대응 요약 문장, pass/unresolved와 생략 이유를 대조한다. 보완 후 실제 요약을 다시 읽는다. 기존 동반 MD와 재생성 원고도 동기화하되 원래 없는 MD 형식은 만들지 않는다. 요약·예고·링크 화면의 기존 구조를 유지한다. 검증 JSON은 `{schema_version:1, html, html_sha256, audit_path, audit_sha256, semantic_status, browser_status, evidence, unresolved}`를 기록한다. 실제 검사 뒤에만 status를 바꾸며 HTML·감사표 해시 변경 후에는 기록을 갱신해야 한다.
