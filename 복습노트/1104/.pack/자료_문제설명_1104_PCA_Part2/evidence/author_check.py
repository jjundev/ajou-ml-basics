"""1104 PCA Part2 문제설명 저작자 검산.

설명 조각(solve/verify/pitfall/sum)에 적은 모든 수치 주장을 sympy 정확 연산 또는
반올림 규칙이 명시된 수치 연산으로 다시 계산한다. 증명 문항(p6, p10)은 기호 항등식을
보조로 확인하고, 일반 논증은 independent-review.md에 기록한다.
"""
import json
import random
from sympy import (Matrix, Rational, eye, simplify, sqrt, symbols, zeros,
                   factor, expand, Function, nsimplify)

results = []


def check(key, desc, ok, detail=""):
    results.append({"item": key, "claim": desc, "pass": bool(ok), "detail": str(detail)})


lam = symbols("lambda")

# ---------------- p1 ----------------
lams = symbols("l1:8")
V = lambda M: sum(lams[:M])
check("p1:a", "V_M - V_{M-1} = lambda_M (M=1..7, V_0=0)",
      all(simplify(V(M) - V(M - 1) - lams[M - 1]) == 0 for M in range(1, 8)))
check("p1:a", "V_2 ~ 46+32 = 78 (figure reading arithmetic)", 46 + 32 == 78)
check("p1:b", "0->50: ~370, 150->200: ~525-505 = 20, 50->200: 525-370 = 155",
      (370 - 0, 525 - 505, 525 - 370) == (370, 20, 155))

# ---------------- p3 ----------------
check("p3:b", "J_784 = empty sum over i=785..784 = 0", sum([] ) == 0 and list(range(785, 785)) == [])
# J_M - J_{M+1} = lambda_{M+1} >= 0  (symbolic, D=6 toy, nonnegative eigenvalues)
D = 6
ev = [Rational(x) for x in (9, 5, 3, 2, 1, 0)]
J = lambda M: sum(ev[M:])
check("p3:c", "J_M - J_{M+1} = lambda_{M+1} >= 0 (toy D=6)",
      all(J(M) - J(M + 1) == ev[M] and ev[M] >= 0 for M in range(D)))
check("p3:c", "J_M nonincreasing so J_550 <= J_500 <= J_400 (toy monotone)",
      all(J(M) >= J(M + 1) for M in range(D)))
# full square orthonormal B => B B^T = I and b_j^T B B^T x = b_j^T x  (random 4x4 orthonormal via Gram-Schmidt)
random.seed(1)
Mx = Matrix(4, 4, lambda i, j: random.randint(-3, 3))
while Mx.det() == 0:
    Mx = Matrix(4, 4, lambda i, j: random.randint(-3, 3))
Q = Matrix.hstack(*[c.normalized() for c in Matrix.orthogonalize(*[Mx[:, k] for k in range(4)])])
check("p3:b", "square orthonormal B: B^T B = I and B B^T = I (4x4 example)",
      simplify(Q.T * Q - eye(4)) == zeros(4) and simplify(Q * Q.T - eye(4)) == zeros(4))
# zero-variance pixel -> S e_d = 0
Xc = Matrix([[1, -1, 2, -2], [0, 0, 0, 0], [3, -3, 1, -1]])  # centered rows, pixel 2 constant 0
S = Xc * Xc.T / 4
check("p3:c", "pixel with zero variance: S e_d = 0 (eigenvalue 0)", S * Matrix([0, 1, 0]) == zeros(3, 1))

# ---------------- p4 ----------------
A = Matrix([[1, 1, 0], [0, 1, 1]])
AtA = A.T * A
check("p4:a", "A^T A = [[1,1,0],[1,2,1],[0,1,1]]", AtA == Matrix([[1, 1, 0], [1, 2, 1], [0, 1, 1]]))
cp = (AtA - lam * eye(3)).det()
check("p4:a", "first-row cofactor form equals det",
      expand((1 - lam) * ((2 - lam) * (1 - lam) - 1) - (1 - lam) - cp) == 0)
check("p4:a", "det = (1-l)(l^2-3l) = -l(l-1)(l-3)",
      expand(cp - (1 - lam) * (lam**2 - 3 * lam)) == 0 and expand(cp + lam * (lam - 1) * (lam - 3)) == 0)
check("p4:a", "(2-l)(1-l) = l^2-3l+2", expand((2 - lam) * (1 - lam) - (lam**2 - 3 * lam + 2)) == 0)
w = {3: Matrix([1, 2, 1]), 1: Matrix([1, 0, -1]), 0: Matrix([1, -1, 1])}
check("p4:a", "eigvecs (1,2,1),(1,0,-1),(1,-1,1) with AtA products (3,6,3),(1,0,-1),(0,0,0)",
      all(AtA * v == k * v for k, v in w.items()) and AtA * w[3] == Matrix([3, 6, 3]))
check("p4:a", "pairwise dot products 0", w[3].dot(w[1]) == 0 and w[3].dot(w[0]) == 0 and w[1].dot(w[0]) == 0)
v1, v2, v3 = w[3] / sqrt(6), w[1] / sqrt(2), w[0] / sqrt(3)
Vm = Matrix.hstack(v1, v2, v3)
check("p4:a", "V orthonormal", simplify(Vm.T * Vm) == eye(3))
s1 = sqrt(3)
s2 = 1
Sig = Matrix([[sqrt(3), 0, 0], [0, 1, 0]])
check("p4:b", "sigma = sqrt3, 1", sqrt(3)**2 == 3 and 1**2 == 1)
check("p4:c", "A v1 = (3,3)/sqrt6, u1 = (1,1)/sqrt2, 3/sqrt18 = 1/sqrt2",
      simplify(A * v1 - Matrix([3, 3]) / sqrt(6)) == zeros(2, 1) and simplify(3 / sqrt(18) - 1 / sqrt(2)) == 0)
u1 = simplify(A * v1 / sqrt(3)); u2 = simplify(A * v2 / 1)
U = Matrix.hstack(u1, u2)
check("p4:c", "U = 1/sqrt2 [[1,1],[1,-1]]", simplify(U - Matrix([[1, 1], [1, -1]]) / sqrt(2)) == zeros(2))
check("p4:c", "A v3 = 0", simplify(A * v3) == zeros(2, 1))
check("p4:c", "A = U Sigma V^T", simplify(U * Sig * Vm.T - A) == zeros(2, 3))
check("p4:c", "layer coefficients sqrt3/sqrt12 = 1/2 and layers sum to A",
      simplify(sqrt(3) / sqrt(12) - Rational(1, 2)) == 0 and
      Rational(1, 2) * Matrix([[1, 2, 1], [1, 2, 1]]) + Rational(1, 2) * Matrix([[1, 0, -1], [-1, 0, 1]]) == A)
AAt = A * A.T
check("p4:b", "A A^T = [[2,1],[1,2]] eigenvalues 3,1; |A v1| = sqrt3",
      AAt == Matrix([[2, 1], [1, 2]]) and set(AAt.eigenvals()) == {3, 1} and simplify((A * v1).norm() - sqrt(3)) == 0)
check("p4:c", "A A^T u1 = 3 u1, A A^T u2 = u2", simplify(AAt * u1 - 3 * u1) == zeros(2, 1) and simplify(AAt * u2 - u2) == zeros(2, 1))
check("p4:d", "sizes U 2x2, Sigma 2x3, V 3x3; product 2x3", (U.shape, Sig.shape, Vm.shape, (U * Sig * Vm.T).shape) == ((2, 2), (2, 3), (3, 3), (2, 3)))
bad = simplify(Matrix.hstack(-u1, u2) * Sig * Vm.T)
check("p4:pitfall", "flipping u1 only gives [[0,-1,-1],[-1,-1,0]]", bad == Matrix([[0, -1, -1], [-1, -1, 0]]))
check("p4:pitfall", "sigma1=3 => |A v1/3| = 1/sqrt3", simplify((A * v1 / 3).norm() - 1 / sqrt(3)) == 0)

# ---------------- p5 ----------------
s = [9.6438, 6.3639, 0.7056]
U1 = [-0.6710, -0.7197, -0.0939, -0.1515]
U2 = [0.0236, 0.2054, -0.7705, -0.6030]
V1 = [-0.7367, -0.6515, -0.1811]
V2 = [0.0852, 0.1762, -0.9807]
k1 = s[0] * V1[2]
k2 = s[1] * V2[2]
L1 = [k1 * x for x in U1]
L2 = [k2 * x for x in U2]
A2 = [a + b for a, b in zip(L1, L2)]
r4 = lambda xs: [round(x + 0.0, 4) for x in xs]
check("p5:a", "sigma1*(-0.1811) = -1.7465 (raw -1.74649)", round(k1, 4) == -1.7465 and abs(k1 + 1.74649) < 1e-5, k1)
check("p5:a", "layer1 Chandra = (1.1719,1.2570,0.1640,0.2646)", r4(L1) == [1.1719, 1.2570, 0.1640, 0.2646], L1)
check("p5:a", "Star Wars entry 1.74649*0.6710 = 1.1719", round(1.74649 * 0.6710, 4) == 1.1719)
check("p5:b", "sigma2*(-0.9807) = -6.2411", round(k2, 4) == -6.2411, k2)
check("p5:b", "layer2 Chandra = (-0.1473,-1.2819,4.8087,3.7634)", r4(L2) == [-0.1473, -1.2819, 4.8087, 3.7634], L2)
check("p5:b", "A(2) Chandra = (1.0246,-0.0250,4.9727,4.0280)", r4(A2) == [1.0246, -0.0250, 4.9727, 4.0280], A2)
check("p5:b", "Blade Runner 1.25695 + (-1.28192) = -0.02497", round(L1[1], 5) == 1.25695 and round(L2[1], 5) == -1.28192 and round(L1[1] + L2[1], 5) == -0.02497)
diffs = [abs(a - b) for a, b in zip(A2, [1, 0, 5, 4])]
check("p5:b", "differences (0.0246,0.0250,0.0273,0.0280) all <= 0.03", r4(diffs) == [0.0246, 0.0250, 0.0273, 0.0280] and max(diffs) <= 0.03, diffs)
book = [1.0244, -0.0250, 4.9724, 4.0278]
check("p5:b", "max diff vs book (4.102) <= 0.0003", max(abs(a - b) for a, b in zip(r4(A2), book)) <= 0.0003 + 1e-12)
Am = [[5, 4, 1], [5, 5, 0], [0, 0, 5], [1, 0, 4]]
rows = [sum(x * x for x in r) for r in Am]
check("p5:c", "row sums of squares 42,50,25,17; total 134", rows == [42, 50, 25, 17] and sum(rows) == 134)
check("p5:c", "sigma3^2 = 0.4979, ratio 0.37%", round(s[2]**2, 4) == 0.4979 and round(s[2]**2 / 134 * 100, 2) == 0.37)
check("p5:c", "sigma3/sigma1 ~ 0.07", round(s[2] / s[0], 2) == 0.07)
sq = [x * x for x in s]
check("p5:c", "squares 93.003, 40.499, 0.498 sum 134.000; kept 99.63%",
      [round(x, 3) for x in sq] == [93.003, 40.499, 0.498] and round(sum(sq), 3) == 134.0 and round((sq[0] + sq[1]) / 134 * 100, 2) == 99.63)
book1 = [0.1215, 0.1303, 0.0170, 0.0274]
check("p5:a", "book (4.100b) col3 * sigma1 = (1.1717,1.2566,0.1639,0.2642)", r4([s[0] * x for x in book1]) == [1.1717, 1.2566, 0.1639, 0.2642])
amelie = [s[0] * U1[2] * x for x in V1]
check("p5:pitfall", "row mix-up gives Amelie row (0.6671,0.5900,0.1640)", r4(amelie) == [0.6671, 0.5900, 0.1640], amelie)
# rank-one Frobenius identity ||s u v^T||_F^2 = s^2 for unit u, v (symbolic)
a, b, c, d, e = symbols("a b c d e", real=True)
uu = Matrix([a, b]); vv = Matrix([c, d, e]); sg = symbols("s", positive=True)
lhs = sum(x**2 for x in (sg * uu * vv.T))
check("p5:c", "||s u v^T||_F^2 = s^2 |u|^2 |v|^2", expand(lhs - sg**2 * (a**2 + b**2) * (c**2 + d**2 + e**2)) == 0)

# ---------------- p6 ----------------
# symbolic check with a generic idempotent example and noncommutative identity
P = Matrix([[1, 2], [0, 0]])  # oblique projection: P^2 = P
check("p6:a", "example oblique projection P^2=P and (I-P)^2 = I-P", P * P == P and (eye(2) - P)**2 == eye(2) - P)
Mq = Matrix(2, 2, symbols("m0:4"))
check("p6:a", "(I-M)^2 = I - 2M + M^2 for generic 2x2 M", expand((eye(2) - Mq)**2 - (eye(2) - 2 * Mq + Mq**2)) == zeros(2))
check("p6:pitfall", "dropping one cross term then using M^2=M gives I (wrong)", (eye(2) - P + P * P) == eye(2))
check("p6:b", "id - (id - P) = P", eye(2) - (eye(2) - P) == P)
B = Matrix([[1], [1]]) / sqrt(2)
PB = B * B.T
check("p6:a", "B^T B = I => (BB^T)^2 = BB^T and (I-BB^T)^2 = I-BB^T",
      simplify(B.T * B) == eye(1) and simplify(PB * PB - PB) == zeros(2) and simplify((eye(2) - PB)**2 - (eye(2) - PB)) == zeros(2))

# ---------------- p7 / p9 ----------------
A = Matrix([[3, 2, 2], [2, 3, -2]])
AAt = A * A.T
check("p7:a", "A A^T = [[17,8],[8,17]], (17-l)^2-64, eigen 25,9",
      AAt == Matrix([[17, 8], [8, 17]]) and expand((AAt - lam * eye(2)).det() - ((17 - lam)**2 - 64)) == 0 and set(AAt.eigenvals()) == {25, 9})
u1 = Matrix([1, 1]) / sqrt(2); u2 = Matrix([1, -1]) / sqrt(2)
check("p7:a", "A A^T u1 = 25 u1, u2 = 9 u2", simplify(AAt * u1 - 25 * u1) == zeros(2, 1) and simplify(AAt * u2 - 9 * u2) == zeros(2, 1))
check("p7:a", "||A||_F^2 = 34 = 25 + 9", sum(x**2 for x in A) == 34)
check("p7:b", "A^T(1,1) = (5,5,0), A^T(1,-1) = (1,-1,4)", A.T * Matrix([1, 1]) == Matrix([5, 5, 0]) and A.T * Matrix([1, -1]) == Matrix([1, -1, 4]))
v1 = simplify(A.T * u1 / 5); v2 = simplify(A.T * u2 / 3)
check("p7:b", "v1 = (1,1,0)/sqrt2, v2 = (1,-1,4)/(3sqrt2), |v2|^2 = 18/18",
      simplify(v1 - Matrix([1, 1, 0]) / sqrt(2)) == zeros(3, 1) and simplify(v2 - Matrix([1, -1, 4]) / (3 * sqrt(2))) == zeros(3, 1) and simplify(v2.norm()**2) == 1)
check("p7:b", "A v1 = 5 u1, A(1,-1,4) = (9,-9), A v2 = 3 u2",
      simplify(A * v1 - 5 * u1) == zeros(2, 1) and A * Matrix([1, -1, 4]) == Matrix([9, -9]) and simplify(A * v2 - 3 * u2) == zeros(2, 1))
v3 = Matrix([2, -2, -1]) / 3
check("p7:c", "v3 orthogonal to (1,1,0),(1,-1,4), |(2,-2,-1)| = 3",
      Matrix([1, 1, 0]).dot(Matrix([2, -2, -1])) == 0 and Matrix([1, -1, 4]).dot(Matrix([2, -2, -1])) == 0 and Matrix([2, -2, -1]).norm() == 3)
Vm = Matrix.hstack(v1, v2, v3)
check("p7:c", "V orthonormal", simplify(Vm.T * Vm) == eye(3))
check("p7:d", "A v3 = 0 (rows: 6-4-2, 4-6+2)", A * v3 == zeros(2, 1))
check("p7:d", "rows = 1/2(5,5,0) +- 1/2(1,-1,4)",
      Rational(1, 2) * Matrix([[5, 5, 0]]) + Rational(1, 2) * Matrix([[1, -1, 4]]) == A[0, :] and
      Rational(1, 2) * Matrix([[5, 5, 0]]) - Rational(1, 2) * Matrix([[1, -1, 4]]) == A[1, :])
Sig = Matrix([[5, 0, 0], [0, 3, 0]])
Um = Matrix.hstack(u1, u2)
check("p7:d", "A V = U Sigma and A = U Sigma V^T", simplify(A * Vm - Um * Sig) == zeros(2, 3) and simplify(Um * Sig * Vm.T - A) == zeros(2, 3))
layer2 = simplify(3 * u2 * v2.T)
check("p7:d", "3 u2 v2^T coefficient 1/2 and layers sum to A",
      simplify(3 / (sqrt(2) * 3 * sqrt(2)) - Rational(1, 2)) == 0 and layer2 == Rational(1, 2) * Matrix([[1, -1, 4], [-1, 1, -4]]) and
      Rational(5, 2) * Matrix([[1, 1, 0], [1, 1, 0]]) + layer2 == A)
check("p7:pitfall", "flip v2 only -> [[2,3,-2],[3,2,2]]",
      Rational(5, 2) * Matrix([[1, 1, 0], [1, 1, 0]]) - layer2 == Matrix([[2, 3, -2], [3, 2, 2]]))
check("p7:pitfall", "|A^T u1| = 5", simplify((A.T * u1).norm()) == 5)

A1 = simplify(5 * u1 * v1.T)
check("p9:b", "A1 = 5/2 [[1,1,0],[1,1,0]], u1 v1^T = 1/2[[1,1,0],[1,1,0]]",
      A1 == Rational(5, 2) * Matrix([[1, 1, 0], [1, 1, 0]]) and simplify(u1 * v1.T) == Rational(1, 2) * Matrix([[1, 1, 0], [1, 1, 0]]))
R = A - A1
check("p9:c", "A - A1 = [[1/2,-1/2,2],[-1/2,1/2,-2]], sum sq 9 = sigma2^2, = 3 u2 v2^T",
      R == Matrix([[Rational(1, 2), Rational(-1, 2), 2], [Rational(-1, 2), Rational(1, 2), -2]]) and sum(x**2 for x in R) == 9 and R == layer2)
check("p9:b", "||A1||_F^2 = 25", sum(x**2 for x in A1) == 25)
check("p9:a", "A v1 = (5,5)/sqrt2", simplify(A * v1 - Matrix([5, 5]) / sqrt(2)) == zeros(2, 1))
noS = A - Rational(1, 2) * Matrix([[1, 1, 0], [1, 1, 0]])
check("p9:pitfall", "without sigma1 error sum sq = (2.5^2+1.5^2+2^2)*2 = 25", sum(x**2 for x in noS) == 25)
check("p9:pitfall", "||A-A1||_F = 3", sqrt(sum(x**2 for x in R)) == 3)

# ---------------- p8 ----------------
A = Matrix([[2, 2], [-1, 1]])
AtA = A.T * A
check("p8:a", "A^T A = [[5,3],[3,5]], (5-l)^2-9, eigen 8,2",
      AtA == Matrix([[5, 3], [3, 5]]) and expand((AtA - lam * eye(2)).det() - ((5 - lam)**2 - 9)) == 0 and set(AtA.eigenvals()) == {8, 2})
check("p8:a", "AtA(1,1) = 8(1,1), AtA(1,-1) = 2(1,-1)", AtA * Matrix([1, 1]) == 8 * Matrix([1, 1]) and AtA * Matrix([1, -1]) == 2 * Matrix([1, -1]))
v1 = Matrix([1, 1]) / sqrt(2); v2 = Matrix([1, -1]) / sqrt(2)
Vm = Matrix.hstack(v1, v2)
check("p8:b", "A(1,1) = (4,0), A(1,-1) = (0,-2)", A * Matrix([1, 1]) == Matrix([4, 0]) and A * Matrix([1, -1]) == Matrix([0, -2]))
u1 = simplify(A * v1 / (2 * sqrt(2))); u2 = simplify(A * v2 / sqrt(2))
check("p8:b", "u1 = (1,0), u2 = (0,-1)", u1 == Matrix([1, 0]) and u2 == Matrix([0, -1]))
Um = Matrix.hstack(u1, u2); Sig = Matrix([[2 * sqrt(2), 0], [0, sqrt(2)]])
check("p8:b", "U Sigma = [[2sqrt2,0],[0,-sqrt2]] and U Sigma V^T = A",
      Um * Sig == Matrix([[2 * sqrt(2), 0], [0, -sqrt(2)]]) and simplify(Um * Sig * Vm.T - A) == zeros(2))
check("p8:b", "flip v2 -> u2 = (0,1) also valid", simplify(A * (-v2) / sqrt(2)) == Matrix([0, 1]) and
      simplify(Matrix.hstack(u1, -u2) * Sig * Matrix.hstack(v1, -v2).T - A) == zeros(2))
AAt = A * A.T
check("p8:c", "A A^T = diag(8,2), u1->8u1, u2->2u2", AAt == Matrix([[8, 0], [0, 2]]) and AAt * u1 == 8 * u1 and AAt * u2 == 2 * u2)
check("p8:c", "U (Sigma Sigma^T) U^T = diag(8,2)", simplify(Um * Sig * Sig.T * Um.T - AAt) == zeros(2))
check("p8:pitfall", "u2=(0,1) with v2 unchanged -> [[2,2],[1,-1]]",
      simplify(Matrix.hstack(u1, Matrix([0, 1])) * Sig * Vm.T) == Matrix([[2, 2], [1, -1]]))
check("p8:pitfall", "sigma1=8 => |A v1/8| = 1/(2sqrt2)", simplify((A * v1 / 8).norm() - 1 / (2 * sqrt(2))) == 0)
cpA = expand((A - lam * eye(2)).det())
check("p8:pitfall", "det(A-lI) = l^2-3l+4, discriminant -7", cpA == lam**2 - 3 * lam + 4 and 9 - 16 == -7)

# ---------------- p10 ----------------
# symbolic: ||Ax||^2 = sum sigma_i^2 c_i^2 for x = sum c_i v_i, using SVD of the p7 matrix
A = Matrix([[3, 2, 2], [2, 3, -2]])
vv = [Matrix([1, 1, 0]) / sqrt(2), Matrix([1, -1, 4]) / (3 * sqrt(2)), Matrix([2, -2, -1]) / 3]
sg = [5, 3, 0]
cs = symbols("c1:4", real=True)
x = sum((ci * vi for ci, vi in zip(cs, vv)), zeros(3, 1))
check("p10:a", "||Ax||^2 - sum sigma_i^2 c_i^2 = 0 (symbolic, p9 matrix)",
      simplify(expand((A * x).dot(A * x)) - sum(s_**2 * c_**2 for s_, c_ in zip(sg, cs))) == 0)
check("p10:a", "||x||^2 = sum c_i^2", simplify(expand(x.dot(x)) - sum(c_**2 for c_ in cs)) == 0)
check("p10:a", "A^T A v_i = sigma_i^2 v_i", all(simplify(A.T * A * v - s_**2 * v) == zeros(3, 1) for v, s_ in zip(vv, sg)))
xe = vv[0] + vv[1]
check("p10:verify", "c=(1,1,0): ||Ax||^2 = 34, Av1+Av2 = (8,2)/sqrt2, sigma1^2||x||^2 = 50",
      simplify((A * xe).dot(A * xe)) == 34 and simplify(A * xe - Matrix([8, 2]) / sqrt(2)) == zeros(2, 1) and 25 * simplify(xe.dot(xe)) == 50)
check("p10:pitfall", "wrong sum sigma|c| = 8 vs sqrt34 ~ 5.83", 5 + 3 == 8 and round(float(sqrt(34)), 2) == 5.83)
check("p10:c", "||A v1|| = 5 = sigma1", simplify((A * vv[0]).norm()) == 5)
# random numeric sanity (supplement only): ratio <= sigma1 and attained
import numpy as np
rng = np.random.default_rng(0)
Mr = rng.normal(size=(4, 3))
Ur, Sr, Vt = np.linalg.svd(Mr)
ratios = [np.linalg.norm(Mr @ xx) / np.linalg.norm(xx) for xx in rng.normal(size=(2000, 3))]
check("p10:d", "random 4x3: max ratio over 2000 samples <= sigma1, ratio at v1 = sigma1 (numeric supplement)",
      max(ratios) <= Sr[0] + 1e-12 and abs(np.linalg.norm(Mr @ Vt[0]) - Sr[0]) < 1e-12, (max(ratios), Sr[0]))

ok = all(r["pass"] for r in results)
with open(__file__.replace("author_check.py", "author_results.json"), "w") as f:
    json.dump({"all_pass": ok, "n": len(results), "results": results}, f, ensure_ascii=False, indent=1)
for r in results:
    print(("PASS " if r["pass"] else "FAIL ") + r["item"] + " | " + r["claim"])
print(f"{len(results)} checks; ALL PASS" if ok else "SOME FAILED")
