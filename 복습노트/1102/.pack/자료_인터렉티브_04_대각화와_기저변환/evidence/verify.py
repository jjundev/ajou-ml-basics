import json
import math
import numpy as np

CASES = [
    {"name": "sym_default", "A": [[2.0, 1.0], [1.0, 2.0]], "c": [1.0, 1.0], "lams": [3.0, 1.0], "orth": True},
    {"name": "sym_e1", "A": [[2.0, 1.0], [1.0, 2.0]], "c": [1.0, 0.0], "lams": [3.0, 1.0], "orth": True},
    {"name": "mml_4_11", "A": [[2.5, -1.0], [-1.0, 2.5]], "c": [1.0, -1.0], "lams": [3.5, 1.5], "orth": True},
    {"name": "nonsym", "A": [[2.0, 1.0], [0.0, 1.0]], "c": [1.0, 1.0], "lams": [2.0, 1.0], "orth": False},
]

def null_dir(A, lam):
    r1 = np.array([A[0, 0] - lam, A[0, 1]], dtype=float)
    r2 = np.array([A[1, 0], A[1, 1] - lam], dtype=float)
    r = r1 if np.hypot(*r1) >= np.hypot(*r2) else r2
    n = np.hypot(*r)
    v = np.array([-r[1] / n, r[0] / n], dtype=float)
    if v[0] < -1e-12 or (abs(v[0]) <= 1e-12 and v[1] < 0):
        v = -v
    return v

results = []
for case in CASES:
    A = np.array(case["A"], dtype=float)
    c = np.array(case["c"], dtype=float)
    lams = case["lams"]
    p1 = null_dir(A, lams[0])
    p2 = null_dir(A, lams[1])
    if p1[0] * p2[1] - p1[1] * p2[0] < 0:
        p2 = -p2
    P = np.column_stack([p1, p2])
    Pinv = np.linalg.inv(P)
    D = np.diag(lams)
    # 1. Verify AP = PD
    assert np.allclose(A @ P, P @ D, atol=1e-12)
    # 2. Verify P^-1 A P = D
    assert np.allclose(Pinv @ A @ P, D, atol=1e-12)
    # 3. Verify A = P D P^-1
    assert np.allclose(P @ D @ Pinv, A, atol=1e-12)
    # 4. Verify 3-step vector chain: c -> x = Pc -> Ax -> P^-1 Ax = Dc
    x = P @ c
    Ax = A @ x
    Dc = D @ c
    assert np.allclose(Pinv @ Ax, Dc, atol=1e-12)
    assert np.allclose(Ax, P @ Dc, atol=1e-12)
    # 5. Verify orthogonality
    is_orth = np.allclose(Pinv, P.T, atol=1e-12)
    assert is_orth == case["orth"]
    results.append({
        "name": case["name"],
        "lams": lams,
        "P": P.tolist(),
        "Pinv": Pinv.tolist(),
        "x": x.tolist(),
        "Ax": Ax.tolist(),
        "Dc": Dc.tolist(),
        "orth": bool(is_orth),
        "detA": float(np.linalg.det(A)),
        "prodLams": float(lams[0] * lams[1])
    })

# Defective matrix check: [[1, 1], [0, 1]]
A_def = np.array([[1.0, 1.0], [0.0, 1.0]])
eigvals = np.linalg.eigvals(A_def)
assert np.allclose(eigvals, [1.0, 1.0])
assert np.linalg.matrix_rank(A_def - 1.0 * np.eye(2)) == 1  # nullity = 1 < 2 -> defective

print(json.dumps({"status": "ok", "cases": results}, indent=2))
