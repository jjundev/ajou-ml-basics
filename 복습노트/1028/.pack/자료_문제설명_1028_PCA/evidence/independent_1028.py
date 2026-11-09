"""저작자 독립 검산(1028 재선정 5문항). 설명 조각의 모든 수치·식 주장을 정확 계산으로 확인. python3 independent_1028.py"""
import json
import sympy as sp
R = {}
def chk(key, cond, note):
    assert cond, key
    R[key] = note
# p1
e1, e2 = sp.Matrix([1, 0]), sp.Matrix([0, 1]); x = sp.Matrix([4, -7]); z, t = sp.symbols('z t')
chk('p1:a', 4*e1 - 7*e2 == x, 'x=4e1-7e2')
xt = sp.Matrix([0, z])
chk('p1:b', 0*e1 + z*e2 == xt and (e2.T*e2)[0] == 1 and (e2.T*xt)[0] == z and e2*z == xt, 'xt=0e1+ze2, e2^Te2=1, code=e2^T xt=z, e2 z=xt')
chk('p1:c', all((t*e2)[0] == 0 for _ in [0]) and sp.Matrix([1, 0])[0] != 0, 'span[e2] elements [0,t]; e1 not in U')
chk('p1:d', sp.Matrix.hstack(e2).rank() == 1, 'rank{e2}=1 -> dim U=1')
# p2
b1 = sp.Rational(1, 5)*sp.Matrix([3, 4]); b2 = sp.Rational(1, 5)*sp.Matrix([4, -3]); B = sp.Matrix.hstack(b1, b2)
chk('p2:a', B.T*B == sp.eye(2) and (b1.T*b1)[0] == 1 and (b2.T*b2)[0] == 1 and (b1.T*b2)[0] == 0, 'B^TB=I; 1/25 factors')
xx = b1 + 2*b2
chk('p2:b', xx == sp.Rational(1, 5)*sp.Matrix([11, -2]) and B.T*xx == sp.Matrix([1, 2]) and B.rank() == 2, 'ONB; check point x=b1+2b2=(1/5)[11,-2], B^Tx=[1,2]')
chk('p2:pitfall', (sp.Rational(1, 5)*(9 + 16)) == 5, 'single 1/5 gives 5')
# p3
c1, c2 = sp.Matrix([1, -1]), sp.Matrix([1, 1]); x3 = sp.Matrix([5, 1]); B3 = sp.Matrix.hstack(c1, c2)
lam = B3.solve(x3)
chk('p3:a', lam == sp.Matrix([2, 3]) and 2*c1 + 3*c2 == x3 and B3.T*B3 == 2*sp.eye(2) and (B3.T*B3).inv()*B3.T*x3 == lam, 'coords [2,3]; (B^TB)^-1 B^T x=[2,3]')
q1, q2 = c1/sp.sqrt(2), c2/sp.sqrt(2)
chk('p3:b', sp.sqrt((c1.T*c1)[0]) == sp.sqrt(2) and sp.sqrt((c2.T*c2)[0]) == sp.sqrt(2) and (c1.T*c2)[0] == 0 and B3.T*x3 == sp.Matrix([4, 6])
    and sp.simplify((q1.T*x3)[0] - 2*sp.sqrt(2)) == 0 and sp.simplify((q2.T*x3)[0] - 3*sp.sqrt(2)) == 0
    and sp.simplify(2*sp.sqrt(2)*q1 + 3*sp.sqrt(2)*q2 - x3) == sp.zeros(2, 1), 'norms sqrt2, orthogonal, B^Tx=[4,6]=2*coords; q-coords 2sqrt2,3sqrt2')
chk('p3:pitfall', 4*c1 + 6*c2 == sp.Matrix([10, 2]), '4b1+6b2=[10,2]')
# p4
x1, x2 = sp.symbols('x1 x2', real=True); X = sp.Matrix([x1, x2])
A1 = sp.Matrix([[4, 2], [2, 3]]); A2 = sp.Matrix([[4, 2], [2, 0]])
q1f = sp.expand((X.T*A1*X)[0]); q2f = sp.expand((X.T*A2*X)[0])
chk('p4:a', q1f == sp.expand(4*x1**2 + 4*x1*x2 + 3*x2**2) and sp.expand((2*x1 + x2)**2 + 2*x2**2 - q1f) == 0 and A1 == A1.T
    and (X.T*A1*X).subs({x1: 1, x2: -2})[0] == 8 and A1*sp.Matrix([1, -2]) == sp.Matrix([0, -4]),
    'x^TA1x=(2x1+x2)^2+2x2^2; sum of squares zero iff x2=0 and 2x1+x2=0 -> x=0 (proof); A1[1,-2]=[0,-4], value 8')
v = sp.Matrix([1, -2])
chk('p4:b', q2f == sp.expand(4*x1**2 + 4*x1*x2) and sp.expand((2*x1 + x2)**2 - x2**2 - q2f) == 0 and A2*v == sp.Matrix([0, 2]) and (v.T*A2*v)[0] == -4
    and (sp.Matrix([1, 0]).T*A2*sp.Matrix([1, 0]))[0] == 4 and (sp.Matrix([1, 1]).T*A2*sp.Matrix([1, 1]))[0] == 8 and (sp.Matrix([0, 1]).T*A2*sp.Matrix([0, 1]))[0] == 0,
    'x^TA2x=(2x1+x2)^2-x2^2; x=[1,-2] -> -4; samples [1,0]->4, [1,1]->8, [0,1]->0')
chk('p4:pitfall', sp.expand(4*x1**2 + 2*x1*x2 + 3*x2**2) != q1f, 'single cross term is wrong')
# p5
u = [sp.Matrix(c) for c in ([0, -1, 2, 0, 2], [1, -3, 1, -1, 2], [-3, 4, 1, 2, 1], [-1, -3, 5, 0, 7])]
x5 = sp.Matrix([-1, -9, -1, 4, 1]); B5 = sp.Matrix.hstack(*u[:3]); B4 = sp.Matrix.hstack(*u)
abc = B5.solve_least_squares(u[3])
chk('p5:basis', abc == sp.Matrix([1, 2, 1]) and B5*abc == u[3] and B5.rank() == 3 and B4.rank() == 3 and B4*sp.Matrix([1, 2, 1, -1]) == sp.zeros(5, 1), 'u4=u1+2u2+u3; rank 3; B4 v=0 for v=[1,2,1,-1]')
G = B5.T*B5; h = B5.T*x5
lam5 = G.solve(h); proj = B5*lam5; r = x5 - proj
chk('p5:a', G == sp.Matrix([[9, 9, 0], [9, 16, -14], [0, -14, 31]]) and h == sp.Matrix([9, 23, -25]) and lam5 == sp.Matrix([-3, 4, 1]) and proj == sp.Matrix([1, -5, -1, -2, 3])
    and proj == B4*(B4.T*B4).pinv()*B4.T*x5, 'normal eq lambda=(-3,4,1), proj=[1,-5,-1,-2,3]; same as pseudo-inverse projector on all 4')
chk('p5:b', r == sp.Matrix([-2, -4, 0, 6, -2]) and (r.T*r)[0] == 60 and sp.sqrt(60) == 2*sp.sqrt(15) and (x5.T*x5)[0] == 100 and (proj.T*proj)[0] == 40, 'r, |r|^2=60, d=2sqrt15; 100=40+60')
chk('p5:c', all((r.T*ui)[0] == 0 for ui in u) and (r.T*proj)[0] == 0, 'r . u_i = 0 for all four; r . proj = 0')
print(json.dumps(R, ensure_ascii=False, indent=1))
