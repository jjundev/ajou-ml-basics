# Problem-panel tabs revision 2026-10-19

Current stage HTML SHA256: eca6d284e85d2e4f2fb62db06b8b6575c4ef5f3dafe7167fa45a3650f15b3812.
- 10 problems: provenance paragraphs relocated byte-identically; 7 core explanations identical except removal of that paragraph. Question/source/answer JSON, source HTML and both PDFs byte-identical to80d29c1.
- 62 terminology entries: definition, notation, per-question role reviewed by root and fresh panel_tabs_final_review; no numeric answer leakage.
- Current real Chrome:60 question/viewport/theme combinations, all3tabs; no console/KaTeX/resource/overflow defects. 1280x900,1024x900,375x812, light/dark; docking,keyboardmove/resize,persistence,breakpoint,focusedmobiletab->desktop,printall10+metadata+restore checked.
- Root visually inspected all20 desktop terminology-panel upper sections across both rounds, provenance-panel sample, mobile dark and floating panels. All final screenshots retained under tmp/ml-panel-tabs/native/roundN/screenshots.
- Core math: unchanged problem-only blind input and answer payload compared; prior independent86subparts preserved; current exact/symbolic checks rerun27+29pass. This UI revision does not claim a new problem-only blind run. Fresh reviewer independently checked new definitions and UI.
- Shared full suite: see panel-final-disposition.md;4existingfailures reproduced with HEAD modules in baseline-failures.log. Legacy1014/1019MD/layout and macOS canonical sibling-directory creation are outside this revision.
- New UI regressions: original/nooriginal,metadatafallback,keyboard,screenbreakpoint,print,accessiblelongformula,focustransfer.
- User spacing hotfix: actual12pxintertabgap,56pxtabheight,24pxbodygap; root desktop/mobile screenshot inspection and18layout/panel tests pass; current120case browser sweep rerun.
