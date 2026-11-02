"""Independent checks of the 1028 interactive computations.

The pages use closed-form 2x2 eigenvectors and normal equations. Here the same answers come from
SVD, least squares and exact fractions, then get compared with the numbers the pages produce.
"""
from fractions import Fraction as F
import json, math, pathlib, sys
import numpy as np

run = pathlib.Path(__file__).parent
dump = json.loads((run / 'dump.json').read_text(encoding='utf-8'))
results = {'1': [], '2': [], '3': []}
TOL = 1e-9


def close(a, b, tol=TOL):
    return np.allclose(np.asarray(a, float), np.asarray(b, float), atol=tol, rtol=0)


def first_direction(P):
    """First right singular direction of the N x 2 matrix, sign fixed so x >= 0."""
    _, s, vt = np.linalg.svd(P, full_matrices=False)
    b = vt[0]
    if b[0] < 0:
        b = -b
    return b, s * s / len(P)


# Topic 1: sample moments, directions via SVD, reconstruction via an explicit projector
for row in dump['t1']:
    X = np.array(row['raw'])
    N, mu, sigma = len(X), X.mean(0), X.std(0)
    assert N == 40 and close(mu, [3, 2]) and close(sigma, [row['sigma1'], 1])
    Xc = X - mu
    Z = Xc / sigma
    assert close((Z[:, 0] * Z[:, 1]).mean(), row['rho'])
    b_raw, lam_raw = first_direction(Xc)
    b_std, lam_std = first_direction(Z)
    assert close(math.degrees(math.atan2(b_raw[1], b_raw[0])), row['rawDeg'], 1e-8)
    assert close(math.degrees(math.atan2(b_std[1], b_std[0])), row['stdDeg'], 1e-8)
    assert close(lam_raw[0] / lam_raw.sum(), row['keepRaw']) and close(lam_std[0] / lam_std.sum(), row['keepStd'])
    assert close(abs(b_std), [math.sqrt(.5)] * 2)
    assert close(lam_std, [1 + row['rho'], 1 - row['rho']])
    P = np.outer(b_std, b_std)
    assert close(Z @ P, row['projected'])
    restored = mu + (Z @ P) * sigma
    assert close(restored, row['restored'])
    r_std = Z - Z @ P
    assert close(r_std @ b_std, np.zeros(40))
    results['1'].append(dict(sigma1=row['sigma1'], rho=row['rho'], rawDeg=round(row['rawDeg'], 4), stdDeg=round(row['stdDeg'], 4), keepRaw=round(row['keepRaw'], 5), keepStd=round(row['keepStd'], 5)))

by = {(r['sigma1'], r['rho']): r for r in dump['t1']}
stated = [((1, .6), 45.0, 80.0, 45.0), ((2, .6), 19.3, 88.4, 45.0), ((4, .6), 8.9, 96.3, 45.0), ((4, .9), None, None, 45.0)]
for key, raw_deg, raw_keep, std_deg in stated:
    r = by[key]
    if raw_deg is not None:
        assert round(r['rawDeg'], 1) == raw_deg and round(r['keepRaw'] * 100, 1) == raw_keep
    assert round(r['stdDeg'], 1) == std_deg
assert round(by[(4, .6)]['keepStd'] * 100, 1) == 80.0 and round(by[(4, .9)]['keepStd'] * 100, 1) == 95.0
r = by[(2, .6)]
X = np.array(r['raw'])
line = (np.array(r['b']) * [2, 1]); line /= np.linalg.norm(line)
assert np.abs((X - np.array(r['restored'])) @ line).max() > 1, 'S5 residual should not be perpendicular in raw axes'

# Topic 2: exact fractions for the discrete datasets, numpy moments for the N=40 grid
for name, want_sum in (('note', (2, 2, 8)), ('sample', None)):
    d = dump['t2']['datasets'][name]
    data = [(F(str(a)), F(str(b))) for a, b in d['data']]
    N = len(data)
    assert sum(p[0] for p in data) == 0 and sum(p[1] for p in data) == 0
    s = (sum(p[0] * p[0] for p in data), sum(p[0] * p[1] for p in data), sum(p[1] * p[1] for p in data))
    if want_sum:
        assert s == tuple(F(x) for x in want_sum)
    X = np.array([[float(a), float(b)] for a, b in data]).T
    xxt = X @ X.T
    assert close([xxt[0, 0], xxt[0, 1], xxt[1, 1]], [float(x) for x in s])
    assert close([d['sum']['a'], d['sum']['b'], d['sum']['d']], [float(x) for x in s])
    assert close([d['avg']['a'], d['avg']['b'], d['avg']['d']], [float(x / N) for x in s])
    results['2'].append(dict(dataset=name, N=N, sum=[str(x) for x in s], S=[str(x / N) for x in s]))
assert F(2, 3) == F(2) / 3

for row in dump['t2']['grid']:
    Y = np.array(row['shape'])
    M = np.array(row['moved'])
    C = np.cov(Y.T, bias=True)
    want = [[row['sigma1'] ** 2, row['rho'] * row['sigma1'] * row['sigma2']], [row['rho'] * row['sigma1'] * row['sigma2'], row['sigma2'] ** 2]]
    assert close(C, want) and close(Y.mean(0), [0, 0])
    assert close([row['S']['a'], row['S']['b'], row['S']['d']], [C[0, 0], C[0, 1], C[1, 1]])
    mean = np.zeros(2) if row['centered'] else np.array([row['mu1'], row['mu2']], float)
    raw = M.T @ M / len(M)
    assert close([row['raw']['a'], row['raw']['b'], row['raw']['d']], [raw[0, 0], raw[0, 1], raw[1, 1]])
    assert close(raw, C + np.outer(mean, mean))
    results['2'].append(dict(sigma1=row['sigma1'], sigma2=row['sigma2'], rho=row['rho'], mean=mean.tolist(), S=C.round(6).tolist(), secondMoment=raw.round(6).tolist()))
g = dump['t2']['grid'][0]
assert close([g['raw']['a'], g['raw']['b'], g['raw']['d']], [29, 16.2, 10])

# Topic 3: exact fractions for the rational cases, lstsq for the sweep
b, x = (F(2), F(0)), (F(1), F(0))
assert sum(p * q for p, q in zip(b, x)) == 2 and F(2) / sum(p * p for p in b) == F(1, 2)
u, v, X3 = (F(3, 5), F(4, 5), F(0)), (F(4, 5), F(-3, 5), F(0)), (F(2), F(1), F(2))
dot = lambda p, q: sum(a * c for a, c in zip(p, q))
assert dot(u, u) == dot(v, v) == 1 and dot(u, v) == 0 and (dot(u, X3), dot(v, X3)) == (2, 1)
assert dot(X3, X3) - 2 * 2 - 1 * 1 == 4, 'distance to the plane is 2'
for row in dump['t3']:
    one, two = row['one'], row['two']
    bv, xv = np.array(one['b']), np.array(one['x'])
    lam = np.linalg.lstsq(bv.reshape(2, 1), xv, rcond=None)[0][0]
    assert close(lam, one['lam']) and close(bv @ xv, one['z'])
    assert close(np.linalg.norm(xv - lam * bv), one['errLam']) and close(np.linalg.norm(xv - (bv @ xv) * bv), one['errZ'])
    assert close(bv @ (xv - lam * bv), 0) and close(one['dotLam'], 0)
    B = np.column_stack([two['b1'], two['b2']])
    X = np.array(two['X'])
    sol = np.linalg.lstsq(B, X, rcond=None)[0]
    assert close(sol, two['lam']) and close(B.T @ X, two['z'])
    assert close(B @ sol, two['proj']) and close(B @ B.T @ X, two['code'])
    assert close(B.T @ (X - B @ sol), [0, 0])
    assert close(np.linalg.norm(X - B @ sol), 2), 'plane z=0 is unchanged, so the distance stays 2'
    orthonormal = close(B.T @ B, np.eye(2))
    assert orthonormal == close(two['z'], two['lam'], 1e-9)
    results['3'].append(dict(phi=row['phi'], l1=row['l1'], l2=row['l2'], z=np.round(two['z'], 4).tolist(), lam=np.round(two['lam'], 4).tolist(), errLam=round(two['errLam'], 4), errZ=round(two['errZ'], 4), orthonormal=bool(orthonormal)))
r = dump['t3']
assert round(r[1]['two']['errZ'], 2) == 2.29 and np.round(r[1]['two']['z'], 2).tolist() == [2.0, 1.87] and np.round(r[1]['two']['lam'], 2).tolist() == [1.42, 1.15]
assert np.round(r[0]['two']['z'], 2).tolist() == [2.0, 1.0]
assert round(r[2]['two']['z'][0], 2) == 3.0 and round(r[2]['two']['lam'][0], 2) == 1.33
assert round(r[3]['one']['z'], 2) == 4.73 and round(r[2]['one']['z'], 2) == 2.37 and round(r[3]['one']['lam'] * 4, 6) == round(r[3]['one']['z'], 6)

for n, rows in results.items():
    out = run / n / 'evidence'
    out.mkdir(exist_ok=True)
    (out / 'independent-math.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
print('PASS', {k: len(v) for k, v in results.items()})
