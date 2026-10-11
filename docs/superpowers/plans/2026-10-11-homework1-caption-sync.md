# 과제1 음성·자막 일치 수정 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 과제1 25편을 같은 Aoede 목소리로 문장·구절별 재합성하고 전체 설명과 대응하는 자막을 표시한다.

**Architecture:** 기존 pcm-chunks-v1과 제작 단계를 재사용한다. 과제1 전용 명시적 청크 쌍 데이터와 검증기를 추가하고 기존 저작기에 연결한다. 단계 재개·백업·검토용 영상 교체는 과제1 전용 실행기에 모아 공용 TTS·타임라인 계약을 바꾸지 않는다.

**Tech Stack:** Python 3/unittest, 기존 Vertex AI Express TTS, PyMuPDF, HyperFrames/GSAP/Chrome, libass FFmpeg.

**Spec:** `docs/superpowers/specs/2026-10-11-homework1-caption-sync.md` — 위 대화의 설계와 사용자 확정을 동결한 명세. 실행자는 둘 다 읽는다.

## Global Constraints

- 대상은 과제1 P1–P25의 기존 25편이다.
- Vertex AI Express / gemini-2.5-flash-tts / Aoede / ko-KR / mono PCM 24kHz 16bit를 유지한다.
- 청크 분할 후 공백 정규화한 text 결합은 기존 원고와 같아야 한다.
- 최대 2줄/줄당 34자의 cue를 사용한다. 긴 문장은 의미 구절에서 나누고 보호된 수식은 자르지 않는다.
- SRT 반올림 오차 ≤1ms, 영상 경계 오차 ≤1프레임이다. 단어 내부 정렬은 주장하지 않는다.
- 1920×1080, 30fps, 원본 PDF 공개·필기·페이지 계약과 기존 자막 스타일을 유지한다.
- 기존 raw WAV, 캐시, 이전 영상과 PDF 원본을 보존한다.
- 실제 전청크·최종 영상 청취 근거가 없으면 complete=false/live_audio=unverified이며 공식 publish/latest를 갱신하지 않는다.
- 자동 에너지 절단, 글자 수 비례 배분, 임의 연결 무음, 모델 자동 대체를 하지 않는다.
- 기존 설정의 tts_concurrency=2/max_attempts=4/budget_usd=null을 유지한다. 사용자는 재합성을 승인했다. 키는 기존 .env에서만 읽고 출력하지 않는다. 가격·예상 비용·가용성을 추정하지 않는다.
- 렌더는 문항·파트 순차 처리하고 저장된 render-options를 사용한다. 새 음성에 대한 필기 공백·지연 검토 근거를 갱신한다.
- 작업 시작 시 git 상태를 기록하고 기존 미커밋 변경을 보존한다. 아래 커밋은 실행 중 생긴 변경만 선별한다. push는 포함하지 않는다.

## Review Focus

1. 쉼표가 들어간 벡터·행렬과 음수 분수: 수식 내부 쉼표가 cue를 쪼개거나 부호·분모를 바꾸지 않아야 한다 — Task 1.
2. 소개·이유·검산·최종 설명: 계산 단계 이외에도 원고를 누락하지 않아야 한다 — Task 1.
3. 새 음성 길이와 복수 페이지(P22): 필기·페이지 진입을 이전 타임라인으로 재사용하지 않아야 한다 — Task 2.
4. TTS 실패·중단·재개: 성공 청크를 다시 결제하거나 기존 최종 영상을 손상시키지 않아야 한다 — Task 2.
5. 부분 성공·오래된 검수: 미완성 파일을 교체하거나 구버전 검수로 완료를 주장하지 않아야 한다 — Task 3.

---

## 파일 구조와 실행 기준

이 계획에서 `A=문제풀이영상/과제1/과제1_제작자료`, `S=.agents/skills/ml-solution-video`이다. 기존 batch는 `A/current-batch.json`에서 읽는다. 스크립트는 repo 루트에서 실행한다.

| 파일 | 책임 |
|---|---|
| 새 `A/speech-pairs.json` | P1–P25의 segment별 명시적 text/caption_text 청크와 대응 검토 근거 |
| 새 `A/homework_chunks.py` | 데이터 조회·원고 보존·cue 계약 검증·manifest 적용 |
| 수정 `A/author-homework.py:65-78` | 신규 저작도 동일 쌍 데이터 사용; 실행 시에만 batch 읽도록 import 부작용 제거 |
| 새 `A/resynthesize-homework.py` | 백업, 기존 manifest 교체, check부터 단계 재개, P1 선행 검증 |
| 새 `A/collect-corrected-videos.py` | 검증된 검토용 결과의 보존 교체·journal 복구·상태 기록 |
| 새 `A/tests/test_homework_chunks.py` | 원고·수식·누락 회귀 |
| 새 `A/tests/test_resynthesis.py` | 합성·재개·타이밍 단계 회귀 |
| 새 `A/tests/test_corrected_delivery.py` | 검증·교체·실패 복구 회귀 |
| 수정 `A/README.md` 및 생성 JSON 기록 | 새 결과의 정확한 검수 상태·SHA·미완료 문항 |

`narration.py`의 N, `captions.py`의 구버전 C/R, 기존 PDF/map/layers는 보존한다. 신규 manifest에는 쌍 데이터에서 결합한 자막을 사용한다. generic speech_chunks/subtitles/TTS를 수정할 필요가 생기면 먼저 재현 테스트로 필요성을 증명하고 범위를 기록한다.

### Task 1: 원고를 보존하는 명시적 음성·자막 청크

**Files:** Create `A/speech-pairs.json`, `A/homework_chunks.py`, `A/tests/test_homework_chunks.py`; Modify `A/author-homework.py`.

**Interfaces:**
- Consumes: 기존 25개 `source/manifest.json`의 problem_id/segments와 `solution_video.subtitles.chunk_caption`, `solution_video.speech_chunks.validate_speech_chunks`.
- Produces: `load_pairs(path: Path) -> dict`; `paired_segment(problem_id: str, segment: dict, pairs: dict) -> dict`; `apply_pairs(manifest: dict, pairs: dict) -> dict`. 입력 dict는 변형하지 않는다.
- JSON: `{schema_version:1, problems:{P1:{segments:{write0:{chunks:[{id,text,caption_text}], review_notes:"..."}}}}}`. 모든 기존 segment id를 정확히 포함한다. review_notes에는 원고의 각 의미와 숫자·기호 대응을 실제 대조한 내용을 적는다.

- [ ] **Step 1: 실패 테스트 작성.** unittest의 `test_p1_three_sentences_are_three_cues`는 write0의 세 문장과 앞 명세의 세 자막을 정확히 비교한다. `test_missing_segment_rejected`는 check/intro/final 중 하나 누락 시 InputError, `test_original_text_preserved`는 단어 삭제·순서 변경 시 InputError를 기대한다. `test_math_groups_and_signed_fractions`는 `(1, −2, 3)` 내부 쉼표와 `−1/3`이 보존되고 기존 chunk_caption에 통과함을 확인한다. `test_all_25_manifests_covered`는 25개 모두 segment/chunk identity가 유일하고 원고 재결합이 동일함을 검사한다.
- [ ] **Step 2: 실패 확인.** `PYTHONPATH="$PWD/$A:$PWD/$S/scripts:$PWD/$S/tests" python3 -m unittest discover -s "$A/tests" -p test_homework_chunks.py -v` → 신규 모듈/쌍 데이터 누락으로 FAIL. 여기서 A/S는 위 경로로 셸 변수에 설정한다.
- [ ] **Step 3: 명시적 쌍 저작 및 함수 구현.** 모든 segment 원고를 문장·의미 구절로 분할한다. 공백 정규화한 text 결합만 기존 원고와 비교한다. 자막은 생략 없는 문맥별 숫자·기호 표기로 직접 작성한다. 청크당 기존 chunk_caption의 cue가 정확히 하나여야 한다. 각 쌍의 의미 대응은 직접 검토하고 review_notes를 기록하며 자동 문자열 비교를 의미 증명으로 간주하지 않는다. author-homework.py는 동일 apply_pairs를 사용하되 기존 PDF 저작·P12/P22 수정 결과를 변경하지 않는다.
- [ ] **Step 4: 통과 확인.** Step 2 명령 → 전체 PASS; 기존 `test_speech_chunks.py`, `test_subtitles.py`도 unittest discover로 각각 실행 → PASS. 유료 요청 0.
- [ ] **Step 5: 선별 커밋.** 위 네 파일에서 이번 변경만 stage하고 `git diff --cached --stat` 확인 후 `git commit -m "fix: pair homework narration with complete captions"`.

### Task 2: 같은 목소리 재합성과 재개 가능한 제작

**Files:** Create `A/resynthesize-homework.py`, `A/tests/test_resynthesis.py`; generates current RUN/source/verification/renders records and `A/이전버전/음성자막수정전/` backups.

**Interfaces:**
- Consumes: Task 1의 `apply_pairs`; 기존 `run_bundle_stage(action, run, args, transport=None)`, `speech_tts` 캐시와 stage state.
- Produces: `prepare_revision(batch: Path, pairs_path: Path) -> dict`; `run_revision(batch: Path, problem_ids: list[str], args: object) -> dict`. 반환 `{items:[{problem_id,status,failed_stage,reason}], paid_requests:int}`. 상태는 passed/failed이고 스크립트 실패가 한 문항의 예외를 숨기지 않는다.
- CLI: `python3 "$A/resynthesize-homework.py" --batch "$BATCH" --pairs "$A/speech-pairs.json" --problems P1 --hyperframes-entry "$HF" --env-file .env`; --problems 생략 시 P1–P25, `--prepare-only`는 백업·저작·check까지만, `--resume`는 현재 hash/state의 첫 무효 단계부터 재개한다. 성공한 P1을 검증 후 나머지 순차 실행한다.

- [ ] **Step 1: 실패 테스트 작성.** `test_prepare_preserves_existing_media_and_layers`는 원본 MP4/raw WAV/PDF/layers SHA가 prepare 전후 같고 백업 영수증이 일치함을 assert한다. `test_same_voice_and_text_cache`는 provider/model/voice와 정확한 text 캐시 재사용을 확인한다. `test_tts_failure_resume`는 mock transport의 두 번째 요청 실패 후 성공 청크가 재호출되지 않음을 assert한다. `test_changed_voice_rebuilds_timing`은 음성 샘플 수 변경 후 caption_cues가 실측 경계, SRT 오차 ≤1ms, 필기·page_spans 재계산 및 P22 페이지 reset 회귀 통과를 assert한다.
- [ ] **Step 2: 실패 확인.** Task 1과 같은 PYTHONPATH로 `python3 -m unittest discover -s "$A/tests" -p test_resynthesis.py -v` → 신규 실행 함수가 없어 FAIL.
- [ ] **Step 3: 실행기 구현.** 이전 manifest/검토 기록/설정/목록/MP4를 변경 전에 SHA로 백업한다. current RUN의 manifest에 apply_pairs를 적용하고 content fingerprint 의존 coverage/math-review를 실제 원고·자막 대조 후 갱신한다. PDF/layers는 보존한다. check → tts → assemble → render → captions → verify를 수행한다. tts는 이미 timing을 만들므로 단순 중복 retime은 하지 않는다. 필기 설정 또는 청취에 근거한 trim 변경 때만 retime한다. 옛 audio/visual/pacing 승인은 재사용하지 않는다. 요청 비용 기록은 실제 반환값만 기록한다. 캐시와 runtime 실행 경로를 확인하고 없는 의존성을 전역 자동 설치하지 않는다.
- [ ] **Step 4: 테스트 통과 확인.** Step 2 → PASS. `PYTHONPATH="$PWD/$S/scripts:$PWD/$S/tests" python3 -m unittest discover -s "$S/tests" -v` 및 기존 Node writing/teaching runtime 테스트 → PASS, skip는 별도 보고. 테스트 transport는 synthetic이며 유료 요청 0.
- [ ] **Step 5: 실제 P1 선행 검증.** --prepare-only 전체 25편 통과 후 위 CLI로 P1 합성·렌더를 실행한다. 새 원고/자막 전체 대응, 실제 음성 검수 가능 여부, 수식·필기·무음·자막 화면을 확인한다. 청취 불가 상태는 미검수로 기록하되 허위 승인은 쓰지 않는다. 기술 실패 또는 확인된 음성 결함이 있으면 같은 RUN에서 원인을 고친 뒤 재개한다.
- [ ] **Step 6: 나머지 24편 실행.** P1의 기술·화면 검사 성공 후 --resume으로 P1–P25 실행한다. 문항 렌더는 순차, TTS concurrency=2. 각 문항 실패 후 성공 형제는 보존하고 실패 이유를 기록한다.
- [ ] **Step 7: 선별 커밋.** 실행기·테스트·추적 대상 제작 기록의 이번 변경만 stage한다. 캐시/master/로그/비밀 제외를 확인하고 `git commit -m "fix: resynthesize homework speech in measured chunks"`.

### Task 3: 25편 검증과 실패 시 복구 가능한 전달

**Files:** Create `A/collect-corrected-videos.py`, `A/tests/test_corrected_delivery.py`; Modify `A/README.md`; Update `A/검토영상_목록.json`, `A/검증결과.json`, `A/진행상태.json`; generates `A/음성자막수정_교체기록.json`.

**Interfaces:**
- Consumes: Task 2 current RUN의 final.mp4/report/timeline 및 기존 명명 규칙.
- Produces: `collect_corrected(batch: Path, destination: Path) -> dict` 반환 `{expected:25,replaced:list[str],failed:list[dict],complete:bool,live_audio:str}`. `recover_delivery(journal: Path) -> None`는 pending/백업/대상 SHA를 검사해 중단 교체를 복구한다.
- CLI: `python3 "$A/collect-corrected-videos.py" --batch "$BATCH"`; `--recover`는 교체 journal 복구만 수행한다.

- [ ] **Step 1: 실패 테스트 작성.** `test_stale_report_blocks_replacement`는 현재 fingerprint/final SHA와 다른 report가 있으면 대상 유지. `test_partial_failure_preserves_old_video`는 24개 성공/1개 실패 때 실패 문항의 이전 SHA 유지, 전체 성공으로 기록하지 않음을 assert한다. `test_copy_failure_and_recovery`는 copy/replace 중 오류 때 백업 보존·복구 후 파일 SHA 일치를 assert한다. `test_missing_listening_stays_unverified`는 기술 통과만 있는 입력이 검토용 교체는 가능하나 complete=false/live_audio=unverified, publish/latest 미변경임을 assert한다.
- [ ] **Step 2: 실패 확인.** 같은 PYTHONPATH로 `python3 -m unittest discover -s "$A/tests" -p test_corrected_delivery.py -v` → 신규 함수 누락으로 FAIL.
- [ ] **Step 3: 보존 교체 구현.** 현재 hash에 묶인 technical_complete와 새 화면 검토 근거 및 자막 대응 검토를 확인한다. audio 검수 상태를 별도 판정한다. 기존 collect-review-videos.py의 안전한 파일명은 유지하되 단순 captions receipt만으로 교체하지 않는다. 백업 SHA 확인 → pending 복사 → SHA 확인 → os.replace 순으로 문항별 journal을 갱신한다. 강제 종료 때 여러 파일의 원자적 교체를 주장하지 않는다. 성공/실패 목록과 README를 실제 상태로 갱신한다.
- [ ] **Step 4: 통과 확인.** Step 2와 A/tests 전체 → PASS. 현재 25개 RUN의 SRT 전체 문구·실측 경계, PCM 영수증, 실제 파일 SHA, media decode·1920×1080/30fps, 원본 SHA, 필기/페이지/자막 검사를 완료한다. P1의 세 문장이 서로 다른 cue임과 P22 계속 페이지를 직접 화면 대조한다.
- [ ] **Step 5: 청취와 교체.** 실제 청취 가능한 경로가 있으면 모든 청크·최종 영상의 발음/누락/자연스러운 연결/자막 대응을 검수하고 현재 hash의 증거만 기록한다. 불가능하면 그 한계를 기록하고 수정 검토용 25편을 전달한다. 수학·음성 결함이 확인된 문항은 재합성/재검증 전 교체하지 않는다. 일반 오류 복구를 확인한 뒤 전달 CLI를 실행한다.
- [ ] **Step 6: 최종 결과 확인 및 선별 커밋.** 25편 대상과 목록 SHA, 이전 버전 보존, 실패/미검수 표시를 독립 대조한다. `git diff --cached --stat`로 이번 범위만 확인하고 `git commit -m "fix: deliver homework videos with matching captions"`. 사용자에게 파일 위치·25편 진행 결과·실제 음성 검수 경계·실패 문항을 보고한다.

## 자체 검토 기록

- 명세의 전체 범위·같은 목소리·기호화·원고 보존은 Task 1/2, 화면 재계산은 Task 2, 전달·음성 검수·보존은 Task 3에 대응한다.
- Review Focus 5개 모두 해당 task에 이름과 assertion이 명시된 테스트가 있다.
- 함수명/입출력/CLI는 task 사이에서 동일하다. 기술 검증과 실제 청취를 혼동하지 않는다.
- 새 쌍 데이터는 의미 검토가 필요한 저작물이다. 검사기의 자동 문자열 일치로 의미 검토를 대체하지 않는다.
- 이 계획 저장 중 구현·TTS·영상 교체·커밋을 실행하지 않았다.

## 실행 인계

권장 방식은 Native: 서로 연결된 3개 task를 같은 세션에서 구현하고 마지막에 독립 검토한다. 계획 검토와 실행 방식 선택 후 시작한다. 사용자가 이미 승인한 25편/동일 목소리/재합성은 재확인하지 않는다. Subagent-driven을 선택하면 task별 구현·검토 에이전트를 사용한다.
