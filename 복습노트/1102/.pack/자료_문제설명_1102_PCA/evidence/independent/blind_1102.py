"""Blind independent solver for 1102 PCA review problems (sympy exact)."""
import json, os, random
import sympy as sp

lam = sp.symbols('lambda')
R = {}
OUT = os.path.dirname(os.path.abspath(__file__))

def eigdata(A):
    n = A.shape[0]
    p = sp.factor((A - lam*sp.eye(n)).det())
    rows = []
    for ev, am, vecs in A.eigenvects():
        basis = [list(v.applyfunc(sp.nsimplify).T) for v in vecs]
        rows.append((ev, am, len(vecs), basis))
    diag = sum(r[2] for r in rows) == n
    return p, rows, diag

def show(name, A):
    p, rows, diag = eigdata(A)
    print(f"== {name}: A = {A.tolist()}")
    print(f"   det(A - lambda I) = {p}")
    for ev, am, gm, b in rows:
        print(f"   lambda={ev}: alg={am}, geo={gm}, E basis={b}")
    print(f"   diagonalizable={diag}, det(A)={A.det()}, invertible={A.det()!=0}")
    return p, rows, diag

def fmt(rows):
    return "; ".join(f"λ={ev} (alg {am}, geo {gm}): E={'span{'+', '.join(str(v) for v in b)+'}'}" for ev, am, gm, b in rows)

# ---- P1
A = sp.Matrix([[5,4],[1,2]])
p, rows, d = show("P1", A)
R["p1:a"] = dict(method="qualitative", answer="(A-λI)x=0 이 x≠0 해를 가지려면 A-λI의 영공간이 비자명 ⇔ A-λI 비가역(rank<n) ⇔ det(A-λI)=0. det≠0이면 역행렬을 곱해 x=0만 남음.", notes="")
R["p1:b"] = dict(method="exact", answer=f"p(λ)=λ²-7λ+6=(λ-1)(λ-6) → λ=6, λ=1", notes=f"sympy: {p}")
R["p1:c"] = dict(method="exact", answer=fmt(rows), notes="E6=span{[4,1]}, E1=span{[1,-1]} (스칼라배 무관)")

# ---- P2
A = sp.Matrix([[3,1],[0,3]])
p, rows, d = show("P2", A)
R["p2:a"] = dict(method="exact", answer="λ=3, 대수적 중복도 2 (p(λ)=(λ-3)²)", notes=f"sympy: {p}")
R["p2:b"] = dict(method="exact", answer="고유벡터 = c·[1,0] (c≠0), E3=span{[1,0]}, 기하적 중복도 1 (<2이므로 결함, 대각화 불가)", notes=fmt(rows))

# ---- P3
A = sp.Matrix([[4,1,1],[1,4,1],[1,1,4]])
p, rows, d = show("P3", A)
x1, x2, x3 = sp.Matrix([-1,1,0]), sp.Matrix([-1,0,1]), sp.Matrix([1,1,1])
for v, l in [(x1,3),(x2,3),(x3,6)]:
    assert A*v == l*v
print("   x3.x1 =", x3.dot(x1), " x3.x2 =", x3.dot(x2), " x1.x2 =", x1.dot(x2))
a, b = sp.symbols('alpha beta')
comb = a*x1 + b*x2
print("   A(αx1+βx2) - 3(αx1+βx2) =", sp.simplify(A*comb - 3*comb).T)
x1p = x1
x2p = x2 - (x2.dot(x1p)/x1p.dot(x1p))*x1p
print("   Gram-Schmidt: x1' =", x1p.T, " x2' =", x2p.T, " x1'.x2' =", x1p.dot(x2p), " A x2' == 3 x2':", A*x2p == 3*x2p)
R["p3:a"] = dict(method="exact", answer="λ=3 (중복 2), λ=6. E3=span{x1=[-1,1,0], x2=[-1,0,1]} (평면 x+y+z=0), E6=span{x3=[1,1,1]}", notes=fmt(rows)+f"; p={p}")
R["p3:b"] = dict(method="exact", answer=f"x3ᵀx1={x3.dot(x1)}, x3ᵀx2={x3.dot(x2)} → 직교. x1ᵀx2={x1.dot(x2)} ≠0 → x1,x2는 직교하지 않음", notes="서로 다른 고윳값의 고유벡터는 대칭행렬에서 자동 직교; 같은 고유공간 안의 기저는 직교 보장 없음")
R["p3:c"] = dict(method="exact", answer=f"A(αx1+βx2)=αAx1+βAx2=3(αx1+βx2) → E3 안. GS: x1'=x1=[-1,1,0], x2'=x2-(x2·x1/x1·x1)x1=x2-½x1={list(x2p.T)} (∝[-1,-1,2]); x1'·x2'=0", notes="정규화하면 [-1,1,0]/√2, [-1,-1,2]/√6")

# ---- P4
A = sp.Rational(1,2)*sp.Matrix([[7,-1],[-1,7]])
p, rows, d = show("P4", A)
p1 = sp.Matrix([1,-1])/sp.sqrt(2); p2 = sp.Matrix([1,1])/sp.sqrt(2)
P = p1.row_join(p2)
Dm = sp.simplify(P.inv()*A*P)
print("   P =", P.tolist(), " P^-1 == P^T:", sp.simplify(P.inv()-P.T)==sp.zeros(2), " D =", Dm.tolist())
R["p4:a"] = dict(method="exact", answer="p(λ)=λ²-7λ+12=(λ-4)(λ-3): λ1=4, λ2=3; p1=[1,-1]/√2, p2=[1,1]/√2 (부호 자유)", notes=f"sympy p={p}; "+fmt(rows))
R["p4:b"] = dict(method="exact", answer="대각화 가능: 서로 다른 고윳값 2개 → 일차독립 고유벡터 2개가 R²의 기저 (또한 대칭행렬이라 스펙트럼 정리로 직교대각화 가능)", notes="")
R["p4:c"] = dict(method="exact", answer=f"P=(1/√2)[[1,1],[-1,1]], D=P⁻¹AP=diag(4,3). P가 직교행렬(정규직교 열)이므로 P⁻¹=Pᵀ, 즉 D=PᵀAP, A=PDPᵀ", notes=f"sympy D={Dm.tolist()}")

# ---- P5
A = sp.Matrix([[1,0],[1,1]]); pa, ra, da = show("P5a", A)
B = sp.Matrix([[-2,2],[2,1]]); pb, rb, db = show("P5b", B)
R["p5:a"] = dict(method="exact", answer="λ=1 (alg 2), E1=span{[0,1]} (geo 1, 대각화 불가)", notes=f"p={pa}; "+fmt(ra))
R["p5:b"] = dict(method="exact", answer="p=λ²+λ-6=(λ+3)(λ-2): E2=span{[1,2]}, E-3=span{[-2,1]} (직교)", notes=f"p={pb}; "+fmt(rb))

# ---- P6
res = []
for i, M in enumerate([sp.Matrix([[1,0],[0,1]]), sp.Matrix([[1,0],[0,0]]), sp.Matrix([[1,1],[0,1]]), sp.Matrix([[0,1],[0,0]])], 1):
    _, rows, d = show(f"P6 M{i}", M)
    res.append((i, d, M.det()!=0, M.det(), fmt(rows)))
R["p6:main"] = dict(method="exact",
    answer="M1: 대각화 가능·가역 (이미 대각, det=1) / M2: 대각화 가능·비가역 (이미 대각, det=0, λ=0 존재) / M3: 대각화 불가·가역 (λ=1 alg2 geo1, det=1) / M4: 대각화 불가·비가역 (λ=0 alg2 geo1, det=0). 네 조합이 모두 나와 두 성질은 독립",
    notes=" | ".join(f"M{i}: diag={d}, inv={inv}, det={dt}; {f}" for i, d, inv, dt, f in res))

# ---- P7
A = sp.Matrix([[2,3,0],[1,4,3],[0,0,1]]); pa, ra, da = show("P7a", A)
R["p7:a"] = dict(method="exact", answer=f"p(λ)=-(λ-1)²(λ-5). E1=span{{[-3,1,0]}} (alg 2, geo 1), E5=span{{[1,1,0]}}. 차원 합 2<3 → 대각화 불가", notes=f"p={pa}; "+fmt(ra)+f"; diag={da}")
A = sp.Matrix([[1,1,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]); pb, rb, db = show("P7b", A)
R["p7:b"] = dict(method="exact", answer="p(λ)=λ³(λ-1). E0=span{[1,-1,0,0],[0,0,1,0],[0,0,0,1]} (geo 3=alg 3), E1=span{[1,0,0,0]}. 차원 합 4 → 대각화 가능 (rank 1이지만 가능; 비가역)", notes=f"p={pb}; "+fmt(rb)+f"; diag={db}")

# ---- P8
A = sp.Matrix([[0,-1,1,1],[-1,1,-2,3],[2,-1,0,0],[1,-1,1,0]]); p8, r8, d8 = show("P8", A)
R["p8:main"] = dict(method="exact", answer=fmt(r8) + f"; 대각화 가능={d8}", notes=f"p(λ)={p8}")

# ---- P9
proof = ("증명: λ≠0, v≠0, AᵀAv=λv 라 하자. u=Av 로 두면 AAᵀu=A(AᵀAv)=λAv=λu. "
         "u≠0인지: u=0이면 λv=AᵀAv=Aᵀ0=0 이고 λ≠0이므로 v=0, 모순. 따라서 λ는 AAᵀ의 고윳값(고유벡터 Av). "
         "A↔Aᵀ 역할을 바꾸면 역방향도 성립. 중복도까지: v1..vk가 AᵀA의 λ-고유공간 기저면 Av1..Avk는 일차독립 "
         "(ΣciAvi=0 ⇒ Aᵀ 곱해 λΣcivi=0 ⇒ ci=0) 이므로 dim E_λ(AᵀA)≤dim E_λ(AAᵀ), 대칭이라 같음; 둘 다 대칭이라 기하=대수 중복도. "
         "고윳값 0의 개수만 n과 m 차이로 달라질 수 있음.")
print("== P9 numerical check")
random.seed(1102)
ok = True
for t in range(6):
    m, n = random.randint(1,5), random.randint(1,5)
    A = sp.Matrix(m, n, lambda i,j: random.randint(-4,4))
    e1 = {k:v for k,v in (A.T*A).eigenvals().items() if k!=0}
    e2 = {k:v for k,v in (A*A.T).eigenvals().items() if k!=0}
    cp1 = sp.Poly((A.T*A).charpoly(lam).as_expr(), lam)
    cp2 = sp.Poly((A*A.T).charpoly(lam).as_expr(), lam)
    # lambda^m p_{A^TA} = lambda^n p_{AA^T}
    rel = sp.expand(lam**m*cp1.as_expr() - lam**n*cp2.as_expr()) == 0
    same = (e1 == e2) and rel
    ok &= same
    print(f"   trial{t}: {m}x{n}, rank={A.rank()}, nonzero eigs equal (with mult)={e1==e2}, λ^m p_AtA = λ^n p_AAt: {rel}")
print("   all ok:", ok)
R["p9:main"] = dict(method="proof", answer=proof, notes=f"sympy 무작위 정수 행렬 6개(seed 1102): 0 아닌 고윳값·중복도 일치 및 λ^m p_AᵀA(λ)=λ^n p_AAᵀ(λ) 확인 = {ok}")

with open(os.path.join(OUT, "blind_results.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
print("wrote blind_results.json")
