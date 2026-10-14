# 수학 계산과 검증

assets/ml-math.js는 Node/브라우저의 같은 순수 API다. 교육용 φ(x)=[1,x]ᵀ, K=2 전용이며 일반 행렬 계산기처럼 소개하지 않는다.

| API | 입력/반환 |
|---|---|
| posterior({xs,ys,n,m0,S0,sigma2}) | 전체 xs/ys finite·동일 길이, 0≤정수 n≤길이, m0 2-vector, S0 symmetric SPD 2×2, σ²>0. 기본 m0=[0,0], S0=I, n=길이. 반환 {mean,cov,n} |
| predict(p,x,sigma2) | {mean,functionVariance,observationVariance}; ν=φᵀSφ와 ν+σ² |
| normalPdf(x,mu,variance) | 양의 분산 정규화 밀도. 0분산은 별도 점질량 |
| sampleWeights(p,seed,count) | 정수 seed, 0..1000 정수 count. 입력 보존·같은 표본 |

잘못된 입력과 비유한 계산은 RangeError다. compute의 같은 posterior에서 그래프·수치를 만든다. σ² 변경은 posterior부터 재계산한다.
tests/independent_math.py는 Fraction 소거법으로 독립 정답을 만든다. 기본 mean=[3/4,2/3], cov=diag(1/4,1/3), x*=2에서 μ=25/12, ν=19/12, total=31/12. n=0,1,3·상관 사전·강한 사전·큰 잡음도 확인한다.
검토: 행렬 차원·SPD·정밀도 σ⁻², 밀도 적분=1, 등고선 거리/포함 확률, 분산/±2표준편차, 입력별 구간/전체 함수 동시 구간을 구별한다. PDF 페이지·교정·독립 계산·화면 JSON/PNG를 evidence에 둔다.
