# 1104 Explanation Connections Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 1104의 여섯 설명 연결과 신규·수정·lite 작성 및 감사 절차를 보완한다.
**Architecture:** 기존 HTML/MD와 big-picture-first 기준을 사용한다. 감사 근거는 RUN/audit.md에 남기고 새 스키마·검사기는 만들지 않는다.
**Tech Stack:** HTML, Markdown, Python 검증기, 실제 브라우저.
**Spec:** 이 대화에서 승인한 「1104 설명 보완과 재발 방지 설계」 및 선택 1번.

## Global Constraints
- 기존 작업본의 다른 변경, ID·링크·패널·읽음 상태를 보존한다.
- 핵심 연결은 본문에 보이고 단순 산술에는 고정 분량을 강제하지 않는다.
- HTML/MD를 함께 검증한다. 커밋·푸시는 이번 실행에 포함하지 않는다.

## Review Focus
- 검토자가 본문 밖에서 보충한 연산을 기존 정의의 재사용과 구별한다.
- 짧지만 충분한 전개를 결함으로 판정하지 않는다.
- 누락이 없는 구간도 근거와 함께 기록한다.
- 여섯 연결의 수식 차원·곱 순서와 대응 MD가 일치한다.
- 좁은 화면에서 수식이 본문 전체를 밀지 않는다.

### Task 1: 기준 행동과 현 작업본 보존
- [x] RUN에 대상 파일을 백업하고 수정 전 검토 사례를 기록한다.
- [x] 여섯 구간과 기존 정규방정식의 충분한 전개를 대조한다.

### Task 2: 기존 스킬 절차 구체화
- [x] big-picture-first.md에 핵심 전환별 질문·연결 선택·검토 증거 형식을 정의한다.
- [x] content-rules.md, review-prompt.md, ml-note-audit/references/audit-brief.md, SKILL.md에 작성·리뷰·감사 경로를 연결한다.
- [x] 변경 지침으로 누락 사례와 충분한 사례를 다시 검토한다.

### Task 3: 노트와 절차 검증
- [x] 여섯 구간의 HTML/MD와 수식 및 기존 링크·ID를 검증하고 RUN/audit.md에 근거를 기록한다.
- [x] 기존 구조 검사와 관련 테스트를 실행한다.
- [x] 375px/데스크톱과 라이트/다크 화면을 확인한다.
- [x] 변경 전체를 독립 검토하고 결과를 보고한다.

## 실행 결과
기존 작업본에 여섯 연결이 이미 반영되어 있어 내용을 보존하고 검증했다. 스킬 절차 5개 파일을 수정했다. 검사 근거와 제한은 /var/folders/t7/zhvnpb1j4tb2pszpcnhlnt2h0000gn/T/ml1104-connections-r_oodomr/audit.md에 기록했다. 커밋·푸시는 하지 않았다.
