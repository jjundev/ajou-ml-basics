# Source-only independent derivation packet

The packet creator has seen existing solutions and is NOT the independent reviewer. No approval or correctness status is granted here.

Read only questions.json and the exact figure resources listed there. Do not open the original source HTML: it contains hints, worked steps and answers. Do not inspect fragments, published explanations, audits, existing harnesses, reference_steps, answer_html, solutions.json, old reviews or parent task transcripts. Derive every subpart independently from question conditions/asks. Do not consult the course repository while deriving.

questions.json uses schema_version 1. Per question the strict whitelist is id, title, conditions_html, ask_html, subpart_ids, figures_html, optional original_question_html, and input_sha256. Embedded equations/inline SVGs are original question markup. Figure resource bytes are copied exactly, with original_src mapping to packet_file and sha256. Empty resources means these actual questions use no external image files.

input_sha256 hashes canonical UTF-8 JSON (ensure_ascii=False, sort_keys=True, separators comma/colon) of that question excluding input_sha256. question_payload_sha256 hashes the canonical questions array including per-question hashes. packet_payload_sha256 hashes the canonical document excluding packet_payload_sha256. These question-only digests remain independent of later 6c review/artifact metadata rebinding.

Return a separate results.json without modifying this packet: schema_version 1, packet_payload_sha256, question_payload_sha256, reviewer provenance/identity/context-isolation statement, and results[] containing id, input_sha256, per-subpart derivations, assumptions/dimension/normalization checks, conclusions, unresolved items. Do not compare with reference answers until independent results are frozen. A later authorized comparison reviewer binds frozen independent results to the current reference content. No review/approval pass should be asserted merely because this packet exists.
