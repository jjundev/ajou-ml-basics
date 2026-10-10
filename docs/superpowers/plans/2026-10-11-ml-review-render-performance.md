# ML Review Video Restore and Multicore Render Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 소스가 없는 ML 개념 복습영상 스킬을 동결 Git 원본에서 복원하고 EC2 멀티코어 render/revoice 정책을 적용한다.

**Architecture:** 기존 ML 스킬을 복원해 수학·출처·자막 계약을 유지하고 EC2의 렌더 정책/장면 캐시/복구 부품만 이식한다. 스킬 내부 독립 모듈을 사용하며 풀이영상 계획과 실행 의존성은 없다. 폰트 준비와 composition 지문 보정은 1회 재조립을 요구할 수 있다.

**Tech Stack:** Python unittest, Node/HyperFrames, Chrome/puppeteer-core, FFmpeg/libass, GSAP, KaTeX, Pretendard.

**Spec:** `docs/superpowers/specs/2026-10-11-ml-render-performance-design.md`의 전역·개념 복습영상 계약. 풀이영상은 `2026-10-11-ml-solution-render-performance.md`로 별도 구현한다.

## Global Constraints

- 복원 기준 `7b2028e82f92962dd12b7f8b76580f6ee7b39682`의 `.agents/skills/ml-review-video/`만 복원; 현재 non-cache 충돌은 덮지 않는다.
- EC2 기준 `7098e0cc042dab4f2660eebe1fa69c3ebc28dcae`의 ec2-review-video 부품만 이식. ML 수식/계산/출처/selection/형제 게시·자막 유지.
- Darwin / Apple M5 / 물리 CPU 10코어 / 메모리 16GiB 이상 workers=6, 기타 환경·탐지 실패 workers=2.
- 정확한 다섯 설정 키: schema_version=1/workers=정수1–6/encoder=cpu/browser_gpu=auto/fast_capture=false.
- CLI → 유효 저장값 → 호스트 기본값. 손상 저장값은 override로 숨기지 않는다. resume/resume-set은 설정을 쓰지 않는다.
- CPU 인코딩·브라우저 GPU auto·`--experimental-fast-capture=false`·delivery1080p30·mono24kHz 유지. 장면 순차 처리.
- 설정 변경은 render 이후만 무효화; TTS/PCM/타임라인/조립 보존. 폰트 준비 코드 변경의 1회 composition 무효화는 음성을 유지한다.
- 실패·Ctrl+C 시 미디어/기록 쌍 복구; 복구 실패 사본 유지·재시도 차단. timeout/중단은 실행한 자식 종료·회수 후 pending 정리.
- 유료 음성·자동 게시·기존 영상 재생성·push·전역 설치 제외. 실험 미디어는 제작자료 내부, synthetic 결과는 실제 음성 승인과 분리.
- 실행 worktree를 확보하고 기존 과목 자료·다른 스킬·캐시를 보존한다. 이번 계획 작성 턴에는 복원을 실행하지 않는다.

## Review Focus

1. 복원 경로에 새 non-cache 작업이 존재: 충돌을 보고하고 해당 파일을 보존 — Task 1.
2. prepare --from-run/다른 호스트/옵션 없는 구형 RUN: 유효 저장값 유지, resume 쓰기 없음 — Task 2.
3. 손상 cache 기록/renderer·폰트 변경: stale 영상 재사용 금지, 음성은 보존 — Task 3.
4. timeout의 분리 세션 자식·interrupt·rollback 실패: 프로세스 회수와 이전 파일/사본 보존 — Task 3.
5. revoice가 retime만 하거나 일부 장면만 재렌더: 실제 캡처만 기록, source/형제/latest 보존 — Task 2/3.

---

## File Structure

`S=.agents/skills/ml-review-video`. 복원: Git 객체의 S 전체 non-cache 파일. 생성: `S/assets/{restore-provenance,render-port-provenance}.json`, `S/tests/{test_restore,test_render_options,test_render_cli,test_render_acceptance_inputs}.py`, `S/tests/render_performance_acceptance.py`, `S/scripts/lib/render_options.py`. 수정: `S/scripts/video.py`, `S/scripts/lib/{batch,state,render,composition}.py`, 필요 시 `S/scripts/lib/revoice.py`의 정책 전달만 수정; `S/tests/{test_render,test_state,test_composition,test_revoice}.py`, `S/SKILL.md`, `S/references/rendering-and-verification.md`. ML math_evidence/math_render/출처 모듈은 EC2 것으로 바꾸지 않는다.

### Task 1: ML 개념 복습영상 원본 복원

**Files:** Restore Git 기준 S 전체; Create `S/tests/test_restore.py`, `S/assets/restore-provenance.json`.

**Interfaces:** Consumes 로컬 Git 객체. Produces 기존 `video.main(argv=None) -> int`, ML `lib.math_evidence.validate_math_evidence(run,m) -> list`, `lib.math_render`/selection/단일·batch·revoice CLI 및 bundled 자산. 복원 manifest는 schema_version=1/commit/files(상대 path/source_sha256)로 기록; 이후 수정 파일의 현재 hash는 render-port manifest에 기록한다.

- [x] **Step 1: 실패 검사 작성.** test_restore는 아직 _util을 import하지 않고 pathlib/unittest로 실행한다. `test_complete_ml_source_tree_restored`에서 SKILL.md/scripts/video.py/scripts/lib/math_evidence.py/scripts/lib/math_render.py/assets/runtime/vendor/gsap.min.js/tests/test_ml_calculation.py 존재를 assert한다. `test_restore_inventory_matches_pinned_archive`는 manifest commit 전체 SHA와 각 원본 file inventory/hash를 복원 직후 대조한다. 후속 변경 파일은 별도 manifest의 source_sha256과 대조한다.
- [x] **Step 2: RED 확인.** `python3 -m unittest discover -s .agents/skills/ml-review-video/tests -p test_restore.py -v` → 실행 소스 부재 FAIL.
- [x] **Step 3: 원본 복원.** 현재 S의 non-cache 파일 목록/hash를 먼저 기록한다. 새 파일과 충돌하면 보존하고 차이를 보고한다. `git archive 7b2028e82f92962dd12b7f8b76580f6ee7b39682 .agents/skills/ml-review-video`를 임시 디렉터리에 추출하고 비교한 뒤 S에 non-cache 파일만 복사한다. test_restore 새 파일과 pycache를 지우지 않는다. 원본 바이트의 restore-provenance 기록을 생성한다. current branch 전체를 과거 commit으로 이동하지 않는다.
- [x] **Step 4: GREEN·baseline 확인.** Step 2 → PASS. `python3 -m unittest discover -s .agents/skills/ml-review-video/tests -v`, `python3 /Users/hyunjun_macbook_pro/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/ml-review-video` → 회귀 PASS/Skill is valid!; 현재 symlink ml-review-pack과 template 경로를 확인한다. 별도 baseline 문제는 재현·보고하고 회귀 기대값을 임의 완화하지 않는다.
- [x] **Step 5: 복원 체크포인트 커밋.** S 아래 non-cache 파일만 명시 목록으로 stage, 캐시/원자료 없음 확인; `git commit -m "feat(ml-review-video): restore pinned ML review workflow"`.

### Task 2: 설정 정책과 신규 RUN·단계 지문

**Files:** Create `S/scripts/lib/render_options.py`, `S/tests/test_render_options.py`; Modify `S/scripts/video.py`의 prepare 분기, `S/scripts/lib/{batch,state}.py`, `S/tests/test_state.py`.

**Interfaces:** Consumes Task 1의 기존 prepare/RunStore/cache 인터페이스. Produces `detect_hardware() -> dict`, `default_render_options(hardware: dict | None = None) -> dict`, `validate_render_options(options: dict) -> dict`, `load_render_options(run: Path, workers: int | None = None, *, hardware: dict | None = None) -> dict` (ValueError). Existing `prepare_set`, `RunStore.recover`, `stage_fingerprint` signatures unchanged. 생산 render/revoice 연결은 Task 3에서만 수행한다.

- [x] **Step 1: 옵션/재개 실패 검사 작성.** test_defaults_exact_hardware/test_strict_workers/test_invalid_saved_not_hidden/test_host_move_preserves_saved/test_load_read_only; assertions는 workers=6 for 정확한 M5/10/16GiB, unknown=2, invalid True/2.0/'6'/0/7과 추가 키·변경 고정값을 ValueError로 거부한다. 기존 2 설정+CLI4→4, override 없음→2. load/resume/resume-set 전후 파일/hash 동일.
- [x] **Step 2: RED 확인.** `python3 -m unittest discover -s .agents/skills/ml-review-video/tests -p test_render_options.py -v` → 신규 모듈 부재 FAIL.
- [x] **Step 3: 정책·저장 구현.** EC2 정책 복사, 신규 단일/batch RUN 설정 생성, from-run의 복사된 저장값 검증·유지. config.json 음성 필드를 변경하지 않는다. stage_fingerprint render/verify/publish에 정책 코드·옵션을 포함하되 이전 stages는 불변.
- [x] **Step 4: GREEN 확인.** Step 2와 전체 unittest 회귀 → PASS. test_state에 옵션 변경 전후 voice/timing/composition fingerprint와 WAV hash 불변, render 지문 변경·recover가 render 반환을 assert한다. prepare/from-run의 기본값 생성·저장값 유지 검사는 test_render_options의 mock 입력으로 실행한다. 렌더 CLI 인자는 다음 Task에서 추가한다.
- [x] **Step 5: 정책 체크포인트 커밋.** 이 Task의 Files만 stage; `git commit -m "feat(ml-review-video): persist render worker policy"`. 이 단계는 정책·준비·재개 기능 자체로 테스트 가능한 결과이며 실제 workers 반영은 Task 3의 결과다.

### Task 3: 장면 캐시·쌍 복구·폰트 준비와 생산 연결

**Files:** Modify `S/scripts/lib/{render,composition,state}.py`, `S/scripts/video.py`, `S/tests/{test_render,test_composition,test_state,test_revoice,test_restore}.py`, `S/SKILL.md`, `S/references/rendering-and-verification.md`; Create `S/tests/test_render_cli.py`, `S/assets/render-port-provenance.json`. 필요할 때만 revoice.py 수정.

**Interfaces:** Consumes Task 2 정책과 기존 cache/PCM/timeline. Produces EC2 동결 시그니처 `cpu_backend(entry,options) -> dict`, `render_parts(parts,run,backend) -> list[Path]`, `commit_media_receipt(pending,data,media,receipt) -> None`, `mux_with_receipt(parts,audio,timeline,destination,backend,*,captured=None) -> Path`; 기존 `probe_backends`, `mux`, `render_revoice` signature 유지. source 변경을 음성 approval로 대체하지 않는다.

- [x] **Step 1: 실패 검사 작성.** EC2 CapturePolicyTest/FailureSafetyTest를 ML에 맞춰 이식. test_options_affect_cache_key/test_renderer_font_html_change_invalidates/test_cache_hit_avoids_render/test_corrupt_receipt_rerenders/test_30fps_required/test_scene_and_master_pair_rollback/test_interrupt_restore/test_rollback_failure_blocks_retry/test_timeout_kills_detached_descendant 추가. 아래와 같은 결과를 assert한다.

```python
self.assertEqual(record['render_options']['workers'], 6)
self.assertIn('--experimental-fast-capture=false', record['args'])
self.assertEqual(render_call_count_after_cache_hit, render_call_count_before)
self.assertEqual(old_media.read_bytes(), before_media)
self.assertEqual(old_receipt.read_bytes(), before_receipt)
self.assertFalse(pending.exists())
```

timeout 검사는 실제 테스트 자식/분리 세션 손자 PID의 종료·직계 프로세스 reap를 확인한다. rollback 실패에서는 사본 바이트 유지·경로가 오류에 포함·재교체 없음. test_fonts_ready_precedes_timeline_registration과 composition tool fingerprint 변경→composition 재개/voice 불변 추가. test_render_cli에 실제 parser+mock 도구로 `test_render_and_revoice_forward_workers`, `test_cli_never_probes_gpu`, `test_prepare_from_run_preserves_saved`, `test_option_change_resumes_render`, `test_revoice_retime_only_captures_nothing`을 추가한다. rerender selected scene만 workers4 전달, captured=[] 허용, GPU probe 호출0, 음성/WAV와 composition 지문 불변을 assert한다.
- [x] **Step 2: RED 확인.** `python3 -m unittest discover -s .agents/skills/ml-review-video/tests -p test_render.py -v` → 새 계약 FAIL; 기존 회귀 결과와 분리한다.
- [x] **Step 3: 렌더 부품 이식.** EC2 동결 render.py의 CPU backend/순차 cache/UUID pending/프로세스 종료/쌍 복구/기록을 이식한다. render/revoice parser에 --render-workers type=int/choices=range(1,7)을 추가하고 RunStore.recover 전에 옵션 검증·저장. CLI를 cpu_backend·mux_with_receipt에 연결; render 출력에 master+receipt 등록. render에서는 저장된 timeline을 읽어 설정 때문에 재작성하지 않는다. revoice의 새 음성에 따른 기존 retime은 유지하되 옵션만으로 재합성하지 않는다. retime 창은 captured 목록에서 제외. revoice 원본 hash/독립 RUN/형제 게시 계약 보존.
- [x] **Step 4: 폰트 준비·지문 구현.** ML math_render/fragment 검증을 유지하며 document.fonts.ready 이후 GSAP timeline 구성·등록. composition.py hash를 composition 지문에 추가하고 이 변화만 한 번 재조립을 요구. workers 변경은 composition을 무효화하지 않는다.
- [x] **Step 5: provenance·설명 갱신.** restore manifest 기준값은 보존; render-port manifest에 EC2 full commit과 파일별 source/destination/source_sha256/ported_sha256/test_evidence, ML 자체 수정 목록 기록. test_restore는 수정 파일의 원본 SHA/현재 port hash 모두 검증한다. SKILL/references의 기존 자동 CPU/NVENC probe 안내를 CPU 고정 정책/기록/복구로 교체한다.
- [x] **Step 6: GREEN 확인.** 전체 `python3 -m unittest discover -s .agents/skills/ml-review-video/tests -v` 및 `python3 /Users/hyunjun_macbook_pro/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/ml-review-video` → PASS/Skill is valid!; 새 CLI 검사도 PASS. 수식·SSE 계산·selection·기존 revoice·자막 회귀를 포함한다. 다른 과목 runtime import/path가 없는지 검사한다.
- [x] **Step 7: 체크포인트 커밋.** Files의 실제 수정 파일만 stage; `git commit -m "feat(ml-review-video): render sequential scenes with verified workers"`.

### Task 4: ML 수식·그래프 성능과 정확도 수용 검사

**Files:** Create `S/tests/render_performance_acceptance.py`, `S/tests/test_render_acceptance_inputs.py`, `docs/superpowers/reports/2026-10-11-ml-review-render-performance.md`; Modify `S/references/rendering-and-verification.md`.

**Interfaces:** Consumes `tests/integration_smoke.py`의 ML regression/SSE author 방식과 생산 assemble/render_parts/mux_with_receipt/burn_subtitles. Produces `run_acceptance(destination: Path, hyperframes_entry: Path, *, motion_duration: float = 0.6) -> dict`; CLI `--destination --hyperframes-entry --motion-duration` (0.6 또는24). JSON `technical_complete/metrics/frames_equal/pcm_equal/aac_equal/source_unchanged/paid_requests=0/published=false`.

- [x] **Step 1: RED 작성·확인.** test_destination_nonempty/test_invalid_cli_path/test_no_paid_voice_or_publish/test_motion_duration_outside_contract/test_frame_difference_is_failure; 빈 입력/겹치는 경로는 렌더/쓰기 0, frame 차이는 technical_complete=false, 유료/게시 호출은 AssertionError. `python3 -m unittest discover -s .agents/skills/ml-review-video/tests -p test_render_acceptance_inputs.py -v` → harness 부재 FAIL.
- [x] **Step 2: harness 구현.** integration_smoke의 (0,0),(1,1),(2,2), w=0/1/2, SSE=5/0/5와 분수/첨자 수식을 사용해 실제 ML template/GSAP/KaTeX/폰트로 60초/2장면을 구성한다. 각 장면 30초이며 motion은 해당 발화 slot 안에서 0.6초 또는24초. fixture/calculation/math-evidence/source SHA를 동결하고 synthetic PCM만 사용한다. workers2/6을 순차 실행하고 모든 frame MD5·혼합 WAV·추출 AAC·원본 hash·영수증을 대조한다. captions를 별도 scratch에 굽고 전체 decode/하단 영역 확인. static 재사용에 따른 느려짐도 metrics에 그대로 남긴다.
- [x] **Step 3: 단위 GREEN 확인.** Step 1 명령 → PASS. paid/publish 호출0, fixture hash 불변.
- [x] **Step 4: 실제 정적·동적 시험 실행.** `python3 .agents/skills/ml-review-video/tests/render_performance_acceptance.py --destination <새 제작자료/static> --hyperframes-entry <실제 절대 CLI> --motion-duration 0.6`, 이어 같은 명령의 새 destination `<새 제작자료/dynamic>`와 `--motion-duration 24`. 두 결과 technical_complete=true/전체 frame·PCM·AAC 동일/원본 불변이 완료 기준. 처음/중간/끝 수식·축·단위·그래프 PNG를 직접 확인한다. 실패를 고속 캡처/다른 GPU 정책/오차 완화로 숨기지 않는다.
- [x] **Step 5: 최종 회귀·보고·커밋.** 최종 변경이 있으면 Task 3 GREEN을 반복한다. 보고서에 두 조건의 workers2/6 시간·frame/hash·버전·실제 명령·그림 확인·synthetic/live_audio=unverified·실패 한계를 기록한다. 코드·문서만 stage; `git commit -m "test(ml-review-video): compare multicore ML math and graph renders"`. 미디어·env·캐시·원자료 제외. merge/push/게시 여부는 사용자 후속 지시에 따른다.

실행 결과와 세부 판단/한계: `../reports/2026-10-11-ml-review-render-performance.md`. 구현은 codex/ml-render-performance에 완료하며 merge/push는 후속 선택이다.
