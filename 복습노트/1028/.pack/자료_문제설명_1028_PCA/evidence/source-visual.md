# 원문 대조 (source_visual)

MML PDF(교과서/Mathematics_for_Machine_Learning.pdf)를 페이지 이미지(evidence/pages/*.png, 80dpi)와 pdftotext로 확인하고 source.json의 조건·질문·원문 인용과 대조했다.

- p1 Example 10.1 — PDF 324–325(책 318–319), 식 (10.4)–(10.5): 교과서 x=[5,3]^T → 카드 [4,-7]^T 수치 변형, x~=[0,z]^T·0e1+ze2·code z 구조 동일. 원문 인용 "it is sufficient to remember/store the coordinate/code z ..." 일치. (c) span·(d) 차원은 교과서의 U=span[e2], dim(U)=1 진술에 대응.
- p2 Example 3.8 — PDF 85(책 79), Definition 3.9·식 (3.35): 교과서 b=1/√2[1,±1] → 카드 1/5[3,4],1/5[4,-3] 변형. 인용 "form an orthonormal basis since b1^T b2=0 and ||b1||=1=||b2||" 일치. (a) B^TB, (b) 판정은 카드 추가 구성.
- p3 Example 2.20 — PDF 57(책 51), Figure 2.9: 교과서 x=[2,3]^T, b1=[1,-1]^T, b2=[1,1]^T, 좌표 ½[-1,5]^T 확인. 카드는 x만 [5,1]^T로 변경했다고 명시 — 일치. 그림 없음(카드 figures 없음).
- p4 Example 3.4 — PDF 80(책 74), Definition 3.4·식 (3.11)–(3.13): 교과서 A1=[[9,6],[6,5]], A2=[[9,6],[6,3]], x=[2,-3]^T 반례 → 카드 [[4,2],[2,3]], [[4,2],[2,0]], 반례 [1,-2]^T 변형. 인용 "A2 is symmetric but not positive definite because x^T A2 x … can be less than 0" 일치. 카드 조건의 정의(x≠0에서 x^TAx>0)가 Definition 3.4와 일치.
- p5 Exercise 3.5 — PDF 102(책 96): 네 생성 벡터 [0,-1,2,0,2],[1,-3,1,-1,2],[-3,4,1,2,1],[-1,-3,5,0,7], x=[-1,-9,-1,4,1], (a) πU(x), (b) d(x,U) 모두 일치. (c)는 카드 추가 소문항.

결론: 모든 문항 조건·소문항이 원문과 일치하거나 명시된 변형이며 불일치 없음.
