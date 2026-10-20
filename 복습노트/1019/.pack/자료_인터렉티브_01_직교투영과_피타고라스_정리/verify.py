from fractions import Fraction as F
import json, pathlib, pymupdf
run=pathlib.Path(__file__).parent
out=run/'evidence';out.mkdir(exist_ok=True)
checks=[]
for z in (0,1):
    y=(F(2),F(0),F(1));b=(F(1),F(1),F(0));a=(F(0),F(0),F(z))
    theta_hat=sum(bi*(yi-ai) for bi,yi,ai in zip(b,y,a))/sum(bi*bi for bi in b)
    assert theta_hat==1
    hat=tuple(ai+bi*theta_hat for ai,bi in zip(a,b))
    r=tuple(yi-hi for yi,hi in zip(y,hat))
    assert sum(bi*ri for bi,ri in zip(b,r))==0
    for t in (F(-1,2),F(0),F(1),F(193,100),F(5,2)):
        q=tuple(ai+bi*t for ai,bi in zip(a,b))
        direct=sum((yi-qi)**2 for yi,qi in zip(y,q))
        split=sum(ri*ri for ri in r)+sum((hi-qi)**2 for hi,qi in zip(hat,q))
        assert direct==split==F(2)+(1-z)**2+2*(t-1)**2
        checks.append(dict(z=z,theta=str(t),theta_hat=str(theta_hat),direct=str(direct),split=str(split)))
(out/'independent-math.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
sources=[]
for file,pages in [('강의노트/Lecture04_Linear_Regression_Part2_rev_HO.pdf',[19,20,21,24]),('교과서/Mathematics_for_Machine_Learning.pdf',[88,89,90,91])]:
    doc=pymupdf.open(file)
    sources.append(file+'\n'+'\n'.join(f'PDF page {n}\n'+doc[n-1].get_text() for n in pages))
(out/'source-excerpts.txt').write_text('\n\n'.join(sources),encoding='utf-8')
print('PASS: 10 independent exact rational checks; source pages extracted')
