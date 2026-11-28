# 독립 검산 대조 (review-1028-PCA)

## 1. 독립 검산 실행 파일
- `evidence/independent_1028.py` → `evidence/independent_results.json` (SymPy 정확 연산)
- `evidence/blind/blind_check.py` → `evidence/blind/blind_results.txt` (별도 SymPy 블라인드 검산)
- `evidence/independent/blind_solve.py` → `evidence/independent/blind_solve.txt`

## 2. 축약된 최종 답 및 핵심 중간식 대조
- `p1:a`: `x=4e1-7e2` — SymPy 일치.
- `p1:b`: `x~=0e1+ze2`, `e2^T e2=1`, `z=e2^T x~`, `e2 z=x~` — SymPy 일치.
- `p1:c`: `U=span[e2]` — 양방향 포함 및 닫힘·`e1∉U` 확인.
- `p1:d`: `dim(U)=1` — `rank([e2])=1` 일치.
- `p2:a`: `B^T B = I` — 분수 정확 연산 일치.
- `p2:b`: `B^T B == I`, `rank(B)=2` → 정규직교 기저 일치.
- `p3:a`: 좌표 `[2,3]^T` — `B3.solve(x3)=[2,3]`, `(B^TB)^{-1}B^Tx=[2,3]` 일치.
- `p3:b`: `||b1||=||b2||=sqrt(2)` → 정규화 아님 일치.
- `p4:a`: `x^T A1 x = (2x1+x2)^2 + 2x2^2`, 제곱합=0 ⇔ `x=0` → 양의 정부호 일치.
- `p4:b`: `x^T A2 x = (2x1+x2)^2 - x2^2`, `x=[1,-2]^T`에서 `-4<0` (블라인드 `[-1,2]^T`도 이차형식 대칭으로 `-4`) → 양의 정부호 아님 일치.
- `p5:a`: `u4=u1+2u2+u3`, `rank=3`, `λ=(-3,4,1)`, `π_U(x)=[1,-5,-1,-2,3]^T` (4열 pinv 사영자와 동일) — 일치.
- `p5:b`: `r=[-2,-4,0,6,-2]^T`, `||r||^2=60`, `d=2*sqrt(15)`, `100=40+60` — 일치.
- `p5:c`: `r·u_i = 0` (`i=1..4`) — 일치.
