# 내적에서 행렬 사영으로

대상: 1104 정리노트 `s1-projection`(기저를 고정하고 좌표 구하기), `s1-discarded`(버린 방향에서 복원오차 계산하기) 및 1102 정리노트 `s1-matrix-again`(1.2 행렬로 다시 쓰는 사영 좌표). 표준 단위기저에서 내적으로 성분을 읽던 직관($\mathbf{x}=x_1\mathbf{e}_1+x_2\mathbf{e}_2$)에서 출발해, 회전된 정규직교 기저 하나와의 내적($z_1=\mathbf{b}_1^\top\mathbf{x}$, 직선 사영)이 어떻게 열벡터들을 기둥으로 나란히 세운 행렬 곱($\mathbf{z}=\mathbf{B}^\top\mathbf{x}$, 평면 사영)과 가중합 복원($\tilde{\mathbf{x}}=z_1\mathbf{b}_1+z_2\mathbf{b}_2=\mathbf{B}\mathbf{z}$), 그리고 버린 수직 축의 잔차($\mathbf{x}-\tilde{\mathbf{x}}=z_3\mathbf{b}_3$)로 확장되는지 확인한다.

조작 변수:
- 직선 모드(2차원 회전 기저, $D=2$): 기저 회전각 $\theta$(0–175°, 5°), 점 좌표 $x_1, x_2$(−4–4, 0.1).
- 평면 모드(3차원 부분공간 사영과 행렬 $\mathbf{B}$, $D=3$): 남길 기저 개수 $M\in\{1,2\}$ 버튼 전환, 평면 수평 회전각 $\theta$(0–175°, 5°), 평면 기울기 $\phi$(−60–60°, 5°), 3차원 점 좌표 $x_1, x_2, x_3$(−3–3, 0.1).
- 보기 옵션: 이름표, 성분 분해선($z_1\mathbf{b}_1, z_2\mathbf{b}_2$ 평행사변형 보조선).

관찰할 변화:
- 직선 모드에서 $\theta=0^\circ$이면 $z_1=x_1, z_2=x_2$로 표준기저 내적과 일치하고, $\theta$를 돌려도 정규직교 기저이므로 $z_1\mathbf{b}_1+z_2\mathbf{b}_2=\mathbf{x}$와 $\|\mathbf{x}\|^2=z_1^2+z_2^2$가 항상 성립한다. 첫 축 하나($M=1$)만 남기면 $\tilde{\mathbf{x}}=z_1\mathbf{b}_1$이 직선 위 가장 가까운 사영점이 되고, 버린 둘째 축 성분 $z_2\mathbf{b}_2$가 곧 직각 잔차 $\mathbf{x}-\tilde{\mathbf{x}}$가 된다.
- 평면 모드에서 $M=1$이면 열 1개짜리 $\mathbf{B}=[\mathbf{b}_1]\in\mathbb{R}^{3\times 1}$이 만드는 직선에 사영되어 $\tilde{\mathbf{x}}=z_1\mathbf{b}_1$이고, $M=2$로 바꾸면 열 2개를 나란히 세운 $\mathbf{B}=[\mathbf{b}_1\ \mathbf{b}_2]\in\mathbb{R}^{3\times 2}$가 만드는 평면에 사영되어 1층 내적 성분 $z_1\mathbf{b}_1$과 2층 내적 성분 $z_2\mathbf{b}_2$의 벡터합이 평면 위 그림자 점 $\tilde{\mathbf{x}}=\mathbf{B}\mathbf{z}$가 된다.
- 버린 법선 방향 성분(평면 모드 $M=2$에서는 $z_3\mathbf{b}_3$, $M=1$에서는 $z_2\mathbf{b}_2+z_3\mathbf{b}_3$)이 곧 복원 잔차 $\mathbf{x}-\tilde{\mathbf{x}}$이며, 남긴 부분공간의 모든 축과 수직($\mathbf{B}^\top(\mathbf{x}-\tilde{\mathbf{x}})=\mathbf{0}$)이고 $\|\mathbf{x}\|^2=\|\tilde{\mathbf{x}}\|^2+\|\mathbf{x}-\tilde{\mathbf{x}}\|^2$가 성립한다.

모드: 직선(그래프, $D=2$, 평면 정면 고정, playback 없음), 평면(그래프, $D=3, M\in\{1,2\}$, 3차원 회전 가능, playback 없음), 수식(수식 전개형: 표준기저 내적 → 단일 단위벡터 내적과 크기 보정 → 열벡터 묶음 $\mathbf{B}$와 전치 $\mathbf{B}^\top$ → 층별 내적 $\mathbf{z}=\mathbf{B}^\top\mathbf{x}$ → 가중합 복원 $\tilde{\mathbf{x}}=\mathbf{B}\mathbf{z}$ → 남긴 성분과 버린 성분의 직교 분해).

출처: Lecture05 실제 PDF 11–12쪽·15쪽, Lecture06 실제 PDF 5–10쪽, 1102 STT P02(행렬 표기와 차원), 1104 STT Part 06(평면 점 (6,8) 내적 예와 정규방정식)·Part 07(버린 방향 잔차 전개), 정리노트 1104 `s1-projection`·`s1-discarded`, 정리노트 1102 `s1-matrix-again`, 정리노트 1028 `s4-code`·`s5-encoder-decoder`, MML 10.1–10.3절(실제 PDF 323–331쪽).

학습용 예시: 질문의 $\mathbf{x}=(3,4)$와 1104 수업 칠판 예 $\mathbf{x}=(6,8)$을 직선 모드 단계 preset으로 넣는다. 3차원 평면 모드는 $\mathbf{x}=(2, 1.5, 2)$를 기본점으로 두고 바닥 평면($\theta=0^\circ, \phi=0^\circ$)과 기울어진 평면($\theta=30^\circ, \phi=20^\circ$)을 비교한다.

단순화와 보충: 3차원 평면 기저 $\mathbf{b}_1,\mathbf{b}_2,\mathbf{b}_3$는 $z$축 회전 $R_z(\theta)$ 뒤 $x$축 기울기 $R_x(\phi)$를 곱한 회전행렬의 세 열로 만들어 언제나 정규직교($\mathbf{B}^\top\mathbf{B}=\mathbf{I}$)가 유지되게 한다.

중복 확인: 1028 03번(`정규직교와 code`)은 $\|\mathbf{b}\|\neq 1$과 $\phi\neq 90^\circ$로 정규직교 조건을 깨뜨려 $\mathbf{z}$와 사영 계수 $\boldsymbol{\lambda}$의 괴리를 보는 실험이고, 1102 01번(`사영 분산과 첫 주성분`)은 점 구름 40개의 분산 $V_1=\mathbf{b}_1^\top\mathbf{S}\mathbf{b}_1$을 최대화하는 실험이다. 이 자료는 정규직교 기저에서 단일 벡터 내적이 열벡터 묶음 행렬 $\mathbf{B}\in\mathbb{R}^{D\times M}$의 평면 사영($\mathbf{z}=\mathbf{B}^\top\mathbf{x}, \tilde{\mathbf{x}}=\mathbf{B}\mathbf{z}$)과 직교여공간 잔차($\sum_{j>M}z_j\mathbf{b}_j$)로 확장되는 과정을 다룬다.

검증: 독립 검산은 `evidence/verify.py`(Fraction 및 NumPy 직교사영·잔차·피타고라스 검산), 설명 감사는 `evidence/audit.md`, 화면은 `evidence/qa.cjs`.
