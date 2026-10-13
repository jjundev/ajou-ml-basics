# 복습팩 배포 후 문제설명

기본 HTML·MD·PDF 쌍의 검증과 `publish_files` 배포가 성공한 직후, 완료 보고 전에 실행한다. 신규 생성·사용자 요청에 따른 기존 팩 갱신·lite 모두 최종 전체 문항을 대상으로 한다. PDF 비율만 바꾸는 마이그레이션은 제외한다.

- `ABS_REPO`: 실제 저장소 절대 경로.
- `ABS_REVIEW`: 방금 배포한 복습문제 HTML 하나의 정확한 절대 경로. 최신 날짜·날짜만으로 다시 선택하지 않는다.
- `EXPLAIN_SKILL`: 형제 `ml-problem-explain`의 절대 경로.
- `EXPLAIN_RUN`: 팩마다 `tmp/ml-problem-explain/<고유ID>/`의 비어 있는 절대 경로.

1. `EXPLAIN_SKILL/SKILL.md`, `references/authoring.md`, `references/verification.md`를 읽고 전체 절차를 적용한다.
2. `python <EXPLAIN_SKILL>/scripts/mpe_cli.py extract --repo <ABS_REPO> --target <ABS_REVIEW> --run <EXPLAIN_RUN>`을 실행한다.
3. source.json의 모든 문항·소문항과 관련 MML·교안·원 PDF·정리노트를 읽고, 각 설명 조각을 저작한다. understand → recall → start → solve → verify → pitfall → retry와 요약을 작성한다. CLI는 저작기가 아니다.
4. 별도 계산·상징 계산·증명/정성 검토로 독립 검산하고 evidence에 스크립트·결과·쪽·근거를 남긴다. 수치 예제만으로 증명을 승인하지 않는다.
5. `build --run <EXPLAIN_RUN>`, `check --run <EXPLAIN_RUN>`을 실행한다.
6. 현재 입력·참조·조각·산출물 해시에 묶인 source_visual/content/independent/browser 네 실제 검토를 수행한다. lite에서도 생략하지 않는다. 1280×900/375×812, light/dark에서 모든 본문·요약·목차·pager·수식·링크·자원을 확인한다. 합성 테스트 승인을 실제 승인으로 사용하지 않는다.
7. 실제 검토를 review.json에 기록하고 `publish --run <EXPLAIN_RUN>`을 실행한다. 입력이나 조각을 고쳤다면 재build·재검토한다. 공개 경로의 원문/개념 anchor와 로컬 자원을 확인한다.

팩별 결과는 published/withheld, 이유, HTML/MD, RUN, 백업 경로로 기록한다. 실패하면 검증된 기본 팩과 이전 설명을 보존하고 “복습팩 생성됨 / 문제설명 보류”로 보고한다. 이전 설명이 남아 있어도 갱신된 입력에 대한 검증 완료로 표시하지 않는다. 설명 실패 때문에 기본 팩을 rollback하지 않는다. 설명 소유 파일만 고유 백업·교체하며 교체 실패는 설명 발행기가 복구한다.

과거 팩 backfill은 기존 복습문제의 명시 HTML 경로마다 이 절차만 수행한다. 기본 팩을 재생성하지 않으며 원본 노트·문제·PDF·그림과 과제 설명을 보존한다.
