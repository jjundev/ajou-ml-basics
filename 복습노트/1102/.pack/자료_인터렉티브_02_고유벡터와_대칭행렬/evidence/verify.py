"""Independent checks of dump.json (compute() outputs) by other routes: numpy linear algebra,
closed forms and exact Fractions. Usage: python3 verify.py <run dir> → writes <n>/evidence/independent-math.json"""
import json, math, sys, os
from fractions import Fraction as F
import numpy as np

run = sys.argv[1]
d = json.load(open(os.path.join(run, 'dump.json')))
TOL = 1e-9
report = {}

def close(a, b, tol=TOL):
    return abs(a - b) <= tol * max(1.0, abs(b))

# ---------- topic 1: projection variance ----------
t1 = {'checks': 0, 'fail': []}
W = np.array(d['t1']['sample'])
N = len(W)
cov_w = W.T @ W / N
assert N == 40
assert np.allclose(W.mean(0), 0, atol=1e-12), 'sample mean'
assert np.allclose(cov_w, np.eye(2), atol=1e-12), 'sample cov'
for g in d['t1']['grid']:
    X = np.array(g['pts']).T            # D x N, lecture convention
    S = X @ X.T / N                       # S = (1/N) X Xᵀ
    a, th = math.radians(g['alpha']), math.radians(g['theta'])
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    S_closed = R @ np.diag([g['sa'] ** 2, g['sb'] ** 2]) @ R.T
    b = np.array([math.cos(th), math.sin(th)])
    z = b @ X
    V1_direct = float(np.mean(z ** 2))
    V_closed = g['sa'] ** 2 * math.cos(th - a) ** 2 + g['sb'] ** 2 * math.sin(th - a) ** 2
    lam = np.linalg.eigh(S)[0][::-1]
    checks = [
        ('S numpy', np.allclose(S, np.array(g['S']), atol=1e-12)),
        ('S closed form', np.allclose(S, S_closed, atol=1e-12)),
        ('V1 direct', close(g['V1'], V1_direct)),
        ('V1 = bᵀSb', close(g['quad'], float(b @ S @ b))),
        ('V1 closed', close(g['V1'], V_closed)),
        ('V1 + Vp = tr S', close(g['V1'] + g['Vp'], float(np.trace(S)))),
        ('total = mean |x|²', close(g['total'], float(np.mean(np.sum(X ** 2, 0))))),
        ('lambda1', close(g['l1'], float(lam[0]))),
        ('lambda2', close(g['l2'], float(lam[1]))),
        ('weighted avg = V1', close(g['weighted'], g['V1'])),
        ('V1 <= lambda1', g['V1'] <= lam[0] + 1e-9),
        ('mean zero', abs(g['mean'][0]) < 1e-12 and abs(g['mean'][1]) < 1e-12),
    ]
    if not g['tied']:
        vals, vecs = np.linalg.eigh(S)
        p1 = vecs[:, 1]
        deg = math.degrees(math.atan2(p1[1], p1[0])) % 180
        dd = abs(deg - g['p1deg']) % 180
        checks.append(('p1 direction', min(dd, 180 - dd) < 1e-7))
    else:
        checks.append(('tied only when sa = sb', g['sa'] == g['sb']))
    for name, ok in checks:
        t1['checks'] += 1
        if not ok: t1['fail'].append({'case': {k: g[k] for k in ('alpha', 'sa', 'sb', 'theta')}, 'check': name})
# presets written in the step texts
def V(alpha, sa, sb, theta):
    a, th = math.radians(alpha), math.radians(theta)
    return sa ** 2 * math.cos(th - a) ** 2 + sb ** 2 * math.sin(th - a) ** 2
t1['step_values'] = {'x-axis V1': V(0, 2, .8, 0), 'y-axis V1': V(0, 2, .8, 90), 'total': 4 + .64,
                     'tilted x-axis V1': V(30, 2, .8, 0), 'keep x': 4 / 4.64, 'keep y': .64 / 4.64, 'keep tilted': V(30, 2, .8, 0) / 4.64}
assert close(t1['step_values']['tilted x-axis V1'], 3.16)
report['t1'] = t1

# ---------- topic 2: eigenvectors and EVD ----------
t2 = {'checks': 0, 'fail': []}
for g in d['t2']:
    A = np.array(g['A'], dtype=float)
    tr, det = np.trace(A), np.linalg.det(A)
    roots = np.roots([1, -tr, det])          # characteristic polynomial, other route than the closed form
    real = bool(np.all(np.abs(roots.imag) < 1e-9))
    checks = [('kind complex iff non-real roots', (g['kind'] == 'complex') == (not real)),
              ('symmetric flag', g['sym'] == bool(abs(A[0, 1] - A[1, 0]) < 1e-9))]
    if real:
        r = sorted(roots.real, reverse=True)
        checks.append(('eigenvalues', all(close(x, y, 1e-7) for x, y in zip(g['lams'], r))))
        for lam, v in zip(g['lams'], g['vecs']):
            v = np.array(v)
            if g['kind'] != 'scalar':
                checks.append(('Av = λv', np.allclose(A @ v, lam * v, atol=1e-9)))
            checks.append(('unit', close(float(np.linalg.norm(v)), 1.0)))
    x = np.array([math.cos(math.radians(g['theta'])), math.sin(math.radians(g['theta']))])
    Ax = A @ x
    checks.append(('Ax', np.allclose(Ax, g['Ax'], atol=1e-12)))
    cross = x[0] * Ax[1] - x[1] * Ax[0]
    checks.append(('parallel flag', g['parallel'] == bool(np.linalg.norm(Ax) < 1e-9 or abs(cross) < 1e-9 * max(1, np.linalg.norm(Ax)))))
    if g['kind'] == 'two':
        p1, p2 = np.array(g['vecs'][0]), np.array(g['vecs'][1])
        gap = math.degrees(math.acos(min(1, abs(p1 @ p2))))
        checks.append(('gap', close(g['gap'], gap, 1e-7)))
        if g['sym']:
            checks.append(('symmetric → orthogonal eigenvectors', abs(p1 @ p2) < 1e-9))
    if g['evd']:
        P, D, Pinv = (np.array(g['evd'][k]) for k in ('P', 'D', 'Pinv'))
        checks += [('P⁻¹ numpy', np.allclose(Pinv, np.linalg.inv(P), atol=1e-9)),
                   ('AP = PD', np.allclose(A @ P, P @ D, atol=1e-9)),
                   ('PDP⁻¹ = A', np.allclose(P @ D @ Pinv, A, atol=1e-9)),
                   ('det P > 0', np.linalg.det(P) > 0),
                   ('orth flag ⇔ P⁻¹ = Pᵀ', g['evd']['orth'] == bool(np.allclose(Pinv, P.T, atol=1e-9))),
                   ('det A = λ1λ2', close(float(np.linalg.det(A)), g['lams'][0] * g['lams'][1], 1e-7))]
        st = [np.array(m) for m in g['stages']]
        checks += [('f=0 is I', np.allclose(st[0], np.eye(2))), ('f=1 is P⁻¹', np.allclose(st[1], Pinv, atol=1e-9)),
                   ('f=2 is DP⁻¹', np.allclose(st[2], D @ Pinv, atol=1e-9)), ('f=3 is A', np.allclose(st[3], A, atol=1e-9)),
                   ('P⁻¹p_i = e_i', np.allclose(Pinv @ P, np.eye(2), atol=1e-9))]
    for name, ok in checks:
        t2['checks'] += 1
        if not ok: t2['fail'].append({'A': g['A'], 'theta': g['theta'], 'check': name})
# step text: x = e1 on [[2,1],[1,2]] turns by atan(1/2)
t2['step_values'] = {'turn e1 deg': math.degrees(math.atan2(1, 2)), 'MML 4.11 eig': sorted(np.linalg.eigvalsh(np.array([[2.5, -1], [-1, 2.5]])).tolist()),
                     'nonsym gap deg': math.degrees(math.acos(abs(np.array([1, 0]) @ (np.array([-1, 1]) / math.sqrt(2)))))}
report['t2'] = t2

# ---------- topic 3: repeated eigenvalue, Gram–Schmidt ----------
t3 = {'checks': 0, 'fail': []}
A3 = [[F(3), F(2), F(2)], [F(2), F(3), F(2)], [F(2), F(2), F(3)]]
mv = lambda M, v: [sum(M[i][j] * v[j] for j in range(3)) for i in range(3)]
dot = lambda u, v: sum(a * b for a, b in zip(u, v))
x1, x2, x3 = [F(-1), F(1), F(0)], [F(-1), F(0), F(1)], [F(1), F(1), F(1)]
gs = [a - dot(x1, x2) / dot(x1, x1) * b for a, b in zip(x2, x1)]
exact = {'A x1 = x1': mv(A3, x1) == x1, 'A x2 = x2': mv(A3, x2) == x2, 'A x3 = 7 x3': mv(A3, x3) == [7 * c for c in x3],
         'gram-schmidt x2\'': gs == [F(-1, 2), F(-1, 2), F(1)], 'x1ᵀx2 / |x1||x2| = 1/2': dot(x1, x2) ** 2 / (dot(x1, x1) * dot(x2, x2)) == F(1, 4),
         'char poly roots 1,1,7': all(abs(np.linalg.det(np.array(A3, dtype=float) - l * np.eye(3))) < 1e-9 for l in (1, 7))}
t3['exact'] = {k: bool(v) for k, v in exact.items()}
A = np.array(A3, dtype=float)
for g in d['t3']:
    v1, v2 = np.array(g['v1']), np.array(g['v2'])
    P = np.array(g['P'])
    Dm = np.diag([1, 1, 7])
    c = float(v1 @ v2)
    checks = [('v1 eigen', np.allclose(A @ v1, v1)), ('v2 eigen', np.allclose(A @ v2, v2)),
              ('in plane', abs(v1.sum()) < 1e-12 and abs(v2.sum()) < 1e-12), ('c', close(g['c'], c)),
              ('c = cos(β−α)', close(c, math.cos(math.radians(g['beta'] - g['alpha'])), 1e-9)),
              ('errT numpy', close(g['errT'], float(np.linalg.norm(P @ Dm @ P.T - A)), 1e-9))]
    if not g['gs'] or not g['indep']:
        # closed form for unit v1, v2 in the eigenplane: ‖v1v1ᵀ + v2v2ᵀ − Π‖_F = √2|cos(β−α)|
        checks.append(('errT closed √2|c|', close(g['errT'], math.sqrt(2) * abs(c), 1e-9)))
    if g['indep']:
        checks.append(('PDP⁻¹ = A', g['errInv'] is not None and g['errInv'] < 1e-9))
        u2 = np.array(g['u2'])
        checks += [('u2 ⟂ v1', abs(u2 @ v1) < 1e-12), ('u2 eigen', np.allclose(A @ u2, u2)), ('u2 unit', close(float(np.linalg.norm(u2)), 1))]
        if g['gs']:
            checks.append(('gs → PᵀP = I', np.allclose(P.T @ P, np.eye(3), atol=1e-9)))
            checks.append(('gs → errT 0', g['errT'] < 1e-9))
    else:
        checks.append(('dependent → no P⁻¹', g['errInv'] is None and abs(np.linalg.det(P)) < 1e-9))
    checks.append(('p3 ⟂ columns', abs(g['p3v1']) < 1e-12 and abs(g['p3v2']) < 1e-12))
    for name, ok in checks:
        t3['checks'] += 1
        if not ok: t3['fail'].append({'alpha': g['alpha'], 'beta': g['beta'], 'gs': g['gs'], 'check': name})
case = next(g for g in d['t3'] if g['alpha'] == 0 and g['beta'] == 60 and g['gs'])
u2 = np.array(case['u2'])
t3['note_u2_matches'] = bool(np.allclose(u2, np.array([-1, -1, 2]) / math.sqrt(6)))
t3['step_values'] = {'errT 60°': math.sqrt(2) * 0.5, 'errT 20°': math.sqrt(2) * math.cos(math.radians(20)), 'errT 0°': math.sqrt(2)}
report['t3'] = t3

ok = all(not report[k]['fail'] for k in report) and all(t3['exact'].values()) and t3['note_u2_matches']
for n, k in (('1', 't1'), ('2', 't2'), ('3', 't3')):
    with open(os.path.join(run, n, 'evidence', 'independent-math.json'), 'w') as fh:
        json.dump({'ok': not report[k]['fail'], **report[k]}, fh, ensure_ascii=False, indent=2, default=str)
print('PASS' if ok else 'FAIL', {k: (report[k]['checks'], len(report[k]['fail'])) for k in report}, t3['exact'], t3['note_u2_matches'])
for k in report:
    for f in report[k]['fail'][:5]: print(k, f)
