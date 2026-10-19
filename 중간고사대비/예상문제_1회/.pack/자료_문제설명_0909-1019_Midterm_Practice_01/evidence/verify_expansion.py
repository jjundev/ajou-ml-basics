from pathlib import Path
import json,sys
import sympy as s
R=Path(__file__).resolve().parent
M=s.Matrix; Q=s.Rational
checks=[]
def equal(name,a,b):
    delta=a-b
    ok=all(s.simplify(v)==0 for v in delta) if isinstance(delta,s.MatrixBase) else s.simplify(delta)==0
    checks.append({'name':name,'status':'pass' if ok else 'fail','actual':str(a),'expected':str(b),'method':'symbolic'})
def main():
    t,z,x1,x2=s.symbols('t z x1 x2', real=True)
    V=M([[1,0,1],[0,1,1],[1,1,2]]);U=V[:,:2]
    equal('p1 dependency',V*M([1,1,-1]),s.zeros(3,1))
    equal('p1 all solutions',V*M([2-t,1-t,t]),M([2,1,3]))
    equal('p1 Gram inverse',(U.T*U).inv(),Q(1,3)*M([[2,-1],[-1,2]]))
    equal('p1 c inconsistent',V.row_join(M([2,1,4])).rank()-V.rank(),1)
    x=M([x1,x2]);A=M([[4,1],[1,2]]);b=M([1,0]);q=(x.T*A*x)[0]/2-(b.T*x)[0]
    equal('p2 Jacobian',M([x1*x1+x2,x1*x2]).jacobian(x),M([[2*x1,1],[x2,x1]]))
    equal('p2 gradient',M([s.diff(q,v) for v in x]),A*x-b)
    equal('p2 Hessian',s.hessian(q,x),A)
    equal('p2 stationary',A.inv()*b,M([Q(2,7),-Q(1,7)]))
    equal('p2 determinant',A.det(),7)
    g=s.exp(-z*z/2-(z-2)**2/6)/(2*s.pi*s.sqrt(3))
    equal('p3 square',z*z+(z-2)**2/3,Q(4,3)*(z-Q(1,2))**2+1)
    Z=s.integrate(g,(z,-s.oo,s.oo));equal('p3 integral',Z,s.exp(-Q(1,2))/s.sqrt(8*s.pi))
    equal('p3 q coefficient',1/s.sqrt(2*s.pi*Q(3,4)),s.sqrt(2/(3*s.pi)))
    F=M([[1,-1],[1,0],[1,1]]);y=M([0,1,4]);G=F.T*F
    equal('p4 Gram',G,s.diag(3,2));equal('p4 cross',F.T*y,M([5,4]))
    ml=G.inv()*F.T*y;mp=(G+s.eye(2)).inv()*F.T*y
    equal('p4 ML',ml,M([Q(5,3),2]));equal('p4 MAP',mp,M([Q(5,4),Q(4,3)]))
    equal('p4 ML prediction',(M([[1,2]])*ml)[0],Q(17,3));equal('p4 MAP prediction',(M([[1,2]])*mp)[0],Q(47,12))
    equal('p4 inverse prior',(2*s.eye(2)).inv(),s.eye(2)/2)
    points=[M([0,0]),M([2,0]),M([0,2])];mu=sum(points,s.zeros(2,1))/3
    C=sum(((p-mu)*(p-mu).T for p in points),s.zeros(2,2))/3
    equal('p5 mean',mu,M([Q(2,3),Q(2,3)]));equal('p5 covariance',C,M([[8,-4],[-4,8]])/9)
    B=M([[1,1],[1,-1]])
    equal('p5 affine mean',B*mu+M([1,-1]),M([Q(7,3),-1]))
    equal('p5 affine covariance',B*C*B.T,s.diag(Q(8,9),Q(8,3)))
    equal('p5 cross covariance',C*B.T,M([[Q(4,9),Q(4,3)],[Q(4,9),-Q(4,3)]]))
    # Symbolic two-parameter derivatives of the general least-squares form.
    g11,g12,g22,h1,h2,v,w,m1,m2,lam=s.symbols('g11 g12 g22 h1 h2 v w m1 m2 lam',real=True)
    sig,tau=s.symbols('sig tau',positive=True);th=M([v,w]);m=M([m1,m2]);gg=M([[g11,g12],[g12,g22]]);h=M([h1,h2])
    quad=(th.T*gg*th)[0]-2*(th.T*h)[0]
    equal('p6 quadratic gradient',M([s.diff(quad,u) for u in th]),2*gg*th-2*h)
    obj=quad/(2*sig)+((th-m).T*(th-m))[0]/(2*tau)
    equal('p7 posterior gradient',M([s.diff(obj,u) for u in th]),(gg*th-h)/sig+(th-m)/tau)
    equal('p7 lambda equation',sig*M([s.diff(obj,u) for u in th]),(gg+sig/tau*s.eye(2))*th-h-sig/tau*m)
    F7=M([[1,1],[2,2]]);y7=M([1,2])
    equal('p7 numeric ridge',(F7.T*F7+s.eye(2)).inv()*F7.T*y7,M([Q(5,11),Q(5,11)]))
    equal('p7 general ridge',(F7.T*F7+lam*s.eye(2)).inv()*F7.T*y7,M([5/(10+lam),5/(10+lam)]))
    equal('p8 square',(t-1)**2+(2-t)**2+t*t,3*(t-1)**2+2)
    post=s.sqrt(3/(4*s.pi))*s.exp(-3*(t-1)**2/4)
    equal('p8 normalizes',s.integrate(post,(t,-s.oo,s.oo)),1)
    equal('p8 mean',s.integrate(t*post,(t,-s.oo,s.oo)),1)
    equal('p8 variance',s.integrate((t-1)**2*post,(t,-s.oo,s.oo)),Q(2,3))
    equal('p8 f variance',4*Q(2,3),Q(8,3));equal('p8 y variance',4*Q(2,3)+2,Q(14,3))
    yy=s.symbols('y',real=True);vv=s.symbols('variance',positive=True);aa=1+1/vv
    equal('p9 completing square',(yy-t)**2+t*t/vv,aa*(t-yy/aa)**2+yy*yy/(1+vv))
    equal('p9 integral coefficient',s.sqrt(2*s.pi/aa)/(2*s.pi*s.sqrt(vv)),1/s.sqrt(2*s.pi*(1+vv)))
    factor=s.sqrt(10*s.pi)/s.sqrt(4*s.pi);equal('p9 factor',factor,s.sqrt(Q(5,2)))
    equal('p9 posterior probability',factor/(2+factor),s.sqrt(10)/(4+s.sqrt(10)))
    F10=M([[1,0],[1,1],[1,-1]]);y10=M([2,2,0]);G10=F10.T*F10
    theta=G10.inv()*F10.T*y10;P=F10*G10.inv()*F10.T;r=y10-F10*theta
    equal('p10 theta',theta,M([Q(4,3),1]))
    equal('p10 projection',P,M([[2,2,2],[2,5,-1],[2,-1,5]])/6)
    equal('p10 symmetric',P.T,P);equal('p10 idempotent',P*P,P)
    equal('p10 orthogonal',F10.T*r,s.zeros(2,1));equal('p10 SSE',(r.T*r)[0],Q(2,3))
    beta=M(s.symbols('beta1 beta2'));u=F10*beta
    equal('p10 arbitrary point distance',((y10-u).T*(y10-u))[0],(r.T*r)[0]+((F10*theta-u).T*(F10*theta-u))[0])
    errors=[c for c in checks if c['status']!='pass']
    result={'status':'fail' if errors else 'pass','count':len(checks),'errors':errors,'checks':checks}
    (R/'math-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False));return bool(errors)
if __name__=='__main__': sys.exit(main())
