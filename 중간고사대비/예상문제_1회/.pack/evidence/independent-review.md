# 예상문제 1회 행벡터 미분 독립 검토

검토일: 2026-10-20 (Asia/Seoul). 검토자: skill_convention 독립 검토.

대상: `stage/.pack/cards/p1~p10.html`, `explanations/p1~p10.html`, `questions.json`, `solutions.json`, `panel-content.json`, `blueprint.json`. 이전 evidence·검토 pass는 계산의 근거로 사용하지 않았다. 이 검토는 수학과 생성 입력에 한정하며 PDF·브라우저 시각 검토를 수행했다는 뜻이 아니다.

## 직접 검산

새 SymPy 성분 미분과 유리수 계산 29개가 통과했다. 실행 결과·입력 SHA-256은 `independent-checks.json`에 기록했다.

- **p2:** $q=2x_1^2+x_1x_2+x_2^2-x_1$를 직접 미분하면 $(4x_1+x_2-1,\ x_1+2x_2)$이다. 이는 $x^\top A-b^\top$인 $1\times2$ 행벡터다. Jacobian은 $\bigl(\begin{smallmatrix}2x_1&1\\x_2&x_1\end{smallmatrix}\bigr)$로 출력×입력이고, 각 2차 편미분은 Hessian $A$와 같다. 정상조건을 전치하면 $Ax=b$이며 해 $(2/7,-1/7)^\top$를 대입해 확인했다. 대칭 $A$의 선도 주행렬식은 $4,7>0$이므로 유일한 전역 최소점이라는 결론도 맞다.
- **p4 일반 prior:** $S=\Sigma_0^{-1}=S^\top$로 놓고 $\frac1{2\sigma^2}\sum_n(y_n-\sum_j\Phi_{nj}\theta_j)^2+\frac12\sum_{i,j}\theta_iS_{ij}\theta_j$를 성분 미분했다. $j$번째 편미분은 $\sum_n(\Phi\theta-y)_n\Phi_{nj}/\sigma^2+\sum_i\theta_iS_{ij}$이고, 가로로 모으면 $(\Phi\theta-y)^\top\Phi/\sigma^2+\theta^\top S$다. 0으로 놓고 $\sigma^2$를 곱한 다음 전치하면 $(\Phi^\top\Phi+\sigma^2 S)\theta=\Phi^\top y$다. 문제의 수치에서 ML $(5/3,2)^\top$, MAP $(5/4,4/3)^\top$, 두 평균 예측 $17/3,47/12$가 다시 계산됐다. 공분산 대신 그 역행렬이 들어가는 설명과 절편까지 prior 적용하는 조건이 일치한다.
- **p6:** 일반적인 $3\times2$ 기호 행렬로 SSE를 성분 전개·미분했다. $\partial Q/\partial\theta_j=-2\sum_n(y_n-\sum_k\Phi_{nk}\theta_k)\Phi_{nj}$이므로 행 gradient는 $-2y^\top\Phi+2\theta^\top\Phi^\top\Phi$다. 전치 후 정규방정식과 정확히 같았다. 이 성분 항등식은 일반 $N,K$에도 동일하다. 현재 문제는 $K=2$이며 변수는 열벡터다. 정규방정식 유도와 역행렬 존재의 전제를 구분했고, 열독립에 따른 Gram 양의 정부호 증명이 타당하다.
- **p7:** prior의 $j$번째 미분은 $(\theta_j-m_{0j})/\tau^2$이므로 전체 행 gradient는 $(\Phi\theta-y)^\top\Phi/\sigma^2+(\theta-m_0)^\top/\tau^2$다. $\sigma^2$를 곱한 정상조건을 전치하면 $(\Phi^\top\Phi+\lambda I)\theta=\Phi^\top y+\lambda m_0$, $\lambda=\sigma^2/\tau^2$다. 일반 기호 $m_0$로 정확히 검산했다. Hessian은 $\Phi^\top\Phi/\sigma^2+I/\tau^2$이며 열종속이어도 양의 정부호다. 수치 MAP $(5/11,5/11)^\top$와 $\lambda=0$의 비유일성, 각 계수 $5/(10+\lambda)$의 극한도 맞다.

Hessian을 성분 정의로 설명하고 매끄러운 현재 이차식에서 대칭성을 사용하는 것은 행 gradient 관례와 충돌하지 않는다. 열벡터 변수·출력×입력 Jacobian을 행벡터로 바꾼 부분은 발견되지 않았다. p10은 스칼라 $t$에 관한 방향 미분이라 $-2h^\top\Phi^\top r$가 스칼라인 현재 식이 맞으며 열 gradient의 잔재가 아니다.

## 나머지 문항과 원천 일치

- p1: 선형관계·일반해·Gram 역행렬을 다시 확인했다.
- p3: Gaussian 제곱완성·평균 $1/2$·분산 $3/4$·곱 적분 $e^{-1/2}/\sqrt{8\pi}$가 맞다.
- p5: 세 점의 외적에서 공분산을 새로 계산하고 $A\Sigma A^\top$, $\Sigma A^\top$를 정확히 대조했다. 무상관/비독립의 반례 확률도 맞다.
- p8: prior와 두 likelihood의 precision 합 $3/2$에서 posterior 분산 $2/3$를 확인했다. 잠재분산 $8/3$, 미래 관측분산 $14/3$가 맞다.
- p9: evidence 분산 $2,5$, Bayes factor $\sqrt{5/2}$, posterior odds $\sqrt{10}/4<1$, $P(M_1\mid0)\simeq0.44151844$로 사후 선택 $M_2$가 맞다.
- p10: ML $(4/3,1)^\top$, 투영행렬의 대칭·멱등성, 잔차 직교, SSE $2/3$를 재계산했다.
- 위 미분 비대상 6개 문항의 카드·상세 해설 12개 파일은 backup과 바이트 동일함도 확인했다. 이는 답을 바꾸지 않았다는 보존 증거이며 수학 검산은 위와 같이 별도로 수행했다.
- 10개 `questions.origin`과 `blueprint.questions`가 같고, JSON 조건과 풀이 summary가 각각 해당 카드에 포함되는지 검사했다. p2의 panel-content gradient는 행벡터, Jacobian/Hessian 정의는 올바르다. 명시적 전치가 필요한 p2·p4·p6·p7의 카드와 상세 해설 모두 해당 단계를 포함한다.

## 발견 및 상태

1. **Important, p2 understand:** 같은 단락에서 벡터 출력 $f$를 소개한 직후 $\nabla_xf=\partial f/\partial x$를 행벡터로 선언하면 vector Jacobian과 혼동된다. 스칼라 $q$로 바꿔야 한다. 메인에게 즉시 보고했다.
2. **Minor, p6 verify(e):** $K$를 정의하지 않은 현재 두 계수 문제에서 추정량을 $K\times1$로 쓰는 대신 $2\times1$로 명확히 쓰는 것이 적절하다. 원천 JSON와 상세 해설의 대응 항목 확인을 요청했다.

최종 재검토에서 p2의 선언이 스칼라 $q$로 수정됐고, p6의 상세 해설과 원천 solutions.json 모두 $2\times1$로 수정됐음을 실제로 다시 읽었다. 해당 문맥·원천을 재확인한 뒤 `independent-checks.json`의 현재 입력 해시와 발견 상태를 갱신했다. **최종 수학/입력 검토: pass. 미해결 발견 없음.** 이 문서는 실제 PDF 전체 페이지 검수와 별개다.

## 공통 코드 변경 중요 오류 검토

`check_vector_derivatives.py`와 회귀검사, 예상문제 `build_exam.py`/`check_exam.py` 연결, `build_review_pdf.py`의 caption 검증 변경을 실제로 읽었다. 중요한 오류는 발견되지 않았다.

- 검사기는 대표적 열 gradient 패턴 탐지라는 명시된 범위를 갖는다. 행 식·데이터 열벡터·Jacobian·전치 후 정규방정식을 구별하는 현재 검사와 테스트가 일치한다. 완전한 수학 증명이나 모든 수식 판정기로 해석하지 않는다.
- 시험 build/check는 exam_adapter를 먼저 import하고 이 모듈이 두 shared scripts 경로를 추가하므로 새 검사기 import가 해소된다. 생성된 문제·해설 조각에서 위반 발견 시 발행 이전에 실패하는 흐름이다. reference의 NFC/NFD 경로 해결도 기존 resolve를 재사용한다.
- PDF 변경은 image bbox 자체가 흰 자막 영역을 덮는다는 이유만으로 거부하던 한 조건을 제거했다. text·drawing bbox 검사는 유지되고, 해당 영역의 실제 raster 샘플이 하나라도 255보다 작으면 거부하는 gate도 유지된다. 따라서 흰 영역을 포함한 전체 페이지 이미지의 오탐을 해소하면서 실제 이미지 잉크는 계속 거부한다. 템플릿·페이지 규격 변경은 없다.
- 새 규칙/PDF 회귀검사를 직접 실행했다: `python -m pytest --confcutdir=.claude/skills/ml-review-pack/tests --rootdir=.claude/skills/ml-review-pack .claude/skills/ml-review-pack/tests/test_vector_derivatives.py .claude/skills/ml-review-pack/tests/test_pdf_image_caption.py -q` → **15 passed in 0.70s, exit 0**.
- 첫 기본 pytest 호출은 상위 `.claude/skills/ml-interactive`의 기존 깨진 링크를 수집하다 WinError 123으로 실패했다. 위처럼 테스트 루트/설정 탐색 범위를 한정한 뒤 통과했으며, 이를 테스트 실패 수정으로 보고하거나 해당 링크를 변경하지 않았다.
