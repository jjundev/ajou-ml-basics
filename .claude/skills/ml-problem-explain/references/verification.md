# 검토 기록과 발행

기계 검사는 구역·소문항·수식 보존·자원·파일 해시를 검사해요. 의미와 답이 맞다는 판단은 하지 않아요. build가 만든 `review.json`은 전부 `not_run`이에요. 실제 확인을 수행한 에이전트만 기록을 갱신해요. 과제 원 PDF 또는 MML의 문항 페이지와 대조하고, 원 답안을 독립 검산의 결과로 간주하지 않아요.

JSON의 `input_hash`는 현재 원본과 설명 조각에 묶여요. build 출력의 `artifact_hashes`도 그대로 검토 대상이에요. 조각·원본·렌더링 파일을 바꿨다면 다시 build하고 검토해요. 예전 검토 보고서는 통과하지 않아요.

- `source_visual`: 문항 조건·그림·소문항을 PDF/MML의 실제 페이지와 대조. reviewer와 evidence에 자료/페이지/대조 결과.
- `content`: 상위 status/reviewer/evidence 및 items의 모든 `pN:a` 또는 `pN:main`. 첫 줄·유도 이유·모든 답·검산·가정·충돌 여부 확인.
- `independent`: 같은 모든 items, method=`exact|symbolic|numerical|proof|qualitative`, conclusion과 evidence. 검산 스크립트·출력·자료 위치를 구체적으로 기록.
- `browser`: 1280×900 및 375×812, light/dark. 목차·이전/다음·요약·수식·표·그림·링크를 확인. 콘솔·KaTeX 오류·누락 자원·문서 가로 넘침은 0. 긴 수식 자체의 국소 스크롤은 가능. 외부 요청 없이 로컬 자원으로 렌더링.

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
