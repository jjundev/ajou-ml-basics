# ML Midterm Derivation Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Native inline authoring, one fresh blind check and one final whole-change review.

**Goal:** 두 회차 6–10번을 소문항별 강의 공식 유도형으로 수정하고 PDF 4개와 문제설명 HTML 2개에 반영한다.
**Architecture:** 기존 회차의 저작 JSON/cards/explanations와 로컬 PDF/MPE 생성기를 재사용한다. 수정 전 전체 팩을 RUN에 백업하며 검증되지 않은 결과는 최종 전달하지 않는다.
**Tech Stack:** Python, existing PDF/MPE renderers, local KaTeX, Playwright, SymPy.
**Spec:** 직전 채팅의 승인된 grill-yourself 설계와 사용자 “진행해줘. native로 1·2회 모두 수정…” 요청.

## Global Constraints
- 범위 시작–1019, 대문항 각10개, 과제 변형5+모델 분석5. 1–5는 보존하고 연결·조건을 점검.
- 각6–10에4–6 소문항. 앞 결과가 다음 단계에 쓰이며 최종 공식을 조건에 미리 주지 않음.
- 2회6번 미지분산 문항을 알려진 분산의 스칼라 회귀 ML 유도로 교체.
- 이름/양식/16:9 PDF 템플릿 유지. 가독성을 위한 계속 페이지 허용. 배점·시간 추가 없음.
- Native, 현재 codex/ml-midterm-practice에서 사용자 기존 작업을 이어감. 커밋/푸시 없음.
- OUT=중간고사대비/예상문제_{1,2}회; RUN=tmp/ml-midterm-derivation/native.

## Review Focus
- 이름만 유도로 바꾸거나 첫 소문항에 여러 유도를 몰아넣지 않았는가.
- posterior/evidence 공식 대입으로 도출을 우회하거나 P/H를 조건에서 제공하지 않았는가.
- 새 소문항의 모든 조건·차원·정규화·역행렬 조건과 논증이 맞는가.
- 문제/해설/HTML/MD의 소문항 정합성과 새 해시 검토가 확보되는가.
- 길어진 유도에서 PDF 계속 페이지 및 모바일 수식이 잘리지 않는가.

### Task 1: 저작 입력·유도 연결 수정
**Files:** 각 OUT/.pack/{questions,solutions,blueprint}.json, cards/, explanations/, evidence/derivation-map.json.
**Interfaces:** 기존 EXAM/SourcePack 계약; subparts a–f, solve/verify 모든 키 일치.
- [x] 기존 입력에서 단계 분리·우회 금지 수용검사 실패 확인 (구조 증거만, 의미 검증 아님).
- [x] 10개 모델 분석 문항의 질문/해설/설명과 근거를 수정; first5 동일 확인.
- [x] 새 문제만으로 별도 블라인드 검산, 전 소문항 비교; 정확/상징 검산과 실제 원문 대조.
Expected: all authored subparts agree; no unresolved math ambiguity.

### Task 2: PDF/HTML 생성과 실제 검수
**Files:** 각 OUT/HTML2개, PDF2개, .pack/설명MD와 소유자료, evidence.
**Interfaces:** 기존 build_base/build_explain와 browser_check; 매번 새 리뷰 not_run.
- [x] 고정 템플릿 확인/PDF marker 후 PDF4개 생성. 모든 페이지 렌더·시각 검사.
- [x] 설명 생성, 각10문항×3화면×2테마 브라우저/패널 검사 및 소문항 시각 검수.
- [x] Native 마지막 새 검토자에게 전체 변경 검토; Critical/Important 한 번 수정.
Expected: current-source PDFs and HTML, no render/math/console/overflow defects.

### Task 3: 검증 기록·발행·전달
**Files:** 각 OUT/.pack/제작검증.md, delivery.json, evidence, owned validation/manifest.
- [x] 실제 수행한4검토와 새 참조/산출 해시로 승인하고 기존 publish API 사용.
- [x] 양쪽 좁은 테스트/check_exam.py/소문항·파일 정합성 확인.
- [x] 새 파일 링크와 핵심변경/검증결과 전달. 커밋하지 않음.
Expected: both check_exam.py pass; changed paths only packs and this plan.

## 실행 결과
1회42·2회44소문항, 모델분석10문항 유도사슬 개정. 문제/해설 PDF 각10쪽(총40), 설명 HTML/MD 갱신. 독립86소문항 대조일치, root정확/상징56검사, 브라우저120조합, 테스트25개 통과. fresh 최종검토 Critical0/Important0/Minor2(표현개선,검증기록에 미반영 명시). 양쪽 check_exam PASS, scoped diff whitespace검사 통과. 커밋·푸시 없음.
