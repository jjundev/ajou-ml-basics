# 음성과 사용량

Vertex AI Express / gemini-2.5-flash-tts / Aoede / ko-KR가 기본이다. assets/vertex-direction.txt의 승인 지시문을 사용한다. 다른 음성을 요청할 때만 동일 원고 샘플을 비교한다. 공급자나 모델을 자동 대체하지 않는다.

환경변수 GOOGLE_API_KEY 또는 GEMINI_API_KEY, 또는 명시적인 --env-file을 사용한다. 키를 대화·로그·설정 파일에 복사하지 않는다. 기존 프로젝트 .env를 자동 탐색하지 않는다.

기본 config.budget_usd는 null(제한 없음)이다. 단가 조회·검증 없이 제작을 진행한다. config.price는 생략할 수 있다. 비용을 계산할 수 없을 때는 금액을 null로 남기며 0달러로 표시하지 않는다.

요청별 cost-ledger.json에 모든 시도와 성공·실패 상태, API가 반환한 토큰 사용량을 기록한다. 성공한 문단의 음성 metadata에도 사용량을 보존한다. 캐시 재사용은 새 API 요청으로 집계하지 않는다. 샘플·재시도·전사도 동일 ledger로 기록한다.

사용자가 원할 때만 budget_usd에 USD 상한 문자열을 설정한다(예: "2.00"). 달러 제한 계산에는 config.price의 input_per_million, output_per_million 단가 문자열이 필요하지만 verified_at/source 같은 별도 확인 증빙은 요구하지 않는다. 입력 payload byte 수와 max_output_tokens로 요청 비용을 예약한다. 명시한 달러 제한이 있는데 단가가 없으면 제한을 조용히 무시하지 않고 단가 설정 또는 제한 해제를 안내한다. 제한 없이 기록한 과거 사용량의 금액을 모르는 실행에 달러 제한을 추가하면 새 실행을 사용하거나 제한을 해제하도록 안내한다.

상한은 로컬 요청 제한이며 클라우드의 실제 청구 한도를 보장하지 않는다. 429/일시적 서버 오류만 최대 4회 재시도하며 반복 429는 다음 batch를 1개로 줄인다. 인증/모델 오류·잘린 음성은 성공 캐시에 저장하지 않는다.

--revoice는 별도 실행에서 음성과 시간표를 교체한다. 음성 파일명에 입력 hash를 넣어 이전 성공 음성을 보존한다.

## 프로젝트 로컬 API 키

첫 설치에서만 `scripts/setup_env.py --source /Users/hyunjun_macbook_pro/Documents/Univ/생명과학/.env --destination REPO/.env`로 복사한다. REPO는 절대 경로로 펼친다. 동일 파일은 재사용하며 다른 목적지 파일은 보존하고 충돌을 보고한다. 권한은 0600, .gitignore의 .env 제외를 확인한다. 원본/목적지 symlink는 허용하지 않는다. 키·내용·키 해시를 출력하지 않는다.

prepare-set, prepare와 tts에 `--env-file REPO/.env`를 전달한다. 명시 파일의 GOOGLE_API_KEY, GEMINI_API_KEY 순서로 선택하고 다른 셸 키로 대체하지 않는다. 파일을 지정하지 않았을 때만 환경변수 fallback을 쓴다. config.json에는 경로만 저장한다. .env는 스냅샷·제작자료·fixture·커밋에서 제외한다. 키 로딩 확인은 네트워크 없이 가능하지만 실제 인증 성공은 제작 때 별도로 확인한다.
