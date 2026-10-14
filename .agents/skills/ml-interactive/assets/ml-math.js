(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.MLMath=factory();})(globalThis,function(){
const vector=(a,n)=>Array.isArray(a)&&a.length===n&&a.every(Number.isFinite);
function requireSPD(S){
  if(!Array.isArray(S)||S.length!==2||!S.every(r=>vector(r,2))||
    Math.abs(S[0][1]-S[1][0])>1e-12||!(S[0][0]>0)||!(S[1][1]>0)||
    !(S[0][0]*S[1][1]-S[0][1]*S[1][0]>0))
    throw new RangeError('covariance must be finite symmetric SPD');
  if(!Number.isFinite(S[0][0]*S[1][1]-S[0][1]*S[1][0])) throw new RangeError('covariance overflow');
}
function validate({xs,ys,n,m0,S0,sigma2}){
  if(!Array.isArray(xs)||!xs.every(Number.isFinite)||!vector(ys,xs.length)||
    !Number.isInteger(n)||n<0||n>xs.length||!vector(m0,2)||
    !Number.isFinite(sigma2)||!(sigma2>0)) throw new RangeError('invalid regression input');
  requireSPD(S0);
}
function validatePosterior(p){
  if(!p||!vector(p.mean,2)) throw new RangeError('invalid posterior mean');
  requireSPD(p.cov);
}
function inverse(S) {
  const [[a,b],[c,d]]=S,det=a*d-b*c;
  if(!(det>0) || !Number.isFinite(det)) throw new RangeError('covariance must be SPD');
  return [[d/det,-b/det],[-c/det,a/det]];
}
function posterior({xs,ys,n,m0=[0,0],S0=[[1,0],[0,1]],sigma2}={}) {
  if(n===undefined && Array.isArray(xs)) n=xs.length;
  validate({xs,ys,n,m0,S0,sigma2});
  if(n===0) return {mean:[...m0],cov:S0.map(r=>[...r]),n};
  const A=inverse(S0);
  const b=[A[0][0]*m0[0]+A[0][1]*m0[1],A[1][0]*m0[0]+A[1][1]*m0[1]];
  for(let i=0;i<n;i++){
    const x=xs[i],y=ys[i],beta=1/sigma2;
    A[0][0]+=beta; A[0][1]+=beta*x; A[1][0]+=beta*x; A[1][1]+=beta*x*x;
    b[0]+=beta*y; b[1]+=beta*x*y;
  }
  const cov=inverse(A);
  const mean=[cov[0][0]*b[0]+cov[0][1]*b[1],cov[1][0]*b[0]+cov[1][1]*b[1]];
  validatePosterior({mean,cov});
  return {mean,cov,n};
}
function predict(p,x,sigma2) {
  validatePosterior(p);
  if(!Number.isFinite(x)||!(sigma2>0)||!Number.isFinite(sigma2)) throw new RangeError('invalid prediction input');
  const mean=p.mean[0]+x*p.mean[1];
  const raw=p.cov[0][0]+2*x*p.cov[0][1]+x*x*p.cov[1][1];
  if(!Number.isFinite(raw)||raw < -1e-12) throw new RangeError('invalid function variance');
  const functionVariance=Math.max(0,raw);
  const observationVariance=functionVariance+sigma2;
  if(![mean,functionVariance,observationVariance].every(Number.isFinite)) throw new RangeError('prediction overflow');
  return {mean,functionVariance,observationVariance};
}
function normalPdf(x,mu,v) {
  if(![x,mu,v].every(Number.isFinite)||!(v>0)) throw new RangeError('normal density needs positive variance');
  return Math.exp(-.5*(x-mu)**2/v)/Math.sqrt(2*Math.PI*v);
}
function sampleWeights(p,seed,count) {
  validatePosterior(p);
  if(!Number.isInteger(seed)||!Number.isInteger(count)||count<0||count>1000)
    throw new RangeError('invalid sampling input');
  const L00=Math.sqrt(p.cov[0][0]),L10=p.cov[1][0]/L00;
  const L11=Math.sqrt(p.cov[1][1]-L10*L10);
  let s=seed>>>0;
  const u=()=>{s=(Math.imul(1664525,s)+1013904223)>>>0;return (s+.5)/4294967296;};
  return Array.from({length:count},()=>{
    const r=Math.sqrt(-2*Math.log(u())),a=2*Math.PI*u();
    const z0=r*Math.cos(a),z1=r*Math.sin(a);
    return [p.mean[0]+L00*z0,p.mean[1]+L10*z0+L11*z1];
  });
}
return {posterior,predict,normalPdf,sampleWeights};
});
