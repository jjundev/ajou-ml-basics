---
name: ml-interactive
description: 머신러닝기초 날짜나 주제로 수치·분포·그래프를 조작하는 인터랙티브 자료가 필요할 때 사용한다. 인터랙티브 HTML 생성, ML 시각 실험, 기존 자료 연결 또는 /ml-interactive [MMDD|주제]에 사용한다. 정리노트와 복습문제 생성은 ml-review-pack을 사용한다.
---

# 머신러닝 인터랙티브

공통 그래프·수식 전개 셸로 개념을 직접 조작하는 HTML을 만들고 정리노트의 해당 설명에 새 탭 링크를 연결한다. 원본은 `.claude/skills/ml-interactive`, `.agents/skills/ml-interactive`는 상대 심볼릭 링크다. Node.js 20 이상이 필요하다.

## 대상과 근거

REPO는 현재 머신러닝 프로젝트다. `복습노트/`, `STT/`, `강의노트/`, `교과서/Mathematics_for_Machine_Learning.pdf`를 확인한다. 인자 없이 호출하면 날짜·주제 사용법을 안내한다.

```powershell
node SKILL/scripts/resolve.cjs REPO '1014'
node SKILL/scripts/resolve.cjs REPO '가우시안 곱'
```

출력의 folder, notes, noteHtml, stt, existing, next는 실제 파일 경로다. 구형 루트 MD와 .pack MD를 모두 읽고 같은 이름이면 .pack이 우선이다. NFC/NFD 경로를 임의로 다시 조합하지 않는다. 날짜 범위가 모호하면 AMBIGUOUS_TARGET을 보고한다.

정리노트·STT·강의 PDF·MML 관련 절을 읽어 배운 범위와 예고를 구별한다. PDF 페이지는 실제 파일에서 확인한다. 수식이 충돌하면 유도와 교과서로 검산하고 교정 근거를 기록한다.

## 생성

1. [주제 선정](references/topic-selection.md)을 읽는다. 날짜는 좋은 후보 2–4개, 특정 주제는 1개가 기본이다. 부족하면 억지로 채우지 않는다. existing의 제목과 HTML 내용을 읽어 같은 실험을 중복 생성하지 않는다.
2. OS 임시 폴더에 새 RUN을 만든다. 주제별 brief.md에 목표·조작 변수·관찰할 변화·모드·출처·학습용 데이터·단순화를 적는다. 실행은 사용자가 선택한 방식과 실제 도구에 맞추며 모델이나 위임을 강제하지 않는다.
3. assets/template.dc.html을 RUN/n/Main.dc.html로 복사한다. [장면 계약](references/scene-api.md)과 [디자인](references/design.md)에 따라 제목·슬롯·주제 훅을 저작한다. 모드별 `view`는 그래프형(기본 `graph`) 또는 수식 전개형(`formula`)으로 고른다. 수식형은 STEPS의 수식 데이터로 공통 본문을 사용하고 DOM 삽입·버튼 복제 없이 작성한다. 제목과 도구 정렬·공통 스크롤바·간결한 설명을 기본으로 삼는다. 평면 그래프는 정면 고정 시점, 의미 있는 시간 변화만 playback을 쓴다. compute(state)의 같은 결과에서 그래프와 패널을 만든다. K=2 회귀에는 MLMath를 재사용하고 다른 모델은 별도 순수 계산과 독립 정답을 준비한다.
4. check.cjs SOURCE가 ok여야 한다. steps.cjs SOURCE로 preset·수치·문구를 대조한다. [수학 검증](references/math-validation.md)에 따라 다른 계산 경로로 검산하고 행렬 차원·공분산·분산/표준편차·밀도/확률을 원자료에 대조한다. 근거와 결과는 evidence/에 둔다. 이어서 형제 스킬 [ml-note-audit](../ml-note-audit/SKILL.md)의 "생성 절차에서 부를 때"로 설명 감사를 한다. `<대상>`은 SOURCE의 STEPS 수식·설명 문구·패널 문장, `<형제 자료>`는 같은 날짜의 정리노트다. 결과는 evidence/audit.md에 두고 Critical·Important를 고친 뒤 4단계를 다시 확인한다.
5. build.cjs SOURCE PREVIEW로 로컬 수식·폰트 미리보기를 만든다. 도구 준비는 [디자인](references/design.md)의 브라우저 도구 절을 따른다. 실제 브라우저에서 1440×900·375×812, 두 테마·모든 모드, 입력 최소/최대/빈 값, 단계, 초기화, 키보드, drawer/Escape를 확인한다. 수식·콘솔 오류, 외부 리소스 요청, 가로 넘침이 없어야 한다. 캡처를 눈으로 확인한다. 첫 콘텐츠의 불필요한 구분선, 모든 스크롤 영역의 스타일, 제목과 도구 정렬을 확인한다. 확대·축소·초기화는 현재 본문(그래프 또는 수식)에 작동해야 하며, 수식형은 단계 누적·현재 단계 설명·양 끝 버튼 비활성화도 검증한다.
6. 통과한 주제만 save.cjs SOURCE DEST '한국어_이름'으로 저장한다. 반환한 nn/html/dir을 사용하고 번호를 하드코딩하거나 덮어쓰지 않는다. dir에 brief·evidence와 상대 note-links.json을 저장한 뒤 아래 연결을 수행한다. 최종 공개 경로에서도 수식·폰트를 확인한다.

HTML은 날짜 폴더의 인터렉티브_NN_<이름>.html, 원본·근거는 .pack/자료_인터렉티브_NN_<이름>/이다. vendor는 .pack/vendor/ml-interactive/에 공유하고 provenance 해시 불일치는 중단한다. 다른 과목 저장소·vendor는 수정하지 않는다.

## 연결과 복원

연결만 요청되면 새 번호·자료를 만들지 않는다. [노트 연결](references/note-links.md)을 읽고 기존 자료와 설명을 대조해 절 ID·실제 조작에 맞는 안내·위치를 정한다. 본문·위젯·스타일·스크립트·MD·PDF는 보존하고 연결 문장과 새 탭 속성만 바꾼다.

```powershell
node SKILL/scripts/link-notes.cjs RUN/note-links.json --dry-run
node SKILL/scripts/link-notes.cjs RUN/note-links.json
node SKILL/scripts/link-notes.cjs RUN/note-links.json
node SKILL/scripts/relink.cjs REPO '1014' --dry-run
node SKILL/scripts/relink.cjs REPO '전체'
```

재실행은 unchanged여야 한다. 재생성한 노트에는 저장된 상대 명세로 복원한다. 절 ID가 바뀌면 내용을 읽어 새 대응을 정하고 명세를 갱신한다. 확정할 수 없으면 skipped 이유를 보고하며 임의의 절·페이지 끝에 붙이지 않는다. metadata 없는 자료는 내용을 읽어 명세를 먼저 만든다. 실제 클릭으로 새 탭 목적지·원 노트 유지·모바일 안내를 확인한다.

## 완료와 보류

주제별 실패는 통과한 다른 주제를 막지 않는다. 생성 성공과 연결 보류를 구분한다. 파일·모드·조작·단순화/보충·수학/화면 검증·연결 절·added/updated/unchanged/skipped·RUN과 백업을 보고한다. 자동 커밋·외부 게시를 하지 않는다.
