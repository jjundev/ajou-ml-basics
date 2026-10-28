# 1028 PCA 독립 검산

1. 블라인드 검산자(별도 서브에이전트): 입력은 evidence/problem-data-only.json(문제 조건·질문만)과 MML 이론 페이지. 참고 풀이·설명 조각·정답 파일 열람 금지. 결과 evidence/blind/blind_check.py, blind_results.txt. 투영은 두 방법(정규방정식, Gram-Schmidt/가중 단일 사영 합)으로 일치.
2. 저작자 검산: evidence/independent_1028.py -> independent_results.json (sympy 정확 유리수). p3는 RREF 피벗으로 기저 선택 후 정규방정식 + Gram-Schmidt QQ^T x 두 경로, p4는 A-정규방정식 + 거리 제곱 완전제곱(미분 미사용) 두 경로.
3. evidence/independent/blind_solve.py, blind_solve.txt: 이 작업 시작 전에 RUN에 이미 있던 별도 블라인드 풀이(작성 주체 미확인). 결과는 위 두 검산과 동일하며, p3 영공간 [-1,-2,-1,1]로 u4=u1+2u2+u3를 확인.

| item | 블라인드 | 저작자 검산 | 참고 답 | 결론 |
|---|---|---|---|---|
| p1:a | 4e1-7e2 | 4,-7 | 4e1-7e2 | 일치 |
| p1:b | 0e1+ze2, z만 저장 | code z | 동일 | 일치 |
| p1:c | span[e2], dim 1 | rank 1 | 동일 | 일치 |
| p2:main | 점곱 0, 길이 1,1, det -1 | 동일, B^TB=I | 동일 | 일치 |
| p3:a | [1,-5,-1,-2,3], λ=(-3,4,1) | 동일(두 경로) | 동일 | 일치 |
| p3:b | 2sqrt15 | d^2=60 | sqrt60=2sqrt15 | 일치 |
| p4:a | [1/2,0,-1/2] | 동일(두 경로) | 동일 | 일치 |
| p4:b | 1 | r^TAr=1 | 1 | 일치 |

참고: 블라인드 검산자의 서술 메모 "v4 = 2v1 + v2"는 오기다(2u1+u2=[1,-5,5,-1,6]≠u4). 그 스크립트의 계산 결과(rank 3, 잔차가 네 생성 벡터와 직교)는 맞고, 올바른 관계 u4=u1+2u2+u3는 sympy solve(independent_results.json u4_in_terms_of_u1u2u3=[1,2,1])와 기존 blind_solve.txt 영공간으로 확인했다. 답 충돌이 아니므로 disputed 아님.
p2는 증명형: 정의의 모든 조건(직교·정규·일차독립·차원)을 정확 계산으로 확인했으며 숫자 예시로 대체하지 않았다.
