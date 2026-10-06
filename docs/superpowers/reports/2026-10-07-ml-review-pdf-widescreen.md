# 머신러닝기초 복습문제 PDF 16:9 적용 검증

2026-10-07. 기존 7개 팩, 47문항, PDF 14개(101페이지)를 같은 이름으로 교체했다. 생성기와 스킬의 향후 기본값도 `video-16x9`다. 커밋·push·merge는 하지 않았다.

## 출력과 보존

- PDF 1440×810pt(1920×1080 CSS px), 하단 180px/135pt 흰 자막 여백. 전체 DOM 및 PDF text/image/drawing 검증 통과.
- 실행 전 snapshot의 177파일 중 PDF14개를 제외한 모든 원본 bytes 일치. 복습/정리 HTML·MD, 135개 그림, 기존 파일명·PDF 링크 보존. 기존 migration의 source/layout/MD/figure SHA 및 링크 검사 통과.
- 설계의 “그림149개”는 실제 인벤토리로 정정한다: 그림135개 + 복습 HTML/MD14개 =149개이며, 정리 HTML/MD14개를 포함한 전체 원본은163개다. 실제 그림 누락 없이 snapshot177파일(원본163 + 기존PDF14)을 전부 확인했다.
- 페이지 수 101 → 101. 새 계속 페이지 없음. 계속 페이지 재측정·누락 typography 실패는 별도 통합 테스트로 검증.

| 날짜 | 문항 | 문제 쪽 | 답안 쪽 | 논리/물리 대응 |
|---|---:|---:|---:|---|
| 0909 | 5 | 5 | 6 | P1–P5: 문제/답안 각각 같은 번호 페이지, 답안 마지막 Hint |
| 0914 | 7 | 7 | 8 | P1–P7: 문제/답안 각각 같은 번호 페이지, 답안 마지막 Hint |
| 0916 | 6 | 6 | 7 | P1–P6: 문제/답안 각각 같은 번호 페이지, 답안 마지막 Hint |
| 0921 | 6 | 6 | 7 | P1–P6: 문제/답안 각각 같은 번호 페이지, 답안 마지막 Hint |
| 0923 | 7 | 7 | 8 | P1–P7: 문제/답안 각각 같은 번호 페이지, 답안 마지막 Hint |
| 0928 | 8 | 8 | 9 | P1–P8: 문제/답안 각각 같은 번호 페이지, 답안 마지막 Hint |
| 0930 | 8 | 8 | 9 | P1–P8: 문제/답안 각각 같은 번호 페이지, 답안 마지막 Hint |

## 글자·수식 비교

- 같은 최종 후보의 A4와 16:9 DOM에서 14533개 가시 text node를 대응. 미대응 페이지 0. 최대 화면 크기 차이 0.00007589px (<0.1px).
- 본문 panel, 풀이 solution, display math, Hint 수식의 페이지별 fitting 배율 차이 0. 조밀한 한국어 fixture는 A4의 solution <1 및 동일 화면 크기 검증 통과.
- KaTeX `vlist-s`의 U+200B는 1px 크기 내부 배치 마커이며 가시 글자가 아니므로 text 크기 비교에서 제외했다. PDF 추출 문자 차이는 이 마커와 줄바꿈에 의해 붙는 U+2010 자동 하이픈뿐이었다. 원본 콘텐츠 SHA와 가시 DOM 문자열 대응은 동일하다.
- 래스터 그림 속 글꼴은 CSS 보정 대상이 아니다. 확률표 숫자와 방향 그래프의 라벨/화살표는 확대 PNG로 별도 확인했다.

## 시각 검수

- Poppler `pdftoppm`으로 101쪽 전체를 1440×810 PNG로 저장. 30개 4쪽 contact sheet에서 모든 페이지를 직접 확인했다. 잘림·겹침·깨진 수식·자막 침범 없음.
- 0909 답안 P3/P5 행렬, 0914 P5/P7 긴 수식, 0916 P2–P5 확률표, 0921 P3/P4 방향 그래프와 P6 적분 증명, 0923 P7 4×4 역행렬, 0928 P6/P7 Jacobian, 0930 P3/P6/P7/P8 두 열 증명과 마지막 답안을 확인. 행렬·표·그래프·긴 증명은 개별 원본 PNG로도 확대 확인.
- Hint 부록은 날짜별 답안 마지막 페이지에서 모두 확인. 문제지 필기 공간 및 제작자 표기는 자막 여백 위에 머문다.

## 검증 실행

- baseline PDF tests: 37/37.
- layout 통합 테스트: 8/8 RED→GREEN. build 기본 video/명시 A4와 second PDF failure 검증 통과.
- Task2 PDF tests: 44/44(의도적으로 먼저 작성한 migration RED 테스트 제외). 전체47개 실행에서는 배포 전 A4 산출물 검사만 예상대로 실패; 배포 후 migration3/3 통과.
- 전체 회귀: review124개(122통과·2skip), preview70/70, root53개(31통과·22skip), Node9/9. `git diff --check` 통과. 추가 실제 장문 풀이 pagination 테스트1/1 통과(기존 구현으로 분할·보존됨). 독립 리뷰와 최종 gate는 아래에 기록한다.
- PyMuPDF의 Python3.14 Swig 메타데이터 DeprecationWarning은 기존 의존성 경고이며 실패가 아니다.

## 출처와 SHA

EC2 고정 커밋 `757fa081521008d46542e23d5a1a53112391aed2`의 Git object에서 직접 복사. 런타임 외부 checkout 의존성 없음.

| 파일 | SHA256 |
|---|---|
| `workbook/templates/problem.html` → `pdf-problem.html` | `1ddb009d96f3a844778bd8f4378126d0fd52d037296dff89223adb69bc38bdc7` |
| `workbook/templates/answer.html` → `pdf-answer.html` | `557b30b2918b4b41ff37763c80869ce28ce6b55f81c42e1ce34bfa30af3c1b06` |
| `workbook/templates/video-16x9.css` → `pdf-video-16x9.css` | `d56658538e1b67df08a7eea0282e733afd999c6255e58ecc13cd4c72d13ad870` |

| 산출물 | 파일 | SHA256 |
|---|---|---|
| 0909 problems | `복습문제_0909_Data_Models_Learning-문제.pdf` | `2e403aac32268415c351080933b4549f90bb3e366d0201e2630f07b78b7c7f6a` |
| 0909 answers | `복습문제_0909_Data_Models_Learning-답안.pdf` | `5382bc33ca828b899bcd006eea81b72dcff88cea170c183b8b76aa5887d05795` |
| 0914 problems | `복습문제_0914_ERM_and_MLE-문제.pdf` | `189510ada3c431bb5c782aea94cc2aff6beb1c363b787f2c8a5abb121ef8a377` |
| 0914 answers | `복습문제_0914_ERM_and_MLE-답안.pdf` | `8445d5eb96b93bb988903dd96fb51d09bec68c95c97ba33674eae1db9394e3c4` |
| 0916 problems | `복습문제_0916_MAP_and_Generative_Models-문제.pdf` | `d18c9a9c2e039b4e83ac890e608532eb558ad3741b71437ac9fb6a6982f46491` |
| 0916 answers | `복습문제_0916_MAP_and_Generative_Models-답안.pdf` | `6bbe9b2413034364bef0e0d42abb03021df48dde30236c61933ead001155f57e` |
| 0921 problems | `복습문제_0921_Bayesian_Inference_Model_Selection-문제.pdf` | `a0d70fc6d1b91d3cf0987b02a46d185883e9ae1133dd8163200a79e09cfa1016` |
| 0921 answers | `복습문제_0921_Bayesian_Inference_Model_Selection-답안.pdf` | `fe93a44592ec46fdcd45a696f1c35830aa961471ea294a672992e913377ca59b` |
| 0923 problems | `복습문제_0923_Linear_Regression-문제.pdf` | `af4b5c487978712f73df3df49ed30851956f2186799e2fa1b32130dd75b4002a` |
| 0923 answers | `복습문제_0923_Linear_Regression-답안.pdf` | `c0855dd0f5786a639726d0661e7879f884fea94f90a2fd4d2dd3c14362510010` |
| 0928 problems | `복습문제_0928_Linear_Regression-문제.pdf` | `5cc04e0dcab898be65c1e0836227a1d472ded7aac3040566660f34dad5f3aa2a` |
| 0928 answers | `복습문제_0928_Linear_Regression-답안.pdf` | `646ad8df0d7ae785dcbd1d4367acb0a8b1ad1abfd5ece5406d44e960dc76ebbb` |
| 0930 problems | `복습문제_0930_Bayesian_Linear_Regression-문제.pdf` | `8dbe94b2645f41bac8faaaafa23650b0c9fa5ea921a2d97fbde4b845ee433698` |
| 0930 answers | `복습문제_0930_Bayesian_Linear_Regression-답안.pdf` | `05f36cc737d27a5c580dc41d41fc7305c8f2f7e5a4dd444549e986359a9ebe7a` |

## 백업·근거·실행 판단

- 기존 PDF와 publication 백업: `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.superpowers/sdd/2026-10-07-ml-review-pdf-widescreen/artifacts/originals/`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.superpowers/sdd/2026-10-07-ml-review-pdf-widescreen/artifacts/backups/`.
- 원본 snapshot, stages, comparison: `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.superpowers/sdd/2026-10-07-ml-review-pdf-widescreen/artifacts/{before,stages,comparison}.json`.
- 날짜별 validation/페이지 typography: `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.superpowers/sdd/2026-10-07-ml-review-pdf-widescreen/artifacts/build/<date>/run-*/validation.json`.
- 전체 PNG 및 검수 sheet: `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.superpowers/sdd/2026-10-07-ml-review-pdf-widescreen/artifacts/png/<date>/<mode>/`.
- 같은 feature checkout에서 작업했다. 시작 시 미추적 파일은 설계·계획 두 개뿐이며, 별도 worktree를 만들지 않았다. 동시에 checkout을 수정하는 작업이 있으면 조정이 필요하다는 비용을 감수했다.
- 사용자 별도 승인 전 commit 단계는 보류하고 백업·ledger를 유지했다. Git 이력에 아직 결과가 없으므로 이 scratch를 삭제하면 검증 근거와 백업을 잃는다.
- migration 실패 검사를 Task2 완료 전에 작성했으므로 Task2 gate에서 의도적 artifact 실패를 제외하고 Task3 배포 후 검증했다. 배포 회귀가 Task3까지 보류되는 비용은 migration3/3으로 해소했다.
- 리뷰 도구는 commit range를 요구하지만 commit이 미승인이다. HEAD 대비 tracked diff와 신규 파일 본문을 별도 review package에 담아 현재 checkout 전체를 리뷰한다. 범위 누락 비용은 파일 목록 대조로 막는다.

배포 상태: 7날짜 모두 설치 완료, stage/public PDF bytes 일치, 원본 불변 확인.

## 독립 리뷰 및 수정

Fresh context의 gpt-6-astra reviewer가 Important3건, Critical0·Minor0을 지적했다. 다음 회귀를 모두 RED로 확인한 뒤 한 수정 pass에서 해결했다.

- `test_hint_appendix_math_preserves_a4_scales`: A4에서0.873106으로 줄어드는 Hint 부록 display 수식 배율을 `appendix_math`로 측정·복원한다. 부록 페이지 분포가 달라도 문항 href로 항목 순서에 대응하며 누락 배율은 실패한다.
- `test_real_question_overflow_paginate`: 긴 질문10개를 split하기 전에 caption issue가 먼저 선택되어 실패하던 순서를 수정했다. 의미 블록 넘침을 먼저 분할하고 최종 caption 검사는 유지한다.
- `test_pdf_caption_gate_accounts_for_stroke_width`: y674pt·폭8pt 선의 caption 침범을 stroke paint 범위 확장과 전체 caption raster로 차단한다. fill 도형의 width=None도 기존 wide PDF 통합 테스트로 검증하며0으로 처리한다.
- 추가 보강: 실제 장문 풀이와21개 Hint의 다른 부록 흐름에서 단계/수식 배열 보존을 검사한다.

보완 audit로 기존14개 PDF의101쪽을 stage/public 모두 다시 검사했다. caption raster 전 픽셀255(흰색), A4/wide Hint 부록 display scale도 같았다. 현재 산출물은 위 결함의 영향을 받지 않았으므로 검수된 PDF bytes를 유지했다. 날짜별 validation typography에 이 추가 측정값도 기록했다. 상세 근거는 `artifacts/final-audit.json`이다.

Reviewer가 직접 반복하지 않은101쪽 시각 검수·전체 suite·EC2 object 비교는 이번 세션의 직접 실행 근거를 유지한다. 시각/출처 검증은 작성자의 검사에 의존한다는 제한을 기록하며, 수정 후 전체 suite와 보완 caption/Hint audit를 다시 실행했다. 기존14개 결함 여부를 reviewer가 단정하지 않은 부분은 보완 audit로 모두 통과 확인했다. 재리뷰는 하지 않았고 회귀로 수정 여부를 검증했다.

## 최종 gate

- review129개:127통과·2skip; preview70/70; root53개:31통과·22skip; Node9/9. 합계237통과·24skip, 실패0.
- 최종 `git diff --check` 통과. 근거 로그 `/tmp/ml-fixed-final-{review,preview,root,node}.log`, 보완 PDF audit `/tmp/ml-final-audit.log`.
- 독립 리뷰3건 모두 회귀 RED→GREEN 및 전체 suite로 수정 확인, 보류된 Minor 없음.
- `codex/ml-review-video`에서 미커밋 상태로 보존한다. 설계·계획·보고서 및 코드/테스트/PDF만 변경했고, `.agents/skills/ml-review-pack` symlink와 원본163파일은 그대로다.
