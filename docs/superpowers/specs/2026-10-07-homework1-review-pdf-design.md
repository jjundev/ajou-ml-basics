# 과제1 → 복습문제 양식 문제지·해설지 PDF 변환 설계

## Intent
`과제/과제1/26_10_Introduction_to_Machine_Learning_homework1_rev.pdf`의 Problem 1–25를 기존 복습문제 카드 HTML 계약(원문·조건·구할 것·Hint·단계별 풀이·정답)으로 옮기고, `ml-review-pack`의 PDF 빌더로 문제지(`-문제.pdf`)·해설지(`-답안.pdf`) 쌍을 만든다. 페이지 규격·글자 배율·자막 여백 검증은 기존 복습문제와 같다. 완료 = 두 PDF가 `validation.json` `status: validated`, 전체 페이지 PNG 육안 검수 통과, 모든 정답이 Fraction 정답 키와 일치.

Classification: architectural — 현재 빌더는 `복습문제_MMDD_slug.html` 파일명과 `MML Example|Exercise` 출처만 받으므로 새 입력 종류(과제)를 수용해야 한다.

## Behavior when done
- `과제/과제1/과제1_Homework1-문제.pdf`, `과제1_Homework1-답안.pdf`가 생긴다.
- 카드 1개 = Problem 1개, 페이지 머리에 `과제 · P7 · HW1 Problem 7 · 7 / 25`. 긴 문제는 `(계속)` 페이지로 분할된다.
- 문제지: 원문(영어 전문)·조건·구할 것·Hint. 해설지: + 단계별 전체 유도·정답.
- 원 과제의 Hint(P10, 11, 13, 14, 18)는 그대로 옮기고, 나머지는 한 줄 "풀이 방향"을 작성한다.
- 빌드 실패 시 종료코드 1, 공개 폴더 무변경(기존 동작).

## Not in this round
- 과제 MD 파일·정리노트 링크 — 복습팩 전용 산출물.
- 과제2 이후 — 프로필만 만들어 두면 같은 명령으로 재사용.

## Approaches
| Option | Approach | Pro | Con | Chosen |
|---|---|---|---|---|
| A | 빌더에 `--profile review\|homework` 추가 (파일명·출처 정규식, kind 배지, 제목, 출력 접두어) | 템플릿·검증·분할 재사용, 과제2부터 재사용 | 스크립트 4개 수정·테스트 추가 | ✔ |
| B | `복습문제_1019_Homework1.html` + `MML Exercise 1.1`로 위장 | 코드 무수정 | 출처·배지가 거짓 정보 | — |
| C | 별도 HTML→PDF 직접 작성 | 파이프라인 독립 | 측정·자막대·분할 검증 재구현, 양식 드리프트 | — |

## Decisions
| # | Decision | Answer |
|---|---|---|
| 0 | 접근 | A (프로필) |
| 1 | 카드 단위 | 문제 1개 = 카드 1개, 소문항은 ask 안 `<ol>` |
| 2 | 출처 표기 | `HW1 Problem N`, 배지 `과제` |
| 3 | 원문 블록 | 영어 문제 전문 |
| 4 | Hint | 원 Hint 그대로, 없으면 한 줄 작성 |
| 5 | 템플릿 | 수정 없음 (provenance SHA 고정) |
| 6 | 정답 검증 | Fraction 정답 키 + 카드 정답 TeX 토큰 대조 |
| 7 | 산출 위치 | `과제/과제1/` |
| 8 | 페이지 규격 | `video-16x9` [confirmed] |
| 9 | 조건·질문 언어 | 한국어 "~해요" 체 + 영어 원문 블록 [confirmed] |
| 10 | 해설 깊이 | 제출 답안 수준 전체 유도 [confirmed] |

## Addendum (plan 작성 중 발견)
Windows 체크아웃에서 PDF 빌더가 동작하지 않는다.
- `review_pdf_publish.py`가 POSIX 전용 `fcntl`을 import → `build_review_pdf.py` import 실패.
- `core.autocrlf=true`로 텍스트가 CRLF로 체크아웃 → 템플릿 provenance SHA·레이아웃 `source_sha256` 불일치.
기준선: skill 테스트 111개 중 failures 2, errors 6 — 모두 이 두 원인. 결정 #11: `.gitattributes`(`* text=auto eol=lf`) + `msvcrt` 잠금 분기로 해결한 뒤 본 작업을 진행한다.
