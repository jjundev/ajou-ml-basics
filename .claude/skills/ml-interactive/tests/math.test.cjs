const test=require('node:test'), assert=require('node:assert/strict');
const M=require('../assets/ml-math.js');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-12,`${a} != ${b}`);
test('posterior agrees with independently eliminated rational fixtures',()=>{
  const rows=require('./fixtures/math-golden.json');
  const number=s=>{const [a,b]=s.split('/').map(Number);return b===undefined?a:a/b;};
  for(const row of rows){const tau2=number(row.tau2),sigma2=number(row.sigma2);
    const p=M.posterior({xs:[-1,0,1],ys:[0,1,2],n:row.n,S0:[[tau2,0],[0,tau2]],sigma2});
    p.mean.forEach((v,i)=>near(v,number(row.mean[i])));
    p.cov.forEach((r,i)=>r.forEach((v,j)=>near(v,number(row.cov[i][j]))));
    const q=M.predict(p,number(row.xstar),sigma2);for(const key of Object.keys(q))near(q[key],number(row.prediction[key]));
  }
});
test('symmetric observations and prediction match rational answers',()=>{
  const p=M.posterior({xs:[-1,0,1],ys:[0,1,2],sigma2:1});
  near(p.mean[0],3/4); near(p.mean[1],2/3);
  near(p.cov[0][0],1/4); near(p.cov[1][1],1/3); near(p.cov[0][1],0);
  const q=M.predict(p,2,1);
  near(q.mean,25/12); near(q.functionVariance,19/12); near(q.observationVariance,31/12);
});
test('off-diagonal posterior is retained',()=>{
  const p=M.posterior({xs:[0,1],ys:[1,2],sigma2:1});
  near(p.mean[0],4/5); near(p.mean[1],3/5);
  near(p.cov[0][1],-1/5); near(p.cov[1][0],-1/5);
});
test('zero data preserves nonzero mean and correlated prior',()=>{
  const S0=[[2,.5],[.5,1]],m0=[1,-2];
  const p=M.posterior({xs:[-1,0,1],ys:[0,1,2],n:0,m0,S0,sigma2:1});
  assert.deepEqual(p.mean,m0); assert.deepEqual(p.cov,S0);
});
test('rejects invalid inputs rather than plotting NaN',()=>{
  for(const input of [
    {sigma2:0},{sigma2:-1},{sigma2:NaN},{n:-1},{n:.5},{n:4},
    {S0:[[1,2],[2,1]]},{S0:[[1,0],[1,1]]},{xs:[Infinity,0,1]},
    {ys:[0,1]}, {m0:[0,NaN]}
  ]) assert.throws(()=>M.posterior({xs:[-1,0,1],ys:[0,1,2],sigma2:1,...input}),RangeError);
  assert.throws(()=>M.normalPdf(0,0,0),RangeError);
});
test('fixed seed repeats samples and input matrices are unchanged',()=>{
  const p=M.posterior({xs:[-1,0,1],ys:[0,1,2],sigma2:1});
  const before=JSON.stringify(p);
  assert.deepEqual(M.sampleWeights(p,1014,12),M.sampleWeights(p,1014,12));
  assert.equal(JSON.stringify(p),before);
});
test('normal density has unit area and predictive variances remain distinct',()=>{
  const h=16/4096;
  let area=0;
  for(let i=0;i<=4096;i++) area+=M.normalPdf(-8+i*h,0,1)*((i===0||i===4096)?0.5:1)*h;
  assert.ok(Math.abs(area-1)<1e-6);
  for(const tau2 of [.25,1,4]) for(const sigma2 of [.1,1,2]) for(const n of [0,1,3]){
    const p=M.posterior({xs:[-1,0,1],ys:[0,1,2],n,sigma2,S0:[[tau2,0],[0,tau2]]});
    assert.ok(p.cov[0][0]*p.cov[1][1]-p.cov[0][1]**2>0);
    for(const x of [-3,0,3]){
      const q=M.predict(p,x,sigma2);
      near(q.observationVariance-q.functionVariance,sigma2);
    }
  }
});
