# 검토 기록과 발행

기계 검사는 구역·소문항·수식 보존·자원·파일 해시를 검사해요. 의미와 답이 맞다는 판단은 하지 않아요. build가 만든 `review.json`은 전부 `not_run`이에요. 실제 확인을 수행한 에이전트만 기록을 갱신해요. 과제 원 PDF 또는 MML의 문항 페이지와 대조하고, 원 답안을 독립 검산의 결과로 간주하지 않아요.

JSON의 `input_hash`는 현재 원본과 설명 조각에 묶여요. build 출력의 `artifact_hashes`도 그대로 검토 대상이에요. 조각·원본·렌더링 파일을 바꿨다면 다시 build하고 검토해요. 예전 검토 보고서는 통과하지 않아요.

- `source_visual`: 문항 조건·그림·소문항을 PDF/MML의 실제 페이지와 대조. reviewer와 evidence에 자료/페이지/대조 결과.
- `content`: 상위 status/reviewer/evidence 및 items의 모든 `pN:a` 또는 `pN:main`. recall의 문제 단서와 개념 연결·공식·기호의 뜻·적용 가정·선택 이유·소문항별 누락 여부, 첫 줄·유도 이유·모든 답·검산·가정·충돌 여부 확인. recall은 정의/판단 기준만 필요한 문항도 허용하지만 제목만으로는 충분하지 않아요. start와 긴 설명을 복제하지 않았는지, 요약의 핵심 개념·공식이 본문과 일치하는지 확인해요.
- `independent`: 같은 모든 items, method=`exact|symbolic|numerical|proof|qualitative`, conclusion과 evidence. 검산 스크립트·출력·자료 위치를 구체적으로 기록.
- `browser`: 1280×900 및 375×812, light/dark. 모든 문항의 목차·이전/다음·요약·수식·표·그림·링크를 확인. 콘솔·KaTeX 오류·누락 자원·문서 가로 넘침은 0. 짧은 인라인 수식의 스크롤 컨테이너와 수식 영역의 보이는 스크롤바는 0. 구역 24px·제목 아래 12px·소문항 16px 간격, 행렬 잘림과 겹침을 실제 렌더링으로 확인. 긴 수식은 의미 단위 줄바꿈을 우선하고, 더 나눌 수 없는 긴 수식만 안내와 함께 스크롤바 없는 국소 이동을 허용. 외부 요청 없이 로컬 자원으로 렌더링.

각 단계와 items는 status=`pass`, 비어 있지 않은 reviewer/evidence여야 발행돼요. `not_run`, `fail`, `disputed`는 발행을 보류해요. numerical은 유한한 tolerance>0, 0<=residual<=tolerance도 필요해요. proof에 숫자 예제 확인만 있는 evidence는 수동 검토에서 승인하면 안 돼요.

```json
{
  "status": "pass",
  "reviewer": "검증을 수행한 에이전트",
  "evidence": "evidence/transpose.py 및 transpose-result.txt: 입력 행렬과 일치",
  "method": "exact",
  "conclusion": "전치 후 다시 전치하면 원 행렬과 정확히 같음"
}
```

사용한 근거 파일은 대상 작업 디렉터리의 `evidence/` 아래 보관해요. `references`에는 읽은 저장소 내부 자료의 절대 path와 SHA-256을 기록해요. 발행 직전 재확인돼요. `artifact_hashes`에는 manifest를 포함한 현재 stage 파일의 상대경로→SHA-256을 기록해요. build가 넣은 값을 승인 전 점검하며 임의로 오래된 검토에 새 해시만 덮어씌우지 않아요.

답 충돌·조건 모호함·원문 미확인은 해당 팩을 disputed로 표시하고 이유를 보고해요. 다른 독립 팩은 통과하면 발행할 수 있어요. 기존 파일은 변경하지 않고 설명 소유 파일만 백업 후 교체하며 실패 시 복구해요.


## 현재 기준과 재렌더링 검토 계약

현재 `review_policy_version`은 `problem-explain-2026-10-15`다. 새 review.json·manifest의 버전이 일치해야 발행된다. 구버전/버전 없는 검토를 단순히 현재 버전으로 바꾸거나 pass를 복사하지 않는다. 기준 변경은 실제 content·independent 재검토를 요구한다.

content는 recall의 근거 있는 명칭 대응, pitfall의 오답 판별 기준, 부정형의 참·거짓과 선택 적합성, understand·solve·verify·pitfall·sum의 결함 공개·공식 답 확인 여부가 일관적인지 확인한다. 과목별 disputed 규칙은 유지한다. 독립 검산은 작성자와 다른 검산자가 정답·참고 풀이·설명 조각을 보지 않고 문제·그림·필요한 이론 자료만으로 먼저 수행한다. 컨트롤러가 그 결과를 참고 답과 대조한다.

rerender의 검토 재사용은 동일한 입력·조각·입력 그림과 무결한 발행 자료, 검증된 모든 참조, 같은 검토 기준을 전제로 한다. 참조가 없거나 바뀌면 content·independent도 not_run으로 두고 다시 검토한다. 전자회로2는 problems.txt가 같더라도 문제 MD·그림이 바뀌면 재사용하지 않는다. source_visual·browser는 매번 새 stage에서 수행한다. 구조 검사는 내용 검증이 아니다.

browser는 1280×900·1024×900·375×812, light/dark에서 실제 확인한다. 1023→1024 경계에서 목차·문제 기본 열림, 저장한 닫힘 유지, 원문 탭(원문 없는 문항은 숨김), 문제 패널 왼쪽·오른쪽 붙이기·띄우기, 이동·크기 조절·화면 내 제한, 모바일 접힘, 그림 확대와 인쇄 문제/원문 보존을 확인한다. 유효한 객관식은 오답·정답·다시 풀기·판정 이동, 모델 없는 문항은 정적 표시를 확인한다. 코드 문자·들여쓰기·수식·소문항·원문을 보존하고 외부 요청·콘솔/KaTeX 오류·누락 자원·문서 가로 넘침은 0이어야 한다.

참조 HTML·MD·SVG가 로컬 그림을 사용하면 해당 그림도 references에 절대 경로와 SHA-256으로 별도 기록한다. 참조 그림 해시 누락·변경은 검토 재사용과 새 발행을 막는다. 옮긴 그림의 이전 바이트를 확인할 수 없으면 현재 파일을 자기 자신과 비교해 같은 그림이라고 간주하지 않는다.
