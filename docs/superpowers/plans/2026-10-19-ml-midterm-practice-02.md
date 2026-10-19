# ML Midterm Mock Exam 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox syntax.

**Goal:** 1회와 같은 형식의 새 10문항 모의평가 2회, 문제/해설 PDF와 전 문항 문제설명 HTML을 만든다.
**Architecture:** 1회의 검증된 로컬 어댑터를 2회 폴더로 복사하고 회차 식별자만 조정한다. 공용 생성기와 1회는 보존한다. 검토 승인은 복사하지 않는다.
**Tech Stack:** Python, 기존 course PDF/MPE renderers, local KaTeX, Playwright, SymPy.
**Spec:** 사용자 요청 '커밋하고, 같은 방식으로 2회 문제를 만들어줘' 및 1회 계획의 범위/양식 계약.

## Global Constraints
- 0909–1019 직교투영까지, 과제 변형 5 + 모델 분석 5, 대문항 10개.
- 시간·배점은 지정하지 않음. 실제 출제 확정으로 표현하지 않음.
- Native 실행을 유지. 별도 블라인드 검산과 마지막 새 검토자만 사용.
- OUT=중간고사대비/예상문제_2회; RUN=tmp/ml-midterm-practice-02/native.
- 중간고사 모의평가 2회 문제설명이라는 문서/탭 제목. PDF 기존16:9 양식.

## Review Focus
- 1회 숫자만 바꾼 반복 대신 연쇄미분, 다변량변환, 특징 중복, 분산 추정, 두 관측 evidence, ridge 비투영을 연습.
- Gaussian 둘째 인수는 분산, 모든 역행렬 조건/잡음독립/미래잡음독립을 명시.
- 미지 잡음분산의 잔차0 경계에서는 양의 분산 ML 부재를 정확히 구별.
- 두 미래 관측은 조건부 독립과 사후 주변 독립을 구별.
- 기존 회차의 pass/해시/페이지검사를 새 회차 승인으로 재활용하지 않음.

### Task 1: 출제와 입력 구성
**Files:** OUT/.pack/{blueprint,questions}.json, cards/, tools/, evidence/blind-input.html.
**Interface:** 기존 EXAM/CardProfile/SourcePack 계약 유지; slug=Midterm_Practice_02.
- [x] 새 회차/제목/10문항/5:5/1회와 문제 중복 없음 검사 작성, 초기 실패 확인.
- [x] 관련 과제·교과서·교안 원문을 읽고 실제 PDF 페이지 대조. 출처표 갱신.
- [x] 서로 다른 새 10문항을 저작하고 문제만 블라인드 검산자에게 전달.

### Task 2: 풀이와 검산
**Files:** OUT/.pack/{solutions.json,explanations/,evidence/}.
**Interface:** 7구역 + 모든 solve/verify 소문항; answer-checks.items=pN:part.
- [x] 참고 해설/설명 저작, 정확/상징 계산 검산.
- [x] 별도 블라인드 결과를 전 소문항 대조하고 충돌을 해결.
- [x] 기존 구조·출처·정답누출 검사 통과.

### Task 3: PDF와 설명 제작
**Files:** OUT/HTML2개, PDF2개, .pack/설명MD 및 소유자료.
**Interface:** build_base/build_explain API 그대로; 새 검토는 not_run.
- [x] 고정 템플릿 해시 확인 후 PDF 생성, 전쪽 PNG 시각 검수.
- [x] 설명 생성 후 모든10문항×3화면×2테마 브라우저/동작 검사, 화면 시각 검수.
- [x] 새 최종 검토자에게 내용·답·출처·회차·레이아웃 검토 요청. 중요한 결함 수정·회귀검사.

### Task 4: 발행과 전달
**Files:** .pack/제작검증.md, delivery.json, 검토/해시.
- [x] 실제 원문/내용/독립/브라우저 검토 승인 후 기존 publish API 사용.
- [x] 최신 해시·링크·PDF·검토 검증 및 좁은 테스트 통과.
- [x] 커밋1회 식별자와 2회 세 파일 링크 제공. 2회는 이번 요청의 '커밋하고 다음 만들기' 순서에 따라 미커밋으로 남김.

## 실행 판단
이번 요청은 승인된 1회 방식의 후속 회차 제작이므로 설계 재승인을 요청하지 않고 실행한다. 이미 분리된 codex/ml-midterm-practice 브랜치와 고유 OUT/RUN을 사용한다. 신규 기능보다 저작 중심이므로 기존 생성기 테스트를 재사용하고 회차/중복 회귀검사만 추가한다.

## 실행 결과
1회 a89fdf9 커밋 완료. 2회 PDF 각10쪽과10문항31소문항 HTML/MD 발행. 독립검산31, 정확/상징검산28, 실브라우저60조합, 추가51캡처, PDF20쪽 시각검수, 좁은 테스트12개 PASS. 최종 검토 Critical0/Important0/Minor1. Minor는6번 독자용 출처 연결 설명 권고이며 제작검증에 상세 근거를 남기고 조각 수정은 보류. 새2회와이계획은미커밋.
