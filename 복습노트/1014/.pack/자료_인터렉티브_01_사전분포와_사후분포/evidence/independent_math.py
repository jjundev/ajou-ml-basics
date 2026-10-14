"""Independent exact answers: solve the two normal equations by elimination."""
from fractions import Fraction as F
import json

def solve(a,b,c,d,r,s):
    # Eliminate the first unknown; intentionally independent of JS's inverse route.
    second=(s-c*r/a)/(d-c*b/a)
    return [(r-b*second)/a,second]

def exact(n=3,tau2=F(1),sigma2=F(1),xstar=F(2)):
    xs=list(map(F,[-1,0,1]))[:n];ys=list(map(F,[0,1,2]))[:n]
    a=1/tau2+F(n)/sigma2;b=sum(xs,F(0))/sigma2
    d=1/tau2+sum((x*x for x in xs),F(0))/sigma2
    m=solve(a,b,b,d,sum(ys,F(0))/sigma2,sum((x*y for x,y in zip(xs,ys)),F(0))/sigma2)
    columns=[solve(a,b,b,d,F(1),F(0)),solve(a,b,b,d,F(0),F(1))]
    S=[[columns[j][i] for j in range(2)] for i in range(2)]
    v=S[0][0]+2*xstar*S[0][1]+xstar*xstar*S[1][1]
    return {'n':n,'tau2':str(tau2),'sigma2':str(sigma2),'xstar':str(xstar),
            'mean':[str(v) for v in m],'cov':[[str(v) for v in row] for row in S],
            'prediction':{'mean':str(m[0]+xstar*m[1]),'functionVariance':str(v),'observationVariance':str(v+sigma2)}}

if __name__=='__main__':
    print(json.dumps([exact(),exact(0,xstar=F(0)),exact(1,xstar=F(0)),exact(xstar=F(3)),exact(tau2=F(1,4),xstar=F(3)),exact(sigma2=F(2),xstar=F(3))],indent=2))
