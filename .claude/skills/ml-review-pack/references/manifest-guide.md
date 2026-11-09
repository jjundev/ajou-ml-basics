# manifest.json 작성 규칙 (메인 에이전트)

manifest는 이번 팩의 계약이다. 작성자, 검사기, 조립기가 모두 이 파일을 기준으로 삼는다.
정본 예시: `tests/fixtures/mini-run/manifest.json`, 실제 규모 예시: `tests/fixtures/manifest-0909-0916.json`.
작성 후 반드시 `python3 <SKILL>/scripts/manifest.py <RUN>/manifest.json` → `OK`.

## 최상위
| 키 | 값 |
|---|---|
| `course` | `"머신러닝기초"` |
| `range` | `"0921"` 또는 `"0921-0923"` (첫 STT–마지막 STT 날짜) |
| `slug` | 이번 범위 대표 강의자료 제목의 영문 밑줄 형태, 예: `"Linear_Regression"`. 두 강의자료에 걸치면 뒤쪽 것 |
| `note_title` | `"<주제> — 5살도 이해하는 정리노트"` |
| `note_subtitle` | `"정방철 교수님 머신러닝기초 · 0921 · 0923 수업 (Lecture02~03, MML 9장)"` 형식 |
| `review_title` | `"복습문제 N선 — <range 물결표기> 수업 범위"` |
| `review_intro` | 인라인 HTML만(`<b>`, `<i>`, `<code>`, `<a>`). 템플릿이 `<p>`로 감싸므로 `<p>`·`<ul>`·`<div>` 같은 블록 태그는 쓰지 않는다. 문제 구성(본문 예제 변형 몇 개, 연습문제 몇 개)과 "먼저 풀어 보고, 막히면 힌트를 열어 보세요"처럼 "~해요" 체 한 문장 안내(이모지 없이) |
| `footer_note` | HTML 허용. `출처: 정방철 교수님 강의자료(LectureXX–YY) · 수업 녹음 전사(MMDD…) · Deisenroth, Faisal, Ong, <i>Mathematics for Machine Learning</i> (2020) N장.` |
| `footer_review` | HTML 허용. `출처: Deisenroth, Faisal, Ong, <i>Mathematics for Machine Learning</i> (Cambridge University Press, 2020). 풀이는 자체 작성이며 수치는 Python으로 검증했습니다.` |
| `sessions` | 날짜별 `{date, stt, summary, slides}` |

## sections / topics
- `big-picture-first.md`에 따라 첫 학습 토픽은 `s0-learning-map` 같은 ID로 학습 목표와 개념 관계를 먼저 제시한다. 기존 큰 그림 토픽이 있으면 그것을 보강한다. 별도 manifest 키를 추가하지 않는다.
- 이 토픽만 `layers: ["formal"]`, `supp: false`로 쓸 수 있다. 기호 사용이 가능하며 eli5·prof 레이어는 요구하지 않는다. 기타 개념 토픽에는 아래 기본 규칙을 적용한다.
- 섹션 id는 `s0`, `s1`, … 순서. 마지막 섹션은 항상 "요약 · 예고"이며 토픽 `s<N>-cheatsheet`, `s<N>-next`, `s<N>-links`를 둔다.
- 섹션은 **개념 순서(슬라이드 로드맵)** 로 묶는다. 날짜는 토픽 태그로만 드러낸다.
- 토픽 id는 `s<n>-<kebab>`(영문 소문자). 토픽 하나 = 슬라이드 1~3장 또는 칠판 유도 하나.
- `short`는 상단 목차 글자(예: `"2 최소제곱"`), `title`은 `"2. 최소제곱법"`.
- `layers`: 개념 토픽은 `["eli5", "formal", "prof"]`. 교수님 발언이 없으면 `prof` 대신 빼되 이유를 보고서 "스킬이 정한 사항"에 적는다. 요약·예고 섹션 토픽은 `[]`.
- `supp`: 요약의 `🕳️ 미룬 유도`를 보충으로 싣는 토픽만 `true`.
- `required_terms`: 토픽당 3~9개. 요약의 **용어·식 목록과 강조 발언**에서 고른다.
  - 식은 작성자가 **공백까지 그대로** 쓸 TeX 문자열이다(예: `"\\boldsymbol{\\theta}_{\\text{ML}}"`).
  - 교수님 비유의 핵심 단어(예: `"김밥"`)를 최소 하나 넣어 교수님 말씀(prof) 레이어 누락을 잡는다.
- `preview_topic`: `s<N>-next`.
- `forbidden_outside_preview`: 슬라이드 대조표에서 "예고만/안 다룸"인 슬라이드의 핵심 용어 3~8개. 본문에 나오면 검사 실패.

## parts / problems
- `parts`: `partA`(교과서 본문 예제 변형), `partB`(교과서 연습문제). 한쪽이 0개면 그 part는 뺀다.
  각 항목은 `{"id": "partA", "title": "A. 교과서 예제 변형", "short": "A 예제"}`처럼 `id`·`title`·`short`가 모두 있어야 한다(`short`는 상단 목차 글자).
- 문제 선별은 `references/problem-selection.md`. 개수 8~12.
- 문제 `id`: `p1`, `p2`, … 빈 번호 없이 순서대로(카드 파일명 `cards/<id>.html`이 된다). `part`: 위 `parts`의 id 중 하나.
- `source`: `"MML Example 9.1"` / `"MML Exercise 6.3"` 정확히 이 형식. 명세표 빈칸을 채운 자작 문제만 `"자작 pN"`(N은 이 문제의 id 번호, `problem-selection.md`의 "자작 문제" 절). `variant`: 본문 예제를 문제로 바꿨으면 `true`, 자작은 `false`.
- `anchor`: 풀이가 기대는 정리노트 토픽 id(카드에 링크로 쓰지는 않는다). `level`: 1~3. `date`: 관련 수업 날짜.
- `terms`: 카드에 반드시 나올 TeX/숫자(정답 포함). **모두 빈 문자열이 아닌 문자열**이다. 숫자도 따옴표로 쓴다(`"0.2"`, `"\\frac{1}{5}"`). `required_terms`, `forbidden_outside_preview`도 같다(`manifest.py`가 검사).
- `answer`: Python으로 계산한 정답 문자열. 계산 예:
  ```bash
  python3 -c "from fractions import Fraction as F; print(F(2,10), F(2+3,10+6))"
  ```
  계산 스크립트를 `<RUN>/answers.py`로 남기고 보고서에 경로를 적는다.

## links
- `href`는 작성자가 `<a href="…">`에 **글자 그대로** 넣을 값이다(검사기가 해당 `topic` 안의 링크와 정확히 비교한다). `%20` 같은 인코딩도 그대로.
- `{"topic": "s<N>-links", "href": "복습문제_<range>_<slug>.html"}`는 항상. 파일명은 `manifest.py`의 `review_name`이 만드는 것과 정확히 같아야 한다.
- 확률 개념(Bayes, prior, MLE/MAP, 조건부확률)이 나오면 추가강의 eli5 링크를 건다:
  `../../강의노트/추가%20강의/eli5_lecture10_statistical_inference_part1.html`, `…lecture11_statistical_inference_part2.html`, `…lecture12_statistical_inference_part3.html`
- 이전 복습팩과 이어지는 개념이면 `../<이전 range>/정리노트_<이전 range>_<slug>.html#<토픽>` 링크를 건다(팩마다 `복습노트/<range>/` 폴더라 한 단계 위로 올라간다). 토픽은 기본 `s<N>-links`, 특정 토픽에 거는 편이 분명하면 그 토픽 id.

## PDF 연결
PDF stage 빌드 후 links 토픽의 links에 `.pack/복습문제_<range>_<slug>-문제.pdf`, `.pack/…-답안.pdf` href(`manifest.pdf_hrefs`)를 추가한다. 기존 review HTML link는 유지한다. PDF가 없던 첫 HTML 검사에는 아직 PDF 링크를 넣지 않는다.
