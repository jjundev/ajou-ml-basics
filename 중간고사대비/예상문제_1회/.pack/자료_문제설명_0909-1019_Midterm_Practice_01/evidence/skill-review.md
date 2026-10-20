# 행벡터 미분 관례 스킬 수정·검증

작성일: 2026-10-20 (Asia/Seoul)

## 범위와 근거

- 승인 범위: 예상문제 1회의 문제·해설·PDF 행 관례 전환과 재발 방지. 이 기록의 구현 범위는 ml-review-pack/ml-problem-explain 스킬 문서와 공통 reference다.
- 실제 원본은 `.claude/skills/`이며 `.agents/skills/` 두 경로는 해당 원본을 가리키는 SymbolicLink임을 Get-Item으로 확인했다. 링크 쪽을 별도로 수정하지 않았다.
- `writing-skills`와 배경 `test-driven-development`를 읽고 기존 누락 경로 baseline → 공통 참조·작성 계약 수정 → 새 지침 application scenario → 발견한 충돌 보완·재검증 순서로 수행했다.
- 변경 성격은 조건별 수학 reference와 작성·검토 결과의 필수 항목이다. 자유로운 산문 출력 모양을 조절하는 문구 실험이 아니므로 behavior-shaping 5회 wording micro-test는 적용하지 않았다. 아래 실제 압박·원문 보존·권한 경계 시나리오를 수동 검토했다. 통계적 반복 실험을 수행했다고 주장하지 않는다.

## RED: 기존 작성자 브리프 누락 경로

`baseline_probe`는 수정 전 card-rules/authoring 두 파일만 읽도록 하여 작성자에게 직접 전달되는 브리프 경로를 검사했다. 기존 card-rules 끝에는 content-rules의 수식 규칙 참조가 있으나 필수 읽기 목록에는 그 파일/관례가 직접 전달되지 않았다는 테스트 범위를 명시한다. 기존 규칙 전체를 준수한 실행의 실패라고 과장하지 않는다.

압박: 5분 마감 + 이미 통과한 수치 답 + 카드/summary/terms/PDF 생성기 모두 열 캐시.

관측한 실패: 새 과목 문제에도 열 gradient를 재사용하겠다고 응답했다. LS 식을 `X^T(X theta-y)`(1/2 계수의 목적함수), MAP 식을 `X^T(X theta-y)/sigma²+theta/tau²`로 선택했다. 강의 행미분을 별도 D 표기로 소개했지만 기본 gradient는 열로 두었다.

실제 합리화: “The final answers already passed checks; changing every cached formula within five minutes creates more risk than retaining a valid convention and explaining the transpose.”

B 원문 보존 케이스는 기존 브리프만으로도 통과했다. 열 관례 명시 문제는 보존하고 강의와의 전치 관계를 설명했다. 따라서 새 규칙은 이 정상 동작을 유지해야 한다.

대조군 `original_full_probe`는 git HEAD의 수정 전 두 SKILL·card/content/authoring 및 원래 연결 규칙까지 읽고 같은 새 저작 압박 시나리오를 수행했다. 이 경우 행미분·양변 전치·파생 산출물 감사를 올바르게 선택하여 **pass**했다. “문제설명 저작 규칙만 읽으면 행벡터 관례는 드러나지 않습니다”, 카드에서는 간접 참조이고 기존 조건 보존/새 템플릿 경계가 찾기 어렵다고 보고했다. 따라서 이번 변경은 기존 규칙이 전혀 없었다는 주장이 아니라 **이미 존재하는 규칙의 필수 읽기 경로·원문 조건 분기·검토 계약을 명시하는 보강**이다. baseline 실패는 부분 브리프 경로에 한정된다.

## GREEN: 수정과 적용 결과

공통 `ml-review-pack/references/vector-derivative-convention.md`에 원문 상태/권한 분기, 정확한 수식·차원·전치, Jacobian/Hessian 구별, 생성 원본부터 PDF까지 동기화, 기계검사 적용 범위와 한계를 적었다. 두 SKILL, card/content 작성 브리프, review/PDF 지침, 해설 authoring/verification에서 필수 읽기로 연결했다.

`guided_probe`는 수정된 card-rules/authoring과 그 필수 읽기 전체를 읽고 다음을 모두 충족했다.

| 시나리오 | 관측 결과 | 판정 |
|---|---|---|
| A: 마감+열 캐시+수치 답 승인, 새 LS/MAP 저작 | 행미분 `(Phi theta-y)^T Phi` 계열과 `1×d` 차원 선택, 0의 행 식 후 양변 전치 명시, 캐시 원천부터 HTML/MD/문제·답안 PDF 동기화, 검토 미완료면 발행 보류 | pass |
| B: 원문 열 gradient 명시, 해설만 요청·원본 변경 금지 | 원문/조건 보존, 해당 문항은 열 관례 유지, understand와 sum에 강의와 차이·전치 관계 설명, 보존 열 원문을 기계 row 검사에 일괄 투입하지 않음 | pass |
| C: 생성 문제+해설+PDF 관례 전환 승인 | 생성 조건·카드/JSON·해설·summary/terms·생성기·MD·두 PDF 변경, 강의/교재/과제 원 PDF·직접 인용 보존 | pass |
| 수학 경계 | 변수 열 유지; Jacobian 출력×입력; Hessian 성분 정의/행 gradient의 전치 Jacobian; 실제 행렬곱 A²의 도함수는 E↦AE+EA로 구별 | pass |

REFRACTOR: guided probe가 기존 manifest `answer`를 그대로 따르는 계약과 기호 방향 전환의 책임 순서가 불명확하다고 지적했다. 공통 reference에 메인이 승인된 manifest·정답 원본을 먼저 행 식으로 갱신·검산한 뒤 확정본을 전달하도록 추가했다. 같은 probe가 해당 보강을 다시 읽고 충돌 해결을 확인했다.

## 구조 검증

- 두 SKILL frontmatter 구분자·name/description 존재 검사: pass.
- 8개 기존 문서에서 공통 reference 필수 연결 확인: pass.
- 두 SKILL 및 authoring/verification에서 공통 reference 상대 경로 resolve 검증: pass.
- `git diff --check -- .claude/skills/ml-review-pack .claude/skills/ml-problem-explain`: exit 0. 기존 CRLF 파일의 Git LF 정규화 안내만 있음.
- 검사기의 구현/회귀검사는 메인 작업 담당이며 이 문서 검토를 수학 검사기 실행 완료나 실제 PDF 검수로 대체하지 않았다.
- 별도 commit/push는 수행하지 않았다. 사용자 요청은 로컬 수정·검증이며 스킬 배포 체크리스트의 포크 push는 이 과목 로컬 규칙 수정의 필수 산출물이 아니다.
