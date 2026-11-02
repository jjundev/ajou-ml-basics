// Dumps compute() results over an input grid so verify.py can check them by a different route.
const fs = require('node:fs');
const path = require('node:path');
const skill = process.argv[2];
const { loadComponent } = require(path.join(skill, 'scripts', 'harness.cjs'));
const run = __dirname;
const out = {};

{
  const { c } = loadComponent(path.join(run, '1', 'Main.dc.html'));
  out.t1 = [];
  for (const sigma1 of [0.5, 1, 2, 4, 5]) for (const rho of [0.2, 0.6, 0.9, 0.95]) {
    const d = c.compute({ sigma1, rho });
    out.t1.push({ sigma1, rho, raw: d.raw, restored: d.restored, projected: d.projected, b: d.estd.b, rawDeg: d.eraw.deg, stdDeg: d.estd.deg, keepRaw: d.keepRaw, keepStd: d.keepStd });
  }
}
{
  const { c } = loadComponent(path.join(run, '2', 'Main.dc.html'));
  out.t2 = { datasets: {}, grid: [] };
  for (const dataset of ['note', 'sample']) {
    c.setState({ dataset });
    const d = c.compute(Object.assign({}, c.state, { f: 12 }));
    out.t2.datasets[dataset] = { data: d.data, sum: d.sum, avg: d.avg };
  }
  for (const [sigma1, sigma2, rho, mu1, mu2, centered] of [[2, 1, 0.6, 5, 3, false], [2, 1, -0.6, 5, 3, false], [2, 1, 0, 0, 0, false], [2, 2, 0.6, 5, 3, true], [0.5, 3, -0.95, -5, 5, false], [3, 0.5, 0.95, 5, -5, true]]) {
    const d = c.compute(Object.assign({}, c.state, { mode: 'read', f: 0, sigma1, sigma2, rho, mu1, mu2, centered }));
    out.t2.grid.push({ sigma1, sigma2, rho, mu1, mu2, centered, shape: d.shape, moved: d.moved, S: d.S, raw: d.raw, mm: d.mm });
  }
}
{
  const { c } = loadComponent(path.join(run, '3', 'Main.dc.html'));
  out.t3 = [];
  for (const [len, theta, x1, x2, phi, l1, l2] of [[2, 0, 1, 0, 90, 1, 1], [1, 0, 1, 0, 60, 1, 1], [1, 30, 1, 3, 90, 1.5, 1], [2, 30, 1, 3, 30, 0.5, 2], [2.5, 175, 4, 4, 150, 2, 2], [0.5, 45, -4, 2.5, 120, 1.2, 0.7]]) {
    const d = c.compute({ len, theta, x1, x2, phi, l1, l2 });
    out.t3.push({ len, theta, x1, x2, phi, l1, l2, one: d.one, two: d.two });
  }
}
fs.writeFileSync(path.join(run, 'dump.json'), JSON.stringify(out));
console.log('dumped');
