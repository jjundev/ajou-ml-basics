from fractions import Fraction as F
from pathlib import Path
import json
R=Path(__file__).resolve().parent
def transpose(a):return list(map(list,zip(*a)))
def mul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def inv(a):
 n=len(a); t=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
 for i in range(n):
  k=next(k for k in range(i,n) if t[k][i]);t[i],t[k]=t[k],t[i];z=t[i][i];t[i]=[x/z for x in t[i]]
  for k in range(n):
   if k!=i:
    z=t[k][i];t[k]=[x-z*y for x,y in zip(t[k],t[i])]
 return [row[n:] for row in t]
out={}
for i,q in enumerate(json.loads((R/'work/problem-data.json').read_text()),1):
 B=q.get('B',[[v] for v in q.get('b',[])])
 bt=transpose(B); gram=mul(bt,B); pinv=mul(inv(gram),bt); P=mul(B,pinv); x=[[F(v)] for v in q['x']]; lam=mul(pinv,x);proj=mul(P,x);res=[[a[0]-b[0]] for a,b in zip(x,proj)]
 assert all(v==0 for row in mul(bt,res) for v in row)
 assert mul(P,P)==P
 out[f'p{i}']={k:[[str(v) for v in row] for row in v] for k,v in dict(B=B,gram=gram,coordinates=lam,P=P,projection=proj,residual=res).items()}
 out[f'p{i}']['distance_squared']=str(sum(row[0]**2 for row in res))
(R/'answers.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
