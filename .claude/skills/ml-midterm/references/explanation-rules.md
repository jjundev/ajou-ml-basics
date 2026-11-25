# 상세 해설과 검토

저작 전에 다음을 전체 읽는다.

- [MPE 저작](../../ml-problem-explain/references/authoring.md)
- [MPE 검토/발행](../../ml-problem-explain/references/verification.md)
- [공통 벡터 미분 관례](../../ml-review-pack/references/vector-derivative-convention.md)

현재 1회의 `.pack/explanations/pN.html`이 재생성 입력이다. understand→recall→start→solve→verify→pitfall→retry, 직계 sum[hidden] 하나, provenance/terms를 그대로 유지한다. 실제 소문항마다 solve/verify가 각각 한 번 대응하고 본문 답은 펼친다. 제목·간격·문제→원문→출제 근거→용어 탭·패널·테마·읽음·모바일은 공통 템플릿 그대로다.

공식 적용형은 **공식→주어진 값 대입→결론과 핵심 이유**다. p4(b,c), p8(d~f)처럼 알려진 공식을 쓰는 문제에서 공식을 처음부터 재증명하지 않는다. 유도·증명형(p6/p7/p10)은 요구한 중간 단계를 남긴다. 단서→개념 선택→실제 첫 줄을 연결하고 긴 설명을 recall/start/solve에 복제하지 않는다. `~해요` 체와 영어 용어를 쓴다.

기호가 필요한 곳은 뜻·역할·차원·실제 구성을 설명한다. phi 함수, phi(x) 특징벡터, Phi 설계행렬과 행·열 index를 구별한다. 용어 패널은 이름·뜻·기호·이 문제에서의 역할이다. 새 스칼라 미분은 행벡터, 변수는 열벡터, Jacobian은 출력×입력이며 0으로 놓은 행 식의 **양변 전치**로 열 정규방정식에 연결한다. 기존 명시적 열 관례의 해설만 요청은 공통 reference의 원문 보존 분기를 따른다.

## 해설만 처리

`/ml-problem-explain 중간고사 N회`, 기존 예상문제 HTML 또는 그 문제설명 HTML은 전용 EXAM 어댑터를 쓴다. `exam_config.resolve_exam_target(repo,target)`으로 같은 폴더의 유일한 원본·blueprint·회차를 확인한다. 복수 원본이면 후보를 제시해 명시하게 한다. 일반 mpe_cli.extract/load_source는 EXAM을 지원하지 않으므로 보내지 않는다.

예를 들어 기존 2회 해설 요청은 새 고유 RUN과 다음을 사용한다.

```powershell
uv run python .claude/skills/ml-midterm/scripts/midterm_cli.py explain --repo . --out 중간고사대비/예상문제_2회 --run tmp/ml-midterm/explain02-first
```

기존 최신 조각을 읽고 요청한 부분만 보강한 뒤 다시 explain한다. 원 문제 HTML·cards·참고 답·영어 본문·PDF를 수정하지 않는다. base/english는 호출하지 않는다. 대상이 일반 날짜/기간/과제/인자 없음/all이면 기존 MPE 경로를 그대로 사용하며 예상문제를 자동 선택에 추가하지 않는다.

## 검토와 발행

explain은 RUN/explanation-result.json의 stage HTML/MD/manifest와 review.json을 만든다. source/fragment/reference/resource/artifact hash와 현재 정책에 묶인다. 네 검토는 매번 not_run이며 이전 pass에 새 hash만 넣지 않는다. 빌드 후 공통 템플릿·코드가 바뀌면 게시를 거부하므로 다시 빌드하고 검토한다.

source_visual/content/independent/browser와 모든 실제 소문항을 MPE verification 계약에 맞춰 검토한다. 독립 검산자는 답·해설을 보기 전에 조건·질문·그림·필요 이론만으로 계산/논증한다. 답 대조 후 불일치는 disputed로 보류한다. 구조·수식 검사만으로 수학 검토를 통과시키지 않는다. 새 출제 검산 결과는 OUT/.pack/evidence/answer-checks.json의 items에 `pN:a` 등 실제 항목을 키로 두고 status/method/conclusion/evidence를 기록한다.

브라우저는 실제 stage 파일을 검사한다.

```powershell
uv run python .claude/skills/ml-midterm/scripts/browser_check.py <stage-HTML> --evidence <OUT>/.pack/evidence/browser-check.json --shots <RUN>/shots
```

1280×900·1024×900·375×812, 두 테마의 60문항 조합과 모든 영어 본문, 1023→1024, 닫힘 저장, 도킹·이동·크기, 목차·이전/다음·요약·키보드·reload·원문 없음 fallback·인쇄 한영 보존을 검토한다. 외부 요청·콘솔/KaTeX·누락 자원·가로 넘침은 0이다. 실제 스크린샷도 읽는다. source_visual과 수학 검산은 이 리포트로 대체하지 않는다.

실제 검토를 기록한 후 같은 repo/out/run으로 `publish`한다. 승인된 설명 소유 파일만 공유 publish_explanation으로 발행하며 원 문제/PDF는 보존한다. 일반 MPE rerender가 EXAM까지 지원한다고 가정하지 않는다.

새 제작의 영어 PDF는 english 결과의 problems_pdf/report를 읽고 **전체 페이지를 렌더링해 직접 검수**한다. report의 source_sha256·english_digests·pdf_sha256를 현재 원본/PDF와 대조하고, 검수한 reviewer/pages/evidence를 visual_review에 기록한 뒤에만 status=pass로 한다. 검토 전 상태는 awaiting_visual_review다. 공유 `review_pdf_publish.publish_files({OUT/<PDF명>:stage_pdf, OUT/'.pack/evidence/english-pdf-validation.json':stage_report}, RUN/'english-backup')`를 사용해 별도로 발행한다. 원본/영문이 바뀌면 다시 생성·검수한다.

전체 완료 전 `.pack/delivery.json`을 작성한다: logical_count=10, subpart_count=현재 실제 수, files=발행한 파일의 OUT 상대경로→SHA-256. 현재 원본 HTML·PDF 3개·문제설명 HTML/MD·manifest/그 manifest의 files·validation.json·이번 검토 근거를 포함한다. delivery.json 자체나 비소유 파일을 해시 집합에 무조건 넣지 않는다. 브라우저 리포트는 최종 발행 HTML hash와 같아야 한다. 검토 중 evidence를 stage에 추가하면 artifact hash가 달라지므로 다시 build·검토한다. 외부 evidence는 실제 위치와 hash를 references에 기록한다.

```powershell
uv run python .claude/skills/ml-midterm/scripts/midterm_cli.py check --repo . --out 중간고사대비/예상문제_2회
```

status=pass/errors=[]/exit0이어야 전체 완료다. `check`는 검증만 하며 missing 파일·승인·delivery를 만들어 주지 않는다. 해설만 작업에서는 원래 PDF 검토와 해시도 확인하되 PDF를 다시 생성하지 않는다. 실패하면 RUN/failure.json과 백업 위치, 미완료 단계를 보고한다.
