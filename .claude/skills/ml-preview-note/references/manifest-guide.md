# 예습노트 manifest.json 작성 규칙 (메인 에이전트)

manifest는 이번 예습노트의 계약이다. 작성자, 검사기, 조립기가 모두 이 파일을 기준으로 삼는다.
정본 예시: `tests/fixtures/mini-run/manifest.json`.
작성 후 반드시 `python3 <SKILL>/scripts/preview_manifest.py <RUN>/manifest.json` → `OK`.

## 최상위
| 키 | 값 |
|---|---|
| `course` | `"머신러닝기초"` |
| `lecture` | `"L04"` (`pick` 출력 첫 칸) |
| `slug` | `pick` 출력 셋째 칸(예: `"Linear_Regression_Part1"`) |
| `pdf` | 저장소 기준 PDF 경로(예: `"강의노트/Lecture03_Linear_Regression_Part1_rev.pdf"`) |
| `note_title` | `"<주제> — 수업 전에 보는 예습노트"` |
| `note_subtitle` | `"정방철 교수님 머신러닝기초 · Lecture04 <영문 제목> 예습 (MML N장)"` 형식 |
| `footer_note` | HTML 허용. `출처: 정방철 교수님 강의자료(LectureXX) · Deisenroth, Faisal, Ong, <i>Mathematics for Machine Learning</i> (2020) N장. 수업 전에 만든 노트라 수업 내용과 다를 수 있어요.` |
| `sections`, `links` | 아래 |

## sections / topics
- 섹션 id는 `s0`, `s1`, … 순서(검사기가 강제). `s0`은 "0. 미리 알아둘 것", 마지막 섹션은 "N. 한눈에 보기"이며 토픽 `s<N>-cheatsheet`, `s<N>-links`를 둔다.
- 가운데 섹션은 **슬라이드 순서**대로 묶는다(슬라이드 목차·소제목 단위). 토픽 id는 `s<n>-<kebab>`(영문 소문자), 섹션 id로 시작.
- 토픽 하나 = 슬라이드 1~3장. `slides`는 `"s7"` 또는 `"s7–9"`(en dash). 표지·목차·빈 슬라이드는 빼고 보고서에 적는다. 요약 섹션 토픽은 `""`. `s0`(미리 알아둘 것) 토픽은 슬라이드가 아니라 선수 개념이므로 기본 `""`로 두고, 그 개념이 처음 쓰이는 슬라이드가 분명할 때만 그 번호를 쓴다.
- `short`는 상단 목차 글자(예: `"2 최소제곱"`), `title`은 `"2. 최소제곱법"`.
- `layers`
  - 개념 토픽: `["eli5", "formal", "listen"]`. 들을 거리가 없는 토픽(정의만 있는 짧은 슬라이드)은 `["eli5", "formal"]`.
  - `s0` 토픽: `["eli5", "formal"]`.
  - 요약 섹션 토픽: `[]`.
- `supp`: 슬라이드만으로는 식이 이해되지 않아 교과서 설명을 덧붙이는 토픽만 `true`. 요약 토픽은 항상 `false`.
- `required_terms`: 토픽당 2~6개, **슬라이드에 나오는** 핵심 용어·식. 식은 작성자가 공백까지 그대로 쓸 TeX 문자열(예: `"\\boldsymbol{\\theta}^{*}"`). 빈 문자열 금지. 요약 토픽은 치트시트에 넣을 식 몇 개 또는 `[]`.

## links
- `href`는 작성자가 `<a href="…">`에 **글자 그대로** 넣을 값이다(검사기가 해당 토픽 안의 링크와 정확히 비교하고, 파일이 실제로 있는지도 본다). 출력 폴더가 `예습노트/<Lxx>/`라 저장소 파일은 `../../`로 시작한다.
- MML 쪽: `{"topic": "s<N>-links", "href": "../../교과서/Mathematics_for_Machine_Learning.pdf#page=<쪽>"}` (1단계 3의 숫자).
- 선수 개념이 이전 복습노트에 있으면 `s0` 토픽에 `../../복습노트/<range>/정리노트_<range>_<slug>.html#<토픽 id>`.
- 확률 개념(Bayes, prior, MLE/MAP, 조건부확률)이 나오면 `../../강의노트/추가%20강의/eli5_lecture10_statistical_inference_part1.html`(part2·3은 `lecture11_…part2`, `lecture12_…part3`).
