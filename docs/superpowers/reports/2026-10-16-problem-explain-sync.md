# Problem-explain skill synchronization verification

Completed 2026-10-16 KST. Approved scope A: modify DS/ML/EC2 skills and validate temporary stages. No existing explanation publication, commit or push.

## Changes

- Ported dockable problem/original panels, 1024px desktop defaults, saved preferences, mobile folds, image zoom and print remount; retained DS code styling and each course's reading identities.
- DS/ML read strictly validated input choice models, reject duplicate/invalid/missing models into static display with diagnostics. EC2 workbook questions remain static.
- Added review-only newest-first `all`, choice/subpart separation and Unicode-aware resource handling with strict actual repository containment.
- Added local rerender workflows preserving ML homework/normalization and EC2's problems.txt + MD + figures composite digest. Rerender creates a new stage and never publishes.
- Added `review_policy_version=problem-explain-2026-10-15` to new manifests/reviews. New publication checks both. Missing/old policy or changed input/resources/references resets content/independent approval; visual/browser reviews always reset.
- Added historical input resource hashes, published-fragment integrity checks, guarded asset relocation and separately hashed reference image dependencies. Source SVG numeric stroke-width remains narrowly permitted.
- Added source-based terminology/distractor/negative-question rules and consistent caveats through understand/solve/verify/pitfall/sum; retained course-specific disputed rules and existing EC2 parent integration.
- Pinned changes with reversible DS provenance history, local sync hashes and skill-scoped LF attributes; restored vendor LF bytes to original independently pinned hashes.

## Verification

| Scope | Result | Evidence |
|---|---|---|
| DS complete skill suite | 124 passed | `.scratch/problem-explain-sync-20261015/final-suite-ds.txt` |
| EC2 complete skill suite | 118 passed, 31 unittest subtests passed | `.scratch/problem-explain-sync-20261015/final-suite-ec2.txt` |
| ML complete skill suite | 111 passed; 2 pre-existing delivery failures | `.scratch/problem-explain-sync-20261015/verified-suite-ml.txt` |
| New browser acceptance | 8 per skill, all passed within above suites | `tests/test_sync_browser.py` |
| Persistent synthetic stage previews | 3 resolutions/themes per skill; no page/KaTeX errors or horizontal overflow; math rendered | `preview-*/browser-validation.json` |
| Published output audit | 3092 existing files unchanged; 0 missing; 0 new published files | `.scratch/problem-explain-sync-20261015/protected-audit.json` |
| Git whitespace check | all three skills passed | `git diff --check` |
| Documentation scenario | old policy/image change cannot reuse pass; blind verifier, defect caveats and stage-only respected | fresh read-only agent baseline and follow-up |
| Fresh code review | 2 concrete findings, both fixed with RED→GREEN regressions and final full suites | `red-review-findings.txt`, `review-fixed-ds.txt`, full suite logs |

The browser matrix covers 1280×900, 1024×900 and 375×812 in light/dark, 1023→1024 transition, persisted closed TOC, original-tab availability, dock/float/drag/resize/restoration, valid answer feedback/reset, static fallback, code/math preservation, image zoom and print remount. Persistent preview screenshots were also visually inspected.

## Existing ML failures preserved

- `tests/test_delivery.py::test_published_review_explanation[1014]`
- `tests/test_delivery.py::test_published_layout_keeps_only_html_on_top[1014]`

Both were reproduced before any implementation (`baseline-ml-isolated.txt`). The 1014 delivery is incomplete/inconsistent with that historical delivery audit. Fixing it would touch existing outputs, outside approved scope. The delivery audit was kept intact; no test skip or output regeneration hides these failures. New regression and browser checks passed.

## Decisions made during execution

1. Work directly in the requested repositories with skill snapshots and published-file hashes, preserving pre-existing EC2 edits; no commit/push/publish. This makes review available in the current checkouts; concurrent changes require baseline comparison.
2. Preserve historical read-only structural inspection, enforce current policy on new publication. Old HTML remains readable, while old approvals cannot authorize current-policy publication.
3. Require reference image paths/hashes separately. If historical bytes cannot be proved, rerender requires real re-review; this can require more manual verification after a relocation.
4. Preserve the two existing ML 1014 delivery failures and all existing outputs; their repair is deferred by the explicit no-republication scope.

## Review fixes

- P1: A moved reference image could be compared with its replacement and inherit approval. Missing historical target now fails equivalence, image dependencies need their own hash records, and new publication checks dependency completeness.
- P2: Source resource hashing failed on supported alternate NFC/NFD image spellings. Resource hashing resolves actual paths before containment and hash checks. A canonically equivalent existing sibling directory remains outside the repository.

## Previews

Synthetic UI/mechanical validation only; these are not newly approved course explanations or independent solution checks.

- DS: `.scratch/problem-explain-sync-20261015/preview-ds/stage/문제설명_1007_Test.html`
- ML: `.scratch/problem-explain-sync-20261015/preview-ml/stage/문제설명_1007_Test.html`
- EC2: `.scratch/problem-explain-sync-20261015/preview-ec2/stage/문제설명_1007_Test.html`
