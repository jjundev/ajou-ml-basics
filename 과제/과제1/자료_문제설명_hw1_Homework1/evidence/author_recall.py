"""Authored recall sections; the CLI assembles these, it does not invent explanations."""
from pathlib import Path
import sys, json
repo=Path.cwd()
sys.path.insert(0,str(repo/'.claude/skills/ml-problem-explain/scripts'))
from mpe_shared import parse, outer
from mpe_contract import validate_fragment
from mpe_cli import load_run
run=repo/'tmp/ml-problem-explain/hw1-recall-20261012/run'
item=load_run(run)[0]
baseline=run.parent/'baseline-fragments'
content={}
def add(n, paragraphs, summary):
    content[f'p{n}']=(paragraphs.strip().split('\n\n'), summary)

add(1,r'''
<strong>문제의 단서:</strong> “전치”와 위첨자 $\top$를 보면 전치(transpose), 즉 행과 열을 교환하는 연산을 떠올려요. (a)~(c) 모두 같은 정의를 사용해요.

<strong>개념과 공식:</strong> $(A^\top)_{ij}=A_{ji}$예요. 왼쪽의 $i$는 전치한 행렬의 행 번호, $j$는 열 번호예요. 전치하기 전 $(j,i)$ 자리에 있던 수가 전치한 뒤 $(i,j)$로 이동해요.

<strong>적용 조건:</strong> $m\times n$ 행렬을 전치하면 $n\times m$이 돼요. 정방행렬일 필요는 없어요. 열벡터도 $n\times1$ 행렬이므로 전치하면 $1\times n$ 행벡터가 돼요. 숫자를 계산하거나 부호를 바꾸지 않고 위치만 바꿔요.
''',r'전치(transpose)는 행·열 교환이에요. $(A^\top)_{ij}=A_{ji}$, $m\times n\to n\times m$이에요.')

add(2,r'''
<strong>문제의 단서:</strong> (a)의 $x^\top y$는 내적(inner product), (b)·(c)의 $\|\cdot\|_2$는 유클리드 노름(Euclidean norm), (d)의 “직교”는 내적이 0인지 묻는 말이에요.

<strong>개념과 공식:</strong> 내적은 같은 자리끼리 곱해서 더한 수예요. $$x^\top y=\sum_{i=1}^{d}x_i y_i,\qquad \|x\|_2=\sqrt{x^\top x}.$$ $d$는 좌표 수, $x_i,y_i$는 $i$번째 좌표예요. 노름은 벡터의 길이이므로 제곱의 합에 반드시 제곱근을 씌워요.

<strong>적용 조건:</strong> 두 벡터의 차원은 같아야 하고, 여기서는 실수 좌표의 표준 내적을 사용해요. $x^\top y=0$이면 직교(orthogonal)해요. 각도를 말하려면 두 벡터가 0벡터가 아니어야 해요. 이 문제의 두 벡터는 모두 0벡터가 아니므로 내적 결과로 수직인지 판단할 수 있어요.
''',r'내적은 좌표별 곱의 합, 노름은 $\sqrt{x^\top x}$예요. 내적 0이면 직교해요.')

add(3,r'''
<strong>문제의 단서:</strong> $AB$와 $BA$를 따로 구하고 비교하라고 하면 행렬곱(matrix multiplication)의 계산 규칙과 곱 순서를 떠올려요. 일반적으로 순서를 바꾸면 값도 바뀌어요.

<strong>개념과 공식:</strong> $$ (AB)_{ij}=\sum_{k=1}^{r}A_{ik}B_{kj}. $$ $i$는 결과의 행, $j$는 결과의 열, $k$는 곱해서 더할 자리예요. $A$의 $i$번째 행과 $B$의 $j$번째 열을 짝지어 내적해요.

<strong>적용 조건:</strong> $A$가 $m\times r$, $B$가 $r\times n$이면 $AB$는 $m\times n$이에요. 안쪽 차원 $r$이 맞아야 해요. 이 문제는 두 행렬이 모두 $3\times3$이므로 두 곱을 모두 계산할 수 있지만, 계산 가능하다는 사실만으로 $AB=BA$가 되지는 않아요.
''',r'행×열의 내적이 행렬곱의 원소예요. 안쪽 차원을 확인하고 $AB$, $BA$를 따로 계산해요.')

add(4,r'''
<strong>문제의 단서:</strong> $\det$는 행렬식(determinant)이에요. (a)·(b)는 $2\times2$, (c)는 대각행렬, (d)는 $3\times3$이므로 크기와 모양에 맞는 공식을 골라요.

<strong>(a)·(b)의 공식:</strong> $$\det\begin{pmatrix}a&b\\c&d\end{pmatrix}=ad-bc.$$ 문자 $a,b,c,d$는 네 원소예요. 오른쪽 아래로 가는 곱에서 반대 대각선의 곱을 빼요. (c)는 삼각행렬(triangular matrix)의 성질 $\det C=\prod_i C_{ii}$를 사용해요. $C_{ii}$는 대각 원소예요.

<strong>(d)의 공식:</strong> 첫 행의 여인수 전개(cofactor expansion)는 $$\det D=D_{11}\det M_{11}-D_{12}\det M_{12}+D_{13}\det M_{13}.$$ $M_{1j}$는 첫 행과 $j$번째 열을 지운 $2\times2$ 소행렬이에요. Sarrus 규칙은 아래로 향하는 세 대각선 곱의 합에서 위로 향하는 세 대각선 곱의 합을 빼는 방법이에요.

<strong>적용 조건:</strong> 행렬식은 정방행렬에 정의돼요. 대각 원소만 곱하는 방법은 대각·삼각행렬일 때 사용하고, Sarrus 규칙은 $3\times3$에만 사용해요. (d)는 요청한 두 방법을 모두 적용해 같은 값을 얻는지 확인해요.
''',r'$2\times2$는 $ad-bc$, 삼각행렬은 대각곱이에요. $3\times3$은 여인수 전개와 Sarrus를 비교해요.')

add(5,r'''
<strong>문제의 단서:</strong> $A^{-1}$은 역행렬(inverse matrix), 즉 곱했을 때 항등행렬 $I$를 만드는 행렬이에요. 원소마다 역수를 취하는 연산은 아니에요.

<strong>(a)·(b)의 공식:</strong> $$\begin{pmatrix}a&b\\c&d\end{pmatrix}^{-1}=\frac{1}{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}.$$ $a,b,c,d$는 행렬 원소예요. 대각 원소의 위치를 바꾸고 다른 두 원소의 부호를 바꾼 뒤 행렬식으로 나눠요.

<strong>(c)의 개념:</strong> 블록 대각행렬(block diagonal matrix)이면 서로 섞이지 않는 블록을 각각 뒤집을 수 있어요. $$\operatorname{diag}(B,s)^{-1}=\operatorname{diag}(B^{-1},1/s).$$ $B$는 왼쪽 위 정방 블록, $s$는 오른쪽 아래 스칼라예요. 이 문제의 $C$는 $2\times2$ 블록과 스칼라 2로 분리돼요.

<strong>적용 조건:</strong> 정방행렬의 역행렬은 행렬식이 0이 아닐 때만 존재해요. 블록 공식도 각 블록이 가역이고 $s\ne0$이어야 해요. 계산 후 $AA^{-1}=A^{-1}A=I$로 확인해요.
''',r'역행렬은 곱해서 $I$를 만드는 행렬이에요. 먼저 $\det A\ne0$을 확인해요.')

add(6,r'''
<strong>문제의 단서:</strong> “선형 독립인지”와 “비자명한 관계”를 보면 선형 독립(linear independence)의 정의를 떠올려요. 벡터가 서로 달라 보이는지만으로 판단하지 않아요.

<strong>개념과 기준:</strong> $$c_1x_1+c_2x_2+c_3x_3=0.$$ $c_i$는 찾아야 할 실수 계수예요. 모두 0인 해만 있으면 독립이고, 계수 중 하나라도 0이 아닌 해가 있으면 종속(linearly dependent)이에요. 비자명(nontrivial)은 “모든 계수가 0인 것은 아님”을 뜻해요.

<strong>적용 방법:</strong> $X=[x_1\ x_2\ x_3]$처럼 열로 모으면 같은 조건을 $Xc=0$으로 쓸 수 있어요. $c$는 계수 열벡터예요. 이 문제는 $X$가 정방행렬이므로 $\det X\ne0$이면 독립이지만, 종속이라는 결론의 근거로는 실제 비자명 관계를 보여 주면 돼요.
''',r'$\sum_i c_i x_i=0$에서 비자명한 계수 해가 있으면 종속, 0인 해만 있으면 독립이에요.')

add(7,r'''
<strong>문제의 단서:</strong> “$y$를 세 벡터의 선형결합으로”는 각 벡터를 몇 배씩 더할지 묻는 말이에요. 선형결합(linear combination)을 연립방정식으로 옮겨요.

<strong>개념과 공식:</strong> $$y=c_1x_1+c_2x_2+c_3x_3=Xc.$$ $X=[x_1\ x_2\ x_3]$, $c=(c_1,c_2,c_3)^\top$예요. $y$의 각 좌표가 일치해야 하므로 한 좌표당 방정식 하나를 얻어요.

<strong>적용 조건:</strong> 같은 차원의 벡터끼리 더해야 해요. $y$가 열벡터들의 생성공간(span)에 있어야 해가 존재해요. 이 문제의 정방 $X$가 가역이면 $c=X^{-1}y$로 유일한 계수를 구할 수 있고, 소거법으로도 풀 수 있어요. 마지막에는 계수를 원래 선형결합에 대입해 $y$가 복원되는지 확인해요.
''',r'주어진 벡터를 열로 모아 $Xc=y$를 풀어요. 답은 벡터가 아니라 각 벡터의 계수예요.')

add(8,r'''
<strong>문제의 단서:</strong> $A^\top A$는 열벡터들의 내적을 모은 Gram 행렬(Gram matrix)이에요. 직사각형 $A$ 자체의 역행렬과 $A^\top A$의 역행렬을 구별해요.

<strong>개념과 공식:</strong> $A=[a_1\ a_2]$라 두면 $(A^\top A)_{ij}=a_i^\top a_j$예요. 대각은 열의 길이 제곱, 비대각은 두 열의 내적이에요. $A$가 $3\times2$이므로 $A^\top A$는 $2\times2$예요.

<strong>역행렬의 조건:</strong> $$v^\top A^\top Av=\|Av\|_2^2.$$ $v$는 열 개수에 맞는 계수 벡터예요. $A$의 열이 선형 독립이면 $v\ne0$일 때 $Av\ne0$이어서 Gram 행렬이 양의 정부호(positive definite)이고 가역이에요. 열이 종속이면 가역이 아니에요. 정방행렬이라는 이유만으로 역행렬이 존재한다고 결론내리지 않아요.
''',r'Gram의 원소는 열끼리의 내적이에요. $A^\top A$가 가역일 조건은 $A$의 열 독립이에요.')

add(9,r'''
<strong>문제의 단서:</strong> 특징 사상 $\phi(x)$와 “$n$번째 행”이라는 말에서 특징 행렬(feature matrix)의 배치를 떠올려요. 관측 하나를 행 하나로 적어요.

<strong>개념과 공식:</strong> $$\Phi_{nj}=\phi_j(x_n),\qquad \hat y_n=\phi(x_n)^\top\theta.$$ $n$은 관측 번호, $j$는 특징 번호, $\theta$는 특징별 계수예요. 각 행을 계수 벡터와 내적한 값을 모으면 $\hat y=\Phi\theta$가 돼요. 여기서는 세 관측과 세 특징이 있어 $\Phi$는 $3\times3$이에요.

<strong>모델을 판단하는 기준:</strong> 선형회귀(linear regression)의 “선형”은 파라미터 $\theta$에 대한 선형성을 말해요. 입력 특징에 $x^2$이 있어도 $\theta_0+\theta_1x+\theta_2x^2$는 계수들을 한 번씩 곱해 더하므로 파라미터에 선형이에요. 상수 특징 1이 절편을 담당해요.
''',r'특징은 열, 관측은 행이에요. $\hat y=\Phi\theta$이고 선형성은 파라미터에 대해 판단해요.')

add(10,r'''
<strong>문제의 단서:</strong> 스칼라 함수의 gradient는 변수별 편미분(partial derivative)을 모은 벡터예요. 이 과제는 반드시 열벡터로 쓰라고 했어요.

<strong>(a)·(b)의 공식:</strong> $$\nabla f=\begin{pmatrix}\partial f/\partial u\\\partial f/\partial v\end{pmatrix}.$$ 한 변수로 미분할 때 다른 변수는 상수로 둬요. $\partial(u^2)/\partial u=2u$이고, 교차항은 $\partial(uv)/\partial u=v$, $\partial(uv)/\partial v=u$예요.

<strong>(c)의 공식:</strong> 합성함수의 연쇄법칙(chain rule)을 떠올려요. $r=u+2v-w-3$라 두면 $h=r^2$이므로 $$\nabla h=2r\,\nabla r,\qquad\nabla r=(1,2,-1)^\top.$$ $r$은 괄호 안의 식이에요. 바깥의 제곱을 미분한 값과 안쪽 식의 미분을 곱해요.

<strong>적용 순서:</strong> 먼저 기호로 gradient를 구하고 마지막에 주어진 점을 대입해요. 처음부터 모든 변수를 숫자로 바꾸면 함수가 상수가 되어 원래의 미분 정보를 잃어요.
''',r'편미분을 열벡터로 모아요. 다른 변수는 상수, 괄호의 제곱은 연쇄법칙을 사용해요.')

add(11,r'''
<strong>문제의 단서:</strong> 함수의 출력이 벡터이고 “야코비 행렬”을 구하라고 하면 Jacobian을 떠올려요. 출력 성분별 gradient를 행으로 배열한 표예요.

<strong>개념과 공식:</strong> $$J_{ij}=\frac{\partial f_i}{\partial x_j}.$$ $f_i$는 $i$번째 출력, $x_j$는 $j$번째 입력 변수예요. 출력이 $m$개, 입력이 $d$개이면 $J$는 $m\times d$예요. 여기서는 열 순서를 $(u,v)$로 고정해요.

<strong>(a)·(b)의 차이:</strong> (a)는 출력 2개라 $2\times2$, (b)는 출력 3개라 $3\times2$예요. 선형인 (a)는 미분값이 상수이고, (b)의 $u^2,uv,v^2$는 입력에 따라 미분값이 달라져요. 두 경우 모두 먼저 미분하고 $(1,2)$를 대입해요.
''',r'Jacobian은 출력×입력이에요. $J_{ij}=\partial f_i/\partial x_j$, 열 순서는 $(u,v)$예요.')

add(12,r'''
<strong>문제의 단서:</strong> $x^\top Qx$는 이차형식(quadratic form), 편미분을 0으로 두는 것은 정류점(stationary point)을 찾는 일이에요. 행렬로 쓴 이차식을 좌표별 다항식으로 전개할 수도 있어요.

<strong>(a)의 공식:</strong> $$\nabla_x(x^\top Qx)=(Q+Q^\top)x,\qquad \nabla_x(b^\top x)=b.$$ $x$는 미분하는 변수 벡터이고 $Q,b$는 고정된 계수예요. 이 문제는 $Q=Q^\top$이므로 $\nabla h=2Qx-2b$예요. 대칭 조건을 확인해야 $2Qx$로 줄일 수 있어요.

<strong>(b)의 기준:</strong> $\nabla h=0$은 $Qx=b$라는 연립방정식이 돼요. $Q$가 가역이면 정류점은 하나예요. 정류점이 곧 최솟값이라는 일반 규칙은 없지만, 이 문제처럼 $Q$가 양의 정부호이면 Hessian $2Q$가 양의 정부호여서 유일한 전역 최소예요. 좌표별 전개는 같은 미분을 확인하는 다른 방법이에요.
''',r'대칭 $Q$이면 $\nabla h=2Qx-2b$예요. 정류점은 $Qx=b$, 최소 판정은 양의 정부호를 확인해요.')

add(13,r'''
<strong>문제의 단서:</strong> $X\sim\mathcal N(\mu,\Sigma)$와 “정규화 상수까지”는 다변량 가우시안(multivariate Gaussian)의 밀도 전체를 쓰라는 뜻이에요. 평균을 뺀 뒤 공분산의 역행렬로 거리의 크기를 재요.

<strong>개념과 공식:</strong> $$p(x)=\frac{1}{(2\pi)^{d/2}\sqrt{\det\Sigma}}\exp\left[-\frac12(x-\mu)^\top\Sigma^{-1}(x-\mu)\right].$$ $d$는 차원, $\mu$는 평균 벡터, $\Sigma$는 공분산(covariance), $\Sigma^{-1}$은 정밀도(precision)예요. 앞의 계수는 전체 적분을 1로 만들어요.

<strong>적용 조건:</strong> 보통의 $d$차원 밀도에 이 공식을 쓰려면 $\Sigma$가 대칭 양의 정부호여야 해요. 이 문제는 $d=2$이고 비대각 성분이 있어서 두 좌표를 독립 가우시안으로 따로 곱하면 안 돼요. 중심을 뺀 벡터에 역행렬을 곱한 후 이차식을 전개해요.
''',r'가우시안은 정규화 계수와 중심 이차형식으로 써요. 지수에는 공분산의 역행렬이 들어가요.')

add(14,r'''
<strong>문제의 단서:</strong> 지수 안의 이차식에서 평균·분산·상수를 찾아야 하면 완전제곱(completing the square)을 떠올려요. 중심에서 떨어진 거리의 제곱으로 모양을 바꾸는 방법이에요.

<strong>개념과 공식:</strong> $a>0$일 때 $$az^2+bz+d=a\left(z+\frac{b}{2a}\right)^2+d-\frac{b^2}{4a}.$$ $a,b,d$는 이차식의 계수예요. 중심은 $\mu=-b/(2a)$예요. $\exp[-a(z-\mu)^2/2]$의 가우시안 분산은 $\sigma^2=1/a$예요.

<strong>정규화:</strong> $$\int_{-\infty}^{\infty}e^{-a(z-\mu)^2/2}\,dz=\sqrt{2\pi/a}.$$ 상수로 남은 항도 지수 밖의 계수에 영향을 줘요. 이 문제에서는 $a=4,b=-8,d=7$을 비교해 읽어요. 분산과 표준편차를 구별하고, 전체 밀도의 적분이 1이 되도록 $c$를 결정해요.
''',r'완전제곱으로 중심을 읽어요. 이차항 계수 $a>0$이면 분산은 $1/a$이고 남는 상수도 정규화에 포함해요.')

add(15,r'''
<strong>문제의 단서:</strong> “서로 독립인 가우시안 잡음”과 “전체 우도”는 한 관측의 조건부 밀도를 먼저 쓰고 모두 곱하라는 신호예요. 우도(likelihood)는 관측을 고정하고 파라미터를 바꾸어 보는 함수예요.

<strong>개념과 공식:</strong> $r_n=y_n-(\theta_0+\theta_1x_n)$을 잔차(residual)라 두면 $$p(y_n\mid x_n,\theta)=\frac{1}{\sqrt{2\pi\sigma^2}}e^{-r_n^2/(2\sigma^2)}.$$ $n$은 관측 번호, $\sigma^2$는 알려진 잡음 분산이에요. 독립이므로 $L(\theta)=\prod_{n=1}^N p(y_n\mid x_n,\theta)$예요.

<strong>선택 이유와 조건:</strong> 지수함수들의 곱은 지수 안의 합이 되어 $\sum_n r_n^2$가 나타나요. 상수 계수도 $N$번 곱해요. 고정 입력에서의 조건부 독립과 같은 양의 분산 $\sigma^2$를 사용해야 이 형태가 돼요. 여기서는 상수 인자까지 요구하므로 $\theta$에 무관해도 생략하지 않아요.
''',r'독립 관측의 우도는 밀도의 곱이에요. 지수에는 잔차 제곱의 합, 앞에는 $N$개 정규화 계수의 곱이 와요.')

add(16,r'''
<strong>문제의 단서:</strong> “음의 로그우도”와 “최소제곱과 같은 이유”를 보면 로그가 곱을 합으로 바꾸고, 최대화를 최소화로 바꾸는 성질을 떠올려요.

<strong>개념과 공식:</strong> $$-\log p(y\mid\Phi,\theta)=\frac{N}{2}\log(2\pi\sigma^2)+\frac{1}{2\sigma^2}\|y-\Phi\theta\|_2^2.$$ $N$은 관측 수, $\Phi$는 고정 특징 행렬, $\theta$는 추정할 계수, $y-\Phi\theta$는 잔차 벡터예요. 공분산 $\sigma^2I_N$의 행렬식은 $(\sigma^2)^N$, 역행렬은 $I_N/\sigma^2$예요.

<strong>같은 해가 나오는 조건:</strong> 로그는 증가함수이므로 우도 최대화는 음의 로그 최소화와 같아요. $\sigma^2>0$이 알려져 있으면 첫 항은 $\theta$와 무관하고 제곱오차의 계수는 양수예요. 상수 더하기와 양의 배율은 어느 $\theta$가 더 작은지 바꾸지 않아요. 유도에서는 전체 상수를 쓰고, 최적화의 동등성을 말할 때만 제외해요.
''',r'알려진 양의 분산에서 NLL은 상수+$SSE/(2\sigma^2)$예요. 따라서 ML과 최소제곱의 해가 같아요.')

add(17,r'''
<strong>문제의 단서:</strong> (a)의 “제곱오차 전개→gradient=0”은 최소제곱(least squares)의 정규방정식(normal equations)을 유도하는 순서예요. (b)는 그 일반식에 특징 행렬과 데이터를 넣는 문제예요.

<strong>(a)의 공식:</strong> $J=\|y-\Phi\theta\|_2^2$에서 $$\nabla_\theta J=2\Phi^\top(\Phi\theta-y).$$ 0으로 두면 $\Phi^\top\Phi\theta=\Phi^\top y$예요. $\Phi$는 $N\times K$, $\theta$는 $K\times1$이고 $K$는 계수 수예요.

<strong>역행렬과 최소의 조건:</strong> $\Phi$의 열이 독립이면 $\Phi^\top\Phi$가 양의 정부호라 $$\theta_{\mathrm{ML}}=(\Phi^\top\Phi)^{-1}\Phi^\top y$$가 유일한 최소예요. 열이 종속이면 역행렬 공식은 사용할 수 없어요. 알려진 가우시안 잡음 분산 덕분에 최소제곱 해가 ML 해예요.

<strong>(b)의 개념:</strong> 절편이 있는 모델의 관측 행은 $(1,x_n)$이에요. 예측은 $\hat y=\Phi\theta$, 오차는 $S=\|y-\hat y\|_2^2$예요. 추정 계수, 예측값, 오차제곱합은 서로 다른 결과이므로 순서대로 계산해요.
''',r'정규방정식은 $\Phi^\top\Phi\theta=\Phi^\top y$예요. 역행렬을 쓰려면 특징 열이 독립이어야 해요.')

add(18,r'''
<strong>문제의 단서:</strong> 데이터의 우도에 “사전분포”가 더해지면 MAP(maximum a posteriori), 즉 사후분포를 가장 크게 만드는 추정을 떠올려요. 베이즈 규칙으로 우도와 사전을 연결해요.

<strong>개념과 공식:</strong> $p(\theta\mid y,\Phi)\propto p(y\mid\Phi,\theta)p(\theta)$예요. 0 중심 가우시안 사전의 음의 로그는 $\|\theta\|_2^2/(2b^2)+C$예요. $b^2$는 사전분산이고 $C$는 $\theta$에 무관한 항이에요. 따라서 $$-\log p(\theta\mid y,\Phi)=\frac{\|y-\Phi\theta\|_2^2}{2\sigma^2}+\frac{\|\theta\|_2^2}{2b^2}+C.$$

<strong>릿지와 연결:</strong> 전체를 양수 $2\sigma^2$배 하면 $SSE+\lambda\|\theta\|_2^2$가 되고 $\lambda=\sigma^2/b^2$예요. 두 항의 비율을 맞춰야 하므로 $1/(2b^2)$를 그대로 이 목적함수의 $\lambda$로 쓰면 안 돼요. 릿지 회귀(ridge regression)의 벌점은 계수를 0 쪽으로 당겨요.

<strong>적용 조건:</strong> 두 분산은 알려진 양수이고, 이 문제는 절편까지 모든 계수에 사전을 적용해요. $$\theta_{\mathrm{MAP}}=(\Phi^\top\Phi+\lambda I_K)^{-1}\Phi^\top y.$$ $I_K$는 계수 수에 맞는 항등행렬이에요. $\lambda>0$이면 특징 열이 종속이어도 이 행렬은 양의 정부호여서 역행렬이 존재해요.
''',r'MAP은 우도+사전이에요. $SSE+\lambda\|\theta\|^2$로 맞추면 $\lambda=\sigma^2/b^2$, 절편도 규제해요.')

add(19,r'''
<strong>문제의 단서:</strong> 같은 데이터에서 ML과 서로 다른 사전분산의 MAP을 비교하므로 데이터만 쓰는 정규방정식과 사전을 더한 릿지 식을 나란히 떠올려요.

<strong>(a)의 공식:</strong> $G=\Phi^\top\Phi$, $h=\Phi^\top y$라 쓰면 $$\theta_{\mathrm{ML}}=G^{-1}h,\qquad \theta_{\mathrm{MAP}}=(G+\lambda I_2)^{-1}h.$$ $G$는 특징의 Gram 행렬, $h$는 특징과 관측의 곱을 합한 벡터예요. $\lambda=\sigma^2/b^2$이며 여기서는 $\sigma^2=1$이에요.

<strong>(b)의 비교 기준:</strong> $b^2$가 작을수록 사전이 0 주변에 더 집중되어 $\lambda$가 커져요. 이 문제의 $G$는 대각행렬이라 각 계수는 $h_i/(G_{ii}+\lambda)$로 구해요. 따라서 양의 분자와 커지는 분모를 보고 두 계수가 0 쪽으로 줄어드는 이유를 설명할 수 있어요. 임의의 비대각 Gram에서도 각 좌표가 항상 단조롭게 줄어든다고 일반화하지 않아요.

<strong>적용 조건:</strong> 이 사전은 절편과 기울기 둘 다에 적용해요. 절편을 예외로 두지 말고 두 대각 원소 모두에 $\lambda$를 더해요.
''',r'$\sigma^2=1$이므로 $\lambda=1/b^2$예요. 이 대각 사례는 분모 증가로 절편·기울기 모두 줄어들어요.')

add(20,r'''
<strong>문제의 단서:</strong> 두 특징 열이 같고 “특이한 행렬”을 다루므로 열 종속과 계수의 식별 불가능성(non-identifiability)을 떠올려요. 서로 다른 계수가 같은 예측을 만들 수 있어요.

<strong>(a)·(b)의 개념:</strong> $s=\theta_1+\theta_2$라 두면 예측 $\Phi\theta$는 $s$만으로 결정돼요. $v=(1,-1)^\top$을 더해도 $\Phi v=0$이므로 예측은 바뀌지 않아요. 이 $v$는 영공간(null space)의 벡터예요. 따라서 $\Phi^\top\Phi$는 역행렬이 없고 무규제 적합으로는 두 계수를 각각 결정할 수 없어요.

<strong>(c)의 공식:</strong> $\lambda>0$인 릿지 목적은 $$J=\|y-\Phi\theta\|_2^2+\lambda\|\theta\|_2^2.$$ 정류점은 $(\Phi^\top\Phi+\lambda I)\theta=\Phi^\top y$를 풀어 구해요. 이 문제의 $\lambda$는 5예요. 또는 $d=\theta_1-\theta_2$라 두면 $\theta_1^2+\theta_2^2=(s^2+d^2)/2$여서 완전제곱으로 최솟값을 볼 수 있어요.

<strong>최소의 조건:</strong> 0이 아닌 $v$에 대해 $v^\top(\Phi^\top\Phi+\lambda I)v=\|\Phi v\|^2+\lambda\|v\|^2>0$예요. 모든 계수에 양의 규제를 주면 유일한 전역 최소가 생겨요. 단지 역행렬 계산이 가능해진 것뿐 아니라 목적함수의 모양이 달라진 거예요.
''',r'중복 열은 계수의 합만 식별해요. 양의 릿지 규제가 모든 계수에 붙으면 유일한 최소가 생겨요.')

add(21,r'''
<strong>문제의 단서:</strong> “표본 평균”은 좌표별 평균, “공분산”은 평균에서 벗어난 편차들의 곱을 모은 행렬을 뜻해요. 문제에서 분모를 4로 지정했다는 조건을 먼저 표시해요.

<strong>(a)·(b)의 공식:</strong> $$\bar x=\frac1N\sum_{n=1}^N x_n,\qquad S=\frac1N\sum_{n=1}^N d_n d_n^\top,\quad d_n=x_n-\bar x.$$ $N$은 관측 수, $d_n$은 $n$번째 편차 열벡터예요. $d_nd_n^\top$는 외적(outer product)이라 $2\times2$ 행렬이 되고, $d_n^\top d_n$은 스칼라라 다른 연산이에요.

<strong>적용 조건과 의미:</strong> 이 문제는 $N=4$로 나누는 정의를 사용해요. 불편 추정량(unbiased estimator)을 만들 때 사용하는 $N-1$로 임의 교체하지 않아요. 대각 원소는 각 좌표의 퍼짐, 비대각 원소는 두 좌표가 함께 움직이는 정도예요. $$S=\frac1N\sum_n x_nx_n^\top-\bar x\bar x^\top$$를 이용하면 같은 결과를 다른 방식으로 검산할 수 있어요.
''',r'평균을 뺀 편차의 외적을 평균내요. 이 문제의 공분산 분모는 $N=4$예요.')

add(22,r'''
<strong>문제의 단서:</strong> 좌표를 더하고 상수를 옮기는 식은 아핀 변환(affine transformation) $y=Ax+c$로 정리해요. 평균·공분산·교차공분산은 서로 다른 양이고 곱 순서도 달라요.

<strong>(a)의 공식:</strong> $$\mu_y=A\mu_x+c,\qquad \Sigma_y=A\Sigma_xA^\top,\qquad C_{xy}=\Sigma_xA^\top.$$ $A$는 변환 계수 행렬, $c$는 결정적 상수 벡터, $\mu_x=E[x]$, $\Sigma_x=\operatorname{Cov}(x)$예요. $C_{xy}=E[(x-\mu_x)(y-\mu_y)^\top]$는 입력×출력 방향이에요. 상수 이동은 평균만 바꿔요. 유한한 2차 모멘트가 있으면 가우시안이 아니어도 이 공식이 성립해요.

<strong>(b)의 추가 개념:</strong> 가우시안 지수의 중심에서 $\mu_x$를 읽고, 이차식 $(x-\mu_x)^\top P(x-\mu_x)$의 계수 행렬 $P$는 정밀도(precision)이므로 $\Sigma_x=P^{-1}$이에요. 교차항의 계수는 대칭인 $P_{12},P_{21}$의 합이에요. 공분산을 얻은 뒤 같은 아핀 공식을 적용해요.

<strong>(c)의 추가 개념:</strong> 먼저 $\operatorname{Cov}(x_1,x_2)=E[x_1x_2]-E[x_1]E[x_2]$로 비대각 성분을 구해요. 두 좌표에 같은 잡음이 들어가므로 $y=Ax+\varepsilon u$, $u=(1,1)^\top$로 써요. $\varepsilon$이 $x$와 독립이고 평균이 0이면 $$\Sigma_y=A\Sigma_xA^\top+\operatorname{Var}(\varepsilon)uu^\top,\qquad C_{xy}=\Sigma_xA^\top.$$ $uu^\top$의 모든 원소는 1이에요. 공유 잡음은 비대각 공분산도 늘리므로 $I_2$를 더하면 안 돼요.
''',r'아핀 변환은 $\Sigma_y=A\Sigma_xA^\top$예요. 정밀도는 역행렬로 바꾸고, 공유 잡음은 $uu^\top$를 더해요.')

add(23,r'''
<strong>문제의 단서:</strong> “절편 없는 회귀”는 계수가 $\theta$ 하나뿐인 모델이에요. (a)는 독립 밀도의 곱, (b)는 ML, (c)는 가우시안 사전을 더한 MAP과 새 입력의 예측을 연결해요.

<strong>(a)·(b)의 공식:</strong> $r_n=y_n-\theta x_n$을 잔차라 두면 $$L(\theta)=(2\pi)^{-N/2}\exp\left[-\frac12\sum_n r_n^2\right].$$ 잡음 분산은 1이고 관측 수는 $N=2$예요. 음의 로그를 미분하면 $$\frac{d(-\log L)}{d\theta}=\sum_n x_n(\theta x_n-y_n).$$ $\sum_n x_n^2>0$이면 0으로 두어 $\theta_{\mathrm{ML}}=\sum_n x_ny_n/\sum_n x_n^2$를 얻어요.

<strong>(c)의 공식과 조건:</strong> 사전 $\mathcal N(0,1)$이 더하는 음의 로그는 $\theta^2/2+C$예요. 그 미분은 $\theta$라서 MAP 방정식은 $\theta(\sum_n x_n^2+1)=\sum_n x_ny_n$이 돼요. 여기서 1은 사전 정밀도와 잡음 분산에 따른 값이에요. 모델에 절편을 새로 추가하지 않아요. 예측은 원래 식에 새 입력을 넣어 $\hat y=\theta x$로 계산해요.
''',r'절편 없이 잔차는 $y_n-\theta x_n$이에요. MAP은 0 중심 사전의 $\theta^2/2$를 더해요.')

add(24,r'''
<strong>문제의 단서:</strong> 모든 관측이 같은 $\theta$를 평균으로 공유하고 사전 평균이 1이에요. 회귀의 기울기보다 가우시안 평균 추정(Gaussian mean estimation)과 정밀도 가중 평균을 떠올려요.

<strong>(a)·(b)의 공식:</strong> 알려진 분산 $\sigma^2$의 독립 관측은 $$-\log L=\frac{N}{2}\log(2\pi\sigma^2)+\frac1{2\sigma^2}\sum_n(y_n-\theta)^2.$$ 미분해서 0으로 두면 $N\theta=\sum_n y_n$이 되어 ML은 표본 평균이에요. 여기서는 $N=3$, $\sigma^2=1$이에요.

<strong>(c)의 공식:</strong> 일반 사전 $\theta\sim\mathcal N(m_0,b^2)$를 쓰면 $$\theta_{\mathrm{MAP}}=\frac{\sum_n y_n/\sigma^2+m_0/b^2}{N/\sigma^2+1/b^2}.$$ $m_0$는 사전 평균, $1/b^2$는 사전 정밀도예요. 데이터의 평균과 사전 평균을 확실한 정도에 따라 섞는 가중 평균이에요.

<strong>적용 조건:</strong> 두 분산은 알려진 양수예요. 이 문제는 $m_0=1,b^2=1$이므로 사전 벌점은 $(\theta-1)^2/2$이고 $\theta^2/2$가 아니에요. 어느 추정이 사전에 가까운지는 $|\theta-1|$로 비교해요.
''',r'ML은 표본 평균, MAP은 데이터·사전의 정밀도 가중 평균이에요. 사전 벌점의 중심은 1이에요.')

add(25,r'''
<strong>문제의 단서:</strong> “가우시안의 곱”과 $\propto$를 보면 지수의 이차식들을 더한 뒤 완전제곱하고 정규화하는 과정을 떠올려요. 같은 변수 $x$의 두 밀도를 곱하는 일이므로 서로 다른 확률변수의 합과 구별해요.

<strong>개념과 공식:</strong> 정밀도 $P_i=\Sigma_i^{-1}$를 정의해요. $i=0,1$은 두 밀도의 번호예요. 곱의 지수를 전개하면 이차항은 $P_0+P_1$, 일차항은 $P_0\mu_0+P_1\mu_1$로 모여요. 따라서 $$P_q=P_0+P_1,\qquad \Sigma_q=P_q^{-1},$$ $$\mu_q=\Sigma_q(P_0\mu_0+P_1\mu_1).$$ 평균은 공분산이 아니라 정밀도로 가중해서 결합해요.

<strong>정규화된 밀도:</strong> $$q(x)=\frac{\exp[-\tfrac12(x-\mu_q)^\top P_q(x-\mu_q)]}{(2\pi)^{d/2}\sqrt{\det\Sigma_q}}.$$ $d$는 차원이고 여기서는 2예요. $\propto$는 $x$와 무관한 계수만 생략했다는 뜻이에요. 원래 두 밀도를 곱한 것의 적분은 보통 1이 아니므로 완성 답에는 새 정규화 계수가 필요해요.

<strong>적용 조건:</strong> 두 공분산이 대칭 양의 정부호이면 정밀도의 합도 양의 정부호여서 $\Sigma_q$가 존재해요. 이 계산은 같은 변수에 대한 밀도 함수의 곱이므로 두 확률변수의 독립성을 별도로 가정할 필요가 없어요.
''',r'밀도의 곱은 정밀도를 더해요. $P_q=P_0+P_1$, $\Sigma_q=P_q^{-1}$이며 새 정규화 계수가 필요해요.')

for p in item['pack'].problems:
    paragraphs,summary=content[p.id]
    block='<div class="layer formal" data-explanation="recall"><h4>이 문제를 봤을 때 떠올릴 개념과 공식</h4>'+'\n'.join('<p>'+t+'</p>' for t in paragraphs)+'</div>\n'
    root=parse((baseline/f'{p.id}.html').read_text(encoding='utf-8'))
    # Operate on direct children, keeping all original explanations and subparts intact.
    out=[]
    for node in root.children:
        if not isinstance(node,str) and node.attrs.get('data-explanation')=='start':out.append(block)
        if not isinstance(node,str) and 'sum' in node.classes:
            markup=outer(node)
            idx=markup.index('>')+1
            group='<div class="summary-group"><h4>떠올릴 개념·공식</h4><p>'+summary+'</p></div>'
            out.append(markup[:idx]+group+markup[idx:])
        else:out.append(outer(node))
    fragment=''.join(out)
    errors=validate_fragment(p,fragment)
    assert not errors, errors
    (item['folder']/'explanations'/f'{p.id}.html').write_text(fragment,encoding='utf-8')
print('Authored and structurally checked 25 recall sections and 25 summary groups')
