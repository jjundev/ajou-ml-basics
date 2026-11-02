# 선정과 여러 영상 제작

이 문서는 기본 주제별 제작의 선정 계약과 보조 명령을 정의한다. 에이전트가 읽기·선정·대본·동작·의미 검토를 수행하고, 스크립트는 그 결과의 구조·범위·파일·완료 상태를 검사한다. 스크립트가 자동으로 내용을 추출했다고 주장하지 않는다.

## 선정과 묶기

노트 HTML/MD, 복습문제, 장마감 문서가 있으면 함께 읽고 개념·수치·조건·보충·오개념·문항 판별점을 목록화한다. HTML/MD 충돌은 원자료로 해결한다. 문제의 판별점은 설명할 내용의 근거이며 모든 문제를 풀이 영상으로 만들라는 뜻이 아니다.

각 항목에 하나의 결정을 기록한다.

- `animate`: 구체적인 위치·방향·분리·결합·축적·시간 변화가 이해를 돕는다. 어떤 변화가 어떤 혼동을 해결하는지 이유를 쓴다.
- `text`: 글·정적 그림으로 충분하거나 사용자 지정 범위 밖이다. 비선정 이유를 구체적으로 기록한다.
- `context`: 선정 주제에 필요한 선수 설명이다. 별도 영상으로 만들지 않고 필요한 영상의 `prerequisite_ids`에 연결한다.

한 독립 학습 질문을 한 영상으로 묶는다. 같은 기작의 단계는 합친다. 주개념은 정확히 한 영상에 배정하고, 선수 개념만 여러 영상에서 재사용할 수 있다. 동일한 내용의 질문을 다른 표현으로 중복 선정하지 않았는지 에이전트가 의미를 검토한다.

0개이면 이유와 선정 기록만 남기고 유료 요청·MP4를 생성하지 않는다. 한 개는 한 영상, N개는 N개다. 모든 영상을 합친 통합 영상은 자동으로 추가하지 않는다. `전체 복습 영상` 요청은 기존 `prepare` 단일 파이프라인으로 원문 전체를 다룬다.

길이는 주제별 약 60–180초를 목표로 한다. 실제 PCM과 읽기 간격으로 최종 시간을 정하며 90초로 일괄 고정하거나 길이에 맞춰 개념을 누락하지 않는다. 사용자가 다른 길이를 명시하면 `duration_override_reason`에 요청을 기록하고 양의 정수 초로 지정한다.

## selection.json 계약

아래 필드로 에이전트가 PLAN을 작성한다. source 목록은 `scripts/lib/sources.py`의 `discover(REPO, RANGE)`가 반환한 `files`를 그대로 사용한다. 파일명·ID·해시는 직접 추측하지 않는다.

| 필드 | 값 |
|---|---|
| `schema_version` | `1` |
| `mode` | `selective` |
| `range` | 지정 날짜 또는 범위 |
| `sources` | 발견한 모든 원자료의 id/kind/path/sha256 |
| `source_reviews` | figure 외 모든 파일에 대해 source_id/status=`reviewed`/reason. 실제 읽은 범위·개념 발견·HTML/MD 대조 기록 |
| `topics` | 전체 항목의 id/claim/source_id/locator/kind/decision/reason |
| `clips` | 아래 영상 목록. 빈 배열 가능 |

각 clip은 다음을 가진다.

```json
{
  "id": "bayesian-update",
  "title": "데이터를 보면 사전분포가 어떻게 달라질까",
  "learning_question": "사전분포와 가능도가 사후분포를 어떻게 결정하는가",
  "requirement_ids": ["req-prior", "req-posterior"],
  "prerequisite_ids": ["req-probability"],
  "visual_states": ["사전분포", "관측 가능도", "정규화된 사후분포"],
  "target_duration_seconds": 120
}
```

ID는 영문자로 시작하는 영문·숫자·하이픈·밑줄이며 제목에는 확장자를 넣지 않는다. `requirement_ids`는 해당 영상의 주개념, `prerequisite_ids`는 선수 개념이다. 애니메이션 주개념 누락·중복 소유, 알 수 없는 참조, 제목/질문 중복, 선수 개념 누락을 금지한다. `visual_states`는 최소 두 상태를 의미 있게 설명한다. 제목의 파일명 금지 문자는 제거되므로 제거 후 충돌도 검사한다.

숫자 ID 연결만으로 전체 원문 발견이나 선정 타당성이 증명되지 않는다. source_reviews와 각 선정 이유는 실제 읽은 내용을 근거로 작성한다. 검증기는 파일 해시·목록·소유 관계를 검사할 뿐이다.

## 준비와 개별 제작

아래 `python3 SKILL/scripts/video.py`를 실제 절대 경로로 펼친다.

```text
plan-check RANGE --repo REPO --selection PLAN
prepare-set RANGE --repo REPO --selection PLAN [--review] [--config CONFIG] [--env-file ENV_FILE]
resume-set --batch BATCH
```

plan-check는 원자료 발견 결과와 PLAN의 모든 파일·해시·검토 기록·주제 소유를 검사하며 파일이나 유료 요청을 생성하지 않는다. prepare-set은 `<날짜>_제작자료/실행/<실행ID>/` 안에 BATCH를 만들고 원자료와 PLAN을 동결한다. batch.json의 clips가 각 RUN의 상대 경로를 제공한다. PLAN을 동결한 후 범위를 바꾸려면 새 실행을 준비한다.

각 RUN에는 원자료 스냅샷, source/selection.json, source/clip-scope.json이 생긴다. manifest schema v1을 유지하며 해당 clip의 주개념과 선수 개념만 topics.requirements에 등록한다. 모든 항목은 required=true이며 id/claim/source_id/locator/kind는 PLAN과 같아야 한다. sources.path는 RUN 내부의 스냅샷 상대 경로로 지정한다. 해당 영상에서 실제 설명하는 문제만 questions/scenes에 연결한다. 전체 문제를 읽은 기록은 PLAN에 보존한다.

각 RUN에서 기존 명령을 순서대로 실행한다.

```text
check --run RUN
tts --run RUN [--approve-review]
assemble --run RUN --pack PACK --assets-from LOCAL_ASSETS
render --run RUN --hyperframes-entry LOCAL_HYPERFRAMES_BIN
verify --run RUN --hyperframes-entry LOCAL_HYPERFRAMES_BIN
```

대본·그림·의미 있는 동작은 에이전트가 작성한다. `--review`이면 모든 주제와 장면 구성을 묶어 검토하고 한 번 승인된 범위의 RUN들에 --approve-review를 적용한다. 선호나 주제별 승인을 다시 묻지 않는다. 기본 자동 실행은 선정 이유·예상 길이를 알리고 진행한다.

각 영상의 범위 누락·추가·claim 변경·스냅샷 변조는 유료 요청 전에 막는다. 음성과 렌더 캐시는 각 RUN에 유지하며 완료된 형제 영상은 다시 생성하지 않는다. 선택 제작의 TTS 사용량·요청 예산은 BATCH/cost-ledger.json을 공유한다. 다른 공급자·음성으로 자동 대체하지 않는다.

resume-set은 각 영상의 verified/pending과 첫 미완료 단계를 반환한다. 현재 검증 지문과 증거가 일치하면 verified다. 과거 complete 플래그만으로 완료를 인정하지 않는다. 전체 복습·예전 단일 RUN은 기존 resume/--from-run을 유지한다.

## 검증과 묶음 전달

```text
publish-set --batch BATCH
```

선정한 모든 영상의 실제 편집 소스·음성·내용·화면·MP4·동기화 검증이 완료된 뒤 실행한다. 하나라도 실패·미확인이면 기존 날짜 폴더의 최종 결과를 바꾸지 않는다. 개별 verify는 묶음의 latest를 갱신하지 않는다.

publish-set은 모든 clip의 선정 범위, 원자료, 검증 지문·증거 해시를 확인한다. 제목 있는 최종 영상들을 날짜 폴더로 내보내며, 재개용 RUN/review.mp4는 해당 영상으로 연결하는 상대 심볼릭 링크로 바꾼다. 모든 export가 생성되기 전에는 검증된 원본을 제거하지 않는다. 중간 실패 시 publish-set을 재실행한다.

예전 날짜 폴더의 영상·제작자료는 공통 제작자료의 이전버전으로 옮겨 보존하며 review.mp4 링크도 이전 영상에 맞춘다. 임의의 이전 폴더를 삭제하거나 이전 영상 링크를 새 내용으로 돌리지 않는다. 공통 latest.json은 이번 batch와 전체 영상 목록·해시를 기록한다. 최신 목록을 덮어쓴 과거 묶음은 그대로 재출판하지 않고 새 실행으로 준비한다.

0개인 묶음은 선정 기록만 전달하고 기존 결과가 있다면 이전버전으로 보존한다. 최종 폴더에는 이번 영상 N개와 `<날짜>_제작자료/` 하나만 남긴다. 완료 보고에는 N, 각 제목·길이·경로와 검증 범위를 적는다. 커밋은 별도 사용자 요청이 있을 때 수행한다.

## 구현 검증

`tests/test_selection.py`는 0·1·N개, 범위 누락·중복·공통 선수 개념, 원자료 변경, 부분 실패·재개, 검증 후 여러 영상 전달, 이전 영상·링크 보존, 출력 중단 후 재시도, CLI 및 공용 예산 경로를 다룬다. 가짜 산출물과 임시 폴더만 사용한다. 기존 전체 tests도 실행해 단일 파이프라인 호환을 확인한다.

## 머신러닝 선정 기준

수업에서 배운 범위·교과서 보충·다음 시간 예고를 먼저 구분한다. 예고는 기본적으로 text로 두고 범위 밖 이유를 기록한다. STT·강의 슬라이드·MML로 조건과 수식을 확인하고 coverage.md에 실제 파일·슬라이드·쪽 locator를 남긴다. 새로운 설명용 예시는 원문 수치와 구분한다.

선형회귀의 계수-직선-잔차-손실, 베이지안의 사전-가능도-사후, 주변화의 가중 합, 공분산의 점구름, 아핀 변환의 좌표 변화처럼 최소 두 구체적 상태를 제시할 수 있어야 animate다. 단순 정의와 비교표는 text, 필요한 선수 설명은 context다. 최적화는 수업에서 배운 경우만 선정한다. 한 질문에 필요한 수식 유도와 화면 변화는 하나로 묶고 동일 개념을 중복 선정하지 않는다.

## 각 영상의 도입

관련 원문 동기를 주제별로 연결하여 첫 15–25초를 문제 → 단순 해법의 한계 → 핵심 아이디어로 연다. 동기가 선수 내용이면 context/prerequisite_ids를 사용하고, 주개념에 속하면 해당 requirement의 설명에 포함한다. 과목 전체의 why 페이지를 모든 clip에 강제하지 않는다. 원자료의 근거와 첫 장면의 실제 설명을 coverage 검토에 기록한다. 선수 ID 존재와 대본의 의미 검증을 구분한다.
