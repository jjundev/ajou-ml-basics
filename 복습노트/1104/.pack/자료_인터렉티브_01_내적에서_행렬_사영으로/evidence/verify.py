import json
import math
from fractions import Fraction
import numpy as np

# 1. Exact rational verification (Fraction) for standard basis and Pythagorean identity
def verify_exact_rational():
    for x1, x2 in [(Fraction(3), Fraction(4)), (Fraction(6), Fraction(8))]:
        # Standard basis e1=(1,0), e2=(0,1)
        b1 = (Fraction(1), Fraction(0))
        b2 = (Fraction(0), Fraction(1))
        z1 = b1[0] * x1 + b1[1] * x2
        z2 = b2[0] * x1 + b2[1] * x2
        assert z1 == x1 and z2 == x2
        # 3-4-5 rotated orthonormal basis (3/5, 4/5), (-4/5, 3/5)
        u1 = (Fraction(3, 5), Fraction(4, 5))
        u2 = (Fraction(-4, 5), Fraction(3, 5))
        uz1 = u1[0] * x1 + u1[1] * x2
        uz2 = u2[0] * x1 + u2[1] * x2
        rec_x1 = uz1 * u1[0] + uz2 * u2[0]
        rec_x2 = uz1 * u1[1] + uz2 * u2[1]
        assert rec_x1 == x1 and rec_x2 == x2
        assert uz1 * uz1 + uz2 * uz2 == x1 * x1 + x2 * x2

    # 3D exact rational basis
    X = [Fraction(2), Fraction(3, 2), Fraction(2)]
    x_sq = sum(c * c for c in X)
    assert x_sq == Fraction(41, 4)  # 10.25
    # M = 2 floor plane: proj = (2, 3/2, 0), res = (0, 0, 2)
    assert Fraction(2) ** 2 + Fraction(3, 2) ** 2 == Fraction(25, 4)  # 6.25
    assert Fraction(2) ** 2 == Fraction(4)  # 4.00
    # M = 1 x1-line: proj = (2, 0, 0), res = (0, 3/2, 2)
    assert Fraction(3, 2) ** 2 + Fraction(2) ** 2 == Fraction(25, 4)  # 6.25

# 2. Independent NumPy least-squares (np.linalg.lstsq) verification against STEPS presets
def verify_steps_numpy():
    line_cases = [
        {"theta": 0, "x": [3.0, 4.0], "z1": 3.0, "z2": 4.0, "xSq": 25.0},
        {"theta": 0, "x": [6.0, 8.0], "z1": 6.0, "z2": 8.0, "xSq": 100.0},
        {"theta": 35, "x": [3.0, 4.0], "z1": 4.751761878271159, "z2": 1.555878868102829, "xSq": 25.0},
        {"theta": 55, "x": [3.0, 4.0], "z1": 4.997337486209105, "z2": -0.1631503874627911, "xSq": 25.0},
    ]
    for c in line_cases:
        th = math.radians(c["theta"])
        B_full = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        x = np.array(c["x"])
        # Independent check via matrix solve B_full @ z = x
        z = np.linalg.solve(B_full, x)
        assert np.allclose(B_full.T @ B_full, np.eye(2), atol=1e-12)
        assert np.allclose(z, [c["z1"], c["z2"]], atol=1e-12)
        proj = z[0] * B_full[:, 0]
        res = x - proj
        assert np.allclose(res, z[1] * B_full[:, 1], atol=1e-12)
        assert abs(float(B_full[:, 0] @ res)) < 1e-12
        assert abs(float(np.sum(z ** 2)) - c["xSq"]) < 1e-12

    plane_cases = [
        {"M": 2, "theta": 0, "phi": 0, "X": [2.0, 1.5, 2.0], "errSq": 4.0, "projSq": 6.25},
        {"M": 1, "theta": 0, "phi": 0, "X": [2.0, 1.5, 2.0], "errSq": 6.25, "projSq": 4.0},
        {"M": 2, "theta": 30, "phi": 20, "X": [2.0, 1.5, 2.0], "errSq": 3.1581135040673995, "projSq": 7.0918864959326005},
        {"M": 2, "theta": 60, "phi": 35, "X": [2.0, 1.5, 2.0], "errSq": 4.846977793983499, "projSq": 5.4030222060165},
    ]
    for c in plane_cases:
        th = math.radians(c["theta"])
        ph = math.radians(c["phi"])
        Rz = np.array([[math.cos(th), -math.sin(th), 0.0],
                       [math.sin(th),  math.cos(th), 0.0],
                       [0.0,           0.0,          1.0]])
        Rx = np.array([[1.0, 0.0,           0.0],
                       [0.0, math.cos(ph), -math.sin(ph)],
                       [0.0, math.sin(ph),  math.cos(ph)]])
        R = Rz @ Rx
        assert np.allclose(R.T @ R, np.eye(3), atol=1e-12)
        M = c["M"]
        B = R[:, :M]
        B_perp = R[:, M:]
        x = np.array(c["X"])
        # Independent least-squares solution
        z_ls, _, _, _ = np.linalg.lstsq(B, x, rcond=None)
        z_dot = B.T @ x
        assert np.allclose(z_ls, z_dot, atol=1e-12)
        proj = B @ z_ls
        res = x - proj
        res_perp = B_perp @ (B_perp.T @ x)
        assert np.allclose(res, res_perp, atol=1e-12)
        assert np.allclose(B.T @ res, np.zeros(M), atol=1e-12)
        assert abs(float(np.sum(res ** 2)) - c["errSq"]) < 1e-12
        assert abs(float(np.sum(proj ** 2)) - c["projSq"]) < 1e-12
        assert abs(float(np.sum(proj ** 2) + np.sum(res ** 2)) - float(np.sum(x ** 2))) < 1e-12

if __name__ == "__main__":
    verify_exact_rational()
    verify_steps_numpy()
    print(json.dumps({"ok": True, "rational_cases": 4, "numpy_cases": 8}))
