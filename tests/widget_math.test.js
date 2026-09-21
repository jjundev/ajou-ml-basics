'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const m = require('../scripts/widget_math.js');

const close = (a, b, eps = 1e-9) => assert.ok(Math.abs(a - b) < eps, `${a} !~ ${b}`);

test('polyFeatures builds [1, x, x^2, ...]', () => {
  assert.deepEqual(m.polyFeatures(2, 3), [1, 2, 4, 8]);
});

test('solveLinear solves a 2x2 system', () => {
  const x = m.solveLinear([[2, 1], [1, 3]], [3, 5]);
  close(x[0], 0.8);
  close(x[1], 1.4);
});

test('solveLinear throws on singular matrix', () => {
  assert.throws(() => m.solveLinear([[1, 2], [2, 4]], [1, 2]), /singular/);
});

test('ridgeFit recovers an exact line when lambda = 0', () => {
  const t = m.ridgeFit([0, 1, 2], [1, 3, 5], 1, 0);
  close(t[0], 1);
  close(t[1], 2);
});

test('ridgeFit shrinks parameters toward the origin for huge lambda', () => {
  const t = m.ridgeFit([0, 1, 2], [1, 3, 5], 1, 1e6);
  assert.ok(t.every((v) => Math.abs(v) < 1e-4));
});

test('makeDataset is deterministic per seed', () => {
  assert.deepEqual(m.makeDataset(7).trainY, m.makeDataset(7).trainY);
  assert.notDeepEqual(m.makeDataset(7).trainY, m.makeDataset(8).trainY);
});

test('seed 7 shows overfitting, good fit, underfitting', () => {
  const d = m.makeDataset(7);
  const fit = (deg, lam) => m.ridgeFit(d.trainX, d.trainY, deg, lam);
  const over = fit(9, 0);
  assert.ok(m.mse(over, d.trainX, d.trainY) < 1e-10);
  assert.equal(m.mse(over, d.testX, d.testY).toFixed(3), '0.712');
  assert.equal(m.mse(fit(3, 1e-3), d.testX, d.testY).toFixed(3), '0.109');
  assert.equal(m.mse(fit(1, 0), d.testX, d.testY).toFixed(3), '0.417');
});

test('betaPdf matches closed forms', () => {
  close(m.betaPdf(0.5, 1, 1), 1, 1e-9);
  close(m.betaPdf(0.3, 2, 2), 6 * 0.3 * 0.7, 1e-9);
  assert.equal(m.betaPdf(0, 2, 2), 0);
});

test('coinEstimates reproduces the class coin example', () => {
  const e = m.coinEstimates(10, 2, 4);
  close(e.ml, 0.2);
  close(e.map, 0.3125);
  close(e.pred, 1 / 3);
  const u = m.coinEstimates(10, 2, 1);
  close(u.map, u.ml);
});
