/* 위젯 수학 (정리노트 인라인 원본). 브라우저: 전역 함수 / Node: module.exports */
function polyFeatures(x, degree) {
  const row = [];
  for (let p = 0; p <= degree; p++) row.push(x ** p);
  return row;
}

function solveLinear(A, b) {
  const n = b.length;
  const M = A.map((row, i) => [...row, b[i]]);
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    [M[c], M[p]] = [M[p], M[c]];
    const piv = M[c][c];
    if (Math.abs(piv) < 1e-14) throw new Error('singular');
    for (let r = 0; r < n; r++) {
      if (r === c) continue;
      const f = M[r][c] / piv;
      for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k];
    }
  }
  return M.map((row, i) => row[n] / row[i]);
}

function ridgeFit(xs, ys, degree, lambda) {
  const N = xs.length;
  const D = degree + 1;
  const Phi = xs.map((x) => polyFeatures(x, degree));
  const A = Array.from({ length: D }, (_, i) =>
    Array.from({ length: D }, (_, j) => {
      let s = 0;
      for (let n = 0; n < N; n++) s += Phi[n][i] * Phi[n][j];
      return s + (i === j ? N * lambda : 0);
    })
  );
  const b = Array.from({ length: D }, (_, i) => {
    let s = 0;
    for (let n = 0; n < N; n++) s += Phi[n][i] * ys[n];
    return s;
  });
  return solveLinear(A, b);
}

function predictPoly(theta, x) {
  return theta.reduce((s, t, p) => s + t * x ** p, 0);
}

function mse(theta, xs, ys) {
  return xs.reduce((s, x, i) => s + (ys[i] - predictPoly(theta, x)) ** 2, 0) / xs.length;
}

function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function makeDataset(seed) {
  const rand = mulberry32(seed);
  const gauss = () => {
    const u = 1 - rand();
    const v = rand();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  const truth = (x) => Math.sin(Math.PI * x);
  const trainX = Array.from({ length: 10 }, (_, i) => -1 + (2 * i) / 9);
  const testX = Array.from({ length: 10 }, (_, i) => -0.95 + (1.9 * i) / 9);
  return {
    trainX,
    trainY: trainX.map((x) => truth(x) + 0.25 * gauss()),
    testX,
    testY: testX.map((x) => truth(x) + 0.25 * gauss()),
    truth,
  };
}

function lgamma(z) {
  const g = 7;
  const c = [
    0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
    -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6,
    1.5056327351493116e-7,
  ];
  if (z < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * z)) - lgamma(1 - z);
  z -= 1;
  let x = c[0];
  for (let i = 1; i < g + 2; i++) x += c[i] / (z + i);
  const t = z + g + 0.5;
  return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
}

function betaPdf(t, a, b) {
  if (t <= 0 || t >= 1) return 0;
  return Math.exp((a - 1) * Math.log(t) + (b - 1) * Math.log(1 - t) + lgamma(a + b) - lgamma(a) - lgamma(b));
}

function coinEstimates(N, k, a) {
  return { ml: k / N, map: (k + a - 1) / (N + 2 * a - 2), pred: (k + a) / (N + 2 * a) };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { polyFeatures, solveLinear, ridgeFit, predictPoly, mse, mulberry32, makeDataset, lgamma, betaPdf, coinEstimates };
}
