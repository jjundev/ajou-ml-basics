# 복습팩 문제설명 자동 연결 및 전체 backfill 검증

기존 9팩·63문항·96검토 단위의 문제설명 HTML·MD를 발행했다. 기본 팩 배포 뒤, 완료 보고 전에 `ml-problem-explain` 전체 저작·독립 검산·네 검토·발행 절차를 실행하도록 연결했다. 신규·기존 갱신·lite 모두 명시한 실제 복습문제 HTML 하나를 사용한다. 설명 실패는 기본 팩과 이전 설명을 보존하고 보류로 보고한다.

| 날짜 | 문항 | 검토 단위 | 설명 HTML | MD | 공개 화면 |
|---|---:|---:|---|---|---|
| 0909 | 5 | 7 | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0909/문제설명_0909_Data_Models_Learning.html) | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0909/문제설명_0909_Data_Models_Learning.md) | pass |
| 0914 | 7 | 13 | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0914/문제설명_0914_ERM_and_MLE.html) | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0914/문제설명_0914_ERM_and_MLE.md) | pass |
| 0916 | 6 | 7 | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0916/문제설명_0916_MAP_and_Generative_Models.html) | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0916/문제설명_0916_MAP_and_Generative_Models.md) | pass |
| 0921 | 6 | 11 | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0921/문제설명_0921_Bayesian_Inference_Model_Selection.html) | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0921/문제설명_0921_Bayesian_Inference_Model_Selection.md) | pass |
| 0923 | 7 | 12 | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0923/문제설명_0923_Linear_Regression.html) | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0923/문제설명_0923_Linear_Regression.md) | pass |
| 0928 | 8 | 12 | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0928/문제설명_0928_Linear_Regression.html) | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0928/문제설명_0928_Linear_Regression.md) | pass |
| 0930 | 8 | 9 | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0930/문제설명_0930_Bayesian_Linear_Regression.html) | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/0930/문제설명_0930_Bayesian_Linear_Regression.md) | pass |
| 1007 | 8 | 13 | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/1007/문제설명_1007_Product_of_Gaussians.html) | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/1007/문제설명_1007_Product_of_Gaussians.md) | pass |
| 1012 | 8 | 12 | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/1012/문제설명_1012_Several_Mathematical_Proofs.html) | [열기](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/복습노트/1012/문제설명_1012_Several_Mathematical_Proofs.md) | pass |

## 검증 근거

- 원문 대조: MML PDF의 관련 34쪽을 렌더링해 행렬·표·그래프·조건·소문항을 확인했다. Example 기반 숫자 변형은 원 교과서 문제와 구별해 카드 조건을 기준으로 풀었다. 관련 Lecture01–04와 기존 정리노트의 식을 대조했다.
- 최종 원문 보강: Exercise6.12(c/d) 연속쪽인 PDF230쪽(책224쪽)도 직접 렌더링·대조했다. 0930 P7은(c)의 측정 변환,1012 P6/P7은(d)의 교차공분산·결합분포 중간 단계에 대응한다. 카드가 요청하지 않은 posterior 완성 문제는 추가하지 않았다.
- 수학: 별도 SymPy의 정확 계산·미분·역행렬·잔차 확인과 일반 변수에 대한 증명/정성 검토를 `evidence/verify.py`, `independent-results.json`에 기록했다. 모든 pN:subpart가 포함된다. 숫자 예제로 증명을 대신하지 않았다.
- 내용: understand → recall → start → solve → verify → pitfall → retry 및 요약, 단서·개념·공식·가정·실제 첫 줄·완성 답·검산을 확인했다. 각 자료 폴더에 source snapshot, 저작 스크립트/데이터와 검토 기록을 보존했다.
- 화면: 1280×900 및375×812, light/dark에서 문항252회와 요약252회를 확인했다. 목차·이전/다음·일곱 구역·수식·표·그림·링크를 확인했다. 콘솔/KaTeX/누락 자원/외부 요청/문서 가로 넘침/짧은 인라인 스크롤/보이는 수식 스크롤바 모두0이었다. 긴 Gaussian 곱은 두 이차형식을 먼저 정의해 줄을 나눴다.
- 증거를 산출물에 묶는 마지막 build는 화면 내용과 런타임 자원 bytes를 바꾸지 않았다. 실제 브라우저에서 본 HTML SHA와 모든 JS/CSS/폰트/그림 SHA가 최종 stage 및 공개 파일과 같음을 별도 audit했다. 이전 승인을 재사용하지 않고 not_run에서 현재 입력/조각/참조/산출물 해시에 새 검토를 기록했다.
- 공개 HTML·MD·manifest·validation의 입력·문항·소문항·참조 해시와 현재 파일 해시를 실제 납품 회귀 검사로 확인했다. validation.json은 발행기가 저장하며 자체 owned hash 목록에 넣지 않았다.

## 원본 보존과 가정 보완

- 원본 문제/노트/PDF/기존 그림·제작자료/workbook layouts/STT/교안/MML/과제1 설명 등495개 파일의 SHA-256을 작업 전후 대조했다. 변경0개. JSON 보고서에 전체 baseline과 inventory를 보존했다.
- 기울기의 가파르기는 절댓값, 그래프의 부모 없음은 주변 독립과 다름, 고차 정규화의 효과는 해당 예제의 경향, σ≠0/유한 모멘트/full rank/독립 새 잡음 등의 가정을 설명의 주의사항으로 명시했다. 원 카드의 간략 표현은 수정하지 않았다.
- 0921 설명 HTML의418·441행 끝 공백2개는 복사된 원 SVG에 있던 공백이다. 원본을 조용히 고치지 않고 보존했다. 새 파일을 포함한 별도 whitespace 검사에서 이를 확인했다. 현재 추적 파일 git diff --check는 통과하며, 향후 이 HTML을 stage하면 해당 두 줄은 별도 판단이 필요하다.

## 실행과 회귀 검사

- Python: `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/tmp/ml-explain-env/bin/python` (3.14.8), 임시 venv의 pytest/playwright/PyMuPDF/SymPy/Pillow. production CLI는 Python3.10+ 표준 라이브러리 유지.
- `python -m unittest discover -s .claude/skills/ml-review-pack/tests -q`: 153개 실행,151통과·2생략. 생략은 `TestRegression.test_contract_checks_pass`, `test_markdown_has_no_missing_tokens`로 옛0909-0916 통합HTML이 현재 저장소에 없어 발생했다.
- `python -m pytest .claude/skills/ml-problem-explain/tests -q`: 74통과. 최신 선택 고정값1007의 기존 환경 의존 실패를1007/1012 임시 fixture로 고립했다.
- RED→GREEN: 연결 reference 부재 실패→지침 연결 후 통과;0909 실제 설명 파일 없음 실패→발행 후 통과;나머지8개 없음 실패→전체 발행 후 통과.
- 명시 경로가 더 최신/다른 slug에 밀리지 않음, 전체 문항·소문항, 미검토 발행 거부, stale-input/참조/조각 거부, 일부 팩 독립 실패, 교체 rollback, labels/수식/원문 보존 회귀가 통과했다.

## 작업 기록

- 전용 브랜치: `codex/ml-review-explain`. 기존 checkout에서 작업했고 커밋/푸시는 요청되지 않아 검토 가능한 변경으로 남겼다.
- RUN: `tmp/ml-problem-explain/backfill-20261013/<date>/`. 팩마다 독립 추출 폴더와 UUID stage 및 backups를 사용했다. JSON의 packs 행에 실제 RUN·백업·현재 공개 경로를 기록했다.
- 첫0909 발행 후 개선판은 고유 백업으로 교체했다. 나머지는 첫 발행이었다. 기존 과제1 설명을 변경하지 않았다.
- 임시 venv/RUN과 실행 ledger는 로컬 git exclude로 제외했다. 커밋 이력이 없으므로 재개·검증 근거를 잃지 않도록 임시 실행 자료를 유지했다.

## 최종 독립 리뷰

신선한 문맥의 gpt-6-astra 리뷰어가63문항·96검토 단위의 조건·답·일반 증명을 직접 대조했다. 수학 풀이·현재 발행 결과를 막는 결함은 없었다. Important1개와 Minor2개를 보고했고, 판단에서 제외한 항목은 없었다.

- Important: 납품 테스트의 절대 경로 종속을 수정했다. 다른 home/checkout으로0909를 복사한 실패를 먼저 재현한 뒤, 원 기록은 그대로 두고 저장된 repo 기준 상대 경로를 현재 ROOT에 대응시켰다. 복사본의 임시 manifest 보기만 경로를 변환해 구조 검사한다. 원 manifest/승인 bytes·해시 불변을 검사하며, 이동한 참조나 MD 변조도 거부한다. 실제 납품/이동/변조12검사 및 전체 설명74검사가 통과했다.
- Minor(보류): understand는 짧은 제목 요약이라 조건·목표를 자기 말로 더 풀어 주면 좋다. 정확한 조건·질문이 바로 위에 있고 recall/start가 구체적이라 중요한 누락으로 판정하지 않았다.
- Minor(보류): recall/start의 일부 f\prime/f\prime\prime은 prime이 본문 높이에 조판된다. 미분 계산과 풀이의 답은 맞다. 향후 저작 데이터의 조판 개선 항목으로 남겼다.
- 원 SVG 끝 공백2곳은 기능·표시 영향이 없어 결함으로 분류하지 않았다. 현재 공개9팩의 모든 검토 상태는pass다.

최종 수정 뒤 재검증: 문제설명74통과(이동·변조 감사 포함), 복습팩153개 실행151통과·2기존자료 생략. 독립 리뷰 Important 수정 완료, Minor2개 보류.
