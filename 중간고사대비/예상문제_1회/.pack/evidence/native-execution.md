# SDD ledger — plan: docs/superpowers/plans/2026-10-20-midterm-01-english-problems.md
Native execution. Tasks 1–5 pending.
Ruling: use the existing codex/row-vector-midterm-01 task checkout and preserve uncommitted changes — this is the same pack task, avoids moving user artifacts. No commits requested.
Pre-flight: Task1 normalized English → Task2 payload; Task1 current source and baseline → Task3 binding; Task1 original fields → Task4 MPE; Tasks2–4 reports → Task5 publication: compatible.
Task 1: complete — 42 authored English parts; 9 source/row tests PASS. Korean projection and explanation fragment bytes unchanged.
Task 2: complete — actual English 10-page PDF, 1440×810, zero Korean/caption ink, offline resources; long p8 split8–9 with labels a–f once; Poppler visual review.
Task 3: binding implemented; negative fixtures and final delivery tests pending final publication.
Task 4: independent 42-part blind math review returned no issues; source staged and rebuilt. Browser diagnostic found template punctuation reflow and test selected-tab assumptions; exact source checks kept, rendered comparison normalized punctuation.
Baseline: 13 passed, 2 failed (pre-existing stale approved-review input hash and stale browser hash); refresh both through actual new reviews.
Task 3: complete — strict historical binding, original-only preservation and statement/answer/order/report/PDF failures; English source/PDF/page mapping/page ID/error tampering checks pass.
Task 4: complete — staged and final browser 60/60, exact source/English field checks, all current MPE gates pass with new blind42-item evidence.
Task 5: complete — gated source/English PDF/explanation publication; 313 delivery hashes; check_exam status pass errors []; pack suite38 passed. Whole-repository suite with existing module paths:55 passed,9 failed,22 skipped,192 subtests passed. Failures outside requested pack: lecture inference0909, dated review-note folder paths,6 homework-chunk tests and1 video-resynthesis test (historical Mac paths). No unrelated code changed.
Final review: pending fresh reviewer against uncommitted working-tree diff (spec prohibits automatic commits).
Final review: fresh gpt-6-astra reviewer completed. Critical none. Important single-list English validation defect reproduced by six failing input fixtures then fixed (13 source tests pass).
Final: Ruling: reviewer pagination-test minor regraded Important — the explicit plan requires exercising the current renderer; replaced frozen JSON assertion with live PDF build and printed label/continuation inspection. Injected numbering-reset regression produced a,a,a,a,a,a and RED; restored current paginator for GREEN verification. No content change.
Final: Ruling: declined root-suite diagnosis —9 failures are outside this pack and unchanged files; report them without modifying unrelated lecture/video materials. Cost: repository-wide suite remains red.
Final: Ruling: declined second aesthetic pass by fresh reviewer — Native executor inspected all10 final PDF pages and2 stress continuation pages plus desktop/mobile light/dark screenshot samples; reviewer independently checked geometry/text/white margins and all42 translations. Cost: no second full visual reading, compensated by actual visual review and60 browser content checks.
Final: browser tests expanded to actual TOC navigation and awaited visible Korean/original print blocks (six print combinations), replacing count-only evidence. Original layout/font scheduling is asynchronous; no user-facing shared-template change.

## Fresh review and resolution
# Final fresh-context review

Reviewed the current uncommitted working tree and untracked feature modules against HEAD da9dc53e84d769cbf86e2a50c98496c56684cc08 and the plan's global constraints/data contract. No tracked file was modified by this review.

## Critical

None.

## Important

1. **Enforce the single ordered-list contract before accepting English questions.** `중간고사대비/예상문제_1회/.pack/tools/english_source.py:18-21` flattens every descendant label and `li`, so two separate `<ol type="a">` elements with labels `a` and `b` pass validation. I reproduced this directly with `english_fields`: it returned successfully. Both lists render starting at (a), while the declared labels claim (a)/(b), and the paginator assumes a single task list. The spec explicitly requires one top-level ordered list and labels on its direct `li` children. Validate that structure (including `type="a"` and no misleading start/value overrides) and reject split/nested/incorrectly numbered lists. The currently delivered ten cards have the correct structure; this is an input-validation defect in the promised reusable build path.

## Minor

1. **The pagination regression test does not execute the renderer.** `중간고사대비/예상문제_1회/.pack/tools/tests/test_english_pdf.py:29-32` reads the committed stress-result JSON and asserts its recorded labels. Changing pagination, typography, or continuation handling leaves this test green. Preserve the report as evidence, but add a marked integration test that builds the expanded p8 fixture with the current code and inspects its actual continuation pages/labels. The existing report records a successful past run, so this does not establish a defect in the delivered PDF.

## Independent verification

- Read and compared all ten Korean/English condition blocks and all 42 question pairs. No changed numeric assumptions, requested results, row-gradient conventions, variance conventions, intercept priors, normalization tasks, cross-references, or future-noise independence conditions found.
- Inspected English source/payload/rendering, historical Korean binding, check_exam integration, browser assertions, relevant new tests, final evidence and the execution ledger.
- Independently ran `check_exam.py --out 중간고사대비/예상문제_1회 --repo .`: pass, errors empty.
- Independently compared both Korean PDFs and all ten authored Korean explanation fragments with Git HEAD: byte-identical.
- Independently inspected the actual English PDF with PyMuPDF: ten pages; every page 1440×810 pt; no Hangul text; all pixels in the bottom 135 pt white; common instruction occurs once.
- Reviewed browser checks for all 60 viewport/theme/topic combinations, original-tab content comparison, navigation, saved preference, keyboard order, mobile expansion, dock behavior, fallback and breakpoint transition. Did not rerun the expensive full browser suite.

## Declined to judge

- The nine reported failures outside this pack: no independent root-suite rerun or diagnosis was performed.
- Fresh visual/aesthetic approval of all rendered PDF/browser screenshots: this review independently checked PDF geometry/text/margins and inspected recorded visual/browser evidence, but did not perform another full screenshot-by-screenshot visual review.

Resolution: strict one-list/direct-li/type/start/value validation implemented; six malformed structures were RED and then GREEN. The pagination test now builds actual current-code PDFs and reads printed labels; injected numbering reset was RED, restored current paginator GREEN (25.02s). No deferred reviewer issues. Full final suite and browser evidence are recorded by the final check commands.

Final: fixed single-list validation — six malformed structure cases RED→GREEN; all13 English source tests pass. Pagination regression injection RED (all a labels)→actual current PDF GREEN; final whole-pack suite44/44 PASS (25.04s). Final browser60/60 PASS, six print checks each show10 Korean+10 English blocks, actual TOC navigation checked. check_exam pass/errors[], diff --check clean. No deferred review issues.

Repository-wide failures (55 passed,9 failed,22 skipped,192 subtests passed; unrelated files unchanged):
- FAILED tests/test_ml_stt.py::MlSttTests::test_04_infer_lecture - AssertionErr...
- FAILED tests/test_notes_html.py::TestCurrentDatedPacks::test_all_current_html_contracts
- FAILED 문제풀이영상/과제1/과제1_제작자료/tests/test_homework_chunks.py::Pairs::test_all_25_manifests_covered
- FAILED 문제풀이영상/과제1/과제1_제작자료/tests/test_homework_chunks.py::Pairs::test_math_groups_and_signed_fractions
- FAILED 문제풀이영상/과제1/과제1_제작자료/tests/test_homework_chunks.py::Pairs::test_missing_segment_rejected
- FAILED 문제풀이영상/과제1/과제1_제작자료/tests/test_homework_chunks.py::Pairs::test_original_text_preserved
- FAILED 문제풀이영상/과제1/과제1_제작자료/tests/test_homework_chunks.py::Pairs::test_p1_three_sentences_are_three_cues
- FAILED 문제풀이영상/과제1/과제1_제작자료/tests/test_homework_chunks.py::Pairs::test_reason_math_values_use_symbols
- FAILED 문제풀이영상/과제1/과제1_제작자료/tests/test_resynthesis.py::Revision::test_prepare_preserves_existing_media_and_layers
