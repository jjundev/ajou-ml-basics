"""Course convention checks must reject authored column derivatives, not data vectors."""
import importlib.util
from pathlib import Path
import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_vector_derivatives.py'

def checker():
    spec = importlib.util.spec_from_file_location('vector_check', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_text

@pytest.mark.parametrize('text', [
    '<p>Gradient는 열벡터이다.</p>',
    '<p>열 gradient를 구하라.</p>',
    r'<p>$$\nabla q=Ax-b.$$</p>',
    r'<p>$$\nabla_\theta Q=-2\Phi^\top y+2\Phi^\top\Phi\theta.$$</p>',
    r'<p>$$\nabla q=\begin{pmatrix}4x_1+x_2-1\\x_1+2x_2\end{pmatrix}.$$</p>',
    r'<p>$$\nabla_\theta J=\frac{\theta-m_0}{\tau^2}.$$</p>',
])
def test_column_derivative_is_rejected(text):
    assert checker()(text)

@pytest.mark.parametrize('text', [
    r'<p>$x=(x_1,x_2)^\top$는 열벡터이고 gradient는 행벡터예요.</p>',
    r'<p>$$\nabla q=x^\top A-b^\top.$$</p>',
    r'<p>$$\nabla q=\begin{pmatrix}4x_1+x_2-1&x_1+2x_2\end{pmatrix}.$$</p>',
    r'<p>$$\nabla_\theta Q=-2y^\top\Phi+2\theta^\top\Phi^\top\Phi.$$</p>',
    r'<p>$$\nabla_\theta J=\frac{(\theta-m_0)^\top}{\tau^2}.$$</p>',
    r'<p>$J_f=\begin{pmatrix}2x_1&1\\x_2&x_1\end{pmatrix}$; $Ax=b$.</p>',
    r'<p>$$\nabla q=0\quad\Longrightarrow\quad Ax=b.$$</p>',
])
def test_rows_data_vectors_jacobians_and_stationarity_are_allowed(text):
    assert checker()(text) == []
