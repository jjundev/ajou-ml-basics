# ML Problem Panel Tabs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Native inline implementation; one fresh whole-change reviewer at the end.

**Goal:** 모의평가 1·2회 문제 패널에 출제 근거·용어 탭을 추가하고 현재 HTML 및 재생성 경로에 반영한다.
**Architecture:** 기존 일곱 해설 구역은 보존한다. 설명 조각의 선택적 `data-problem-panel="provenance|terms"` 영역을 공통 템플릿이 현재 문항의 탭으로 옮긴다. 하나의 탭 작업영역을 데스크톱 문제 패널과 모바일 펼침 사이에서 옮겨 상태·수식·접근성을 보존한다.
**Tech Stack:** Python, offline HTML/CSS/JavaScript, local KaTeX, pytest, Playwright.
**Spec:** 직전 채팅의 승인된 grill-yourself 설계와 사용자 Native 실행 지시.

## Global Constraints
- 대상은 중간고사대비/예상문제_{1,2}회 문제설명 HTML/MD와 소유 자료. 문제·해설 PDF, 원 문제, 수학 풀이·답은 변경하지 않는다.
- 탭 순서 문제→원문(있을 때만)→출제 근거→용어. 기본 문제, 문항 전환 시 선택 유지.
- 출제 근거 기존 문장을 전용 탭으로 이동. 각 문항 해설에서 쓰는 용어를 뜻·기호/정의·역할 순서로 작성하며 계산 정답을 넣지 않는다.
- 공통 생성기/템플릿 수정; 다른 기존 발행 HTML은 재생성하지 않는다. 외부 요청 없음.
- 기존 codex/ml-midterm-practice에서 이어 작업. 새 커밋·푸시는 하지 않는다.

## Review Focus
- 원문 있는 문항과 없는 문항 사이 전환, 자료 없는 이전 형식 문항의 빈 상태, 저장된 탭과 초점.
- 375/1024/1280px, light/dark, 좁은 부동 패널에서 탭·위치 버튼 겹침과 가로 넘침.
- 모바일 펼침/접힘·화면 경계 전환·인쇄 후 모든 문항의 조건/원문/메타데이터 보존.
- 문항별 출제 근거와 용어가 다른 문항 내용으로 남거나 계산 정답을 노출하지 않는가.
- 메타데이터가 입력 해시·검증·HTML/MD 재생성에 포함되는가.

### Task 1: 탭 작업영역 및 메타데이터 계약
**Files:** .agents/skills/ml-problem-explain/assets/note-template.html; scripts/mpe_contract.py; tests/test_problem_panels.py.
**Interfaces:** optional direct fragment blocks `data-problem-panel="provenance|terms"`; no changes to Problem or SourcePack.
- [x] 실제 생성물 브라우저 테스트: 두 문항의 탭 이동·문항 전환·누락 안내·모바일·인쇄 보존을 RED로 확인.
- [x] 선택적 메타데이터 검증과 공유 탭 작업영역 구현. 기존 탭 키/패널 배치 지원.
- [x] 새 테스트 GREEN, 공통 스킬 전체 pytest 실행.
Expected: no stale/missing tabs; existing browser and source preservation tests pass.

### Task 2: 20문항 저작과 HTML 재발행
**Files:** 두 OUT/.pack/explanations/*.html; .pack/panel-content.json; 문제설명 HTML/MD 및 생성 자료; 검증 기록.
**Interfaces:** Task1 optional metadata; existing build_explain/check/publish APIs and current hashes.
- [x] 기존 출제 근거를 별도 영역으로 이동하고 문항별 용어 작성. 일곱 해설 구역은 출제 근거 제거 외 바이트 보존.
- [x] 새 stage 생성. 기존 답 검산을 재실행하고 보존 비교, 메타데이터의 의미·근거 검토.
- [x] 20문항×3화면×2테마 탭 동작/오류 검사, 실제 스크린샷 점검 및 별도 최종 검토.
- [x] 현재 근거·산출 해시로 실제 검토 승인 후 발행. PDF/원 문제 바이트 보존, 양쪽 check_exam 및 테스트 통과.
Expected: both delivered HTMLs contain working tabs; source/PDF unchanged; checks pass.

## 실행 결과
1회62·2회61용어,20근거문단을 전용 탭으로 이동. Native 직접구현+새 전체검토 후 초점회귀수정과 이차형식표현수정. 신규6테스트·회차별13+12테스트 통과; 공통117통과/기존4실패(HEAD동일). Chrome120조합/360탭상태/110스크린샷, 발행해시와 실제열람 확인. 원 문제·PDF4개·풀이/답 보존. 이번 변경 커밋·푸시 없음.

## 사용자 간격 핫픽스
커밋 직전 피드백 반영: 탭 간격12px, 위아래패딩12/16px·높이56px, 제목뒤16px·탭아래24px, 모바일내부16px. 공통템플릿과두HTML재생성. 현재120화면조합재검수 및18레이아웃/패널회귀통과. 문항/설명/PDF내용변경없음.
