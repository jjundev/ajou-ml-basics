# 출처·선정 기록·영상별 내용

HTML/MD, 모든 복습문항을 읽는다. 장마감 문서는 있을 때만 읽는다. HTML과 MD가 모두 있으면 핵심 개념·수치·조건을 대조한다. 숫자가 다르면 conflicts에 출처와 차이를 기록하고 근거로 해결하기 전 TTS를 실행하지 않는다.

기본 선택 제작은 [선정·여러 영상](selection-and-batches.md)의 selection.json에 원문 전체 개념 목록과 선정/비선정 이유를 남긴다. 각 RUN의 manifest에는 그 영상에 배정된 주개념과 선수 개념만 등록한다. 전체 복습 요청일 때는 원문 전체 학습 내용을 등록한다. 원자료를 모두 검토했다는 주장과 모든 내용을 영상화했다는 주장을 구분한다.

manifest schema v1의 실제 예시는 tests/_util.py의 minimal_manifest()다. topics.requirements에 해당 영상 범위의 학습 개념·수치·보충·오개념·문항 판별점을 각각 넣고 source_id와 locator를 남긴다. claim·locator·kind는 선정 목록과 일치해야 한다. 반복 설명은 통합하되 각 requirement를 segment에 연결한다. 선택 제작의 questions에는 해당 영상에서 설명할 문항 ID와 판별점 requirement_ids를 연결한다. 전체 복습 요청은 모든 문항을 연결한다. 문항 전체를 먼저 읽었다는 기록은 source_reviews에 보존한다.

coverage_reviews는 claim과 발화문을 직접 대조한 뒤 작성한다. ID 연결이나 문자열 포함만으로 passed를 쓰지 않는다. 영상 범위의 필수 학습 내용은 exclusions로 제외할 수 없다. 영상화하지 않은 학습 내용은 전체 selection 목록의 text 결정과 이유로 남기며 manifest에 필수로 등록한 뒤 exclusions로 빼지 않는다. 원문 전체 개념의 발견 여부와 영상별 선정 범위의 발화 대응을 별도로 검토하고 source/coverage.md에 근거를 남긴다. 기계 검사는 항목 발견 자체·선정 타당성·의미 동일성을 증명하지 못한다.

지난 시험 공지/예고는 notices에 period_label을 기록하고 “당시 수업 안내”로 표시한다. 비학습 반복/내비게이션만 exclusions에 이유와 출처를 남긴다.

## 수식과 범위 확인

충돌은 STT/·강의노트/·교과서/Mathematics_for_Machine_Learning.pdf에서 해결한다. 이 파일들은 확인 자료이며 discovery의 노트 목록을 자동 확장하지 않는다. 확인에 사용한 쪽·슬라이드·문장을 source/coverage.md에 기록하고, 필요하면 RUN 내부에 확인 자료 스냅샷을 둔다. 예고 범위를 학습 완료로 바꾸지 않는다. 독립 가정, 정규화, 부호, 변수 차원, 확률과 확률밀도의 차이를 보존한다.
