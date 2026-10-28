"""1028 PCA 복습문제 독립 검산 (문제 데이터만 입력, 참고 풀이 코드 미사용).
방법: p1 성분 비교(exact), p2 Fraction 점곱/길이 + 행렬식(exact),
p3 sympy rank/RREF로 기저 선택 -> 정규방정식, 그리고 별도로 Gram-Schmidt 정규직교 기저로 사영(경로 2),
p4 A-내적 정규방정식 + 일반 점 lambda1 e1+lambda3 e3 에 대한 A-거리 제곱 최소화(완전제곱, 미분 미사용) 경로 2."""
import json
from fractions import Fraction as F
import sympy as sp

out = {}
# ---- p1
x = sp.Matrix([4, -7]); e1 = sp.Matrix([1, 0]); e2 = sp.Matrix([0, 1])
c = sp.Matrix.hstack(e1, e2).solve(x)
z = sp.symbols('z', real=True)
xt = sp.Matrix([0, z])
ct = sp.Matrix.hstack(e1, e2).solve(xt)
# U = {[0,z]}: closed under +, scalar; spanned by e2; basis size
u_basis = sp.Matrix([[0], [1]])
out['p1'] = {
    'coeffs_x': [int(v) for v in c], 'reconstruct_ok': bool(c[0]*e1 + c[1]*e2 == x),
    'coeffs_xtilde': [str(v) for v in ct], 'code': str((e2.T*xt)[0]),
    'U_basis_rank': int(u_basis.rank()), 'dimU': 1,
}
# ---- p2
b1 = (F(3, 5), F(4, 5)); b2 = (F(4, 5), F(-3, 5))
dot = lambda u, v: sum(a*b for a, b in zip(u, v))
Bm = sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5)], [sp.Rational(4, 5), sp.Rational(-3, 5)]])  # columns b1,b2
out['p2'] = {'b1.b2': str(dot(b1, b2)), '|b1|^2': str(dot(b1, b1)), '|b2|^2': str(dot(b2, b2)),
             'det[b1 b2]': str(Bm.det()), 'BtB': [[str(v) for v in r] for r in (Bm.T*Bm).tolist()]}
# ---- p3
U = sp.Matrix([[0, -1, 2, 0, 2], [1, -3, 1, -1, 2], [-3, 4, 1, 2, 1], [-1, -3, 5, 0, 7]]).T
xv = sp.Matrix([-1, -9, -1, 4, 1])
rref, piv = U.rref()
B = U[:, list(piv)]
G = B.T*B; rhs = B.T*xv
lam = G.LUsolve(rhs)
proj = B*lam; r = xv - proj
# path 2: Gram-Schmidt orthonormal basis Q, projection Q Q^T x
Q = sp.Matrix.hstack(*sp.GramSchmidt([B[:, i] for i in range(B.shape[1])], orthonormal=True))
proj2 = sp.simplify(Q*Q.T*xv)
# path 3: combination expressing u4
coef4 = B.solve_least_squares(U[:, 3])
out['p3'] = {'rank': int(U.rank()), 'pivots': list(piv), 'u4_in_terms_of_u1u2u3': [str(v) for v in coef4],
             'BtB': G.tolist(), 'det_BtB': int(G.det()), 'Btx': list(map(int, rhs)),
             'lambda': [str(v) for v in lam], 'proj': [str(v) for v in proj],
             'proj_gram_schmidt': [str(v) for v in proj2], 'paths_agree': bool(proj2 == proj),
             'residual': [str(v) for v in r], 'Bt_r': [str(v) for v in B.T*r],
             'd2': str((r.T*r)[0]), 'd': str(sp.sqrt((r.T*r)[0])),
             # check minimality: distance from x to arbitrary point of U is >= d (Pythagoras: residual _|_ U)
             'u4_t_r': str((U[:, 3].T*r)[0])}
# ---- p4
A = sp.Matrix([[2, 1, 0], [1, 2, -1], [0, -1, 2]])
out['p4_A_pos_def'] = {'leading_minors': [int(A[:k, :k].det()) for k in (1, 2, 3)], 'symmetric': bool(A == A.T)}
E = sp.eye(3); E1, E2, E3 = E[:, 0], E[:, 1], E[:, 2]
Bu = sp.Matrix.hstack(E1, E3)
Gram = Bu.T*A*Bu; rhs4 = Bu.T*A*E2
l4 = Gram.LUsolve(rhs4)
p4 = Bu*l4; r4 = E2 - p4
# path 2: squared A-distance f(l1,l3) = (e2 - l1 e1 - l3 e3)^T A (...) ; complete the square (no derivative)
l1, l3 = sp.symbols('l1 l3', real=True)
v = E2 - l1*E1 - l3*E3
f = sp.expand((v.T*A*v)[0])
f_cs = sp.expand(2*(l1 - sp.Rational(1, 2))**2 + 2*(l3 + sp.Rational(1, 2))**2 + 1)
# path 3: wrong (dot-product) projection for contrast
p_dot = sp.Matrix([0, 0, 0])
out['p4'] = {'Gram_BtAB': Gram.tolist(), 'rhs_BtAe2': list(map(int, rhs4)), 'lambda': [str(v) for v in l4],
             'proj': [str(v) for v in p4], 'residual': [str(v) for v in r4], 'A_r': [str(v) for v in A*r4],
             '<r,e1>_A': str((r4.T*A*E1)[0]), '<r,e3>_A': str((r4.T*A*E3)[0]),
             'd2_A': str((r4.T*A*r4)[0]), 'd_A': str(sp.sqrt((r4.T*A*r4)[0])),
             'sqdist_poly': str(f), 'complete_square_matches': bool(sp.simplify(f - f_cs) == 0),
             'contrast_dot_product_projection': [int(v) for v in p_dot], 'contrast_dot_distance': 1,
             'contrast_euclid_norm_of_A_residual': str(sp.sqrt((r4.T*r4)[0]))}
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
