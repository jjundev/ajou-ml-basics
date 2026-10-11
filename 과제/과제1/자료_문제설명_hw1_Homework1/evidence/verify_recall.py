"""Exact identities for new recall formulas, plus preservation against baseline."""
from pathlib import Path
import sys,json
import sympy as s
repo=Path.cwd()
sys.path.insert(0,str(repo/'.claude/skills/ml-problem-explain/scripts'))
from mpe_cli import load_run,load_fragments,load_artifacts
from mpe_shared import parse,outer,compact
folder=Path(__file__).parent.parent
item=load_run(folder.parent)[0]
fragments=load_fragments(item)
base=folder.parent.parent/'baseline-fragments'
results={}
def check(name,condition):
    assert condition,name
    results[name]='pass'
x,y=s.symbols('x y',real=True)
a,b,c,d=s.symbols('a b c d',real=True)
v=s.Matrix([x,y]);q=s.Matrix([[a,b],[c,d]])
grad=s.Matrix([s.diff((v.T*q*v)[0],z) for z in v])
check('quadratic_gradient_general',s.simplify(grad-(q+q.T)*v)==s.zeros(2,1))
check('two_by_two_inverse',s.simplify(q*s.Matrix([[d,-b],[-c,a]])-(a*d-b*c)*s.eye(2))==s.zeros(2))
aa=s.symbols('aa',positive=True);bb,dd,z=s.symbols('bb dd z',real=True)
check('complete_square',s.expand(aa*(z+bb/(2*aa))**2+dd-bb**2/(4*aa)-(aa*z*z+bb*z+dd))==0)
sigma2,b2=s.symbols('sigma2 b2',positive=True)
res,theta,m0=s.symbols('res theta m0',real=True)
check('ridge_scale',s.expand(2*sigma2*(res**2/(2*sigma2)+theta**2/(2*b2))-(res**2+sigma2/b2*theta**2))==0)
Y=s.symbols('y0:3',real=True)
loss=sum((yn-theta)**2/(2*sigma2) for yn in Y)+(theta-m0)**2/(2*b2)
meanmap=(sum(Y)/sigma2+m0/b2)/(3/sigma2+1/b2)
check('nonzero_prior_mean',s.simplify(s.diff(loss,theta).subs(theta,meanmap))==0)
Phi=s.Matrix([[1,1],[2,2]])
check('duplicate_column_nullspace',Phi*s.Matrix([1,-1])==s.zeros(2,1))
check('positive_ridge_eigenvalues',set((Phi.T*Phi+5*s.eye(2)).eigenvals())=={5,15})
u=s.Matrix([1,1])
check('shared_noise_outer_product',u*u.T==s.ones(2))
S0=s.diag(1,2);S1=s.Matrix([[2,1],[1,2]])
P=S0.inv()+S1.inv();Sq=P.inv();mq=Sq*S1.inv()*s.ones(2,1)
lhs=(v.T*S0.inv()*v)[0]+((v-s.ones(2,1)).T*S1.inv()*(v-s.ones(2,1)))[0]
rhs=((v-mq).T*P*(v-mq))[0]
check('gaussian_product_complete_square',s.simplify(lhs-rhs)==s.Rational(5,11))
check('gaussian_product_normalizer',Sq.det()==s.Rational(6,11) and Sq.is_positive_definite)
for p in item['pack'].problems:
    old=parse((base/f'{p.id}.html').read_text(encoding='utf-8'))
    new=parse(fragments[p.id])
    oldsections={n.attrs['data-explanation']:outer(n) for n in old.find_all(lambda n:'data-explanation' in n.attrs)}
    newsections={n.attrs['data-explanation']:outer(n) for n in new.find_all(lambda n:'data-explanation' in n.attrs)}
    check(p.id+'_old_explanations_preserved',all(compact(markup)==compact(newsections[k]) for k,markup in oldsections.items()))
    recall=next(new.find_all(lambda n:n.attrs.get('data-explanation')=='recall'))
    check(p.id+'_body_and_subparts',len(recall.text())>150 and '문제의 단서' in recall.text())
artifacts=load_artifacts(item)
html=artifacts.html.read_text(encoding='utf-8');md=artifacts.md.read_text(encoding='utf-8')
check('25_html_sections',len(list(parse(html).find_all(lambda n:n.attrs.get('data-explanation')=='recall')))==25)
check('25_md_sections',md.count('#### 이 문제를 봤을 때 떠올릴 개념과 공식')==25)
check('25_md_summaries',md.count('떠올릴 개념·공식')==25)
(Path(__file__).parent/'recall-exact-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS:',len(results),'exact identity/preservation/coverage checks')
