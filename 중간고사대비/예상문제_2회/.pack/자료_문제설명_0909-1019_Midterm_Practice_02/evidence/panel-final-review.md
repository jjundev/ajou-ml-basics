# Whole-change review — ML problem panel tabs

Base: `80d29c1`; current uncommitted template/contract/test/20 fragment changes and the two staged HTML/MD builds named in review-package.md. Read-only review; this report is the only checkout file written by the reviewer.

## Strengths

- A single workspace moves between desktop and mobile, avoiding duplicate tab IDs and duplicate rendered formulas. Original-tab preference correctly survives a visit to a question without an original.
- Optional metadata is included in the existing fragment input hash, validated before generation, and carried into both HTML and Markdown. Unknown, duplicate, nested, and empty blocks are rejected by the new contract.
- Independently compared all 20 fragments with `git show 80d29c1:<path>`: removing only the relocated provenance paragraph and new metadata sections reproduces each original fragment exactly. All 20 provenance paragraphs are unchanged. No question HTML or PDF diff was present.
- Read all 123 glossary entries and their per-question roles. No computed numerical answer leakage or materially incorrect formulas found. Confirmed all glossary term titles appear in the staged HTML and Markdown.
- Independently exercised both actual stages with Chromium: Home/End tab navigation, desktop→375px collapse/focus fallback, mobile expansion, mobile→1024px, question changes, print-media mounting of all 10 questions and all 10 terms blocks, and post-print tab restoration. No page errors.
- Independently exercised an in-memory variant of the actual stage with an original only on p1 and both metadata blocks omitted on p2: original preference fallback/restoration, both empty states, saved tab after reload, original visibility in print, and restored screen state passed.
- Visually inspected actual round 1 floating-panel and round 2 mobile dark terminology screenshots: tab and docking controls are separated and readable; no observed control overlap.

## Issues

### Critical

None.

### Important

1. **Keyboard focus is lost when the mobile workspace moves to desktop.**
   - File: `.claude/skills/ml-problem-explain/assets/note-template.html:1137` (focus condition), `:1155` (reparent), `:1159` (one-direction restore).
   - Reproduction on both actual stages: viewport 375px, p1 → open “문제 보기” → focus/click `#tab-terms` → resize to 1024px. `document.activeElement` becomes `BODY`, although the selected terms tab remains visible in the desktop panel.
   - Effect: a keyboard user loses their place when crossing the responsive boundary. The next Tab starts from a different part of the document rather than continuing from the selected tab. This directly misses the stated focus-preservation review focus.
   - Cause: moving the focused workspace detaches its active descendant; `refocus` only handles `!wide`. Preserve and restore the focused workspace descendant on mobile→desktop, retaining the existing mobile-collapse fallback where appropriate. Add a browser assertion for activeElement across this direction.

### Minor

1. **The p7 quadratic-form role uses the established term for determinant.**
   - File: `중간고사대비/예상문제_2회/.pack/panel-content.json:258`; mirrored in `중간고사대비/예상문제_2회/.pack/explanations/p7.html:2` and staged HTML/MD.
   - Text: “모수 중심에서 벗어난 정도를 행렬식의 벌점으로 써요.”
   - Effect: “행렬식” normally denotes determinant, also explicitly taught in this glossary. Here the penalty is a quadratic form in the centered parameter vector, not a determinant. The adjacent definition and formula are correct, so this is a localized pedagogical ambiguity rather than a wrong derivation.
   - Suggested text: “모수 중심에서 벗어난 정도를 이차형식의 벌점으로 써요.” Update the authoritative fragment and inventory together, then regenerate.

## Recommendations

Fix the Important focus issue and assert focus restoration at the breakpoint. Correct the localized glossary wording during the same bounded fix pass. Preserve the demonstrated source/core-solution byte parity when regenerating the final delivery.

## Declined to judge

- Re-derivation of pre-existing numerical solutions: outside this panel change; inspected their byte preservation, not a second independent derivation of unrelated prior work.
- Historical MML page attribution accuracy: provenance is byte-identical relocation; revalidating every cited textbook page is outside this implementation diff.
- Four full-suite baseline failures concerning legacy 1014/1019 delivery layout/files and macOS canonical-directory behavior: reproduced baseline evidence was provided and inspected; not classified as new regressions.
- Safari/Firefox and assistive-technology speech output: not exercised in this review; browser conclusions are limited to Chromium and structural keyboard/focus behavior.
- Final publication and final output manifest hashes: staging was the review target; publication is the executor's remaining step after the bounded fix pass.

## Assessment

**Ready to deliver? With fixes.**

The metadata contract, regeneration path, terminology content, and print/navigation behavior align with the plan. The reproducible mobile→desktop keyboard-focus regression should be fixed before publishing; the glossary wording is a small worthwhile correction. No Critical findings.
