"""Author-side independent checks for review-1116-EM_Algorithm P1-P8.

Exact arithmetic (fractions) for given-table problems, Decimal/float for the
rounded textbook tables, and sympy component-wise differentiation for P6/P8
(row convention: d(scalar)/d(column) is 1xD; matrix derivative keeps X's shape).
Run: python3 -I check_p1_p8.py
"""
from fractions import Fraction as F
import math
import sympy as sp

out = []
def log(*a):
    out.append(' '.join(str(x) for x in a))

def rnd(x, n):
    return round(x + 0.0, n)

# ---------- P1 ----------
N = 7
Nk = [F('2.058'), F('2.008'), F('2.934')]
pi_new = [n / N for n in Nk]
log('P1 (a) pi_new exact =', [str(p) for p in pi_new], 'float =', [float(p) for p in pi_new])
log('P1 (a) rounded 3dp =', [rnd(float(p), 3) for p in pi_new])
log('P1 (b) sum Nk =', sum(Nk), ' sum pi_new =', sum(pi_new))
log('P1 (b) components with pi_new > 1/3:', [k + 1 for k, p in enumerate(pi_new) if p > F(1, 3)])
assert [rnd(float(p), 3) for p in pi_new] == [0.294, 0.287, 0.419]
assert sum(pi_new) == 1

# ---------- P2 / P7 (exact table) ----------
x = [F(-4), F(-2), F(-1), F(0), F(2), F(4), F(6)]
h = F(1, 2)
R = [[1, 0, 0], [1, 0, 0], [h, h, 0], [0, 1, 0], [0, h, h], [0, 0, 1], [0, 0, 1]]
R = [[F(v) for v in row] for row in R]
assert all(sum(row) == 1 for row in R)
Nk2 = [sum(R[n][k] for n in range(7)) for k in range(3)]
mu2 = [sum(R[n][k] * x[n] for n in range(7)) / Nk2[k] for k in range(3)]
log('P2 (a) Nk =', [str(v) for v in Nk2], ' sum =', sum(Nk2))
log('P2 (b) weighted sums =', [str(sum(R[n][k] * x[n] for n in range(7))) for k in range(3)])
log('P2 (b) mu_new =', [str(v) for v in mu2], [float(v) for v in mu2])
assert Nk2 == [F(5, 2), F(2), F(5, 2)]
assert mu2 == [F(-13, 5), F(1, 4), F(22, 5)]

var7 = []
for k in range(3):
    s = sum(R[n][k] * (x[n] - mu2[k]) ** 2 for n in range(7))
    var7.append(s / Nk2[k])
    log(f'P7 (a) k={k+1}: deviations', [str(x[n] - mu2[k]) for n in range(7) if R[n][k]],
        ' weighted SS =', s, ' var_new =', s / Nk2[k], float(s / Nk2[k]))
old7 = [F(2), F(1, 2), F(3)]
assert var7 == [F(36, 25), F(19, 16), F(56, 25)]
log('P7 (b) compare old->new:', [(str(o), str(v), 'down' if v < o else 'up') for o, v in zip(old7, var7)])
# cross-check: variance via E[x^2]-mu^2 with the same weights
for k in range(3):
    ex2 = sum(R[n][k] * x[n] ** 2 for n in range(7)) / Nk2[k]
    assert ex2 - mu2[k] ** 2 == var7[k]
log('P7 cross-check E[x^2]-mu^2 matches for all k')

# ---------- P3 / P4 (rounded textbook table, use exact decimals) ----------
x3 = [F(-3), F('-2.5'), F(-1), F(0), F(2), F(4), F(5)]
R3 = [['1.0', '0.0', '0.0'], ['1.0', '0.0', '0.0'], ['0.057', '0.943', '0.0'],
      ['0.001', '0.999', '0.0'], ['0.0', '0.066', '0.934'], ['0.0', '0.0', '1.0'], ['0.0', '0.0', '1.0']]
R3 = [[F(v) for v in row] for row in R3]
log('P3 row sums =', [str(sum(r)) for r in R3])
Nk3 = [sum(R3[n][k] for n in range(7)) for k in range(3)]
S3 = [sum(R3[n][k] * x3[n] for n in range(7)) for k in range(3)]
mu3 = [S3[k] / Nk3[k] for k in range(3)]
log('P3 (a) Nk =', [float(v) for v in Nk3], ' weighted sums =', [float(v) for v in S3])
log('P3 (a) mu_new =', [float(v) for v in mu3], ' rounded 2dp =', [rnd(float(v), 2) for v in mu3])
assert Nk3 == [F('2.058'), F('2.008'), F('2.934')]
assert [rnd(float(v), 2) for v in mu3] == [-2.70, -0.40, 3.70]
old_mu = [-4, 0, 8]
mv = [abs(rnd(float(v), 2) - o) for v, o in zip(mu3, old_mu)]
mv_unrounded = [abs(float(v) - o) for v, o in zip(mu3, old_mu)]
log('P3 (b) |mu_new-mu| from rounded =', [rnd(v, 2) for v in mv], ' unrounded =', [rnd(v, 4) for v in mv_unrounded])
assert max(range(3), key=lambda k: mv[k]) == 2

mu4 = [F('-2.7'), F('-0.4'), F('3.7')]
var4 = []
for k in range(3):
    s = sum(R3[n][k] * (x3[n] - mu4[k]) ** 2 for n in range(7))
    v = s / Nk3[k]
    var4.append(v)
    log(f'P4 (a) k={k+1}: weighted SS = {float(s)}  var_new = {float(v):.6f} -> {rnd(float(v), 2)}')
assert [rnd(float(v), 2) for v in var4] == [0.15, 0.44, 1.53]
old4 = [1, 0.2, 3]
log('P4 (b) old->new:', [(o, rnd(float(v), 2), 'down' if float(v) < o else 'up') for o, v in zip(old4, var4)])
# Textbook prints 0.14 for component 1: check sensitivity with unrounded mean
v1_unrounded_mu = sum(R3[n][0] * (x3[n] - mu3[0]) ** 2 for n in range(7)) / Nk3[0]
log('P4 note: component-1 variance with unrounded table mean =', float(v1_unrounded_mu),
    '(still 0.15 with this rounded table; textbook 0.14 uses unrounded responsibilities)')
# Recompute the textbook E-step from the initial parameters (unrounded responsibilities)
def npdf(xv, m, v):
    return math.exp(-(xv - m) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v)
xs = [float(v) for v in x3]
Ru = []
for xv in xs:
    wts = [npdf(xv, m, v) / 3 for m, v in zip([-4, 0, 8], [1, 0.2, 3])]
    Ru.append([wv / sum(wts) for wv in wts])
Nku = [sum(r[k] for r in Ru) for k in range(3)]
muu = [sum(r[k] * xv for r, xv in zip(Ru, xs)) / Nku[k] for k in range(3)]
varu = [sum(r[k] * (xv - muu[k]) ** 2 for r, xv in zip(Ru, xs)) / Nku[k] for k in range(3)]
log('P4 textbook check: unrounded r_{41} =', f'{Ru[3][0]:.5f}', '(table 0.001)')
log('P4 textbook check: unrounded var_new =', [f'{v:.4f}' for v in varu], '-> 2dp', [rnd(v, 2) for v in varu])
assert [rnd(v, 2) for v in varu] == [0.14, 0.44, 1.53]
# Only the x=0 cell of column 1 changed (0.001 -> 0.00015), rest of the rounded table kept
R3b = [row[:] for row in R3]
R3b[3][0] = F('0.00015')
N1b = sum(r[0] for r in R3b)
v1b = sum(R3b[n][0] * (x3[n] - mu4[0]) ** 2 for n in range(7)) / N1b
log('P4 single-cell sensitivity: r_{41}=0.001 contributes', float(F('0.001') * (x3[3] - mu4[0]) ** 2),
    '; with 0.00015 ->', float(F('0.00015') * (x3[3] - mu4[0]) ** 2), '; var_1 becomes', f'{float(v1b):.4f}')
assert rnd(float(v1b), 2) == 0.14

# ---------- P5 ----------
w = [F('0.29'), F('0.28'), F('0.43')]
log('P5 (a) sum weights =', sum(w))
assert sum(w) == 1
var5 = [0.06, 0.25, 1.63]
sd5 = [math.sqrt(v) for v in var5]
log('P5 (a) sigma =', [f'{s:.6f}' for s in sd5], ' rounded =', [rnd(s, 2) for s in sd5])
assert [rnd(s, 2) for s in sd5] == [0.24, 0.50, 1.28]
mu5 = [-2.75, -0.50, 3.64]
shift5 = [abs(m - o) for m, o in zip(mu5, [-4, 0, 8])]
log('P5 (b) mean shifts =', [rnd(s, 2) for s in shift5], ' variances old->new:',
    [(o, v, 'up' if v > o else 'down') for o, v in zip([1, 0.2, 3], var5)])
assert max(range(3), key=lambda k: shift5[k]) == 2
assert [k + 1 for k in range(3) if var5[k] > [1, 0.2, 3][k]] == [2]

# ---------- P6 (row convention, symbolic with N=4, D=3) ----------
Nn, Dd = 4, 3
Phi = sp.Matrix(Nn, Dd, lambda i, j: sp.Symbol(f'P{i}{j}'))
th = sp.Matrix(Dd, 1, lambda i, j: sp.Symbol(f't{i}'))
y = sp.Matrix(Nn, 1, lambda i, j: sp.Symbol(f'y{i}'))
e = y - Phi * th
L = (e.T * e)[0, 0]
grad_row = sp.Matrix(1, Dd, lambda i, j: sp.diff(L, th[j]))      # 1 x D row
claim = -2 * e.T * Phi                                           # 1 x N times N x D
log('P6 (a) row gradient shape', grad_row.shape, ' claim shape', claim.shape,
    ' difference zero:', sp.simplify(grad_row - claim) == sp.zeros(1, Dd))
assert sp.simplify(grad_row - claim) == sp.zeros(1, Dd)
es = sp.Matrix(Nn, 1, lambda i, j: sp.Symbol(f'e{i}'))
dLde = sp.Matrix(1, Nn, lambda i, j: sp.diff((es.T * es)[0, 0], es[j]))
assert dLde == 2 * es.T
J = sp.Matrix(Nn, Dd, lambda i, j: sp.diff(e[i], th[j]))           # output x input
assert J == -Phi
log('P6 (b) dL/de shape', dLde.shape, '(1xN); de/dtheta shape', J.shape, '(NxD) equals -Phi; product 1xD')
# zero-gradient -> transpose -> normal equation (consistency only)
log('P6 note: setting row gradient to 0^T and transposing gives Phi^T Phi theta = Phi^T y:',
    sp.simplify((claim.T / -2) - (Phi.T * y - Phi.T * Phi * th)) == sp.zeros(Dd, 1))

# ---------- P8 ----------
Dd = 3
t = sp.Matrix(Dd, 1, lambda i, j: sp.Symbol(f't{i}', positive=True))
u = (t.T * t)[0, 0]
f = sp.sin(sp.log(u))
df_row = sp.Matrix(1, Dd, lambda i, j: sp.diff(f, t[j]))
claim_f = (2 * sp.cos(sp.log(u)) / u) * t.T
log('P8 (a) df/dt shape', df_row.shape, ' matches 2cos(log u)/u t^T:',
    sp.simplify(df_row - claim_f) == sp.zeros(1, Dd))
assert sp.simplify(df_row - claim_f) == sp.zeros(1, Dd)
D_, E_, F_ = 2, 3, 4
A = sp.Matrix(D_, E_, lambda i, j: sp.Symbol(f'a{i}{j}'))
X = sp.Matrix(E_, F_, lambda i, j: sp.Symbol(f'x{i}{j}'))
B = sp.Matrix(F_, D_, lambda i, j: sp.Symbol(f'b{i}{j}'))
g = (A * X * B).trace()
dg = sp.Matrix(E_, F_, lambda p, q: sp.diff(g, X[p, q]))          # same (p,q) place as X
log('P8 (b) dg/dX shape', dg.shape, ' equals A^T B^T:', sp.simplify(dg - A.T * B.T) == sp.zeros(E_, F_),
    ' (A^T B^T shape', (A.T * B.T).shape, ')')
assert dg == A.T * B.T
assert (B * A).T == A.T * B.T
log('P8 (b) note: A^T B^T = (BA)^T, BA is F x E, so result is E x F like X')
log('P8 (c) dims: df/dt in R^{1xD}; dg/dX in R^{ExF} (checked with D,E,F = 2,3,4)')

log('ALL ASSERTIONS PASSED')
print('\n'.join(out))
