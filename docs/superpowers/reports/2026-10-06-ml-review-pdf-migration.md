# 머신러닝기초 복습문제 PDF 마이그레이션 검증 보고서

2026-10-06. Native 구현. 전자회로2 템플릿을 변경 없이 재사용했다. 기존 47문항/7개 날짜의 PDF 14개를 생성하고, 향후 생성 스킬에 같은 빌드/검증/배포 계약을 추가했다.

## 출력 및 시각 검수

| 날짜 | 문항 | 문제지 쪽 | 해설지 쪽 |
|---|---:|---:|---:|
| 0909 | 5 | 5 | 6 |
| 0914 | 7 | 7 | 8 |
| 0916 | 6 | 6 | 7 |
| 0921 | 6 | 6 | 7 |
| 0923 | 7 | 7 | 8 |
| 0928 | 8 | 8 | 9 |
| 0930 | 8 | 8 | 9 |

총 101쪽(문제47+해설54). 해설에는 날짜마다 Hint 한 쪽이 포함된다. 각 논리 문제는 본체 한 쪽에 들어갔으며 실제 이관 결과에는 추가 계속 페이지가 필요하지 않았다. 분할 기능은 별도 용량 제한 테스트로 검증했다.

PyMuPDF 1.5배 PNG로 모든 페이지를 렌더링했다. 날짜/모드별 30개 contact sheet의 모든 페이지를 직접 검사했다. 확률표 15개 값/행열 라벨, 방향 그래프 네 화살표/다섯 노드, 4×4 행렬, 장문 증명, 한국어와 수식, 원문/조건/구할 것, 점 격자 필기 공간, 최종 답과 Hint 부록의 잘림·겹침을 확인했다. DOM resource/font/KaTeX/image/geometry gate와 A4 가로 크기·페이지 수·텍스트 검사를 모두 통과했다.

## 원본과 링크 보존

기존 복습문제 HTML/MD와 figures의 SHA-256은 각 workbook/layouts JSON에 고정했다. 이관 전후 bytes를 대조했다. 정리노트는 링크 토픽에 PDF 링크를 넣고 해당 기존 HTML/MD 링크의 잘못된 문항 수만 고쳤다(0909 7→5, 0914 8→7, 0916 7→6). 본문 수식 순서가 같음을 대조했으며 전체 Markdown 재변환은 하지 않았다. 원본 복습문제 소개문처럼 범위 밖의 잘못된 문항 수는 변경하지 않았다.

템플릿 SHA-256:

- problem: `431fdafcd3bce6d86b2bb7881ed4332e6287a9b8c6bd8626628f9e673a4d2655`
- answer: `4d3a13379d759ae8b1b48dd27417919929b4e0bf94a686a7362b79719e949040`

## 문항별 정답 대조

34개 수치/보조 검사는 Fraction·행렬 곱/가우스 소거·독립 잔차·중앙차분으로 실행했다. 13개 기호 문제는 아래 전제/단계를 수동 대조했다. 중앙차분은 기호 증명의 대체가 아닌 보조 검사다. 원본 문제·풀이·정답 문구는 변경하지 않았다.

| 문항 | 검증 방법/결과 |
|---|---|
| 0909-p1 | [-10, 5, 20] |
| 0909-p2 | 3x2 times 3x3: undefined |
| 0909-p3 | [[[Fraction(4, 1), Fraction(3, 1), Fraction(5, 1)], [Fraction(10, 1), Fraction(9, 1), Fraction(11, 1)], [Fraction(16, 1), Fraction(15, 1), Fraction(17, 1)]], [[Fraction(5, 1), Fraction(7, 1), Fraction(9, 1)], [Fraction(11, 1), Fraction(13, 1), Fraction(15, 1)], [Fraction(8, 1), Fraction(10, 1), Fraction(12, 1)]]] |
| 0909-p4 | [[Fraction(14, 1), Fraction(6, 1)], [Fraction(-21, 1), Fraction(2, 1)]] |
| 0909-p5 | [[Fraction(12, 1), Fraction(3, 1), Fraction(-3, 1), Fraction(-12, 1)], [Fraction(-3, 1), Fraction(1, 1), Fraction(2, 1), Fraction(6, 1)], [Fraction(6, 1), Fraction(5, 1), Fraction(1, 1), Fraction(0, 1)], [Fraction(13, 1), Fraction(12, 1), Fraction(3, 1), Fraction(2, 1)]] |
| 0914-p1 | 9/2 |
| 0914-p2 | [Fraction(2, 3), Fraction(1, 2)] |
| 0914-p3 | [0, Fraction(5, 3), 5, Fraction(11, 3)] |
| 0914-p4 | mean=5 variance=1 |
| 0914-p5 | [3.757, 3.507] |
| 0914-p6 | 4.69041575982343 |
| 0914-p7 | -2 ± sqrt5; min/max; 17 ∓ 10sqrt5 |
| 0916-p1 | 정규화 가우시안의 -log: D/2 log(2π)+1/2 log|Σ|+1/2 θᵀΣ⁻¹θ; θ와 무관한 항 제외, posterior 곱의 음의 로그 합 확인. |
| 0916-p2 | [Fraction(4, 25), Fraction(17, 100), Fraction(11, 100), Fraction(11, 50), Fraction(17, 50)] |
| 0916-p3 | [Fraction(13, 50), Fraction(47, 100), Fraction(27, 100)] |
| 0916-p4 | [Fraction(1, 26), Fraction(1, 13), Fraction(3, 26), Fraction(5, 13), Fraction(5, 13)] |
| 0916-p5 | [Fraction(3, 11), Fraction(5, 11), Fraction(3, 11)] |
| 0916-p6 | posterior Beta(alpha+k,beta+N-k); example Beta(6,12), mode5/16 |
| 0921-p1 | p(c|a,b), p(b|a), p(a)의 조건변수 확인. 여기서 의존은 DAG의 부모 관계이며 root가 자손과 통계적으로 독립이라는 뜻으로 읽으면 안 됨. |
| 0921-p2 | a→b, a→c, b→c; 3개 노드쌍/3개 화살표 확인. |
| 0921-p3 | 실제 SVG의 4개 화살표 x1→x3, x2→x3, x5→x2, x2→x4와 각 부모 집합 및 5개 분포 대조. |
| 0921-p4 | 같은 그래프의 부모에 따른 p(x1)p(x5)p(x2|x5)p(x3|x1,x2)p(x4|x2) 확인. |
| 0921-p5 | 1/3 |
| 0921-p6 | 조건부 기대 정의, p(x|y)p(y)=p(x,y), 주변화 및 적분 순서 교환. 기댓값/적분이 존재하는 통상 전제에서 확인. |
| 0923-p1 | [21, 40, Fraction(40, 21), Fraction(38, 21)] |
| 0923-p2 | [6, 12, 2] |
| 0923-p3 | [5] |
| 0923-p4 | [-7] |
| 0923-p5 | rank A=3 augmented=4: empty |
| 0923-p6 | rank2: singular |
| 0923-p7 | A*inv=inv*A=I (16 cells each) |
| 0928-p1 | [[1, -1, 1], [1, 1, 1], [1, 2, 4]] |
| 0928-p2 | K4 / 8x4 / normal equation (full rank) |
| 0928-p3 | 4/25 |
| 0928-p4 | central difference 3 points + product/chain-rule derivation; x != 0 |
| 0928-p5 | central difference 3 points + chain rule; sigma != 0 |
| 0928-p6 | row Jacobian: 2x^T/(1+x^Tx), diag(cos z) A, correct 1xD and ExD |
| 0928-p7 | diag(1-tanh² z) A, MxN; chain rule |
| 0928-p8 | 3 central differences + algebraic sigmoid identity |
| 0930-p1 | Cov(X,X²)=E[X³]-E[X]E[X²]=0; 비퇴화 예제에서 함수적 종속과 무상관 구별. |
| 0930-p2 | 기대의 선형성, 상수배 공분산의 제곱 계수, 독립성으로 교차항0, 주어진 Gaussian 폐쇄성 확인. |
| 0930-p3 | 동일한 측정 이력에 조건을 두고 Aμt와 AΣtAᵀ+Q; 미래 process noise가 측정 이력과 독립인 표준 상태공간 전제에서 단계 확인. |
| 0930-p4 | (x-μ)² 전개, E[x]=μ 대입으로 E[x²]-μ²; 유한 2차 모멘트 전제. |
| 0930-p5 | x를 고정하면 Ax+b 상수, 독립 w의 평균0/공분산Q 유지. 조건부 Gaussian 확인. |
| 0930-p6 | y=Ax+b+w 평균/공분산을 직접 전개; 독립성으로 교차항0, 최종 Aμx+b와 AΣxAᵀ+Q 확인. |
| 0930-p7 | 한 번 더 C 변환과 독립 v 추가: Cμy와 CΣyCᵀ+R, 원래 μy/Σy 대입, 각 차원 확인. |
| 0930-p8 | exact Fraction pairwise identity for 3 datasets; symbolic expansion checked |

0928 P3(b)의 높은 차수에서 정규화 효과가 더 크다는 설명은 해당 교과서 예제의 경험적 설명으로 읽는다. 임의 데이터에 대한 보편 정리는 아니다. 0928 P4는 x≠0, P5는 σ≠0인 정의역에서 미분을 대조했다. 문제 자체의 암묵적 정의역과 통상 확률 전제를 검증 한계로 명시하며 새 조건을 본문에 만들지 않았다.

## 회귀 검사

```text
final-skill-suite.log
test_referenced_files_exist (test_skill_files.TestSkillFiles.test_referenced_files_exist) ... ok
test_steps_present (test_skill_files.TestSkillFiles.test_steps_present) ... ok

----------------------------------------------------------------------
Ran 109 tests in 18.393s

OK (skipped=2)
```

```text
final-preview-suite.log
test_relative_symlink_to_review_template (test_preview_template.TestSharedTemplate.test_relative_symlink_to_review_template) ... ok
test_slots (test_preview_template.TestSharedTemplate.test_slots) ... ok

----------------------------------------------------------------------
Ran 70 tests in 0.086s

OK
```

```text
final-root-suite.log
test_stationary_points (test_review_answers.TestExercise71.test_stationary_points) ... ok
test_lambda (test_review_answers.TestMapL2.test_lambda) ... ok

----------------------------------------------------------------------
Ran 47 tests in 0.430s

OK (skipped=22)
```

```text
final-node-suite.log
ℹ suites 0
ℹ pass 9
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 43.453458
```

ml-review-pack의 기존 skip 2개와 root의 legacy skip22개는 현재 없는 과거 통합 팩을 대상으로 한 검사다. 이들을 실제 회귀 통과로 세지 않는다. 현재 7개 날짜의 HTML·47카드·PDF·노트/MD 링크와 원본 해시 검사를 추가했다.

## 배포/복구 및 실행 기록

검증 동안 별도 detached worktree에서 작업했다. 2번째 PDF 실패는 공개 파일을 쓰지 않으며, 파일 교체 실패는 이전 bytes로 복구하는 테스트를 통과했다. 누락 stage 파일/동시 배포 lock/낡은 source hash도 실패로 차단한다. kernel flock이 descriptor 수명에 따라 소유권을 유지하므로 live lock 파일을 삭제하지 않는다. 다중 파일 OS 원자성은 주장하지 않는다.

격리 checkout의 백업: `work/ml-review-pdf/backups-checkout/`. 과목 폴더 반영 시 별도 백업과 변경 파일 SHA 대조를 수행한다. 커밋·푸시는 하지 않는다. 독립 최종 리뷰/반영 후 결과를 이 보고서에 추가한다.

실행 판단과 비용은 별첨 실행기록에 모두 남긴다.

## 2026-10-07 독립 리뷰 및 수정

새 문맥의 리뷰어가 Critical 0개, Important 4개, 목록 번호 형식 Minor 1개를 찾았다. 목록 번호는 원문 소문항 대응에 영향을 주므로 Important로 재분류했다. 긴 인라인 행렬의 잘림 검사, 원본 기준 상대 PNG 경로, 과목 상대 경로를 유지하는 stage, 인라인 강조 태그에서 문장 분할하지 않는 규칙, ol type/start/reversed/value 보존을 한 번의 수정 패스로 처리했다. 각각 실패 재현 후 통과를 확인했다. CLI 실패 보고서가 과거 성공을 남기는 문제도 같은 패스에서 실패 재현 후 고쳤다.

수정 뒤 기존 14개 payload를 전부 실제 Chrome에서 다시 측정했고 새로운 인라인/콘텐츠 경계 검사에서 오류가 없었다. 기존 PDF bytes와 템플릿 bytes는 바뀌지 않았다. 미래 계약의 실제 0930 자료 8문항을 structured cards로 준비하여 stage의 지난 노트/강의 링크, PDF 쌍, HTML→MD 변환/수식·링크 검사를 끝까지 실행했다(24개 정적 그림). 이는 임시 smoke이며 기존 복습문제/figures를 교체하지 않았다.

최종 회귀: skill114개 중112개 통과/과거자료 skip2개; preview70개 통과; root47개 중25개 통과/과거자료 skip22개; JS9개 통과. 과거자료 skip을 실제 통과 수에 넣지 않았다. 합계 Python207개 + JS9개가 실행되어 통과했다.

보류한 신규 Minor는 없다. 기존 연결 안내 문구의 금지/필수 충돌과 초기 백업 스니펫의 old/new 동일 이름 deduplication은 기존 지침에 남아 있다. 실제 publisher 백업은 덮어쓰는 파일을 별도로 보존한다. 공통 Hint 라벨과 말줄임/목록/계속 페이지 번호 표시는 사용자 요구에 따라 EC2 템플릿 그대로다. 구현은 확인된 macOS/POSIX 환경을 대상으로 하며, 프로세스 강제 종료나 디스크 고장까지의 다중 파일 원자성은 보장하지 않는다.

## 과목 폴더 반영 결과

2026-10-07, 검증된 71개 파일을 기존 과목 폴더에 반영했다. 분기는 `codex/ml-review-video` 그대로이며 커밋·푸시·merge를 수행하지 않았다. 다른 작업의 `.agents/skills/ml-stt/`, `tests/test_ml_stt.py`는 보존했다. 기존 복습문제 HTML/MD와 그림149개 파일의 원본 SHA가 반영 후에도 일치하며, 최종 PDF14개/101쪽과 outputs 사본의 bytes도 모두 같다. 정리노트의 두 PDF href는 실제 Chrome DOM에서 날짜별로 정확한 파일을 가리키는 것을 확인했다.

백업: `/Users/hyunjun_macbook_pro/Documents/Codex/2026-10-06/2-pdf-x20-x20-2-2/work/primary-publication-backups`. 변경 대상의 기존 bytes를 설치 직전 대조했고, 설치된 모든 파일을 사본과 대조했다.

설치된 과목 폴더에서 실행한 검증:

```text
installed-skill-suite.log
test_referenced_files_exist (test_skill_files.TestSkillFiles.test_referenced_files_exist) ... ok
test_steps_present (test_skill_files.TestSkillFiles.test_steps_present) ... ok

----------------------------------------------------------------------
Ran 114 tests in 25.862s

OK (skipped=2)
```

```text
installed-preview-suite.log
test_relative_symlink_to_review_template (test_preview_template.TestSharedTemplate.test_relative_symlink_to_review_template) ... ok
test_slots (test_preview_template.TestSharedTemplate.test_slots) ... ok

----------------------------------------------------------------------
Ran 70 tests in 0.086s

OK
```

```text
installed-root-suite.log
----------------------------------------------------------------------
Ran 53 tests in 0.598s

OK (skipped=22)
Master transcript successfully created: /var/folders/t7/zhvnpb1j4tb2pszpcnhlnt2h0000gn/T/tmpud2n1py_/1005 머러기.md
Master transcript successfully created: /var/folders/t7/zhvnpb1j4tb2pszpcnhlnt2h0000gn/T/tmpud2n1py_/1005_merged2.md
Master transcript successfully created: /var/folders/t7/zhvnpb1j4tb2pszpcnhlnt2h0000gn/T/tmpud2n1py_/1005_merged3.md
```

```text
installed-node-suite.log
ℹ suites 0
ℹ pass 9
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 44.03125
```

실행 판단은 별첨 `2026-10-06-ml-review-pdf-execution-record.md`에 남겼다. 신규 기능의 미해결 Critical/Important/Minor는 없다.
