# Independent check with mpmath (50 digits), separate from the JS compute path.
import json, sys
from mpmath import mp, mpf, exp, log, sqrt, pi, findroot, diff
mp.dps = 50
X = [mpf(v) for v in (1, 2, 3, 4, 10)]
N = lambda x, m, v: exp(-(x-m)**2/(2*v))/sqrt(2*pi*v)
def r1(m1, m2, v): return [N(x,m1,v)/(N(x,m1,v)+N(x,m2,v)) for x in X]
def L(m1, m2, v): return sum(log(mpf('0.5')*N(x,m1,v)+mpf('0.5')*N(x,m2,v)) for x in X)
def em(m1, m2, v):
    r = r1(m1,m2,v); n1 = sum(r); n2 = 5-n1
    return sum(a*x for a,x in zip(r,X))/n1, sum((1-a)*x for a,x in zip(r,X))/n2
def g(m1, m2, v):
    r = r1(m1,m2,v); return sum(a*x for a,x in zip(r,X))/sum(r)
out = {}
# note cross-check: first E-step table and M-step (sigma^2=16, mu=(2.5,6.5))
r = r1(mpf('2.5'), mpf('6.5'), 16)
out['note_r_col1'] = [float(round(a,4)) for a in r]
out['note_N1'] = float(sum(r))
m = em(mpf('2.5'), mpf('6.5'), 16); out['note_mu_new'] = [float(m[0]), float(m[1])]
def run(a, b, v, T):
    p = (mpf(a), mpf(b)); Ls = [L(*p, v)]
    for _ in range(T): p = em(*p, v); Ls.append(L(*p, v))
    return p, Ls
cases = {'s1_16_1': (2.5,6.5,16,1), 's1_16_30': (2.5,6.5,16,30), 's1_4_10': (2.5,6.5,4,10), 's1_4_swap': (6.5,2.5,4,10), 's1_4_diag': (6,6,4,10), 's1_4_curve': (3,4,4,20)}
mono = True
for k,(a,b,v,T) in cases.items():
    p, Ls = run(a,b,v,T)
    mono = mono and all(Ls[i+1] >= Ls[i] - mpf('1e-30') for i in range(len(Ls)-1))
    out[k] = {'mu': [float(p[0]), float(p[1])], 'L': float(Ls[-1])}
out['loglik_monotone_all_cases'] = mono
out['L_sym_4'] = float(L(4,4,4)); out['L_sym_16'] = float(L(4,4,16))
# exhaustive monotonicity over a grid of starts and variances
viol = 0
for v in (1, 2, 4, 8, 16, 20):
    for a in range(-1, 13, 2):
        for b in range(-1, 13, 3):
            p = (mpf(a), mpf(b)); l0 = L(*p, v)
            for _ in range(15):
                p = em(*p, v); l1 = L(*p, v)
                if l1 < l0 - mpf('1e-25'): viol += 1
                l0 = l1
out['monotone_grid_violations'] = viol
# topic 2: fixed points via findroot, slopes, gradient identity
fp = {}
for v, m2, guesses in ((16, 6.5, (3,)), (2, 6.5, (2.4, 7.45, 10))):
    roots = []
    for gs in guesses:
        z = findroot(lambda t: g(t, mpf(m2), v) - t, mpf(gs))
        roots.append({'z': float(z), 'gprime': float(diff(lambda t: g(t, mpf(m2), v), z))})
    fp[f's2={v},m2={m2}'] = roots
out['fixed_points'] = fp
# gradient: dL/dmu1 (pi fixed) == sum r (x-mu)/v at random points, via numeric diff of L
gerr = 0
for (m1, m2, v) in ((2.5, 6.5, 16), (7, 6.5, 2), (-1, 12, 1), (9.5, 3, 5)):
    num = diff(lambda t: L(t, mpf(m2), v), mpf(m1))
    ana = sum(a*(x-m1) for a, x in zip(r1(mpf(m1), mpf(m2), v), X))/v
    gerr = max(gerr, float(abs(num-ana)))
out['grad_identity_maxerr'] = gerr
# frozen line root equals g(current) and equals note mu1_new
out['frozen_root_from_2.5'] = float(g(mpf('2.5'), mpf('6.5'), 16))
# topic 2 iterations
def it(a, m2, v, T):
    z = mpf(a)
    for _ in range(T): z = g(z, mpf(m2), v)
    return float(z)
out['t2_16_1'] = it(2.5, 6.5, 16, 1); out['t2_16_10'] = it(2.5, 6.5, 16, 10)
out['t2_2_from7'] = it(7, 6.5, 2, 10); out['t2_2_from7.5'] = it(7.5, 6.5, 2, 10)
json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
