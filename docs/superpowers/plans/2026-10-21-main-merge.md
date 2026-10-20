# main 병합 결정과 검증

사용자가 `codex/row-vector-midterm-01`의 작업을 main에 병합하고 푸시하도록 요청했다. 병합 부모는 main `d7621b4`와 작업 브랜치 `05d474f`다. 강제 푸시·브랜치 삭제는 수행하지 않는다.

## 충돌 해결

- main에는 과거의 다른 2회차가 남아 있었다. 사용자가 새로 요청하고 검토·커밋한 **중하 난이도 10대문항·35소문항**의 2회차를 선택한다. 과거 2회차의 조각·검토 JSON·완성 HTML을 새 문제와 섞지 않는다. 과거 자료는 main 부모의 Git 기록에 남는다.
- 1회차는 이 작업에서 확정한 행 미분, 공식 적용 간결화, 영어 본문과 그에 대응하는 기존 검토 산출물을 한 세트로 유지한다. main의 다른 버전으로부터 부분 요약·완성 HTML·manifest만 섞어 해시와 의미를 불일치시키지 않는다. 두 부모의 기록은 Git에서 보존한다.
- main의 복습·과제·예습 자료, 요약 보완, 패널 제목 중복 제거, 관련 지침과 검토 보고서는 유지한다.
- 1019 정리노트의 충돌은 main의 공통 화면·보완 요약을 유지하면서 작업 브랜치의 직선·평면·회귀 세 토픽 설명을 결합한다. 모든 기존 요약 문장·공식·토픽 ID를 유지한다. 추가 본문은 계수/적합벡터/새 입력 예측과 차원·곱 순서를 구별하는 설명이다.

## 공통 템플릿 5개 변경의 검토

ml-midterm의 최초 기준은 템플릿 변경을 차단했다. 이 병합에서는 실제 main diff를 읽고 다음 5개를 명시적으로 수용한다. 이는 현재 파일을 무조건 기준으로 삼는 자동 갱신이 아니다.

1. `ml-review-pack/assets/note-template.html`: 우측에 중앙 제목을 중복 표시하는 코드 제거, sum-for를 sums 컨테이너의 ID로 유지.
2. `ml-review-pack/assets/review-template.html`: 중복 aid 제목과 제목 복사 코드 제거. 문제·힌트·풀이·read/solved payload는 유지.
3. `ml-problem-explain/assets/note-template.html`: 같은 중복 제목 제거 및 sums ID 이동. 문제/원문 패널, 도킹, 요약 전환, 저장 키는 유지.
4. `ml-problem-explain/assets/port-provenance.json`: 위 변경의 provenance 갱신.
5. `ml-problem-explain/assets/template-provenance.json`: 위 변경의 provenance 갱신.

공통 PDF 템플릿, 수학 저작·검증 API, 벡터 미분 관례는 이 변경에 포함되지 않는다. 이미 발행한 1·2회 HTML/MD/PDF는 이 템플릿으로 재생성하지 않는다. 이후 새 build는 main의 개선된 공통 템플릿을 사용한다. 나머지 118개 pin은 변경하지 않는다.

2회차의 기존 검토가 참조하던 5개 옛 템플릿은 `ml-midterm/references/template-history/20261020/`에 원래 바이트 SHA-256과 정확히 같은 사본으로 보관한다. 실제 Git blob과 LF/CRLF 후보 중 **기존 검토 해시에 일치하는 바이트만** 선택했다. 원본 검토 JSON도 `pre-main-validation.json`으로 보존한다. references의 경로만 그 사본으로 옮기며, source/fragment/artifact/input/policy hash와 네 검토 판단은 바꾸지 않는다. 경로 이전 근거는 2회차 `.pack/evidence/main-merge-reference-proof.json`에 기록한다. 달라진 템플릿 바이트에 과거 pass를 붙이지 않는다.

1회차에는 과거 Git 줄바꿈 정규화로 인한 checkout 차이가 있었다. 기존 보존 snapshot·산출물 manifest의 SHA-256에 일치하는 원래 바이트로만 복원하고 회차 내부 `.gitattributes`로 재발을 막는다. 해설·답·페이지 내용을 다시 쓰거나 검토 해시를 새 내용에 맞춰 바꾸지 않는다.

## 검증 기록

첫 병합 전 pytest 실행은 브랜치 전환과 겹쳐 파일이 제거된 시점의 7개 실패를 포함했으므로 유효한 결과로 사용하지 않는다. 병합 후 안정된 파일 상태에서 다시 실행한 결과만 최종 근거로 사용한다. 공통 요약 패널 브라우저 테스트는 4개 통과했다. 나머지 최종 명령과 결과는 병합 검증 JSON에 기록한다.

최종 결과: ml-midterm 41개, 공통 해설 38개, 노트/복습 패널4개 테스트 통과(총83개). 1019 노트 실제 브라우저42개 조합 통과. 1·2회차 최종check 모두 pass/errors=[]이며 원래1회차320개 파일은 기존SHA256과 모두 일치한다. 상세 JSON은 `evidence/2026-10-21-main-merge/verification.json`에 보관한다.
