# ml-midterm 구현 검증

2026-10-20, Native 방식으로 기존 `codex/row-vector-midterm-01`에서 구현했다. 새 실전 회차는 만들지 않았다. 새 스킬은 `.claude/skills/ml-midterm/SKILL.md`, 발견 링크는 `.agents/skills/ml-midterm`이다.

## 보존 확인

- 시작 시 1회·STT·복습노트·과제 등 2,542파일 SHA-256을 저장했고 마지막 대조에서 변경 0개였다.
- 1회 재생성 결과의 CSS·script·문제 카드·topic 해설·sum이 기준과 동일했다.
- 같은 Chrome/1280×900/light/p7 상태의 기준/재생성 스크린샷은 픽셀까지 동일했다.
- 한국어 문제 10페이지·답안 10페이지·영어 문제 10페이지 모두 기준 PDF와 렌더링 픽셀이 동일했다. 1440×810pt, 하단135pt 흰 띠도 검사했다.
- 실제 Chrome의 3화면×2테마×10문항=60조합, 영어 원문 60검사, 인쇄 6조합이 pass/errors=[]였다. 1023→1024 경계·도킹·이동/크기·모바일·저장 상태·키보드·원문 없음 fallback을 포함했다.
- 임시 2회 입력의 소문항을 41개로 바꾼 실제 영어 PDF와 리포트가 10문항/41소문항/02파일명을 반영했다.

근거는 저장소 `tmp/ml-midterm-skill/golden-01/`의 golden-comparison.json, pdf-comparison.json, browser-check.json, baseline-p7.png, regenerated-p7.png, pdf-contact.png와 `dynamic-02/english-result.json`이다. 임시 PDF 검증은 구조·양식 검증이며 실제 새 시험의 수학 승인으로 기록하지 않았다.

## 테스트

새 테스트의 실행 명령:

```powershell
python -m pytest .claude/skills/ml-midterm/tests --rootdir .claude/skills/ml-midterm/tests --confcutdir .claude/skills/ml-midterm/tests --basetemp tmp/ml-midterm-skill-tests/final-complete -q
```

- 최종 신규 스킬 전체 **41 passed**(87.38초). 신규 기능 30테스트를 통과한 뒤 독립 검토자의 Important 5건을 11개의 실패 재현 테스트로 확인하고 수정했다.
- MPE 공유 계약·발행·미분 정책 테스트 28개 통과.
- 기존 1회 도구의 비 PDF/브라우저 테스트 39개 통과(5개 제외). 실제 PDF/브라우저는 위 별도 생성 검증을 수행했다.
- 두 스킬의 skill-creator quick_validate 통과, 링크 resolve 및 git diff --check 통과.
- 별도 에이전트의 지침 없는 기준 평가 후 새 지침으로 새출제/생략/충돌/해설/명시HTML/날짜/과제/all/출처/수학충돌/템플릿변경 경로를 전방 검증했다. 기존 날짜·과제·all 선택은 유지됐다.

## 독립 코드 검토와 수정

새 맥락의 gpt-6-astra 검토: Critical 0, Important 5, Minor 0. 다음은 모두 실제 RED→GREEN으로 검증했다.

1. 영어 PDF visual_review의 reviewer/evidence 및 전체 실제 페이지를 필수로 검사한다.
2. delivery.files에서 원본·설명 HTML/MD·manifest 및 소유 파일·validation·출제표·검토 근거·PDF·한국어 입력 snapshot 누락을 거부한다.
3. 한국어 PDF 입력 snapshot에 OUT 기준 상대 그림을 복사해 실제 렌더러가 찾게 한다. 카드 문구와 digest는 유지한다.
4. 원본/설명 그림과 하위 로컬 이미지 의존성을 검토 hash에 넣고 build 이후 변경 시 발행 및 최종 검사에서 거부한다.
5. 실제 NFD 파일/폴더 이름으로 입력·회차 탐색·원본 선택·충돌 검사를 수행한다.

## 기존 전체 MPE 검사에서 남은 실패

확장 검사는 **109 passed, 13 failed**였다. 이번 변경으로 공유 Python 코드나 기존 자료를 수정하지 않았으며, 시작 시점 자료 hash와 현재 자료 hash도 같았다. 실패를 숨기거나 옛 검토 hash를 새 값으로 바꾸지 않았다.

- `test_delivery.py::test_published_review_explanation[0909,0914,0916,0921,0923,0928,0930,1007,1012,1014,1019]` 11건: 기존 발행 자료의 legacy-layout 참조 해시/산출 이력 대조 실패. 예: 0909~1012의 정리노트 MD 참조, 1019 정리노트 HTML 참조.
- `test_delivery.py::test_published_layout_keeps_only_html_on_top[1014]`: 기존 1014 폴더에 MD·자료 폴더가 최상위에도 남아 있다.
- `test_delivery.py::test_delivery_survives_checkout_relocation[None]`: 위 0909 참조 해시 문제를 복제 뷰에서도 재현했다.

진단 목록: `tmp/ml-midterm-skill/shared-preexisting-failures.json`. 이 작업의 보존 범위에 따라 기존 복습팩 재발행/마이그레이션은 수행하지 않았다. 새 스킬 검증과 별개로 남는 기존 실패이며 전체 저장소가 green이라고 주장하지 않는다.

## 실행 중 판단

- 기존 codex 브랜치·체크아웃에서 작업했다. 잘못된 선택이면 후속 cherry-pick이 필요하다.
- Windows에 Git Bash 보조 실행기가 없어 Python으로 작업별 기록·기준 커밋·검증 증거를 남겼다. 보조 도구 출력 형식이 다르다.
- pytest 상위 탐색은 기존 ml-interactive의 잘못된 링크에 걸려 rootdir/confcutdir를 지정했다. 서로 다른 스킬 테스트는 별도 프로세스로 실행해야 한다.
- 회차 전체의 OS 원자적 교체 대신 명세대로 백업/복구가 있는 단계별 발행을 유지했다. 후속 실패 시 검증된 기본 파일은 남을 수 있으며 전체 완료는 보류된다.
- 기존 13실패를 없애기 위한 수업 자료 수정은 하지 않았다. 해당 기존 검사 실패가 남는다.
- 실제 새 시험 저작/수학 승인은 설치 범위에서 제외했다. 향후 회차 저작 때 독립 검산이 필요하다.
- 코드 검토자에게 동일 PDF/브라우저 작업을 중복 실행시키지 않고 직접 실행한 비교 증거를 사용했다. 렌더링 자체의 두 번째 독립 실행은 없다.

원격 push·merge는 수행하지 않았고 현재 브랜치에 구현 커밋을 남겼다.
