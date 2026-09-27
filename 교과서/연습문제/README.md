# 📚 Mathematics for Machine Learning (MML) Part I 연습문제집

아주대학교 머신러닝기초(정방철 교수님) 부교재인 **《Mathematics for Machine Learning》** (Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong 저)의 **Part I: Mathematical Foundations (수학 기초)** 연습문제(Exercises)를 챕터별로 추출한 문제집 모음입니다.

---

## 📁 파일 목록 및 구성

| 파일명 | 챕터 및 분야 | 문제 수 | 원본 페이지 (책 / PDF) | 추출 페이지 수 |
| :--- | :--- | :---: | :---: | :---: |
| [](Chapter_02_Linear_Algebra_Exercises.pdf) | **Ch 2. Linear Algebra** (선형대수) | 20문항 (2.1 ~ 2.20) | pp. 64-69 (PDF 70-75) | 6 pages |
| [](Chapter_03_Analytic_Geometry_Exercises.pdf) | **Ch 3. Analytic Geometry** (해석기하학) | 10문항 (3.1 ~ 3.10) | pp. 96-97 (PDF 102-103) | 2 pages |
| [](Chapter_04_Matrix_Decompositions_Exercises.pdf) | **Ch 4. Matrix Decompositions** (행렬 분해) | 12문항 (4.1 ~ 4.12) | pp. 137-138 (PDF 143-144) | 2 pages |
| [](Chapter_05_Vector_Calculus_Exercises.pdf) | **Ch 5. Vector Calculus** (벡터 미적분학) | 9문항 (5.1 ~ 5.9) | pp. 170-171 (PDF 176-177) | 2 pages |
| [](Chapter_06_Probability_and_Distributions_Exercises.pdf) | **Ch 6. Probability & Distributions** (확률과 분포) | 13문항 (6.1 ~ 6.13) | pp. 222-224 (PDF 228-230) | 3 pages |
| [](Chapter_07_Continuous_Optimization_Exercises.pdf) | **Ch 7. Continuous Optimization** (연속 최적화) | 11문항 (7.1 ~ 7.11) | pp. 247-248 (PDF 253-254) | 2 pages |
| **[](MML_Part1_All_Exercises.pdf)** | **Part I 전체 연습문제 통합본 (북마크/TOC 포함)** | **총 75문항** | **Part I 전 챕터** | **17 pages** |

---

## 💡 주요 문제 유형 안내

1. **Chapter 2 (선형대수)**
   - 군(Group)의 정의 검증 및 방정식 풀이
   - 연립일차방정식  = b$ 가우스 소거법 풀이 및 해공간
   - 역행렬(^{-1}$) 계산
   - 벡터 집합의 선형 독립/종속 판별
   - 부분공간의 기저(Basis) 및 차원(Dimension), 부분공간 교집합( \cap U_2$) 기저 구하기
   - 기저 변환 행렬($) 및 사영/선형사상 표현 행렬(\Phi$) 계산

2. **Chapter 3 (해석기하학)**
   - 대칭양의정부호 행렬에 의한 내적 정의 확인 및 성질
   - 주어진 내적 하에서의 벡터 노름, 거리, 사잇각($\cos	heta$) 계산
   - 부분공간으로의 정사영($\pi_U(x)$) 및 정사영 오차/거리 계산
   - 그람-슈미트(Gram-Schmidt) 직교화 과정을 통한 정규직교기저(ONB) 구성
   - 2차원/3차원 회전 변환 행렬 계산

3. **Chapter 4 (행렬 분해)**
   - 라플라스 전개 및 사루스 법칙을 통한 행렬식($\det$) 계산
   - 고유값(Eigenvalue)과 고유공간(Eigenspace) 계산
   - 행렬의 대각화 가능성 판별 및 대각화 기저 구성
   - 특이값 분해(SVD:  = U\Sigma V^	op$) 직접 계산 및 Rank-1 최적 근사 행렬 도출

4. **Chapter 5 (벡터 미적분학)**
   - 스칼라/단변수 함수 미분 (시그모이드, 지수, 가우시안 등)
   - 1차/고차 테일러 다항식 전개
   - 다변수 벡터 함수의 야코비안(Jacobian) 행렬 계산
   - 행렬/벡터 연쇄법칙(Matrix Chain Rule) 계산
   - 헤시안(Hessian) 행렬 및 다변수 2차 테일러 전개

5. **Chapter 6 (확률과 분포)**
   - 이산 확률변수의 결합/주변/조건부 확률표 계산
   - 가우시안 혼합 모델(GMM)의 주변분포, 평균, 최빈값, 중앙값 계산
   - 베이즈 정리 응용 사후확률 계산
   - 가우시안 켤레사전분포 및 다변량 가우시안 선형변환 계산

6. **Chapter 7 (연속 최적화)**
   - 3차 다항함수의 정상점(Stationary Points) 극대/극소/안장점 판별
   - 확률적 경사하강법(SGD) 갱신 수식
   - 볼록 집합(Convex Set) 및 볼록 함수(Convex Function) 성질 판정
   - 선형계획법(LP) 수식화 및 라그랑주 쌍대(Dual) 문제 유도
   - 2차계획법(QP) 라그랑주 쌍대 문제 유도
   - 힌지 손실(Hinge Loss) 등의 르장드르-펜첼 볼록 켤레(Convex Conjugate) 계산

---

## 🛠 추출 스크립트 사용법

문제집을 다시 추출하거나 특정 챕터만 선택하여 추출할 경우 아래 스크립트를 사용합니다.
