"""Blind verifier: reads problem-data.json only; exact Fraction Gram-Schmidt."""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def dot(a,b): return sum((v*w for v,w in zip(a,b)), F(0))
def matvec(A,v): return [dot(r,v) for r in A]
def transpose(A): return list(map(list,zip(*A)))
def mul(A,B): return [[dot(r,c) for c in transpose(B)] for r in A]
def solve(A,y):
    a=[list(r)+[v] for r,v in zip(A,y)]
    for k in range(len(a)):
        pivot=next(i for i in range(k,len(a)) if a[i][k])
        a[k],a[pivot]=a[pivot],a[k]
        den=a[k][k]; a[k]=[v/den for v in a[k]]
        for i in range(len(a)):
            if i!=k:
                factor=a[i][k]; a[i]=[v-factor*w for v,w in zip(a[i],a[k])]
    return [r[-1] for r in a]
def fmt(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,list): return [fmt(v) for v in x]
    if isinstance(x,dict): return {k:fmt(v) for k,v in x.items()}
    return x

out=[]
for i,item in enumerate(json.loads((ROOT/'problem-data.json').read_text()),1):
    B=[[F(v)] for v in item['b']] if 'b' in item else [[F(v) for v in r] for r in item['B']]
    x=list(map(F,item['x'])); cols=transpose(B); orth=[]
    for col in cols:
        u=col[:]
        for q in orth:
            c=dot(col,q)/dot(q,q)
            u=[v-c*w for v,w in zip(u,q)]
        assert dot(u,u)>0
        orth.append(u)
    P=[[sum((q[r]*q[c]/dot(q,q) for q in orth), F(0)) for c in range(3)] for r in range(3)]
    projected=matvec(P,x)
    residual=[v-w for v,w in zip(x,projected)]
    # Recover original coordinates from B*a=projected using exact normal equations.
    gram=mul(transpose(B),B)
    coordinates=solve(gram,matvec(transpose(B),projected))
    residual_dots=[dot(c,residual) for c in cols]
    assert matvec(B,coordinates)==projected
    assert all(v==0 for v in residual_dots)
    assert mul(P,P)==P
    assert transpose(P)==P
    out.append(fmt(dict(id=f'p{i}',projection_matrix=P,coordinates=coordinates,projected_vector=projected,residual_vector=residual,residual_squared_norm=dot(residual,residual),basis_dot_residual=residual_dots,idempotent=True,symmetric=True)))
(ROOT/'independent_results.json').write_text(json.dumps({'method':'Exact rational unnormalized Gram-Schmidt; P=sum q q^T/(q^T q). Original basis coordinates recovered by exact Gaussian elimination.','results':out},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,indent=2))
