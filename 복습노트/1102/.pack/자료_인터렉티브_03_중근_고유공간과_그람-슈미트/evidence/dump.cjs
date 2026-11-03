// Dumps compute() results over input grids so verify.py can check them by a different route.
// Usage: node dump.cjs <skill dir>  → writes dump.json next to this file
const fs = require('node:fs');
const path = require('node:path');
const { loadComponent } = require(path.join(process.argv[2], 'scripts', 'harness.cjs'));
const run = __dirname, out = {};

{
  const { c } = loadComponent(path.join(run, '1', 'Main.dc.html'));
  out.t1 = { sample: c.sample(), grid: [] };
  for (const [alpha, sa, sb] of [[0, 2, 0.8], [30, 2, 0.8], [30, 1.2, 1.2], [175, 3, 2], [45, 0.5, 2], [120, 2.7, 0.3]]) for (const theta of [0, 30, 75, 90, 120, 175]) {
    const d = c.compute({ alpha, sa, sb, theta });
    out.t1.grid.push({ alpha, sa, sb, theta, pts: d.pts, S: d.S, V1: d.V1, Vp: d.Vp, quad: d.quad, total: d.total, l1: d.l1, l2: d.l2, tied: d.tied, p1deg: d.p1deg, weighted: d.weighted, mean: d.mean });
  }
}
{
  const { c } = loadComponent(path.join(run, '2', 'Main.dc.html'));
  out.t2 = [];
  const mats = [[2, 1, 1, 2], [2, 1, 0, 1], [1, 1, 0, 1], [2, 0, 0, 2], [2.5, -1, -1, 2.5], [0, -1, 1, 0], [1, 2, 2, 4], [-3, 3, -3, 3], [0.3, -2.1, 1.7, -0.4], [-1.2, 0.5, 2.4, 1.9], [0, 0, 0, 0]];
  for (const [a11, a12, a21, a22] of mats) for (const theta of [0, 45, 135, 200]) {
    const d = c.compute({ a11, a12, a21, a22, theta });
    const stages = d.evd ? [0, 1, 2, 3].map((f) => c.stageMatrix(d.evd, f)) : null;
    out.t2.push({ A: d.A, theta, Ax: d.Ax, kind: d.kind, lams: d.lams, vecs: d.vecs, sym: d.sym, gap: d.gap, parallel: d.parallel, turn: d.turn, evd: d.evd, stages });
  }
}
{
  const { c } = loadComponent(path.join(run, '3', 'Main.dc.html'));
  out.t3 = [];
  for (const [alpha, beta] of [[0, 60], [0, 20], [30, 120], [45, 150], [60, 60], [175, 5], [10, 95], [0, 175]]) for (const gs of [false, true]) {
    const d = c.compute({ alpha, beta, gs });
    out.t3.push({ alpha, beta, gs, v1: d.v1, v2: d.v2, u2: d.u2, P: d.P, c: d.c, errT: d.errT, errInv: d.errInv, res1: d.res1, res2: d.res2, p3v1: d.p3v1, p3v2: d.p3v2, indep: d.indep });
  }
}
fs.writeFileSync(path.join(run, 'dump.json'), JSON.stringify(out));
console.log('dumped', out.t1.grid.length, out.t2.length, out.t3.length);
