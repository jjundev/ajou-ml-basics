# SDD ledger — plan: docs/superpowers/plans/2026-10-06-ml-review-pdf-migration.md
Ruling: Projectless native worktree tool cannot select the course repository; used detached git worktree in task work/ — required isolation without changing video branch — needs explicit file installation after QA.
Ruling: No commits or pushes; preserve workspace ledger until user requests commit — explicit spec boundary — uncommitted evidence relies on retained checkout.
Pre-flight 1→2→3→4→5: common frozen types and mode/page interfaces agree.
Pre-flight 5→6→7: staged BuildResult paths, final→stage publisher and narrow note patch agree.
Baseline: ml-review-pack 77 tests OK (2 existing skips); ml-preview-note 70 OK.
Task 1: complete (commits c8768a1..c8768a1, tests: python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_cards.py -v → OK)
Task 2: complete (commits c8768a1..c8768a1, tests: python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_payload.py -v → OK)
Task 3: Ruling: Hint test uses 600mm, not 300mm — template legitimately flows 300mm across two columns; need a truly oversized case — no product change.
Task 3: complete (commits c8768a1..c8768a1, tests: python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_render.py -v → OK)
Task 4: complete (commits c8768a1..c8768a1, tests: python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_pages.py -v → OK)
Task 5: complete (commits c8768a1..c8768a1, tests: python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_[bp]*.py -v → OK)
Task 5: Ruling: kernel flock replaces stale-file lock protocol — ownership is released only when process descriptors close; never delete live lock — portable to the user's POSIX/macOS runtime.
Task 6: Skill baseline (fresh consumer): required HTML 2 + MD 2 + figures only; no PDF and permits completion with unresolved checks. Updated guidance requires validated pair and withholds failed pack.
Task 6: Ruling: add manifest PDF links after PDF stage build — first HTML check otherwise sees missing files — validates all final links again before publication.
Task 4: Ruling: condition blocks that cannot fit unchanged fail safely rather than splitting away necessary premises — protects interpretability; exceptionally large future conditions require manual layout review.
Task 6: Ruling: root tests reference removed combined 0909-0916 artifact — retain legacy assertions with explicit skips and add current 7-pack invariants — legacy content checks remain unavailable, disclosed separately.
Task 6: Ruling: root checker falsely joins adjacent table-cell inline math into $$ — emit block separators like the existing skill checker; actual dated tests RED→GREEN — tiny root utility repair, no document rewrite.
Task 6: Green skill consumer: all six artifacts + figures, stage workflow, hashes, all-page QA, lite retains PDF gates, one PDF failure blocks delivery. Pre-existing contradictory connection prose and duplicate-location backup weakness noted for final review.
Task 6: complete (commits c8768a1..c8768a1, tests: python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -v → OK (skipped=2))
Task 7: complete (commits c8768a1..c8768a1, tests: python3 -m unittest discover -s .claude/skills/ml-review-pack/tests -p test_review_pdf_migration.py -v → OK)
Final: Ruling: review-package empty commit range cannot cover uncommitted files — provide working-tree diff plus every new file to fresh reviewer — historical commit evidence remains unavailable until separately authorized.
Final: Ruling: reviewer list-number formatting Minor is Important for source subquestion identity — preserve type/start/reversed/value attributes — original questions could otherwise be misidentified.
Final: Ruling: add optional ReviewPack.source_path metadata — source-relative images require location without modifying raw FigureInput HTML — compatible default None for existing constructors.
Final: Ruling: failed CLI report replaces stale success evidence — --report must describe failure too — report write itself still depends on writable storage.
Final: fixed inline matrix overflow — test_inline_matrix_overflow_is_rejected RED→GREEN.
Final: fixed source-relative PNG — test_relative_image_is_source_relative RED→GREEN.
Final: fixed course relative stage links — test_relative_course_links_resolve_in_isolated_stage RED→GREEN; structured real 0930 full HTML/MD/PDF stage smoke passed.
Final: fixed inline emphasis page split — test_inline_emphasis_never_becomes_sentence_boundary RED→GREEN.
Final: fixed original list numbers — test_split_preserves_subquestion_numbering RED→GREEN.
Final: fixed stale success report after failed second PDF — test_second_pdf_failure_publishes_neither report assertion RED→GREEN.
Final: full suite 114 skill (112 passed/2 legacy skipped), 70 preview passed, 47 root (25 passed/22 legacy skipped), 9 node passed; all 14 existing payloads pass stricter inline/content geometry gate. No template/PDF bytes changed by fix pass.
Final: Ruling: keep full required conditions and fail if they cannot fit — same safe pagination policy as Task4 — unusually long future premises may need editorial layout review.
Final: Ruling: retain pre-existing classroom-connection rule ambiguity — pedagogical content policy outside format migration — future author may need to interpret exception; noted in report.
Final: Ruling: retain initial backup's duplicate-location deduplication — publisher backs up actual overwritten paths independently — convenience first backup may omit a same-name alternate location.
Final: Ruling: retain common Hint label and EC2 header ellipsis/list decorations/continued-page step numbering — exact template requirement — Hint detail is in answer appendix; long titles may abbreviate.
Final: Ruling: POSIX/macOS lock support only — matches verified environment — Windows would require a different lock implementation.
Final: Ruling: no process-crash/disk-failure multi-file atomicity guarantee — recover ordinary replacement exceptions with backups — forced interruption can require backup recovery.
Final: Ruling: missing combined legacy tests stay explicitly skipped — dated packs receive active tests — cannot claim historical combined artifact coverage.
Final: Ruling: install validated files only; preserve Git state and other task files — user authorized implementation, excluded commits/push — changes remain uncommitted in course checkout, scratch worktree retained.
