#!/usr/bin/env python3
"""Blind independent check for review-1104-PCA_Part2 (p1-p10).

Pure standard library (sympy/numpy not installed): exact arithmetic with
fractions.Fraction for integer/rational matrices, surds handled as
sign * sqrt(rational) with exact squared checks, float checks via math,
and a small Jacobi eigen-solver for the numeric parts (p5, p10).
"""
import math
import random
from fractions import Fraction as F

TOL = 1e-9


# ---------- small linear-algebra helpers ----------
def mat(rows):
    return [[F(x) for x in r] for r in rows]


def T(A):
    return [list(c) for c in zip(*A)]


def mm(A, B):
    return [[sum(a * b for a, b in zip(r, c)) for c in zip(*B)] for r in A]


def mv(A, x):
    return [sum(a * b for a, b in zip(r, x)) for r in A]


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def fmt(v):
    if isinstance(v, list):
        return "[" + ", ".join(fmt(x) for x in v) + "]"
    if isinstance(v, F):
        return str(v)
    return f"{v:.6f}"


def ssqrt(q):
    """sqrt of a non-negative Fraction: exact Fraction if perfect square, else float."""
    q = F(q)
    n, d = q.numerator, q.denominator
    rn, rd = math.isqrt(n), math.isqrt(d)
    if rn * rn == n and rd * rd == d:
        return F(rn, rd)
    return math.sqrt(n / d)


def charpoly_check(M, lam):
    """det(M - lam I) for 2x2 / 3x3 exact."""
    n = len(M)
    B = [[M[i][j] - (lam if i == j else 0) for j in range(n)] for i in range(n)]
    if n == 2:
        return B[0][0] * B[1][1] - B[0][1] * B[1][0]
    a, b, c = B[0]
    d, e, f = B[1]
    g, h, i = B[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def jacobi_eig(S, sweeps=100):
    """Symmetric eigen-decomposition (floats). Returns (eigvals desc, eigvecs as columns list)."""
    n = len(S)
    A = [[float(S[i][j]) for j in range(n)] for i in range(n)]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-30:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-300:
                    continue
                theta = (A[q][q] - A[p][p]) / (2 * A[p][q])
                t = (1 if theta >= 0 else -1) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p] = c * vkp - s * vkq
                    V[k][q] = s * vkp + c * vkq
    vals = [A[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: -vals[i])
    return [vals[i] for i in order], [[V[k][i] for k in range(n)] for i in order]


def check(label, cond):
    print(f"  [{'OK' if cond else 'FAIL'}] {label}")
    assert cond, label


def svd_reconstruct_float(sig, U, V, m, n):
    """sum_i sig_i u_i v_i^T with float entries."""
    R = [[0.0] * n for _ in range(m)]
    for s, u, v in zip(sig, U, V):
        for i in range(m):
            for j in range(n):
                R[i][j] += s * u[i] * v[j]
    return R


def close(A, B, tol=TOL):
    return all(abs(float(a) - float(b)) < tol for ra, rb in zip(A, B) for a, b in zip(ra, rb))


# ---------- P3(b) ----------
def p3():
    print("=== p3:b  J*_784 ===")
    D, M = 784, 784
    terms = list(range(M + 1, D + 1))
    print(f"  index set {{M+1..D}} = range({M+1},{D+1}) has {len(terms)} terms -> empty sum = 0")
    check("J*_784 = 0 (empty sum)", sum(F(0) for _ in terms) == 0)
    # with M = D the projection matrix B B^T of an orthonormal basis of R^D is I
    random.seed(0)
    n = 5
    S = [[random.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    S = [[sum(S[k][i] * S[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    _, B = jacobi_eig(S)
    P = [[sum(B[k][i] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    check("toy D=5: B B^T = I when all D PCs used (so x~ = x)",
          close(P, [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)], 1e-9))


# ---------- P4 ----------
def p4():
    print("=== p4  A = [[1,1,0],[0,1,1]] ===")
    A = mat([[1, 1, 0], [0, 1, 1]])
    AtA = mm(T(A), A)
    print("  p4:a A^T A =", fmt(AtA))
    lams = [F(3), F(1), F(0)]
    for l in lams:
        check(f"det(A^T A - {l} I) = 0", charpoly_check(AtA, l) == 0)
    vt = [[1, 2, 1], [1, 0, -1], [1, -1, 1]]
    for l, v in zip(lams, vt):
        v = [F(x) for x in v]
        check(f"A^T A {fmt(v)} = {l}*v", mv(AtA, v) == [l * x for x in v])
    norms2 = [dot([F(x) for x in v], [F(x) for x in v]) for v in vt]
    print("  ||v~||^2 =", fmt(norms2), "-> v1=(1,2,1)/sqrt6, v2=(1,0,-1)/sqrt2, v3=(1,-1,1)/sqrt3")
    Vf = [[x / math.sqrt(float(nn)) for x in v] for v, nn in zip(vt, norms2)]
    VtV = [[dot(a, b) for b in Vf] for a in Vf]
    check("V orthonormal", close(VtV, [[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
    sig = [ssqrt(l) for l in lams[:2]]
    print("  p4:b sigma =", [f"{float(s):.6f}" for s in sig], "= (sqrt3, 1); Sigma = [[sqrt3,0,0],[0,1,0]] (2x3)")
    # u_i = A v_i / sigma_i ; check exactly via squares
    U = []
    for i in range(2):
        Av = mv(A, [F(x) for x in vt[i]])  # A v~_i (unnormalised)
        # u_i = Av~ / (||v~|| sigma_i);  ||Av~||^2 = sigma_i^2 ||v~||^2 must hold
        check(f"||A v~{i+1}||^2 = sigma^2 ||v~||^2", dot(Av, Av) == lams[i] * norms2[i])
        u = [float(x) / (math.sqrt(float(norms2[i])) * float(sig[i])) for x in Av]
        U.append(u)
        print(f"  p4:c A v~{i+1} = {fmt(Av)} -> u{i+1} = {fmt(u)}")
    print("        i.e. u1=(1,1)/sqrt2, u2=(1,-1)/sqrt2")
    R = svd_reconstruct_float([float(s) for s in sig], U, Vf, 2, 3)
    check("U Sigma V^T = A", close(R, A))
    check("U orthonormal", close([[dot(a, b) for b in U] for a in U], [[1, 0], [0, 1]]))
    print("  p4:d sizes: U 2x2, Sigma 2x3, V 3x3 (V^T 3x3)")


# ---------- P5 ----------
def p5():
    print("=== p5  movie ratings ===")
    A = [[5, 4, 1], [5, 5, 0], [0, 0, 5], [1, 0, 4]]
    s = [9.6438, 6.3639, 0.7056]
    u1 = [-0.6710, -0.7197, -0.0939, -0.1515]
    u2 = [0.0236, 0.2054, -0.7705, -0.6030]
    v1 = [-0.7367, -0.6515, -0.1811]
    v2 = [0.0852, 0.1762, -0.9807]
    c = 2  # Chandra column
    L1 = [s[0] * v1[c] * x for x in u1]
    L2 = [s[1] * v2[c] * x for x in u2]
    A2 = [a + b for a, b in zip(L1, L2)]
    print(f"  p5:a sigma1*v1[Chandra] = {s[0]*v1[c]:.6f}; layer1 Chandra col = {fmt(L1)}")
    print(f"       rounded 4dp: {[round(x, 4) for x in L1]}")
    print(f"  p5:b sigma2*v2[Chandra] = {s[1]*v2[c]:.6f}; layer2 Chandra col = {fmt(L2)}")
    print(f"       A^(2) Chandra col = {fmt(A2)} (rounded {[round(x, 4) for x in A2]})")
    diff = [a - b for a, b in zip([r[c] for r in A], A2)]
    print(f"       A - A^(2) (Chandra) = {fmt(diff)}  max|diff| = {max(abs(x) for x in diff):.4f}")
    fro2 = sum(x * x for r in A for x in r)
    print(f"  p5:c ||A||_F^2 = {fro2} ; sum sigma^2 = {sum(x*x for x in s):.4f}")
    print(f"       sigma3^2 = {s[2]**2:.6f}; sigma3^2/||A||_F^2 = {s[2]**2/fro2:.6%}; "
          f"(s1^2+s2^2)/||A||_F^2 = {(s[0]**2+s[1]**2)/fro2:.4%}; sigma3/sigma1 = {s[2]/s[0]:.4f}")
    print(f"       ||A - A^(2)||_F = sigma3 = {s[2]} (Eckart-Young), so every entry error <= {s[2]}")
    # independent recomputation of the SVD from A (Jacobi on A^T A)
    AtA = [[sum(A[k][i] * A[k][j] for k in range(4)) for j in range(3)] for i in range(3)]
    vals, vecs = jacobi_eig(AtA)
    sig = [math.sqrt(max(v, 0)) for v in vals]
    print("  independent: A^T A =", AtA, "eig =", [f"{v:.6f}" for v in vals])
    print("  independent: sigma =", [f"{x:.4f}" for x in sig])
    for i in range(3):
        print(f"    v{i+1} (sign-free) = {[round(x, 4) for x in vecs[i]]}")
    Us = [[sum(A[r][k] * vecs[i][k] for k in range(3)) / sig[i] for r in range(4)] for i in range(3)]
    for i in range(3):
        print(f"    u{i+1} = {[round(x, 4) for x in Us[i]]}")
    Ah2 = svd_reconstruct_float(sig[:2], Us[:2], vecs[:2], 4, 3)
    print("  independent full A^(2) =")
    for r in Ah2:
        print("    ", [round(x, 4) for x in r])
    err = math.sqrt(sum((A[i][j] - Ah2[i][j]) ** 2 for i in range(4) for j in range(3)))
    check("||A - A^(2)||_F == sigma3 (indep.)", abs(err - sig[2]) < 1e-9)
    check("given sigmas match independent to 4dp", all(abs(a - b) < 6e-5 for a, b in zip(s, sig)))


# ---------- P6 ----------
def p6():
    print("=== p6  projection identity ===")
    # Polynomial algebra in pi with relation pi^2 = pi (coefficients: {0: c_id, 1: c_pi})
    def pmul(p, q):
        r = {0: 0, 1: 0}
        for a, ca in p.items():
            for b, cb in q.items():
                r[min(a + b, 1)] += ca * cb  # pi^k = pi for k>=1
        return r
    rho = {0: 1, 1: -1}  # id - pi
    print("  p6:a (id - pi)^2 with pi^2 = pi :", pmul(rho, rho), "== id - pi ->", pmul(rho, rho) == rho)
    check("(id-pi)^2 = id-pi given pi^2=pi", pmul(rho, rho) == rho)
    # without the relation: (id-pi)^2 = id - 2pi + pi^2 ; equals id - pi  <=> pi^2 = pi
    print("  without relation: (id-pi)^2 = id - 2 pi + pi^2 ; = id - pi  <=> pi^2 = pi (both directions)")
    # concrete oblique (non-orthogonal) projection
    P = mat([[1, 2], [0, 0]])
    I = mat([[1, 0], [0, 1]])
    Q = [[I[i][j] - P[i][j] for j in range(2)] for i in range(2)]
    check("P=[[1,2],[0,0]] oblique: P^2 = P", mm(P, P) == P)
    check("(I-P)^2 = I-P", mm(Q, Q) == Q)
    # p6:b direction: take rho = id - pi a projection; then id - rho = pi is projection
    Rh = mat([[0, 0], [3, 1]])  # rho^2 = rho
    check("rho=[[0,0],[3,1]]: rho^2 = rho", mm(Rh, Rh) == Rh)
    Pi = [[I[i][j] - Rh[i][j] for j in range(2)] for i in range(2)]
    check("pi = I - rho satisfies pi^2 = pi", mm(Pi, Pi) == Pi)
    # counter-check: non-projection N -> I-N not projection
    N = mat([[2, 0], [0, 0]])
    QN = [[I[i][j] - N[i][j] for j in range(2)] for i in range(2)]
    check("N non-projection => I-N non-projection", mm(N, N) != N and mm(QN, QN) != QN)


# ---------- P7 / P9 ----------
def p7_p9():
    print("=== p7 / p9  A = [[3,2,2],[2,3,-2]] ===")
    A = mat([[3, 2, 2], [2, 3, -2]])
    AAt = mm(A, T(A))
    print("  p7:a A A^T =", fmt(AAt))
    lams = [F(25), F(9)]
    for l in lams:
        check(f"det(AA^T - {l} I) = 0", charpoly_check(AAt, l) == 0)
    ut = [[F(1), F(1)], [F(1), F(-1)]]
    for l, u in zip(lams, ut):
        check(f"AA^T {fmt(u)} = {l} u", mv(AAt, u) == [l * x for x in u])
    sig = [F(5), F(3)]
    print("       sigma1=5, sigma2=3 ; u1=(1,1)/sqrt2, u2=(1,-1)/sqrt2")
    vs = []
    for i in range(2):
        Atu = mv(T(A), ut[i])  # A^T u~ ; v = A^T u~ /(sqrt2 sigma)
        vs.append(Atu)
        print(f"  p7:b A^T u~{i+1} = {fmt(Atu)} -> v{i+1} = {fmt(Atu)}/({sig[i]}*sqrt2)")
        check(f"||A^T u~{i+1}||^2 = sigma^2 * 2", dot(Atu, Atu) == sig[i] ** 2 * 2)
    print("       v1 = (1,1,0)/sqrt2 ; v2 = (1,-1,4)/(3 sqrt2)")
    a, b = vs
    cross = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    print(f"  p7:c cross(v~1, v~2) = {fmt(cross)} ; ||.||^2 = {dot(cross, cross)}")
    v3 = [x / 30 for x in cross]  # (2,-2,-1)/3 up to sign... check norm
    v3 = [F(2, 3), F(-2, 3), F(-1, 3)]
    check("v3 = (2,-2,-1)/3 unit", dot(v3, v3) == 1)
    check("v3 perp v1, v2", dot(v3, vs[0]) == 0 and dot(v3, vs[1]) == 0)
    Av3 = mv(A, v3)
    print(f"  p7:d A v3 = {fmt(Av3)}")
    check("A v3 = 0", Av3 == [0, 0])
    AtA = mm(T(A), A)
    check("A^T A v3 = 0 (v3 eigvec with eigenvalue 0 = sigma3^2)", mv(AtA, v3) == [0, 0, 0])
    # full reconstruction float
    Uf = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]
    Vf = [[float(x) / (5 * math.sqrt(2)) for x in vs[0]], [float(x) / (3 * math.sqrt(2)) for x in vs[1]]]
    R = svd_reconstruct_float([5.0, 3.0], Uf, Vf, 2, 3)
    check("U Sigma V^T = A", close(R, A))

    # P9
    print("  p9:a sigma1 = 5, u1 = (1,1)/sqrt2, v1 = (1,1,0)/sqrt2")
    # A1 = 5 * (1/2) * [1,1]^T [1,1,0]
    A1 = [[F(5, 2) * x * y for y in [1, 1, 0]] for x in [1, 1]]
    print("  p9:b A1 =", fmt(A1))
    E = [[A[i][j] - A1[i][j] for j in range(3)] for i in range(2)]
    e2 = sum(x * x for r in E for x in r)
    print("  p9:c A - A1 =", fmt(E), "; sum of squares =", e2, "; sigma2^2 =", sig[1] ** 2)
    check("||A-A1||_F^2 = 9 = sigma2^2", e2 == 9)
    check("A - A1 = sigma2 u2 v2^T", E == [[F(3, 2) * x * y / 3 for y in [1, -1, 4]] for x in [1, -1]])


# ---------- P8 ----------
def p8():
    print("=== p8  A = [[2,2],[-1,1]] ===")
    A = mat([[2, 2], [-1, 1]])
    AtA = mm(T(A), A)
    print("  p8:a A^T A =", fmt(AtA))
    lams = [F(8), F(2)]
    vt = [[F(1), F(1)], [F(1), F(-1)]]
    for l, v in zip(lams, vt):
        check(f"A^T A {fmt(v)} = {l} v", mv(AtA, v) == [l * x for x in v])
    print("       V = (1/sqrt2)[[1,1],[1,-1]]  (columns v1=(1,1)/sqrt2, v2=(1,-1)/sqrt2)")
    print("  p8:b sigma1 = sqrt8 = 2sqrt2, sigma2 = sqrt2")
    for i in range(2):
        Av = mv(A, vt[i])
        print(f"       A v~{i+1} = {fmt(Av)} ; u{i+1} = A v~/(sqrt2*sigma) = {fmt([F(x) / F(2) / ssqrt(lams[i]) if isinstance(ssqrt(lams[i]), F) else float(x)/(math.sqrt(2)*math.sqrt(float(lams[i]))) for x in Av])}")
    print("       u1 = (1,0), u2 = (0,-1)  [with v2=(-1,1)/sqrt2 instead: u2=(0,1)]")
    Uf = [[1.0, 0.0], [0.0, -1.0]]
    Vf = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]
    R = svd_reconstruct_float([2 * math.sqrt(2), math.sqrt(2)], Uf, Vf, 2, 2)
    check("U Sigma V^T = A", close(R, A))
    AAt = mm(A, T(A))
    print("  p8:c A A^T =", fmt(AAt))
    check("AA^T e1 = 8 e1 = sigma1^2 u1", mv(AAt, [F(1), F(0)]) == [F(8), F(0)])
    check("AA^T (0,-1) = 2 (0,-1) = sigma2^2 u2", mv(AAt, [F(0), F(-1)]) == [F(0), F(-2)])


# ---------- P10 ----------
def p10():
    print("=== p10  spectral norm = sigma1 (numeric sanity only) ===")
    random.seed(1)
    m, n = 4, 3
    A = [[random.gauss(0, 1) for _ in range(n)] for _ in range(m)]
    AtA = [[sum(A[k][i] * A[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
    vals, vecs = jacobi_eig(AtA)
    s = [math.sqrt(max(v, 0)) for v in vals]
    worst = 0.0
    for _ in range(20000):
        x = [random.gauss(0, 1) for _ in range(n)]
        Ax = [sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]
        c = [sum(v[k] * x[k] for k in range(n)) for v in vecs]
        lhs = sum(t * t for t in Ax)
        rhs = sum(si * si * ci * ci for si, ci in zip(s, c))
        assert abs(lhs - rhs) < 1e-8 * max(1, lhs)
        worst = max(worst, math.sqrt(lhs / sum(t * t for t in x)))
    Av1 = [sum(A[i][j] * vecs[0][j] for j in range(n)) for i in range(m)]
    r1 = math.sqrt(sum(t * t for t in Av1))
    print(f"  sigma = {[round(x, 6) for x in s]}")
    print(f"  p10:a ||Ax||^2 = sum sigma_i^2 c_i^2 verified for 20000 random x")
    print(f"  p10:b max ratio over random x = {worst:.6f} <= sigma1 = {s[0]:.6f}")
    print(f"  p10:c ||A v1|| / ||v1|| = {r1:.6f} = sigma1")
    check("random ratios never exceed sigma1", worst <= s[0] + 1e-12)
    check("ratio at v1 equals sigma1", abs(r1 - s[0]) < 1e-9)


if __name__ == "__main__":
    p3()
    p4()
    p5()
    p6()
    p7_p9()
    p8()
    p10()
    print("ALL CHECKS PASSED")
