# 벡터 미분 관례: 문제부터 PDF까지

이 과목에서 새로 저작하는 스칼라 목적함수의 미분은 **행벡터**다. 열벡터인 변수 자체와 미분 결과의 방향은 별개다. 정리노트·문제 조건·힌트·참고 풀이·상세 해설·summary/sum·terms·MD·PDF와 이를 재생성하는 카드·JSON·소개 문구에 같은 관례를 적용한다. 작성자와 검토자는 이 파일 전체를 읽는다.

## 원문 조건 먼저 판정

| 입력 상태 | 작성·수정 방법 |
|---|---|
| 새 문제, 또는 방향을 지정하지 않은 기존 문제 | 강의의 행벡터 미분을 사용한다. |
| 기존 원문이 열벡터 미분을 명시하고, 사용자는 해설만 요청 | 원문·조건을 보존하고 해당 문항의 명시적 관례를 따른다. understand와 요약에 강의와의 차이를 밝히고 행·열 식을 연결한다. 이 차이만으로 수학 오류나 disputed로 판정하지 않는다. |
| 사용자가 문제와 해설의 관례 통일까지 명시적으로 요청 | 요청한 생성 원본·조건·풀이·MD·PDF를 함께 수정하고 전치 관계를 검산한다. 강의·교재·과제 원 PDF 등 출처 원문은 보존한다. |
| 원문 관례나 수식 의미가 불명확 | 원자료를 대조하고 미해결 수학적 충돌은 기존 disputed 규칙으로 처리한다. |

수치 답이 같거나 열 gradient가 수학적으로 유효하다는 이유만으로 새 과목 자료에 열 관례를 선택하지 않는다. 반대로 행 관례가 기본이라는 이유로 제공된 원문 조건을 몰래 변경하지 않는다.

카드가 manifest의 `answer`를 그대로 따라야 하는 계약도 유지한다. 승인된 관례 전환으로 기호 답의 방향이 바뀌면 메인이 먼저 manifest·정답 원본을 동치인 행 식으로 갱신·검산하고 작성자에게 확정본을 전달한다. 작성자가 기존 계약과 다른 방향을 카드에서만 몰래 쓰지 않는다. 최종 추정량의 수치·의미는 별도로 보존·대조한다.

## 공식과 차원

변수 $x\in\mathbb R^{d\times1}$, 스칼라 $f$에 대해

$$\nabla_x f:=\frac{\partial f}{\partial x}
=\begin{pmatrix}\partial f/\partial x_1&\cdots&\partial f/\partial x_d\end{pmatrix}
\in\mathbb R^{1\times d}.$$

| 함수·대상 | 이 과목의 미분 |
|---|---|
| $x^\top x=\|x\|^2$ | $2x^\top$ |
| $b^\top x$ | $b^\top$ |
| $x^\top Ax$ | $x^\top(A+A^\top)$ |
| $\frac12x^\top Ax-b^\top x$, $A=A^\top$ | $x^\top A-b^\top$ |

벡터값 함수 $g:\mathbb R^d\to\mathbb R^m$의 Jacobian은 $J_{ij}=\partial g_i/\partial x_j$인 **출력×입력** $m\times d$를 유지한다. Hessian은 $H_{ij}=\partial^2 f/(\partial x_i\partial x_j)$로 정의한다. 행 gradient를 단순히 출력 벡터처럼 다시 Jacobian에 넣어 방향을 추측하지 말고, 성분 정의 또는 열벡터 $(\nabla_xf)^\top$의 Jacobian으로 설명한다. 실제 행렬곱 $A^2=AA$의 미분을 벡터 길이 제곱의 미분 $2x^\top$과 혼동하지 않는다.

## 한 유도 안에서 전치까지 보여 주기

$\Phi\in\mathbb R^{n\times d}$, $\theta\in\mathbb R^{d\times1}$, $y\in\mathbb R^{n\times1}$일 때 최소제곱은

$$Q=\|y-\Phi\theta\|^2,\qquad
\nabla_\theta Q=-2(y-\Phi\theta)^\top\Phi
=-2y^\top\Phi+2\theta^\top\Phi^\top\Phi\in\mathbb R^{1\times d}.$$

$$\nabla_\theta Q=0_{1\times d}
\Rightarrow\theta^\top\Phi^\top\Phi=y^\top\Phi
\xRightarrow{\text{양변 전치}}\Phi^\top\Phi\theta=\Phi^\top y.$$

가우시안 MAP의 $J=\|y-\Phi\theta\|^2/(2\sigma^2)+\|\theta-m_0\|^2/(2\tau^2)$에서는

$$\nabla_\theta J=\frac{(\Phi\theta-y)^\top\Phi}{\sigma^2}
+\frac{(\theta-m_0)^\top}{\tau^2}\in\mathbb R^{1\times d}.$$

0으로 놓은 행벡터 식을 먼저 쓴 뒤 **양변을 전치하여** 열벡터 정규방정식을 얻었다고 적는다. 원래 행벡터 미분을 생략하고 최종 열 방정식만 제시하지 않는다. 필요할 때 역행렬의 존재 조건도 확인한다.

## 필수 검증 기록

검토 근거에 `변수 차원 / 미분 결과 차원 / 곱 순서 / 전치 단계 / 원문 보존 또는 수정 권한 / 동기화 파일`을 남긴다. 본문뿐 아니라 문제 조건·summary/sum·terms·힌트·생성기 소개·카드/JSON·MD·문제 PDF·답안 PDF를 대조한다. 기존 통과 기록·정답 값의 일치만으로 새 검토를 승인하지 않는다. 캐시가 열 관례이면 원천 조각부터 고친 뒤 다시 조립한다.

행 관례로 새로 저작한 HTML·MD(조각 포함)는 다음도 실행한다. 저장소 루트 기준 명령이며 환경에 따라 `python3`를 사용할 수 있다.

```sh
uv run python .claude/skills/ml-review-pack/scripts/check_vector_derivatives.py <저작한 HTML/MD 경로...>
```

검사기는 대표적 열 gradient 선언·식을 찾는 보조 도구이며 모든 수학적 오류를 증명하지 않는다. 보존할 열 관례 원문·인용까지 일괄 입력하지 않는다. 명시적 열 관례 문항은 수동으로 원문 일치와 전치 대응을 검토하고 이유를 기록한다. 검사 통과 후에도 차원·성분 검산과 실제 PDF의 전체 페이지 시각 검수가 필요하다.
