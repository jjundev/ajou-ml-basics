# ML Solution Video Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** ML 복습문제 PDF 원본을 단계별 연필·한국어 설명·기호 자막으로 공개하는 독립 ml-solution-video 제작기를 만든다.

**Architecture:** EC2 고정 커밋의 공통 엔진·자산·검사를 ML 안에 포트한다. 과목 입력·수학 검토를 교체하고, 페이지별 기존 공개 엔진 위에 문항 전체의 페이지·단계·음성 타임라인을 둔다. 실제 입력은 동결하고 게시 전 원문·현재 해시·실청취 근거를 검증한다.

**Tech Stack:** Python 3.11+(TypedDict/NotRequired), unittest, PyMuPDF, Pillow, Node.js, GSAP, HyperFrames, puppeteer-core/Chrome, libass FFmpeg, Pretendard, Vertex AI Express TTS, SHA256/JSON/POSIX 파일 잠금. 설치된 Python과 패키지 조합은 실행 시작에 확인한다.

**Spec:** [확정 설계](/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/docs/superpowers/specs/2026-10-10-ml-solution-video-design.md). 실행자는 먼저 설계와 이 계획을 함께 읽는다.

## Global Constraints

- EC2 source commit은 `eeec3d56513fe9e8a34f45edb05ae1118b08cf62`다. 최신 HEAD로 자동 바꾸지 않는다.
- 스킬 위치는 `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video`; 실행 중 EC2 checkout 또는 EC2 review-video를 요구하지 않는다.
- 기존 입력·과목 스킬·다른 과목 파일을 수정하지 않는다. 현재 ml-review-video의 pyc 캐시는 실행 근거가 아니다.
- 기본은 PDF 원본 공개+설명·주석, 날짜의 모든 문제다. 새 문제·답안·대체 유도·원본에 없는 그래프를 생성하지 않는다.
- 1920×1080/30fps, 기본 원본 PDF 1440×810pt, 하단 180px(900≤y≤1080) 자막 영역. 1920×900으로 다시 축소하지 않는다.
- 신규 기본 pencil, 7.5 chars/sec, 연필 길이 160px. 본문·label 최소 26px, 카메라 이동 12프레임. A4 가로는 기존 profile의 비율 유지로 호환한다.
- 원본 도형별 작성 프레임은 `min(90,max(18,ceil(W/H×글자간격프레임)))`, clip 폭으로 배분, 조각당 최소 1프레임이다.
- 주석 굵기는 유한수 2–12px, 생략값 3px, 저작 기본 보조4/중요관계6/결과강조8px다. move8프레임+작성은 실측 청크 안, 카메라 복귀 전(segment end−13)에 완료한다.
- 기본 Vertex AI Express / gemini-2.5-flash-tts / Aoede / ko-KR / mono PCM 24kHz/16bit. 자동 공급자·모델 대체 없음. 예산 기본 null, 최대 시도4/동시 요청2다.
- spoken-text-only-v1, pcm-chunks-v1. cue 최대 두 줄/줄당34자, SRT 오차≤1ms/표시 경계≤1프레임. 임의 연결 무음·자동 에너지 절단 없음.
- libass `WrapStyle=2, BorderStyle=4, Outline=0, Shadow=4`, Pretendard Bold/FontSize14/Alignment2/MarginV14를 유지한다.
- 정적 SVG pixel/non-target/hidden leak=0, 두 requestAnimationFrame 후 캡처, 정적 게이트에만 disable-gpu. teaching browser만600초/다른 browser120초다.
- 실제 청취가 없으면 complete=false/live_audio=unverified이며 publish/latest를 승인하지 않는다. 2초 초과 필기 지연은 현재 hash의 writing_lags 검토를 요구한다.
- 최종 MP4와 제작자료 폴더만 공개 날짜 폴더에 둔다. 성공 형제 결과·raw WAV·이전 결과를 보존하고 latest는 전체 성공 때만 갱신한다.
- 이번 턴은 문서 작성만이다. 구현은 검토 후 실행 방법을 정한 다음 시작한다. 실행 때 using-git-worktrees로 격리 상태를 확인한다. 아래 Commit 단계는 별도 커밋 요청이 없으면 보류 표시하고 다음 작업으로 진행한다. push/merge는 범위 밖이다.

## Review Focus

1. NFC/NFD 경로·여러 날짜의 P1·여러 팩: identity를 분리하고 모호한 선택을 실패시킨다. Task2 `test_unicode_pack_identity_and_ambiguity`.
2. Hint 부록·조건이 나뉜 계속 페이지·문제/답안 페이지 수 차이: 부록은 제외하고 문항 전체를 원문 순서로 묶는다. Task2 `test_continuation_and_hint_mapping` 및 Task3 `test_all_pages_and_final_answer_coverage`.
3. 그래프/행렬/분수·도형-only·이미 공개된 식으로 복귀: 재조판·선공개·26px 오용 없이 seek 상태가 같다. Task3/6 `test_seek_across_pages_and_visible_equation_focus`.
4. 자막-only/retime/수동 trim/스냅샷·주석·폰트 변조: 현재 근거를 무효화하되 같은 발화 WAV를 재사용한다. Task5/7 `test_caption_retime_trim_and_stage_invalidation`.
5. 문항 실패·실청취 불가·출력 제목 충돌·게시 중 교체 실패: 성공 형제/기존 결과 보존, latest 유지, 완료 주장 금지. Task8 `test_partial_publish_and_rollback` 및 `test_unlistened_audio_cannot_publish`.

---

## Port Baseline

고정 소스 저장소: `/Users/hyunjun_macbook_pro/Documents/Univ/전자회로2`. 최초 포트는 worktree 파일 복사 대신 commit의 git blobs를 읽는다. `.agents/skills/ec2-solution-video/`의 전체 84파일 외에 같은 커밋의 `.agents/skills/ec2-review-video/scripts/lib/{__init__,cache,budget,vertex_tts}.py`, `assets/fonts/Pretendard-Bold.ttf`, `assets/runtime/vendor/gsap.min.js`를 포함한다. 라이브 리뷰용 EC2 영상·키·pyc는 입력이 아니다.

## File Structure

아래 표는 실제 생성 디렉터리와 그 안의 정확한 파일 이름을 지정한다. 모든 신규 코드는 /Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video 안에만 만든다. 포트 파일의 변경 전 bytes는 git object에서 읽고 provenance에 기록한다.

| 디렉터리(절대 경로) | 파일과 책임 |
|---|---|
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video` | `SKILL.md`: 호출/조건/실행 라우팅. 기존 84개 tracked 파일 전체를 포트 대상으로 목록화한다. |
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/agents` | `openai.yaml`: ML 전용 표시/자동 선택. |
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/assets` | `defaults.json`, `writing-defaults.json`, `port-provenance.json`, `layout.css`, `camera.js`, `player.js`, `writing.js`, `pencil.js`, `annotations.js`: 설정·출처·재현 가능한 공개. |
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/assets/pencil` | `pencil-yellow-v1.png`, `pencil-yellow-v1.json`, `pencil-yellow-v1.prompt.txt`: 같은 연필·촉 좌표·제작 근거. |
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/assets/fonts`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/assets/runtime/vendor` | `Pretendard-Bold.ttf`, `gsap.min.js`: 자체 포함 자산. |
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts` | `video.py`: 기존 단계 CLI. `port_baseline.py`: 고정 git blob 포트/목록/SHA 확인, `.env`와 출력영상은 복사하지 않음. |
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/solution_video` | `__init__.py`, `contracts.py`, `util.py`, `page_layout.py`: 타입·도구·profile. `sources.py`, `ml_cards.py`, `page_pairs.py`: 카드·선택·페이지·동결. |
| 같은 모듈 디렉터리 | `pdf_pages.py`, `writing_units.py`, `bundle_layers.py`: 페이지별 PDF 원본 공개와 문항 전체 coverage. `manifest.py`, `math_review.py`, `lesson.py`: 원문 대응·수학 근거·설명 순서. |
| 같은 모듈 디렉터리 | `review_adapter.py`, `speech_tts.py`, `speech_chunks.py`, `subtitles.py`, `reveal.py`, `shape_timing.py`, `narration_pacing.py`, `bundle_timeline.py`: 자체 TTS·실측 타이밍·필기·자막. |
| 같은 모듈 디렉터리 | `writing.py`, `writing_camera.py`, `annotations.py`, `focus.py`, `teaching.py`, `composition.py`, `media.py`: 연필·강조·페이지 전환·렌더. `state.py`, `verify.py`, `publication.py`: 현재 상태·검증·보존 게시. |
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/solution_video/vendor_tts` | `__init__.py`, `cache.py`, `budget.py`, `vertex_tts.py`: EC2 review-video의 필요한 네 파일을 같은 기준 커밋에서 복사. 내부 정적 import, sibling private package 이름 의존성 제거. |
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/references` | `pdf-and-coverage.md`, `narration-and-timing.md`, `verification.md`: 해당 작업 때 읽는 ML 지침. |
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests` | 기존 84파일 목록의 Python/JS 검사 모두 포트하고 EC2 source-specific fixture는 ML 임시 fixture로 교체. `fixtures.py`, `ml_fixtures.py`, `ml_acceptance.py`, `test_ml_port.py`, `test_ml_sources.py`, `test_bundle_layers.py`, `test_math_review.py`, `test_bundle_timeline.py`, `test_ml_cli.py`, `test_ml_publication.py`를 추가. |
| `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/docs/superpowers/reports/2026-10-10-ml-solution-video.md` | 실행 시의 baseline 대응, 테스트 결과·skip, 실제 PDF/음성 검증 범위·미해결을 기록. |

## Shared Interfaces

`contracts.py`의 새 문항 계약은 schema_version=2다. 기존 단일 페이지 core의 schema_version=1은 내부 page view로만 유지한다. 전역 참조 문자열은 `page_id::local_id`; 서로 다른 페이지의 g00001을 섞지 않는다.

- `PageRef`: `{id:str, role:'problem'|'answer', snapshot:str, page_index:int, width_pt:float, height_pt:float, continuation:int}`.
- `ReviewCard`: `{id:str,title:str,source:str,conditions_html:str,ask_html:str,steps:list[str],answer_html:str,figure_paths:list[str]}`. card.id는 Pn, title은 원본 h3, source는 MML 표기다.
- `ProblemBundle`: `{schema_version:2,key:str,pack_id:str,range:str,slug:str,problem_id:str,title:str,mml_source:str,problem_pages:list[PageRef],answer_pages:list[PageRef],source_files:dict[str,str],card:ReviewCard}`. source_files의 키는 html/md/problem_pdf/answer_pdf 및 `figure:<relative>`/`evidence:<relative>`다. 발견 시 절대 경로, 동결 후 RUN 상대 경로다.
- `BundleMap`: `{schema_version:2,pages:dict[str,dict],step_order:list[str],answer_step_id:str}`. pages의 값은 `{work_bbox,steps,terminal_step_id}`; 각 step은 기존 local glyph_ids/shape_ids/writing_units를 가진다.
- `BundleLayers`: `{schema_version:2,page_order:list[str],pages:dict[str,dict],step_order:list[str],answer_step_id:str}`. pages의 값은 기존 PageLayers이며 step_order/answer_step_id는 전역 참조다.
- 전역 manifest: `{schema_version:2,key,pack_id,problem_id,title,segments,reveal_order,shape_anchors,cameras,caption_timing:'pcm-chunks-v1'}`. 모든 segment는 page_id를 가진다. reveal_order/shape_anchors/step_id는 전역 참조다. 문제/이유/작성/검산/summary kind는 기존 이름을 유지한다.
- BundleTimeline: 기존 timeline 필드+`schema_version:2,page_spans:list[{page_id,start_frame,end_frame}]`; events/spans는 page_id와 전역 id를 가진다. page_spans는 인접 겹침 없는 구간이며 같은 페이지 재방문을 허용한다.
- 전역 teaching `{schema_version:2,regions,cues,items}`는 각 region의 page_id와 source_sha256을 갖는다. 원본별 좌표는 PDF point다. segment/page 연결과 이미 공개된 식인지 검사한다.
- `SourceFailure`: `{key:str|None,pack_id:str,problem_id:str|None,reason:str}`. 실패 수집 모드에서는 잘못된 문항만 기록하고 다른 문항을 계속한다.

source_refs는 설계의 `html:<snapshot>#pN`, `md:<snapshot>#pN`, `pdf:<snapshot>#page=N`(1-based), `figure:<snapshot>` 형식을 사용한다. 공통 test fixture 변수는 setUp에서 읽은 입력/지도/검토 객체를 뜻하며 테스트마다 독립 copies를 사용한다.

테스트 공통 fixture API: `make_ml_repo(dest:Path, *, dates:tuple[str,...]=('1007',), continuations:bool=False, a4:bool=False, ambiguous:bool=False)->Path`; 작은 두 카드 P1/P2, 저장 HTML/MD, 대응 PDF/Hint 부록을 생성한다. `make_bundle_run(dest:Path, *, answer_pages:int=1)->Path`는 Task3에서 추가하며 schema2 입력·지도·후속 저작 검토용 원문을 만든다. 기존 `Sandbox`, `make_audio(segment_id,samples,run)`는 유지한다. 테스트 WAV는 synthetic이다.

공통 테스트 명령은 독립 `exec`마다 다음 변수를 다시 설정한다: `S='/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video'; T="$S/tests"`. 전용 모듈 실행은 `PYTHONPATH="$S/scripts:$T" python3 -m unittest discover -s "$T" -p '<정확한파일명>' -v`. 기대 결과 OK, skip은 PASS로 세지 않는다. 아래 테스트 블록은 해당 unittest class 메서드 안의 핵심 assertions다.

### Task 1: 고정 포트와 자체 실행 부품

**Files:** Create 위 표의 기존 EC2 84파일 대상, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/port_baseline.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/solution_video/vendor_tts/`의 네 파일, 폰트·GSAP, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_ml_port.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/ml_fixtures.py`. Modify 신규 포트 안의 `contracts.py`, `util.py`, `review_adapter.py`, `publication.py`, defaults 및 sibling 자산 경로.

**Interfaces:** Consumes 고정 git commit. Produces Shared Interfaces의 타입, `port_baseline(source_repo:Path, dest:Path, commit:str)->dict`와 `validate_port_manifest(skill:Path)->dict`(keys commit/files/valid), `make_ml_repo(...)`. 기존 `generate_voice(segments,run,config,ledger,transport=None,env_file=None)`의 호출 규격은 유지한다.

- [ ] **1. 실패 테스트 작성:** `test_frozen_port_runs_without_ec2_checkout`는 source git blob과 초기 destination bytes SHA를 비교하고, 임시 독립 destination에서 local TTS/cache/budget import·JSON defaults·font/GSAP/pencil 로딩을 검사한다.
  ```python
  result = validate_port_manifest(skill)
  self.assertEqual(result['commit'], 'eeec3d56513fe9e8a34f45edb05ae1118b08cf62')
  self.assertTrue(result['valid'])
  self.assertEqual(default_writing()['chars_per_second'], 7.5)
  self.assertEqual(default_config()['voice'], 'Aoede')
  self.assertNotIn('direction', str(make_speech_payload('평균을 구해요.', default_config())))
  ```
- [ ] **2. RED 실행:** 공통 명령 `-p test_ml_port.py`. 구현 전 module/파일 누락 FAIL을 확인한다.
- [ ] **3. 최소 구현:** git show/cat-file로 고정 tracked 파일을 가져오고 원 경로·source_sha256·initial_copy_sha256·destination·ported_sha256·disposition(copied/adapted/replaced)를 manifest에 기록한다. validate_port_manifest는 baseline_files와 모든 destination의 현재 ported_sha256을 대조하며 source checkout을 요구하지 않는다. 변경한 포트 파일의 ported_sha256은 해당 작업 마지막에 갱신한다. git provenance의 원 SHA와 변경 후 해시를 혼동하지 않는다. private sibling adapter를 vendor_tts 정적 import로 바꾼다. ML_* 환경 이름·자체 자산 경로·ML metadata와 기본값을 설정한다. source-specific 기존 tests는 삭제해 green을 만들지 말고 후속 과목 fixture 교체 대상으로 기록한다. fixture helper와 contracts를 정의한다.
- [ ] **4. GREEN 실행:** `test_ml_port.py`, 기존 `test_speech_tts.py`, `test_shape_timing.py`를 각각 실행. source checkout을 런타임 import 경로에서 제외해도 통과해야 한다.
- [ ] **5. Commit(승인 있을 때):** 새 스킬 변경만 stage, `feat(ml-video): port pinned PDF solution engine`. 타 과목·자료·계획 파일을 함께 stage하지 않는다.

### Task 2: ML 카드·선택·PDF 페이지 대응과 동결

**Files:** Create `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/solution_video/ml_cards.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/solution_video/page_pairs.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_ml_sources.py`. Modify 새 `sources.py`, `ml_fixtures.py`, 기존 `test_sources.py`.

**Interfaces:** Consumes ReviewCard/PageRef/ProblemBundle/SourceFailure와 make_ml_repo. Produces `read_cards(path:Path)->list[ReviewCard]`, `map_pages(card:ReviewCard, problem_pdf:Path, answer_pdf:Path, *, explicit:dict|None=None)->tuple[list[PageRef],list[PageRef]]`, `discover(repo:Path,selector:str,problem_ids:list[str]|None=None,failures:list[SourceFailure]|None=None,*,pack:str|None=None,page_map:dict|None=None)->list[ProblemBundle]`, `freeze_sources(bundles:list[ProblemBundle],batch:Path)->list[ProblemBundle]`.

- [ ] **1. 실패 테스트 작성:** `test_unicode_pack_identity_and_ambiguity`, `test_continuation_and_hint_mapping`, `test_selected_only_and_frozen_assets`에 NFD 폴더·range 경계·같은 P1·같은 날짜 여러 slug·누락 그림/MD·선택하지 않은 손상 문항을 넣는다.
  ```python
  repo = make_ml_repo(self.run, dates=('0930', '1007'), continuations=True)
  bundles = discover(repo, '0930-1007', ['0930:P1', '1007:P1'])
  self.assertEqual(len({b['key'] for b in bundles}), 2)
  self.assertEqual([p['continuation'] for p in bundles[1]['answer_pages']], [1, 2])
  self.assertEqual(len(bundles[1]['problem_pages']), 1)
  with self.assertRaisesRegex(InputError, 'ambiguous'):
      discover(repo, '0930-1007', ['P1'])
  frozen = freeze_sources(bundles, self.run/'batch')
  self.assertFalse(Path(frozen[0]['source_files']['html']).is_absolute())
  ```
- [ ] **2. RED 실행:** `-p test_ml_sources.py`, `-p test_sources.py`. 기존 EC2 기대값을 ML fixture로 교체한 뒤 RED를 확인한다.
- [ ] **3. 최소 구현:** stdlib HTMLParser로 저장 card 원문·이미지 참조를 읽고 NFC 비교한다. P번호/MML 출처/제목과 header 위치를 대조해 계속 페이지를 묶고 Hint 부록을 제외한다. explicit map에도 SHA·범위·중복을 검사한다. source_files는 사용한 상대 그림/evidence만 수집하며 repo 탈출·secret 파일 참조를 거부한다. 조건 비교는 여러 페이지에 분산된 조건 전체를 coverage에 전달하고 단일 페이지 bbox 문자열 동일성만으로 실패시키지 않는다. 실패 수집·선택 문항 격리와 동결을 구현한다.
- [ ] **4. GREEN 실행:** 두 source 테스트 모듈. 실제 1007 dry discovery는 8문항이며 Hint 부록은 페이지 목록에 없어야 한다. prepare나 TTS를 아직 호출하지 않는다.
- [ ] **5. Commit(승인 있을 때):** Task2 Files만 stage, `feat(ml-video): map ML cards to frozen PDF page sets`.

### Task 3: 여러 페이지의 PDF 공개와 전체 coverage

**Files:** Create `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/solution_video/bundle_layers.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_bundle_layers.py`. Modify 새 `pdf_pages.py`, `writing_units.py`, `ml_fixtures.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/browser_check.mjs`, 기존 `test_pdf_pages.py`, `test_writing_units.py`.

**Interfaces:** Consumes ProblemBundle/BundleMap와 기존 `export_page(pdf,page_index,dest)`, `extract_layers(page,mapping)`, `compare_completed(page,evidence)`. Produces `export_bundle(bundle:ProblemBundle,run:Path)->dict[str,dict]`, `extract_bundle(candidates:dict[str,dict],mapping:BundleMap)->BundleLayers`, `verify_bundle_layers(layers:BundleLayers,evidence:Path)->dict`(passed/pages/evidence_hashes), `make_bundle_run(...)`.

- [ ] **1. 실패 테스트 작성:** `test_all_pages_and_final_answer_coverage`, `test_scan_and_unclassified_shape_block_only_that_run`, `test_static_gate_preserves_exact_zero`는 local ID 반복·두 페이지 전체 문자·분수선 중복/누락·중간 페이지 final 오표시·원본 이미지 교체·스캔 풀이를 검사한다.
  ```python
  layers = extract_bundle(candidates, mapping)
  self.assertEqual(len(layers['page_order']), 2)
  self.assertTrue(layers['answer_step_id'].startswith(layers['page_order'][-1]+'::'))
  gate = verify_bundle_layers(layers, self.run/'evidence')
  self.assertTrue(gate['passed'])
  self.assertTrue(all(p['pixel_diff']==p['non_target_diff']==p['hidden_leaks']==0
                      for p in gate['pages'].values()))
  ```
- [ ] **2. RED 실행:** `-p test_bundle_layers.py`. 미지원 두 페이지와 누락 glyph로 인한 FAIL을 확인한다.
- [ ] **3. 최소 구현:** 각 답안 페이지를 별도 layers 폴더로 export하고 local terminal_step_id를 내부 single-page core에 전달한다. 최종 정답 의미는 BundleMap 전체에서만 판단한다. page_id:: 참조에 정확히 한 번 coverage를 요구한다. 페이지별 exact-zero 게이트와 SVG/native PNG 근거를 합산한다. static gate의 두 rAF·disable-gpu 적용 범위를 유지한다.
- [ ] **4. GREEN 실행:** 위 모듈과 기존 PDF/writing_units tests. browser가 없으면 실행 환경을 해결하거나 blocker를 기록하며 해당 검사 skip을 성공으로 보고하지 않는다.
- [ ] **5. Commit(승인 있을 때):** Task3 Files만 stage, `feat(ml-video): reveal complete multi-page PDF solutions`.

### Task 4: 수학 검토·원문 대응·ML 설명 계약

**Files:** Create `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/solution_video/math_review.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_math_review.py`. Modify 새 `manifest.py`, `lesson.py`, 기존 `test_manifest.py`, `test_lesson.py`.

**Interfaces:** Consumes BundleLayers와 전역 manifest. Produces `content_fingerprint(manifest:dict,layers:BundleLayers,coverage:dict)->str`, `validate_math_review(review:dict,step_order:list[str],input_hash:str)->None`, `validate_manifest(manifest:dict,layers:BundleLayers,coverage:dict,math_review:dict)->None`, `validate_lesson(lesson:dict,manifest:dict,layers:BundleLayers,teaching:dict|None)->dict`.

- [ ] **1. 실패 테스트 작성:** `test_math_review_covers_current_order_and_dimensions`, `test_pdf_md_conflict_blocks_paid_work`, `test_reasoned_flow_without_forced_graph_annotation`는 단계 누락·빈 applicable=false 이유·오래된 해시·PDF 부호와 MD의 충돌·글자 순서 위조·reason이 write 뒤인 경우를 거부한다.
  ```python
  validate_manifest(manifest, layers, coverage, math_review)
  math_review['steps'][0]['dimensions'] = {'applicable': False, 'evidence': ''}
  with self.assertRaisesRegex(ReviewError, 'dimensions'):
      validate_math_review(math_review, layers['step_order'], input_hash)
  coverage['pdf_md_agree'] = False
  with self.assertRaisesRegex(ReviewError, 'PDF/MD'):
      validate_manifest(manifest, layers, coverage, valid_math_review)
  ```
- [ ] **2. RED 실행:** `-p test_math_review.py`와 기존 manifest/lesson tests의 ML fixture 버전.
- [ ] **3. 최소 구현:** 설계의 math-review fields와 coverage의 전역 step 순서를 검증한다. source_refs가 동결 파일·정확한 PDF 페이지/MD anchor/HTML card를 참조하도록 검사한다. reasoned는 이유 선행, calculation은 exemption_reason, 모든 write는 한 단계와 연결한다. 원문과 설명의 진위 검토는 작성자가 evidence에 적고 기계 검사가 증명했다고 표현하지 않는다.
- [ ] **4. GREEN 실행:** Task4 모듈과 Task3 tests. 1007 P2 수치 검산은 Fraction(1,2)와 Fraction(3,1), φ·θ=(6,1), 내적 결과 scalar라는 근거가 fixture에 들어간다.
- [ ] **5. Commit(승인 있을 때):** Task4 Files만 stage, `feat(ml-video): require source-bound mathematical review`.

### Task 5: 실측 음성·수식 자막·페이지 타임라인

**Files:** Create `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/solution_video/bundle_timeline.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_bundle_timeline.py`. Modify 새 `speech_chunks.py`, `speech_tts.py`, `review_adapter.py`, `subtitles.py`, `reveal.py`, `narration_pacing.py`, 기존 speech/subtitle/shape_timing/pacing tests.

**Interfaces:** Consumes Task4 검증된 manifest/BundleLayers, 기존 AudioRecord/PCM·generate_voice. Produces `build_bundle_timeline(manifest:dict,layers:BundleLayers,audio:list[dict],config:dict,writing:dict,teaching:dict|None)->dict`, `page_state(timeline:dict,frame:int)->dict`(page_id/visible_ids), 기존 `write_srt(timeline:dict,dest:Path)->Path`, `verify_chunk_sync(run:Path)->dict`. 음성 입력은 전체 문항의 segments다. 페이지별로 TTS를 중복 호출하지 않는다.

- [ ] **1. 실패 테스트 작성:** `test_caption_retime_trim_and_stage_invalidation`의 음성 부분은 text 동일/caption만 수정 후 transport 호출 증가=0, raw WAV SHA 보존·cue 시각 동일을 검사한다. `test_ml_symbols_and_exact_caption_boundaries`는 θ/φ/Σ/⊤/첨자·조건부 확률·중첩/부호 분수·소수와 34자 초과 보호식을 검사한다. `test_shape_budget_and_lag_are_not_hold`는 도형 전체 프레임 보존 및 60프레임 초과 lag의 별도 검토를 검사한다.
  ```python
  self.assertEqual(default_writing()['chars_per_second'], 7.5)
  self.assertEqual(page_state(timeline, 0)['page_id'], timeline['page_spans'][0]['page_id'])
  self.assertEqual(transport_calls_after_caption_edit, transport_calls_before)
  self.assertEqual(raw_sha_after_caption_edit, raw_sha_before)
  self.assertEqual(cue_samples_after_caption_edit, cue_samples_before)
  self.assertEqual(wrap_caption('분산은 φ(x_*)ᵀ Σ_θ φ(x_*)입니다.'),
                   '분산은 φ(x_*)ᵀ Σ_θ φ(x_*)입니다.')
  self.assertEqual(sum(shape_piece_frames), min(90, max(18, math.ceil(W/H*interval))))
  self.assertEqual(pacing['status'], 'review-required')  # lag=61, 현재 검토 없음
  ```
- [ ] **2. RED 실행:** `-p test_bundle_timeline.py`, `-p test_subtitles.py`, `-p test_narration_pacing.py`. 새 ML 기호가 보호되지 않는 반례와 page_span 누락을 확인한다.
- [ ] **3. 최소 구현:** 기존 청크 PCM/영수증/trim 검증을 그대로 활용하고 명시 page_id로 timeline을 조립한다. 기존 분수선·근호선 프레임 배분과 도형-only 예외를 유지한다. caption 보호 토큰을 ML Greek/전치/조건부/행렬 첨자로 확장하며 LaTeX를 자막으로 렌더하지 않는다. cue 구분과 줄바꿈은 별개다. source text만 TTS payload에 넣고 발음은 대본에서 저작한다. retime은 같은 PCM으로 timing만 계산한다. SRT/영상 경계·glyph 작성순서·구도는 실측 샘플에서 계산한다.
- [ ] **4. GREEN 실행:** Task5 tests와 speech_chunks/speech_tts/caption_notation/subtitle_layout_media/shape_timing/pacing 회귀. libass 실제 한 줄/두 줄 박스·WrapStyle2를 검증하고 fake PCM의 기술 통과를 audio 의미 통과로 기록하지 않는다.
- [ ] **5. Commit(승인 있을 때):** Task5 Files만 stage, `feat(ml-video): synchronize measured speech and mathematical captions`.

### Task 6: 페이지 전환·ML focus·발화 주석과 실제 렌더

**Files:** Modify 새 `composition.py`, `annotations.py`, `focus.py`, `teaching.py`, `writing_camera.py`, `media.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/assets/player.js`, `camera.js`, `annotations.js`, 기존 camera/teaching/lesson runtime tests. Create `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_bundle_composition.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/bundle_check.mjs`.

**Interfaces:** Consumes BundleLayers/BundleTimeline/page_state와 전역 teaching. Produces `assemble(bundle:ProblemBundle,layers:BundleLayers,manifest:dict,timeline:dict,run:Path,runtime:Path)->dict`, `load_teaching(run:Path,manifest:dict,layers:BundleLayers)->dict|None`, `lesson_expectations(lesson:dict,manifest:dict,timeline:dict,teaching:dict)->dict`, `render_master(parts:dict,timeline:dict,audio:list[dict],run:Path,hyperframes_entry:Path)->Path`. 기존 내부 페이지 함수는 private로 두고 위 공개 API에 연결한다. bundle_check.mjs는 현재 frame의 page_id·DOM 공개·화면 기대값을 독립 계산하고 test_bundle_composition.py의 browser_result 필드를 JSON으로 반환한다.

- [ ] **1. 실패 테스트 작성:** `test_seek_across_pages_and_visible_equation_focus`, `test_chunk_annotations_fit_speech_and_camera`, `test_constant_ink_width_and_glyph_alias`를 작성한다. 앞 페이지 복귀·아직 미공개 식 focus·겹친 표시·청크 종료 넘침·폰트 alias 불일치·두 페이지 마지막 잔류를 검사한다.
  ```python
  self.assertEqual(browser_result['forward_backward_diff'], 0)
  self.assertEqual(browser_result['future_leaks'], 0)
  self.assertEqual(browser_result['final_annotation_count'], 0)
  self.assertLessEqual(browser_result['tip_error_px'], 1)
  self.assertLessEqual(abs(browser_result['pencil_length_px']-160), .5)
  self.assertEqual(browser_result['stroke_width_px'], 8)
  self.assertTrue(all(p['stable_completed_frame'] for p in chunk_probes))
  ```
- [ ] **2. RED 실행:** `-p test_bundle_composition.py` 및 `node "$T/test_teaching_runtime.cjs"`, `node "$T/test_writing_runtime.cjs"`. 두 페이지 중 누락·잔류·미공개 식 focus에서 실패를 확인한다.
- [ ] **3. 최소 구현:** 여러 원본 SVG를 고유 DOM prefix로 넣고 하나의 paused GSAP timeline으로 활성 page/누적 공개/주석/연필을 frame에서 다시 계산한다. 페이지 전환은 해당 segment 경계에서만 하며 원문·음성 순서를 바꾸지 않는다. focus의 상단 회로 전용 제한을 ML 공개 영역 정책으로 교체한다. marker별 source page hash·이미 공개 상태를 검사한다. 원본 필기와 주석은 한 연필을 공유하고 청크 deadline/중복을 거부한다. 카메라에 굵은 stroke 반경·arrowhead·26px label·sprite 여백을 넣고 최종 페이지 hold에서 모든 보조 연출을 숨긴다. 로컬 HyperFrames renderer에 실제 parts를 전달한다.
- [ ] **4. GREEN 실행:** 신규 browser/Python tests와 writing_flow/camera/lesson/teaching runtime 회귀. synthetic 두 페이지 렌더+ffprobe로 1920×1080/30fps·24kHz·duration·순서·끝 프레임을 확인한다. A4 단일 페이지도 같은 테스트 경로로 검사한다.
- [ ] **5. Commit(승인 있을 때):** Task6 Files만 stage, `feat(ml-video): render page-aware mathematical explanations`.

### Task 7: CLI·상태 해시·대본 검토와 재개

**Files:** Modify 새 `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/video.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/scripts/solution_video/state.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_cli.py`, `test_state.py`. Create `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_ml_cli.py`.

**Interfaces:** Consumes Task2–6 APIs. Produces `prepare_batch(repo:Path,selector:str,problem_ids:list[str]|None=None,review:bool=False,writing_mode:str='pencil',*,pack:str|None=None,page_map:Path|None=None)->Path`, `run_stage(action:str,run:Path,args:argparse.Namespace,transport=None)->dict`, `resume_batch(batch:Path)->dict`, 기존 `stage_fingerprint(run:Path,stage:str)->str`, `recover_run(run:Path)->str|None`, `finish_stage(run:Path,stage:str,outputs:list[Path])->None`, `main(argv:list[str]|None=None)->int`.

CLI: prepare selector --repo PATH [--problems CSV] [--pack SLUG] [--page-map JSON] [--review] [--writing-mode pencil|typing]; extract/check/tts/retime/assemble/render/captions/verify --run PATH; tts의 --config/--env-file/--approve-review, retime의 --writing-config, assemble의 --runtime, render/verify의 --hyperframes-entry; resume-set/publish-set --batch PATH. 결과는 author-required/awaiting-review/passed/failed와 paid_requests를 포함한다.

- [ ] **1. 실패 테스트 작성:** `test_cli_prepare_selection_and_zero_paid_requests`, `test_caption_retime_trim_and_stage_invalidation`의 상태 부분, `test_review_is_one_hash_bound_batch_round`, `test_partial_prepare_resumes_same_frozen_inputs`를 작성한다.
  ```python
  batch = prepare_batch(repo, '1007', ['P1'], review=False)
  self.assertEqual(len(read(batch/'batch.json')['items']), 1)
  self.assertEqual(run_stage('check', run, args, counting_transport)['paid_requests'], 0)
  self.assertEqual(run_stage('tts', conflict_run, args, counting_transport)['status'], 'failed')
  self.assertEqual(transport_calls, 0)
  self.assertEqual(recover_run(changed_layer_run), 'layers')
  self.assertEqual(recover_run(changed_caption_run), 'script')
  self.assertEqual(resume_batch(batch)['items'][0]['run'], original_run_relative_path)
  ```
- [ ] **2. RED 실행:** `-p test_ml_cli.py`와 기존 CLI/state ML fixture tests. 전체 페이지 누락·오래된 검토 허용·default에 추가 승인이 생기는 반례를 확인한다.
- [ ] **3. 최소 구현:** page/pair 입력을 bundle 계약으로 교체한다. prepare는 snapshots/candidates만 만들고 paid=0, author-required에 실제 누락 파일 목록을 반환한다. 전역 content/math/lesson·per-page gate를 check/TTS 전에 실행한다. state FACTORS/MODULES에 모든 pages/markers/폰트/runtime/vendor_tts/코드와 현재 출력 해시를 넣는다. 자막-only 변경은 script 이하를 무효화해 재검토하지만 동일 text의 청크 cache로 paid=0을 유지한다. 음성 성공 일부/실패·extract 재시도·writing/trim 변경은 같은 RUN에서 재개한다. review 승인은 batch 전체 현재 대본 hash에 한 번이고 변경 시 무효다. stage wrapper는 InputError를 failed로 변환한다.
- [ ] **4. GREEN 실행:** Task7 tests, Task1–6 전용 tests. stage 무효화 케이스를 layer/WAV/trim/font/주석/출력 bytes별로 돌리고 sibling run과 캐시가 보존되는지 확인한다. `prepare --help`, `tts --help`, `retime --help`, `resume-set --help`가 정의한 인자를 보여야 한다.
- [ ] **5. Commit(승인 있을 때):** Task7 Files만 stage, `feat(ml-video): orchestrate resumable solution batches`.

### Task 8: 현재 근거 검증·실청취 차단·보존 게시

**Files:** Modify 새 `verify.py`, `publication.py`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/browser_check.mjs`, `teaching_check.mjs`, `writing_flow_check.mjs`, 기존 verify/publication/state tests. Create `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_ml_publication.py`.

**Interfaces:** Consumes 현재 RUN/Task7 state, Task6 render와 모든 페이지 기대 상태. Produces 기존 `verification_fingerprint(run:Path)->str`, `verify_run(run:Path,hyperframes_entry:Path)->dict`, `report_current(run:Path,report:dict)->bool`, `publish_batch(batch:Path)->dict`(complete/published/errors), `output_filename(item:dict,run:Path)->str`.

- [ ] **1. 실패 테스트 작성:** `test_unlistened_audio_cannot_publish`, `test_srt_or_review_tampering_blocks_publish`, `test_partial_publish_and_rollback`, `test_range_and_pack_title_collisions`, `test_dense_teaching_keeps_all_probes`를 추가한다. font/source/code/review hash 변조와 후속 stale report, unsafe Unicode 제목을 포함한다.
  ```python
  self.assertFalse(report_current(run, synthetic_report))
  before_latest = latest.read_bytes()
  result = publish_batch(batch_with_one_failed_item)
  self.assertFalse(result['complete'])
  self.assertEqual(latest.read_bytes(), before_latest)
  self.assertEqual(sibling.read_bytes(), previous_sibling_bytes)
  self.assertEqual(old_output_after_injected_replace_failure, old_output_before)
  self.assertEqual(teaching_browser_timeout, 600)
  self.assertEqual(generic_browser_timeout, 120)
  ```
- [ ] **2. RED 실행:** `-p test_ml_publication.py`와 기존 verify/publication ML tests. 미청취 passed report와 SRT 변조를 거부하지 못하는 상태에서 FAIL을 확인한다.
- [ ] **3. 최소 구현:** 문항 모든 페이지의 SVG/공개/writing_flow/lesson_flow/주석 oracle·미디어를 검사한다. SRT 번호·전체 text/개행/PCM 시각을 기대 SRT와 대조한다. dense teaching만600초를 허용하고 probe를 빼지 않는다. live-listened audio-review는 모든 실제 청크의 네 boolean과 notes·현재 파일 hash를 필요로 한다. unverified 또는 누락 chunk는 complete=false다. 안전한 range/slug+Pn 제목으로 명명하고 잠금·교체 journal/rollback을 유지한다. 성공 문항만 게시하되 failure·형제·기존 파일을 보존, 전체 성공만 latest 갱신, catalog/README는 제작자료 안에 둔다.
- [ ] **4. GREEN 실행:** Task8 모듈과 기존 verify/publication tests. 교체 실패 injection에서 파일·receipt·latest·catalog 모두 이전 상태로 복구되는지 확인한다. 원자적 다중 파일 commit 또는 강제 종료 복구를 주장하지 않는다.
- [ ] **5. Commit(승인 있을 때):** Task8 Files만 stage, `feat(ml-video): verify and safely publish current solution videos`.

### Task 9: ML 지침·전체 회귀·실제 PDF 수용 검사

**Files:** Modify 새 `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/SKILL.md`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/agents/openai.yaml`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/references/pdf-and-coverage.md`, `narration-and-timing.md`, `verification.md`, `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/assets/port-provenance.json` 및 84파일의 남은 EC2 fixture tests. Create `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/ml_acceptance.py`, 실행 보고서 `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/docs/superpowers/reports/2026-10-10-ml-solution-video.md`. 기존 ML 자료/스킬은 수정하지 않는다.

**Interfaces:** Consumes Task1–8 전체 CLI. Produces `run_acceptance(repo:Path,dest:Path,hyperframes_entry:Path,*,env_file:Path|None=None,live:bool=False)->dict`와 CLI `ml_acceptance.py --repo PATH --dest SCRATCH --hyperframes-entry PATH [--live --env-file PATH]`. report는 technical_complete/live_audio/complete/source_hashes/checks/errors/evidence를 구분한다. 기본 live=false/paid=0이며 synthetic은 게시하지 않는다.

- [ ] **1. 실패 테스트 작성:** `test_real_ml_prepare_scope_and_source_preservation`은 실제 1007 P2/P3/P8의 source HTML/MD/PDF·그림 hash 전후 동일, 카드 수8/Hint 제외·한 문항 한 MP4, 실청취 없으면 complete=false를 검사한다. `test_port_disposition_covers_all_baseline_files`는 기존 84 tracked 파일과 3개 최신 커밋 변경 파일의 모든 행에 destination/disposition/test_evidence가 있는지 검사한다.
  ```python
  self.assertEqual(len(discover(repo, '1007')), 8)
  self.assertEqual(before_source_hashes, after_source_hashes)
  self.assertEqual(result['paid_requests'], 0)
  self.assertTrue(result['technical_complete'])
  self.assertFalse(result['complete'])
  self.assertEqual(result['live_audio'], 'unverified')
  self.assertEqual(set(provenance['baseline_files']), set(baseline_tracked_files))
  self.assertTrue(all(row.get('test_evidence') for row in provenance['files']))
  ```
- [ ] **2. RED 실행:** 해당 test와 `ml_acceptance.py --help`. 지침/실제 source 대본 fixture/근거 대응이 없으면 실패함을 확인한다.
- [ ] **3. 최소 구현:** ML 실제 자료를 SCRATCH로 동결하고 P2 수치/차원, P3 그래프, P8 긴 유도에 PageMap·청크 원고·math/coverage/lesson·focus를 원문 대조로 저작한다. 실제 풀이 좌표는 고정된 테스트 자료에만 둔다. PDF→MD 추출 문자열이나 OCR로 의미 승인을 자동 작성하지 않는다. 실제 수학 계산/설명/기호/음영을 직접 대조한다. 원자료에서 수학/그래프 오류를 발견하면 그 문항을 차단하고 보고하며 수정하지 않는다. 모든 기존 EC2 source fixture·absolute path·adapter 문자열을 ML 또는 자체 생성 fixture로 교체하되 공통 회귀의 assertions를 약화하지 않는다. SKILL/참고 문서에 단계·해시·동결·원문/미청취 경계·회복 명령과 실패 이유를 안내한다.
- [ ] **4. 최종 검증:** 다음 명령을 독립 호출로 실행한다. 성공은 아래 각 기준과 실제 결과가 일치할 때만 기록한다.
  ```bash
  S='/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video'; T="$S/tests"
  PATH=/opt/homebrew/opt/ffmpeg-full/bin:$PATH PYTHONPATH="$S/scripts:$T" python3 -m unittest discover -s "$T" -v
  node '/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_writing_runtime.cjs'
  node '/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/test_teaching_runtime.cjs'
  python3 /Users/hyunjun_macbook_pro/.codex/skills/.system/skill-creator/scripts/quick_validate.py '/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video'
  ```
  Python 실패0, JS assertion 통과, Skill is valid!가 기준이다. 기존 acceptance runner 중 EC2 전용 저작은 ML runner로 교체하고 각 test scenario의 연결을 provenance에 기록한다. 모든 provenance의 ported_sha256을 현재 bytes로 갱신한 후 validate_port_manifest를 다시 실행한다. skip·fake PCM을 live 통과 수로 세지 않는다. Node/Python·PyMuPDF/Pillow·Chrome/GSAP/HyperFrames/libass 경로는 시작에 발견한 절대 경로를 실제 명령에 사용한다.
  
  실제 PDF scratch acceptance는 `python3 '/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video/tests/ml_acceptance.py' --repo '/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초' --dest /ABS/SCRATCH --hyperframes-entry /ABS/HYPERFRAMES/dist/cli.js`다. scratch/native PNG·원본 SVG·빈/중간/완성·forward/backward·최종 MP4를 직접 대조한다. 실음성까지 요청받은 실행에서는 --live를 명시해 실제 전청크와 최종 MP4를 청취한다. 실행 환경이 실제 청취를 제공하지 않으면 기술 결과와 검토용 영상만 전달하며 보고서에 complete=false/live_audio=unverified를 기록한다. 키·가격·공급자 가용성을 캐시 기록으로 확인됐다고 말하지 않는다.
- [ ] **5. Commit(승인 있을 때):** 이번 스킬+실행 보고서의 실제 변경 목록을 확인해 stage, `docs(ml-video): document and validate ML solution workflow`. 커밋 전에 현재 source hashes·stage 목록을 다시 확인한다.

## 고정 커밋 계승 대조표

| 기준 | 계승할 동작/검사 | 소유 작업 |
|---|---|---|
| ca4a0ad, 757fa08, 296cebe, 88c3fd5 | PDF 원본·white16:9/A4·연필·writing_units·근거→필기·조건과 전체 흐름 | 1–4, 6 |
| af86ffb | 숫자/연산 caption error/warning, 자막-only cache·최종 검토 | 5, 7–9 |
| a017c9d | 대본-only TTS·pcm-chunks·raw trim·실측SRT·청크 청취·도형 전체 예산·2초 lag·도형-only camera | 5–9 |
| eeec3d5 | stroke_width·화살촉 bounds·Δ/∆ glyph alias·chunk-bound 표시·청크 완료 probe·수식 보호 개행·WrapStyle2·SRT 전체 비교·600초 teaching·정적 두 rAF/disable-gpu | 3, 5, 6, 8, 9 |

코드가 바뀌는 파일만이 아니라 해당 기준의 자산·참고 문서·검증 테스트까지 기록한다. 교과서 회로 문제/이미 제작한 EC2 영상·제작자료를 ML에 복사하지 않는다. 회로 source-specific tests를 대체하면 대응하는 ML 입력/반례와 검사 이름을 provenance에 남긴다.

## Self-Review / Execution Handoff

- 설계의 입력/식별/계속 페이지/원문 공개/수학 검토/음성·자막/주석/상태/게시/검증 요구는 Task1–9와 대조표에 연결했다.
- Shared Interfaces의 이름·필드·0-based 페이지/1-based continuation·전역 ID 규격을 후속 작업에서 동일하게 사용한다. 테스트가 독립 subtask에서 재현되도록 공통 fixture/명령을 정의했다.
- Review Focus의 다섯 반례를 각 소유 작업의 실패 테스트에 넣었다. 최신 baseline file list는 누락/교체를 hash manifest로 추적한다.
- 조건/그래프/수식에 대한 의미 승인은 author evidence, 실제 음성 승인은 live-listened evidence다. 기술 통과와 완료를 구별한다.
- 실행 방법 미정. **Native를 추천**한다. 페이지·대본·타임라인·해시의 공유 계약이 강하게 연결되어 한 구현자가 일관되게 연결하고 마지막 독립 리뷰를 받는 편이 효율적이다. Subagent-driven은 작업마다 새 구현자·리뷰어와 최종 전체 리뷰를 사용한다.
- 두 방식 모두 사용자 검토·방법 선택 후 실행한다. Native를 선택하면 executing-plans, Subagent-driven이면 subagent-driven-development를 적용한다. 이번 계획 작성 중 subagent는 사용하지 않았다.
