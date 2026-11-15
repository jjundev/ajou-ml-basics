from decimal import Decimal
from math import sqrt

import numpy as np


atol = 1e-12

# P4, P7, and P8: check candidates derived from the original problem.
for label, a, expected_u, expected_s, expected_v in [
    (
        "P4",
        [[1, 1, 0], [0, 1, 1]],
        np.array([[1, 1], [1, -1]]) / sqrt(2),
        [[sqrt(3), 0, 0], [0, 1, 0]],
        np.array([[1, 1, 1], [2, 0, -1], [1, -1, 1]]) / [sqrt(6), sqrt(2), sqrt(3)],
    ),
    (
        "P7",
        [[3, 2, 2], [2, 3, -2]],
        np.array([[1, 1], [1, -1]]) / sqrt(2),
        [[5, 0, 0], [0, 3, 0]],
        np.array([[1, 1, 2], [1, -1, -2], [0, 4, -1]]) / [sqrt(2), 3 * sqrt(2), 3],
    ),
    (
        "P8",
        [[2, 2], [-1, 1]],
        np.eye(2),
        [[2 * sqrt(2), 0], [0, sqrt(2)]],
        np.array([[1, -1], [1, 1]]) / sqrt(2),
    ),
]:
    u, s, v = (np.array(m) for m in (expected_u, expected_s, expected_v))
    a = np.array(a)
    np.testing.assert_allclose(u.T @ u, np.eye(u.shape[0]), atol=atol, rtol=0)
    np.testing.assert_allclose(v.T @ v, np.eye(v.shape[0]), atol=atol, rtol=0)
    np.testing.assert_allclose(a @ v, u @ s, atol=atol, rtol=0)
    np.testing.assert_allclose(a.T @ a @ v, v @ s.T @ s, atol=atol, rtol=0)
    np.testing.assert_allclose(a @ a.T @ u, u @ s @ s.T, atol=atol, rtol=0)
    infinity_residual = np.abs(u @ s @ v.T - a).max()
    assert infinity_residual < atol
    print(f"{label} max entrywise SVD residual: {infinity_residual:.3g}")


# P5: use the rounded display and independently recompute from the rating table.
def decimal_tuple(values):
    return tuple(Decimal(value) for value in values.split())


ratings = np.array([[5, 4, 1], [5, 5, 0], [0, 0, 5], [1, 0, 4]])
u1_print = decimal_tuple("-0.6710 -0.7197 -0.0939 -0.1515")
u2_print = decimal_tuple("0.0236 0.2054 -0.7705 -0.6030")
layer1 = tuple(Decimal("9.6438") * u * Decimal("-0.1811") for u in u1_print)
layer2 = tuple(Decimal("6.3639") * u * Decimal("-0.9807") for u in u2_print)
rank2_print = tuple(a + b for a, b in zip(layer1, layer2))
print("P5 (rounded input) layer 1:", *(str(x) for x in layer1))
print("P5 (rounded input) layer 2:", *(str(x) for x in layer2))
print("P5 (rounded input) rank 2:", *(str(x) for x in rank2_print))
print("P5 (rounded input) column delta:", *(str(x - int(y)) for x, y in zip(rank2_print, ratings[:, -1])))

u, s, vt = np.linalg.svd(ratings, full_matrices=False)
exact_layer1 = s[0] * u[:, 0] * vt[0, -1]
rank2 = (u[:, :2] * s[:2]) @ vt[:2]
rank2_col = rank2[:, -1]
print("P5 full precision SVD singular values:", s)
print("P5 full precision SVD layer 1:", exact_layer1)
print("P5 full precision SVD rank-2 column:", rank2_col)
print("P5 full precision SVD rank-2 column delta:", rank2_col - ratings[:, -1])
print("P5 maximum first layer column input rounding drift:", np.abs(np.array(layer1, dtype=float) - exact_layer1).max())
print("P5 maximum rank-2 column input rounding drift:", np.abs(np.array(rank2_print, dtype=float) - rank2_col).max())
print("P5 discarded Frobenius norm, squared norm, energy fraction:", s[2], s[2]**2, s[2]**2 / (s @ s))
print("P5 ratio of sigma_3 to sigma_2:", s[2] / s[1])
np.testing.assert_allclose(s, [9.6438, 6.3639, 0.7056], atol=5e-5, rtol=0)
assert np.abs(np.array(layer1, dtype=float) - exact_layer1).max() < 1e-3
assert np.abs(np.array(rank2_print, dtype=float) - rank2_col).max() < 1e-3
np.testing.assert_allclose(np.linalg.norm(ratings - rank2), s[2], atol=atol, rtol=0)


# P9: evaluate with exact integers after multiplying through by two.
a = np.array([[3, 2, 2], [2, 3, -2]])
rank1_twice = np.array([[5, 5, 0], [5, 5, 0]])
residual_twice = 2 * a - rank1_twice
assert (residual_twice**2).sum() == 4 * 9
print("P9 residual times two:", residual_twice.tolist(), "squared Frobenius norm:", (residual_twice**2).sum() / 4)
