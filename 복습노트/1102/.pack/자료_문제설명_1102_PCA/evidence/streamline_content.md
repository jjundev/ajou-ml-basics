# 1102 PCA 문제설명 축약본 내용·구조·독립 검산 대조

- 대상: `explanations/p1.html`~`p10.html`, 조립된 stage HTML (`문제설명_1102_PCA.html`) 및 동반 Markdown (`.pack/문제설명_1102_PCA.md`).
- 원천 대조(`source_visual`): `복습노트/1102/복습문제_1102_PCA-문제.pdf`(10쪽, SHA-256 `11abe1c6d3ab5b192efbfd8d0b62a5ba69763fdce46feaad47ba28f2382567bf`) 전 10쪽을 `pdftoppm` 이미지 및 `pdftotext`로 시각 대조하고 `source.json`의 조건·질문·소문항과 일치함을 확인.
- 벡터 미분 검사: `check_vector_derivatives.py` 실행 결과 10개 조각 모두 `pass` (`errors: []`, `evidence/check_vector_derivatives.txt`). 본 팩 10문항은 고윳값·고유공간·Gram-Schmidt·대각화·가역성 문항으로 미분 문항이 없음.
- 독립 검산(`independent`): `evidence/check_independent.py` (SymPy 정수/유리수/근호 정확 검산, 10문항 32소문항 pass), `evidence/author_check.py` (32/32 pass), 및 `p8:d`의 `[1,-1,0,0]^T` 기준 $\mathbf{P}$ 행렬식 `det(P) = -1 != 0`, `P^-1 A2 P = diag(1,0,0,0)` 정확 검산 통과.

## 문항·소문항별 내용 대조 요약 (32 소문항)

| 문항 | 소문항 | 구조·유형 | 최종 답·검산·요약·용어·MD 일치 |
|---|---|---|---|
| p1 | a,b,c,d | (b),(c) `ol.deriv`; (a),(d) 단답 | `det(A-λI)=0` 모순 논증, `λ=6,1`, `E_6=span[[4,1]^T]`, `E_1=span[[1,-1]^T]`, 점곱 `3!=0` 비직교. `final-answer`·`verify`·`sum`·`terms`·MD 일치. |
| p2 | a,b,c | (a),(b) `ol.deriv`; (c) 단답 | `λ=3` (2번 겹침), `E_3=span[[1,0]^T]`, `dim E_3=1`. `final-answer`·`verify`·`sum`·`terms`·MD 일치. |
| p3 | a,b,c,d | (a)-(d) `ol.deriv` | `x_1=[-1,1,0]^T`, `x_2=[-1,0,1]^T`, `x_3=[1,1,1]^T`, 점곱 `0,0,1`, `c=1/2`, `x_2'=[-1/2,-1/2,1]^T`, 상호 직교 확인. `final-answer`·`verify`·`sum`·`terms`·MD 일치. |
| p4 | a,b,c,d | (a)-(d) `ol.deriv` | `λ_1=4, λ_2=3`, `p_1=(1/√2)[1,-1]^T`, `p_2=(1/√2)[1,1]^T`, `P^T P=I => P^-1=P^T`, `A=PDP^T` (`D=diag(4,3)`). `final-answer`·`verify`·`sum`·`terms`·MD 일치. |
| p5 | a,b | (a) `ol.deriv`; (b) 단답 | 1행 여인수 전개 `det(A)=4-24+20=0`, 비영 해 존재로 세 열 일차종속. `final-answer`·`verify`·`sum`·`terms`·MD 일치. |
| p6 | a,b,c | (a),(b) `ol.deriv`; (c) 단답 | `E_1(A)=span[[0,1]^T]`, `E_2(B)=span[[1,2]^T]`, `E_-3(B)=span[[-2,1]^T]`, 점곱 `0` 직교. `final-answer`·`verify`·`sum`·`terms`·MD 일치. |
| p7 | a,b | (a) 목록; (b) `table-wrap` 표 | 대각화 가능 `M_1,M_2` / 불가 `M_3,M_4`; 가역 `M_1,M_3` / 비가역 `M_2,M_4` (det `1,0,1,0`). `final-answer`·`verify`·`sum`·`terms`·MD 일치. |
| p8 | a,b,c,d | (a),(c) `ol.deriv`; (b),(d) 단답 | `A_1`: `E_1,E_5` 차원 합 `2<3` 불가; `A_2`: `E_0`(3차원), `E_1`(1차원) 합 `4=4` 가능 (`det P=-1!=0`). `final-answer`·`verify`·`sum`·`terms`·MD 일치. |
| p9 | a,b,c | (b) `ol.deriv`; (a),(c) 단답 | `A_1` 판별식 `-16<0` 실수 대각화 불가; `A_2`: `E_1=span[[3,-1,3]^T]`, `E_2=span[[2,1,0]^T,[2,0,1]^T]`, `D=diag(1,2,2)`, `det P=-1!=0`. `final-answer`·`verify`·`sum`·`terms`·MD 일치. |
| p10 | a,b,c | (a)-(c) `ol.deriv` | 왼쪽 `A`,`A^T` 곱과 결합법칙 증명, `λ!=0` 귀류법으로 `Ax!=0`, `A^T u!=0` 증명, `A=[1,0]` 반례. `final-answer`·`verify`·`sum`·`terms`·MD 일치. |
