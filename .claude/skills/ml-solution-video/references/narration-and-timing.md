# ML 설명, 청크, 필기 타이밍

manifest schema2에 bundle key/pack_id/problem_id/title, segments, reveal_order, shape_anchors, cameras, caption_timing을 넣는다. 각 segment는 page_id, 안전한 ASCII id, kind(problem/reason/write/check/summary), 전역 step_id, text, caption_text, source_refs와 chunks를 갖는다. 문제 PDF로 시작하고 각 전역 단계에 write 하나씩을 원문 순서로 연결한다.

신규 caption_timing은 pcm-chunks-v1이다. 각 chunk `{id,text,caption_text}`는 표시 cue 하나여야 하며, 부모 text/caption_text는 청크를 공백으로 연결한 값이다. 마침표와 수식 밖 쉼표는 cue 경계다. 자연스럽게 읽을 한국어는 text, φ/θ/Σ/전치/첨자/분수/음수와 숫자는 caption_text에 직접 저작한다. 수식 괄호 안 쉼표는 보호한다. 한글 숫자 전역 치환은 하지 않는다. cue 최대2줄/줄당34자이며 수식·중첩 괄호·부호 분수·소수·identifier를 보호한다. 넘어가면 저작을 고치고 줄축소·잘라내기로 숨기지 않는다.

TTS는 spoken-text-only-v1 원고만 요청하고 direction/“원고:”/caption은 넣지 않는다. 기본 Vertex AI Express/gemini-2.5-flash-tts/Aoede/ko-KR, PCM16 mono24kHz다. 모델/공급자 자동 대체 없음, 동시2/시도4/예산null이다. 키는 환경 또는 --env-file에서 읽고 출력하지 않는다. caption만 바뀐 청크는 동일 text WAV를 재사용한다.

raw 청크 WAV는 chunk-audio.json의 샘플/SHA 영수증으로 보존한다. segment WAV는 PCM을 그대로 연결하며 임의 무음을 넣지 않는다. caption_cues는 실제 누적 샘플 시작/끝이고 segment의 필기 hold로 늘리지 않는다. SRT 반올림 오차≤1ms, frame 경계≤1이며 단어 내부 정렬을 주장하지 않는다.

청크를 직접 청취해서 앞뒤 무음 제거가 필요한 경우에만 chunk-trims.json의 schema1 rows `{segment_id,chunk_id,raw_sha256,start_sample,end_sample,reason}`을 저작한다. retime은 raw SHA와 절단 근거를 확인하고 연결 PCM을 다시 만든다. 원본은 보존하며 에너지 자동 절단을 하지 않는다. text 변경이면 먼저 tts, caption/필기만 변경이면 현재 검토를 갱신한 뒤 캐시/PCM을 재사용한다.

page_spans는 겹치지 않는 frame 구간이며 모든 segment 경계를 따른다. 같은 페이지로 복귀할 수 있고 frame seek 시 해당 페이지의 누적 공개 상태를 재구성한다. 원본 SVG의 ID/definition은 페이지 접두사로 분리하며 모양을 재조판하지 않는다.

focus.json schema2는 regions `{id,page_id,source_sha256,bbox}`와 cues `{segment_id,target}`다. annotations.json schema2 items는 id/region_id/segment_id/chunk_id/offset_frames/kind/geometry/source_refs/meaning_notes/hide_at 등을 갖는다. arrow·ellipse·underline·native font outline label을 지원한다. 실제 공개된 식 또는 원본 그래프를 focus할 수 있고 미래 풀이 공개는 거부한다. 주석은 화면상2–12px(기본3,권장4/6/8)이며 카메라 여백에 굵기·화살촉·label·연필을 포함한다. Δ/∆ alias는 실제 font glyph가 같을 때만 허용한다.

chunk 주석은 move8+draw를 실측 음성 chunk 안에서, camera 복귀(segment end−13) 이전에 끝내며 겹침을 거부한다. 최종 hold에서 모든 주석/연필을 숨긴다. 추가 무음으로 표시 deadline을 우회하지 않는다.

writing은 초당7.5글자/연필160px/전환12fr/본문과label26px다. 도형 예산은 원본 전체 폭으로 계산한 `min(90,max(18,ceil(W/H×glyph_interval)))`을 clip 폭에 배분한다. 합계 보존·조각 최소1fr·예산보다 많은 조각 거부를 유지한다. 도형-only 청크는 전체 페이지와 연필만 fit하며 text26 규칙을 오용하지 않는다.

narration-pacing은 실측 PCM 종료와 writing 종료를 구분한다. >60fr 음성 공백은 gaps, >60fr 필기 지연은 writing_lags에 현재 input_hash와 이유를 기록해야 한다. 완료 화면 hold는 필기 중 무음과 다르다. 70–85% 음성 밀도는 저작 안내이며 자동 품질 통과가 아니다.
