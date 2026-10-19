# 2회 실제 자료 대조
검토자 root, 2026-10-19. 쪽은 PDF 파일 1기준; MML 인쇄쪽은 6을 뺀 값.

과제 PDF 3-9쪽을 실제 렌더링해 확인했다. p1은 P6-P8의 독립/표현을 매개변수에 따른 기저로 확장. p2는 P10-P11의 gradient/Jacobian과 MML PDF159 chain rule을 연결. p3은 P13/P22의 Gaussian/아핀 변환을 새 수치로 구성. p4는 P14/P25의 완전제곱과 Gaussian 곱을 prior-likelihood 곱으로 구성. p5는 P9/P17-P19의 특징/ML/MAP를 중복 행과 제곱 특징으로 변형했다. 원문 전재는 없다.

MML PDF153,159 미분과 Jacobian/chain rule, PDF198/200 중심화 공분산·아핀변환·독립 정의, PDF205 주변 Gaussian, PDF207 곱 정규화, PDF298-300 우도·NLL·정규방정식, PDF307-308 MAP/벌점, PDF312 posterior, PDF314 predictive, PDF318-319 evidence와 직교투영을 직접 읽었다. 핵심 페이지159/200/205/207/318/319 및 과제쪽을 렌더링하여 행렬/분산/정규화 표기를 대조했다. 작업 PNG는 RUN/source-*.jpg 및 mml-detail-*.png.

Lecture04 PDF14 예측의 잡음분산, PDF17 모델 선택, PDF23 투영식을 원문 대조했다. 1019 STT 끝의 약50:50 안내와 직교투영 종료를 다시 읽었다.

p6의 미지분산 공동추정은 수업의 알려진 잡음분산 회귀 공식을 그대로 인용한 것이 아니다. 0909 STT1669-1672에서 평균·분산 두 모수 최적화를 소개하며, Gaussian 밀도/ML와 기초 미분을 사용해 문제 안의 주어진 스칼라 모델에서 새로 유도한다. 양의 분산 경계 문제도 그 우도로 증명한다. p7 비등방 prior, p8 두 미래 관측 공분산, p9 공유/별도 모수 evidence, p10 ridge 비투영은 기존 수업 이론을 연결한 새 응용이다. 교수님이 이 구체 문항들을 예고한 것으로 주장하지 않는다.

1회와 달리 새 질문·추론 요구를 구성했다. 공식 시험 시간·배점은 확인되지 않아 적지 않았다.

생성 PDF 문제10쪽/해설10쪽을 전부 PNG 렌더링해 contact sheets로 확인하고 해설7/10쪽 확대 확인. 표/행렬/질문/답/하단135pt 흰 여백과 필기공간에 잘림·겹침·정답노출 없음. Browser60 viewport-theme-topic 조합 PASS, 외부요청/콘솔/KaTeX/문서넘침0. 51개 추가 구역/요약 캡처와 수식 geometry 후보0, recall/solve/verify/summary 전10문항 시각 확인.

파일명이 다른 Lecture04 원본과 rev_HO를 구별해 최종 references가 가리키는 rev_HO PDF14/17/23을 별도로 다시 읽고 렌더링 대조했다. 23쪽은 일반 부분공간 투영 예제이며 해당 공식을 확인했다.
