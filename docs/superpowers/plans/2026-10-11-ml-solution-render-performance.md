# ML Solution Video Multicore Render Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 풀이영상의 단일·여러 페이지 경로에 EC2 멀티코어 설정과 실패 복구를 적용한다.

**Architecture:** ML 내부에 독립 렌더 정책을 추가하고 기존 media 렌더러·두 CLI 경로에 연결한다. 옵션과 기록은 render 단계에만 귀속시키며 최초 EC2 이식 provenance는 보존한다. 개념 복습영상 계획과는 실행 의존성이 없다.

**Tech Stack:** Python unittest, Node/로컬 HyperFrames, Chrome, FFmpeg/libass, PyMuPDF, Pillow, 기존 GSAP/Pretendard.

**Spec:** `docs/superpowers/specs/2026-10-11-ml-render-performance-design.md`의 전역·풀이영상 계약. 개념 복습영상은 `2026-10-11-ml-review-render-performance.md`로 별도 구현한다.

## Global Constraints

- Darwin / Apple M5 / 물리 CPU 10코어 / 메모리 16GiB 이상 workers=6, 기타 환경·탐지 실패 workers=2.
- workers는 정수 1–6. config는 schema_version=1/encoder=cpu/browser_gpu=auto/fast_capture=false와 workers의 다섯 키만 허용.
- CLI → 유효 저장값 → 호스트 기본값. 손상된 저장값을 override로 숨기지 않는다.
- CPU 인코딩·브라우저 GPU auto·`--experimental-fast-capture=false`·delivery 1920×1080/30fps·mono PCM 24kHz 유지.
- 파트·문항은 순차 처리. 옵션 변경은 render 이후만 무효화하며 WAV·대본·타임라인·composition을 유지.
- resume-set은 기존 RUN에 설정을 쓰지 않는다. 기존 승인/단계 지문 우회 금지.
- 예외·Ctrl+C 시 이전 마스터/기록 복구. 복구 실패는 `.rollback` 보존·재시도 차단.
- 풀이영상 PDF·수학 검토·페이지·연필·자막·게시 구조 유지. 유료 TTS·자동 게시·push·전역 설치 제외.
- 실행 시 using-git-worktrees로 분리하고 현재 변경·미추적 파일을 보존한다. 이 계획 작성 턴에서는 구현·커밋하지 않는다.

## Review Focus

1. 기존 RUN/호스트 이동: 저장 workers 유지, resume-set에서 파일 생성 없음 — Task 1/3.
2. JSON bool/실수/문자열/손상 파일: 외부 명령 실행 전 오류, override로 은폐 없음 — Task 1/2.
3. version 2 bundle과 이전 single 경로: 둘 다 설정 전달·기록·재개가 동일 — Task 3.
4. 후반 파트 실패/기록 교체 중 interrupt/복구 실패: 이전 마스터와 복구 사본 보존 — Task 2.
5. 여러 페이지 초기/경계 프레임 raster 차이: 전체 프레임 비교 실패를 숨기지 않음 — Task 4.

---

## File Structure

`S=.agents/skills/ml-solution-video`. 생성: `S/scripts/solution_video/render_options.py`, `S/tests/test_render_options.py`, `S/tests/test_render_cli.py`, `S/tests/render_performance_acceptance.py`, `S/tests/test_render_acceptance_inputs.py`, `S/assets/render-port-provenance.json`. 수정: `S/scripts/solution_video/{media,state,bundle_cli}.py`, `S/scripts/video.py`, `S/tests/{test_media,test_state,test_ml_port}.py`, `S/SKILL.md`, `S/references/verification.md`, `S/assets/port-provenance.json`. 전체 스킬을 EC2 버전으로 덮지 않는다.

## 준비

- [x] `git status --short`, `git rev-parse HEAD`, `git cat-file -t 75a6a581d7b66651d361856fa1bfa35bc85f20b8`을 EC2 저장소에서 확인하고 스킬 소스만 해당 Git 객체에서 읽는다. 로컬 변경이 있는 다른 과목 파일은 가져오지 않는다.
- [x] 실행 worktree를 확보하고 Python/Node/HyperFrames/Chrome/ffprobe/libass 경로와 버전을 보고서에 기록한다. 버전을 자동 업그레이드하지 않는다. 기존 baseline 전체 회귀 결과를 기록한다.

### Task 1: 독립 렌더 옵션 정책

**Files:** Create `S/scripts/solution_video/render_options.py`, `S/tests/test_render_options.py`.

**Interfaces:** Consumes `solution_video.contracts.InputError`, `util.read(Path)`. Produces `detect_hardware() -> dict`, `default_render_options(hardware: dict | None = None) -> dict`, `validate_render_options(options: dict) -> dict`, `load_render_options(run: Path, workers: int | None = None, *, hardware: dict | None = None) -> dict`.

- [x] **Step 1: 실패 검사 작성.** 다음 assertions와 저장값 우선순위/읽기 전용/정확한 키 집합 검사를 추가한다. `load_render_options` 호출 전후 파일 목록·hash가 같아야 한다.

```python
self.assertEqual(default_render_options(dict(platform='darwin', chip='Apple M5', cpu_cores=10, memory_bytes=16*1024**3))['workers'], 6)
self.assertEqual(default_render_options(dict(platform='unknown'))['workers'], 2)
for workers in (True, 2.0, '6', 0, 7):
    with self.assertRaises(InputError):
        validate_render_options(dict(default_render_options({}), workers=workers))
```

- [x] **Step 2: RED 확인.** `python3 -m unittest discover -s .agents/skills/ml-solution-video/tests -p test_render_options.py -v` → 정책 모듈 부재로 FAIL.
- [x] **Step 3: 최소 구현.** EC2 동결 `render_options.py`를 이식한다. 저장 파일을 먼저 검증한 뒤 workers override; load 자체는 쓰지 않는다. 탐지 sysctl 세 항목과 2초 timeout을 유지한다.
- [x] **Step 4: GREEN 확인.** Step 2 명령 → 모든 정책 검사 PASS. 손상 JSON+override에서도 InputError이며 command 호출 0인지 확인한다.
- [x] **Step 5: 체크포인트 커밋.** 정확히 위 두 파일만 stage; `git commit -m "feat(ml-video): add independent render worker policy"`.

### Task 2: 생산 렌더러와 복구 기록

**Files:** Modify `S/scripts/solution_video/media.py`, `S/tests/test_media.py`.

**Interfaces:** Consumes Task 1 함수와 기존 `util.command/checked/local/write/file_hash`. Produces `render_master(parts: list[dict], timeline: dict, audio: list[dict], run: Path, hyperframes_entry: Path, *, render_options: dict | None = None) -> Path`; `_validate_media(path: Path, frames: int, *, audio: bool = False) -> None`; `_commit_master_and_receipt(master_pending: Path, receipt_data: dict, master: Path, receipt: Path) -> None`. 기존 5개 위치 인자는 유지.

- [x] **Step 1: 실패 검사 작성.** EC2 `RenderOutputTests`를 ML Sandbox에 이식하고 아래 결과를 assert한다. 외부 도구는 mock하되 테스트 WAV는 실제 mono24kHz로 생성한다.

```python
# test_saved_options_drive_execution_and_receipt
self.assertEqual(args[args.index('--workers') + 1], '6')
self.assertIn('--experimental-fast-capture=false', args)
self.assertNotIn('--gpu', args)
self.assertEqual(receipt['options']['workers'], 6)
self.assertEqual(receipt['master_sha256'], file_hash(master))
# test_later_part_failure_preserves_master_and_completed_part
self.assertEqual(file_hash(master), before_master)
self.assertEqual(file_hash(receipt_path), before_receipt)
self.assertEqual(file_hash(completed_part), successful_part_hash)
```

동일 테스트 파일에 `test_invalid_options_before_source_checks`, `test_wrong_dimensions_fps_frames`, `test_receipt_write_failure`, `test_interrupt_between_pair_replacements`, `test_failed_restore_keeps_backup`, `test_retry_blocks_unresolved_backup`, `test_stale_pending_not_accepted`를 추가한다. 각 실패에서 이전 파일 byte equality, 실패 pending 부재, log 존재를 assert; 복구 실패에서는 rollback hash 유지와 다음 교체 시도 0을 assert한다.

- [x] **Step 2: RED 확인.** `python3 -m unittest discover -s .agents/skills/ml-solution-video/tests -p test_media.py -v` → 옵션 인자/기록/복구 계약 검사 FAIL.
- [x] **Step 3: 최소 구현.** EC2 media 변경을 ML_FFMPEG 관례와 기존 PCM 배치에 맞춰 이식한다. source check 이전 옵션 검증; 파트 pending→규격 검사→교체; master pending→영상+음성 검사→기록과 복구 교체. 기록 키는 spec 그대로. 예외와 BaseException 교체 복구 경계를 보존한다.
- [x] **Step 4: GREEN 확인.** Step 2 명령 → PASS. 기존 자막·PCM 배치 검사도 PASS.
- [x] **Step 5: 체크포인트 커밋.** 정확히 media.py/test_media.py stage; `git commit -m "feat(ml-video): preserve outputs and record multicore renders"`.

### Task 3: 두 CLI 경로·단계 지문·이식 이력 연결

**Files:** Modify `S/scripts/video.py`, `S/scripts/solution_video/{bundle_cli,state}.py`, `S/tests/{test_state,test_ml_port}.py`, `S/assets/port-provenance.json`, `S/SKILL.md`, `S/references/verification.md`; Create `S/tests/test_render_cli.py`, `S/assets/render-port-provenance.json`.

**Interfaces:** Consumes Tasks 1/2. Existing `prepare_batch(...) -> Path`, `run_stage(action,run,args,transport=None) -> dict`, `run_bundle_stage(action,run,args,transport=None) -> dict`, `stage_fingerprint(run,stage) -> str`, `recover_run(run) -> str | None` signatures unchanged. render JSON adds `render_options: dict`, `render_receipt: str`.

- [x] **Step 1: 실패 검사 작성.** CLI main를 실제 parser로 호출하며 생산 renderer만 mock한다. `test_single_and_bundle_override_reaches_renderer`는 두 pair schema마다 workers=4 전달·설정 저장·기록 경로 반환·render 출력에 두 파일 등록을 assert. `test_prepare_bundle_saves_default`, `test_resume_does_not_create_options`, `test_malformed_options_not_hidden_by_cli`, `test_options_only_invalidate_render`를 추가한다.

```python
for stage in ('inputs','layers','script','voice','timing','composition'):
    self.assertEqual(before[stage], stage_fingerprint(run, stage))
self.assertNotEqual(before['render'], stage_fingerprint(run, 'render'))
self.assertEqual(recover_run(run), 'render')
self.assertEqual(file_hash(wav), before_wav)
```

- [x] **Step 2: RED 확인.** `python3 -m unittest discover -s .agents/skills/ml-solution-video/tests -p test_render_cli.py -v`와 `python3 -m unittest discover -s .agents/skills/ml-solution-video/tests -p test_state.py -v` → 신규 계약 FAIL, 기존 검사 PASS.
- [x] **Step 3: 연결 구현.** parser render에 type=int/choices=range(1,7). bundle prepare에 default 저장; 두 render handler에서 prerequisite recover 전에 load/저장, renderer에 전달, finish_stage에 master+receipt 등록. render FACTORS에 `source/render-options.json`, MODULES에 render_options만 추가. util/contracts나 voice config를 변경하지 않는다.
- [x] **Step 4: 문서·provenance 갱신.** 최초 기준 commit/84개 baseline 목록을 유지하고 수정된 row의 ported_sha256·test_evidence를 갱신한다. 신규 render-port-provenance는 schema_version=1/source_commit/파일별 source·destination·source_sha256·ported_sha256·test_evidence를 포함한다. 스킬 문서에 기본값·override·복구·순차 실행·음성 보존을 명시한다.
- [x] **Step 5: GREEN 확인.** 전체 `python3 -m unittest discover -s .agents/skills/ml-solution-video/tests -v`, `node --test .agents/skills/ml-solution-video/tests/test_writing_runtime.cjs .agents/skills/ml-solution-video/tests/test_teaching_runtime.cjs`, `python3 /Users/hyunjun_macbook_pro/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/ml-solution-video` → 회귀 PASS, `Skill is valid!`. test_ml_port는 최초 commit 불변·새 manifest hash 일치를 검사한다.
- [x] **Step 6: 체크포인트 커밋.** 위 Files의 정확한 파일들만 stage; `git commit -m "feat(ml-video): wire workers into single and bundle render flows"`.

### Task 4: ML 여러 페이지 실렌더 수용 검사

**Files:** Create `S/tests/render_performance_acceptance.py`, `S/tests/test_render_acceptance_inputs.py`, `docs/superpowers/reports/2026-10-11-ml-solution-render-performance.md`; Modify `S/references/verification.md`.

**Interfaces:** Consumes 생산 render_master와 frozen composition/parts/timeline/audio/PCM. Produces `run_acceptance(fixture: Path, destination: Path, hyperframes_entry: Path) -> dict`; CLI `--fixture --destination --hyperframes-entry`; JSON `technical_complete`, `metrics`, `frames_equal`, `pcm_equal`, `aac_equal`, `source_unchanged`, `paid_requests=0`, `published=false`.

- [x] **Step 1: 실패 검사 작성.** `test_missing_input_fails_before_render`, `test_destination_overlaps_fixture`, `test_destination_nonempty`, `test_requires_multiple_pages`, `test_source_hash_change_fails_acceptance`: 사전 오류에서는 외부 호출/쓰기=0, hash 차이는 technical_complete=false를 assert한다. `python3 -m unittest discover -s .agents/skills/ml-solution-video/tests -p test_render_acceptance_inputs.py -v` → 모듈 부재 FAIL.
- [x] **Step 2: 수용 harness 구현.** EC2 acceptance의 직접 생산 renderer 호출 방식을 재사용하되 P10.72/7220 하드코딩을 제거한다. 동결 ML fixture의 실제 total_frames 사용, 여러 page_id 존재 확인. fixture 밖의 새 destination에 복사하여 workers2/6 순차 실행; paid voice/publish 호출은 AssertionError로 차단한다. 각 마스터 전체 framemd5/PCM/AAC와 source hash 비교. stdout/JSON에 두 시간과 frame 수를 기록한다.
- [x] **Step 3: 단위 검사 GREEN 확인.** Step 1 명령 → PASS. 입력 오류시 유료/렌더 호출 0.
- [x] **Step 4: 실제 입력 확보.** 기존 `2026-10-10-ml-solution-video.md` 보고서의 acceptance-final 여러 페이지 RUN을 확인하고 composition/parts/timeline/audio/PCM을 동결 복사한다. 없으면 `tests/ml_acceptance.py --repo <ML_REPO> --dest <새 scratch> --hyperframes-entry <실제 CLI>`를 --live 없이 실행해 생성한다. synthetic/paid0/게시 차단을 확인한다. stale 승인 파일을 생산 CLI에 덮어쓰지 않는다.
- [x] **Step 5: 실렌더 실행.** `python3 .agents/skills/ml-solution-video/tests/render_performance_acceptance.py --fixture <동결 RUN> --destination <새 제작자료 scratch> --hyperframes-entry <검증한 절대 CLI>` → technical_complete=true, 모든 프레임/PCM/AAC 동일, source_unchanged=true. 페이지 전환 전후와 처음/중간/끝 PNG를 직접 보고 기존 자막 경계를 확인한다. raster 불일치면 원인 조사; 허용오차 완화/브라우저 정책 변경으로 통과시키지 않는다.
- [x] **Step 6: 보고·최종 회귀·커밋.** Task 3 GREEN 명령을 최종 변경이 있을 때 재실행한다. 보고서에 실제 명령·버전·해시·프레임·시간·synthetic 한계·완료/실패를 기록한다. 코드/문서만 stage하고 `git commit -m "test(ml-video): verify multicore output parity on ML pages"`; 미디어는 stage하지 않는다. merge/push/게시 여부는 별도 사용자 지시에 따른다.

실행 결과와 세부 판단/한계: `../reports/2026-10-11-ml-solution-render-performance.md`. 구현은 codex/ml-render-performance에 완료하며 merge/push는 후속 선택이다.
