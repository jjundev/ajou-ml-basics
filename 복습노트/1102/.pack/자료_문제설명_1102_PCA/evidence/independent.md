# 1102 PCA 복습문제 독립 검산

- 근거는 origin/main의 1d0da4d1ba57c9b7959a1de8481860bef8de989c에서 가져온 **복습노트/1102/.pack/복습문제_1102_PCA-문제.pdf**이다. 작업트리 PDF의 Git blob을 위 커밋의 blob과 대조했다.
- Git blob dcf72065383fcca754790344ea4827229c0d2ba2, SHA-256 11abe1c6d3ab5b192efbfd8d0b62a5ba69763fdce46feaad47ba28f2382567bf.
- pdftotext 결과로 문항을 전사하고, pdftoppm 120 DPI 렌더(source-01.png~source-10.png) 전 10쪽을 따로 눈으로 확인했다. 각 쪽의 제목, 쪽수, MML 표기, 인용 및 조건, 행렬의 부호·열·행, 모든 소문항이 읽힌다. 원본 문제 PDF에는 별도 도형, 그래프, 범례가 없다.
- 이 기록의 풀이 대상은 각 쪽의 ‘조건’에 제시된 행렬이다. P1·P4의 ‘문제 원문’ 영역은 조건에서 푸는 행렬과 다른 교과서 예시를 표시한다. P2의 인용에는 겹근 2가 나오며 조건의 행렬에는 겹근 3이 나온다. 또한 P2의 ‘only one distinct unit eigenvector’라는 인용을 실수 단위벡터의 개수로 문자 그대로 읽으면 서로 반대인 단위벡터 2개가 있으므로, 고유공간의 일차독립 방향 1개로 읽어야 한다. 소문항 P2:c는 그 차원을 명시적으로 묻고 있어 정답 판정에는 모호성이 없다.
- 기존 답안·해설과 PR 변경 조각을 열지 않고 P1–P10의 소문항 32개를 먼저 계산했다. 아래 등식, 랭크, 직교 여부는 정수·유리수·근호로 검산한다. 부동소수점 허용오차는 사용하지 않는다.

## PDF 1쪽 · P1 2×2 행렬의 고윳값과 고유공간 · MML Example 4.5

조건의 $A=\begin{bmatrix}5&4\\1&2\end{bmatrix}$를 사용한다.

- **P1:a** $(A-\lambda I)x=0$에서 $\det(A-\lambda I)\ne0$를 가정하면 왼쪽에 역행렬을 곱해 $x=(A-\lambda I)^{-1}0=0$이다. 따라서 $x\ne0$인 해가 있으면 행렬식은 0이다.
- **P1:b** $\det(A-\lambda I)=(5-\lambda)(2-\lambda)-4=\lambda^2-7\lambda+6=(\lambda-1)(\lambda-6)$. 고윳값은 $1,6$이다.
- **P1:c** $\lambda=1$이면 행이 주는 식은 $x_1+x_2=0$ 하나이므로 $E_1=\operatorname{span}\{(-1,1)^T\}$. $\lambda=6$이면 $x_1-4x_2=0$이므로 $E_6=\operatorname{span}\{(4,1)^T\}$.
- **P1:d** $(-1,1)\cdot(4,1)=-4+1=-3$. 따라서 두 생성 벡터는 직교하지 않는다. 각 생성 벡터에 0이 아닌 스칼라를 곱해도 점곱이 0이 되지 않는다.

## PDF 2쪽 · P2 겹친 고윳값과 고유공간의 차원 · MML Example 4.6

조건의 $A=\begin{bmatrix}3&1\\0&3\end{bmatrix}$를 사용한다.

- **P2:a** 삼각행렬 $A-\lambda I$의 대각 성분을 곱하면 $(3-\lambda)^2$. 유일한 고윳값 3의 대수적 중복도는 2다.
- **P2:b** $(A-3I)x=(x_2,0)^T=0$이므로 $x_1$이 자유변수이며 $E_3=\{(t,0)^T:t\in\mathbb R\}=\operatorname{span}\{(1,0)^T\}$.
- **P2:c** 생성 벡터 $(1,0)^T$ 하나로 공간 전체를 생성한다. $\dim E_3=1$.

## PDF 3쪽 · P3 대칭행렬의 직교 고유벡터 만들기 · MML Example 4.8

시각 확인 결과 대각 성분은 모두 4이고 나머지 성분은 모두 1이다. 문제는 굵은 벡터 이름과 보통 글씨 좌표 이름을 구분한다.

- **P3:a** $A=3I+\mathbf 1\mathbf 1^T$에서 $(A-3I)x=0$은 $x_1+x_2+x_3=0$과 같다. 지정한 자유변수 순서 $(x_2,x_3)=(1,0),(0,1)$은 각각 $\boldsymbol{x}_1=(-1,1,0)^T$, $\boldsymbol{x}_2=(-1,0,1)^T$를 준다. 이 둘이 $E_3$의 기저다. $(A-6I)x=0$은 각 좌표에 대해 $x_1+x_2+x_3=3x_i$을 요구하므로 세 좌표는 같다. 따라서 $E_6=\operatorname{span}\{(1,1,1)^T\}$이고 지정된 벡터는 $\boldsymbol{x}_3=(1,1,1)^T$이다.
- **P3:b** $\boldsymbol{x}_3^T\boldsymbol{x}_1=-1+1+0=0$, $\boldsymbol{x}_3^T\boldsymbol{x}_2=-1+0+1=0$, $\boldsymbol{x}_1^T\boldsymbol{x}_2=1$. 6의 생성 벡터와 3의 생성 벡터를 하나씩 고른 두 쌍이 직교한다.
- **P3:c** 첫 생성 벡터를 보존해 $\boldsymbol{x}'_1=\boldsymbol{x}_1=(-1,1,0)^T$로 두고, 두 번째 벡터에서 사영을 뺀다. $\boldsymbol{x}'_2=\boldsymbol{x}_2-(1/2)\boldsymbol{x}_1=(-1/2,-1/2,1)^T$. 계수 $1/2$는 $\boldsymbol{x}_1^T\boldsymbol{x}_2/\|\boldsymbol{x}_1\|^2$이다. 두 벡터 모두 0이 아니며 $E_3$의 선형결합으로 얻었으므로 고윳값 3의 고유벡터이다.
- **P3:d** $\boldsymbol{x}'_1{}^T\boldsymbol{x}'_2=1/2-1/2=0$, $\boldsymbol{x}'_1{}^T\boldsymbol{x}_3=-1+1=0$, $\boldsymbol{x}'_2{}^T\boldsymbol{x}_3=-1/2-1/2+1=0$. 세 벡터가 쌍마다 직교한다.

## PDF 4쪽 · P4 대칭행렬의 고윳값 분해 · MML Example 4.11

시각 확인 결과 조건은 $A=\tfrac12\begin{bmatrix}7&-1\\-1&7\end{bmatrix}$이다. 바깥의 $1/2$는 두 행 전체에 적용된다.

- **P4:a** $\det(A-\lambda I)=(7/2-\lambda)^2-1/4=(4-\lambda)(3-\lambda)$. 요구된 내림차순으로 $\lambda_1=4$, $\lambda_2=3$이다.
- **P4:b** $A-4I$의 행은 $x_1+x_2=0$을, $A-3I$의 행은 $x_1-x_2=0$을 준다. 각 해에서 생성 벡터의 노름 $\sqrt2$로 나누면 $p_1=(1,-1)^T/\sqrt2$, $p_2=(1,1)^T/\sqrt2$이다. 각각의 부호를 독립적으로 바꿔도 유효하다.
- **P4:c** $p_1^Tp_1=p_2^Tp_2=1$, $p_1^Tp_2=(1-1)/2=0$. 따라서 $P^TP=I_2$이고 정방행렬 $P$에서 $P^{-1}=P^T$.
- **P4:d** $P=\tfrac1{\sqrt2}\begin{bmatrix}1&1\\-1&1\end{bmatrix}$, $D=\begin{bmatrix}4&0\\0&3\end{bmatrix}$. $PDP^T=\tfrac12\begin{bmatrix}4+3&-4+3\\-4+3&4+3\end{bmatrix}=A$.

## PDF 5쪽 · P5 3×3 행렬식과 열의 일차독립 · MML Exercise 4.1

조건의 세 행은 $(1,3,5)$, $(2,4,6)$, $(0,2,4)$이다.

- **P5:a** 첫 행 여인수 전개의 부호 순서는 $+,-,+$. $\det A=1(4\cdot4-6\cdot2)-3(2\cdot4-6\cdot0)+5(2\cdot2-4\cdot0)=4-24+20=0$.
- **P5:b** 정방행렬의 행렬식이 0이라서 세 열은 일차종속이다. 직접 확인하면 첫째 열에서 둘째 열의 두 배를 빼고 셋째 열을 더한 조합이 0이다.

## PDF 6쪽 · P6 두 행렬의 고유공간과 직교 · MML Exercise 4.3

조건의 $A=\begin{bmatrix}1&0\\1&1\end{bmatrix}$와 $B=\begin{bmatrix}-2&2\\2&1\end{bmatrix}$를 사용한다.

- **P6:a** $\det(A-\lambda I)=(1-\lambda)^2$. $(A-I)x=(0,x_1)^T$이므로 $E_1(A)=\operatorname{span}\{(0,1)^T\}$.
- **P6:b** $\det(B-\lambda I)=(-2-\lambda)(1-\lambda)-4=\lambda^2+\lambda-6=(\lambda-2)(\lambda+3)$. $\lambda=2$이면 $-4x_1+2x_2=0$이므로 $E_2(B)=\operatorname{span}\{(1,2)^T\}$. $\lambda=-3$이면 $x_1+2x_2=0$이므로 $E_{-3}(B)=\operatorname{span}\{(-2,1)^T\}$.
- **P6:c** $(1,2)\cdot(-2,1)=-2+2=0$이므로 두 생성 벡터는 직교한다.

## PDF 7쪽 · P7 대각화 가능성과 가역성은 따로예요 · MML Exercise 4.5

시각 확인 결과 $M_1=I_2$, $M_2=\operatorname{diag}(1,0)$, $M_3=\begin{bmatrix}1&1\\0&1\end{bmatrix}$, $M_4=\begin{bmatrix}0&1\\0&0\end{bmatrix}$이다.

- **P7:a** $M_1$과 $M_2$는 이미 대각행렬이다. $M_3$은 고윳값 1만 가지며 $(M_3-I)x=0$은 $x_2=0$을 강제한다. $M_4$는 고윳값 0만 가지며 $M_4x=0$ 역시 $x_2=0$을 강제한다. $M_3$과 $M_4$에서 각각 고유공간의 차원 합 1이 전체 차원 2보다 작으므로 대각화 불가능이다.
- **P7:b** 네 상삼각행렬은 대각 성분의 곱으로 $\det(M_1),\det(M_2),\det(M_3),\det(M_4)=1,0,1,0$이다. $M_1,M_3$은 가역이고 $M_2,M_4$는 특이행렬이다.

## PDF 8쪽 · P8 고유공간으로 대각화 판정하기 · MML Exercise 4.6

시각 확인 결과 $A_1$의 세 행은 $(2,3,0),(1,4,3),(0,0,1)$이다. $A_2$는 $4\times4$이며 첫째 행만 $(1,1,0,0)$이다.

- **P8:a** $A_1-\lambda I$의 셋째 행으로 전개하면 $(1-\lambda)((2-\lambda)(4-\lambda)-3)=(1-\lambda)^2(5-\lambda)$. $\lambda=1$인 경우 첫째·둘째 행에서 $x_1+3x_2=0$, $x_1+3x_2+3x_3=0$을 얻어 $E_1(A_1)=\operatorname{span}\{(-3,1,0)^T\}$. $\lambda=5$는 셋째 행에서 $x_3=0$, 첫째 행에서 $-3x_1+3x_2=0$을 주므로 $E_5(A_1)=\operatorname{span}\{(1,1,0)^T\}$.
- **P8:b** $A_1$의 전체 차원은 3이며 고유공간 차원 합은 $1+1=2$라서 대각화 불가능이다. 특히 고윳값 1은 대수적 중복도 2에 대해 기하적 중복도가 1이다.
- **P8:c** $A_2$가 위삼각이므로 $\det(A_2-\lambda I)=(1-\lambda)(-\lambda)^3$. $A_2x=(x_1+x_2,0,0,0)^T$. $\lambda=1$이면 $x_2=x_3=x_4=0$이며 $E_1(A_2)=\operatorname{span}\{(1,0,0,0)^T\}$. $\lambda=0$이면 $x_1=-x_2$라서 $E_0(A_2)=\operatorname{span}\{(-1,1,0,0)^T,(0,0,1,0)^T,(0,0,0,1)^T\}$.
- **P8:d** $A_2$의 고유공간 차원 합은 $1+3=4$여서 대각화 가능하다. 위 기저 벡터들을 $E_1,E_0$ 순서로 세우면 행렬의 대각 성분이 모두 1인 위삼각 $P$가 얻어져, $\det P=1$이고 $P^{-1}A_2P=\operatorname{diag}(1,0,0,0)$이다.

## PDF 9쪽 · P9 대각화되는지 판정하고 대각 꼴 구하기 · MML Exercise 4.7

시각 확인 결과 조건은 실수 행렬 $P$이다. $A_1=\begin{bmatrix}0&1\\-8&4\end{bmatrix}$이고, $A_2$의 세 행은 $(5,-6,-6),(-1,4,2),(3,-6,-4)$이다.

- **P9:a** $\det(A_1-\lambda I)=(-\lambda)(4-\lambda)+8=\lambda^2-4\lambda+8$. 판별식은 $16-32=-16$이며 근은 $2\pm2i$이다. 가역 실수 $P$로 계산한 $P^{-1}A_1P$는 실수 행렬이어야 하고, 실수 대각행렬에는 실수 고윳값만 있으므로 실수에서 대각화 불가능이다.
- **P9:b** $A_2$의 대각합은 5, $2\times2$ 주 소행렬식의 합은 $14-2-4=8$, 행렬식은 첫 행 전개로 $5(-4)+6(-2)-6(-6)=4$이다. 따라서 $\det(A_2-\lambda I)=-\lambda^3+5\lambda^2-8\lambda+4=-(\lambda-1)(\lambda-2)^2$. $\lambda=1$이면 둘째 행이 $x_1=3x_2+2x_3$을 주고 이를 첫째 행에 대입하면 $6x_2+2x_3=0$을 얻는다. $x_2=t$이면 $x_1=x_3=-3t$이고 셋째 행도 만족한다. 따라서 $E_1(A_2)=\operatorname{span}\{(-3,1,-3)^T\}$. $\lambda=2$이면 세 행이 모두 $x_1=2x_2+2x_3$과 같은 조건을 주므로 $E_2(A_2)=\operatorname{span}\{(2,1,0)^T,(2,0,1)^T\}$.
- **P9:c** 차원 합은 $1+2=3$이다. $P=\begin{bmatrix}-3&2&2\\1&1&0\\-3&0&1\end{bmatrix}$의 행렬식은 $-3-2+6=1$이며, 각 열에 대응하는 $D=\operatorname{diag}(1,2,2)$에 대해 $A_2P=PD$가 성립한다. 그러므로 $P^{-1}A_2P=D$이고 $P$의 세 열이 요구된 기저다.

## PDF 10쪽 · P10 두 대칭행렬이 나눠 갖는 고윳값 · MML Exercise 4.11

$A\in\mathbb R^{m\times n}$이며 $x\in\mathbb R^n$, $u\in\mathbb R^m$이다. PDF는 0이 아닌 고윳값의 공유를 요구한다.

- **P10:a** 양변 왼쪽에 $A$를 곱하고 행렬 곱의 결합법칙을 적용하면 $(AA^T)(Ax)=A((A^TA)x)=A(\lambda x)=\lambda(Ax)$이다.
- **P10:b** 양변 왼쪽에 $A^T$를 곱하면 $(A^TA)(A^Tu)=A^T((AA^T)u)=A^T(\lambda u)=\lambda(A^Tu)$이다.
- **P10:c** $\lambda\ne0$이고 $x\ne0$이면 $\lambda x=A^TAx\ne0$이므로 $Ax\ne0$이다. 마찬가지로 $\lambda u=AA^Tu\ne0$이므로 $A^Tu\ne0$이다. 따라서 (a)와 (b)가 두 방향 모두에서 고유벡터를 만든다. $\lambda=0$이면 $\|Ax\|^2=x^TA^TAx=0$, $\|A^Tu\|^2=u^TAA^Tu=0$이므로 각 사상에서 영벡터를 얻는다. 실제로 $A=[1\ 0]$이면 $A^TA=\operatorname{diag}(1,0)$, $AA^T=[1]$이고 0을 가질 수 있는 쪽이 다르다. 참고로 $\lambda\ne0$에 제한하면 $A$의 역대응은 $A^T/\lambda$여서 해당 고유공간의 차원까지 같다.
