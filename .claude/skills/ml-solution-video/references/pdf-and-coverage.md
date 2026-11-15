# ML 카드와 PDF 대응

입력은 복습노트 안의 `복습문제_<range>_<slug>.html/.md`와 같은 stem의 `-문제.pdf`, `-답안.pdf`다. 저장된 article.card의 pN, data-source MML Example/Exercise, h3 제목과 상단 PDF badge·제목·출처를 대조한다. P02/p2는 P2로 비교하며 원본 표기를 바꾸지 않는다. NFC/NFD를 비교한다. 계속 페이지는 원문 순서이며 Hint 부록은 문항이 아니다. 서로 다른 날짜의 같은 P1은 합치지 않는다.

prepare의 `source/pair.json`은 schema_version2 ProblemBundle이다. key는 range:slug:Pn이며 problem_pages/answer_pages의 `{id,role,snapshot,page_index,width_pt,height_pt,continuation}`을 보존한다. page_index는 0-based, continuation은 1-based다. source_files는 html/md/problem_pdf/answer_pdf와 사용한 figure/evidence이다. 모든 파일은 source/snapshots에 SHA로 동결하며 inputs.json에 원래 경로와 SHA를 기록한다. 상대 경로가 RUN 밖이나 비밀 파일을 참조하면 거부한다.

명시적 page-map 예:
```json
{"problems":{"1007:Basics:P1":{"sha256":{"problem":"PDF_SHA","answer":"PDF_SHA"},"problem":[0],"answer":[0,1]}}}
```
같은 PDF 내 중복 index·범위·SHA·badge/출처를 검증한다. 헤더가 읽히지 않는 스캔 PDF를 OCR로 자동 교체하지 않는다.

`layers/candidates.json`의 pages마다 original.svg/native.png/candidate.svg/glyphs/shapes가 있다. 원본 PNG와 SVG를 직접 대조한다. animated 영역만 PageMap으로 지정하며 그래프·조건·Hint를 보존한다. 답안 전체 영역 안의 원본 문자·도형을 모두 정확히 한 번 지정한다. 도형 kind가 unclassified면 원본을 확인해 지원 kind를 저작하며 래스터 풀이를 새 글자로 덮지 않는다.

BundleMap:
```json
{"schema_version":2,"pages":{"answer-1":{"work_bbox":[496,65,1287,657],"steps":[{"id":"s1","glyph_ids":["g00100"],"shape_ids":[],"writing_units":[]}],"terminal_step_id":"s1"}},"step_order":["answer-1::s1"],"answer_step_id":"answer-1::s1"}
```
좌표는 PDF point다. 숫자는 예시이며 실제 입력에서 저작한다. local terminal은 해당 페이지의 마지막 단계이고, 전역 answer_step_id만 최종 정답을 뜻한다. step/glyph/shape 전역 참조는 page_id::local_id다. 서로 다른 페이지의 같은 local ID를 섞지 않는다.

pencil의 writing_units는 `{id,line_id,chunk_id,column_id,band:[x0,x1],glyph_ids,shape_ids,camera_break_before}`다. 원본 glyph_ids 읽기 순서를 보존하며 줄·가로 영역·의미 청크를 별도로 저작한다. 첨자/위첨자는 같은 가로 영역의 원래 위치에 공개한다. 긴 분수선은 여러 clip에 나눠 누적하되 전체 도형 예산은 유지한다. 화면에서 26px 본문·160px 연필이 함께 들어오지 않으면 의미 경계 청크를 나눈다. 임의 bbox 정렬을 의미 승인으로 기록하지 않는다.

`extract`는 각 페이지의 원본/빈/부분/완성/제거 화면을 두 rAF 뒤 캡처한다. 정적 게이트에만 disable-gpu를 사용한다. pixel_diff/non_target_diff/hidden_leaks가 모두0이어야 한다. 모든 답안 페이지 게이트와 현재 파일 SHA를 묶는다. native PNG와 SVG의 직접 대조 및 수학 의미 검토는 별도다.

coverage는 status/passed, pdf_md_agree:true, rows의 `{step_id,pdf_text,md_text,source_refs,meaning_review}`이며 전역 단계 순서와 같아야 한다. pdf_text는 실제 매핑 원본 glyph 순서와 대조한다. PDF/MD 부호·전치·수치가 다르면 그 문항을 차단한다.

math-review는 모든 단계의 variables/dimensions/assumptions/derivation/numeric_checks/visual_checks를 `{applicable:boolean,evidence:string}`으로 기록하고 source_refs/meaning_review를 넣는다. applicable:false도 이유가 필요하다. 실제 계산을 검산하고 그래프 음영·표본/노이즈 의미를 구분한다. 기계 검사는 근거의 구조·현재 해시를 검사하며 수학적 진실을 증명하지 않는다.

`content_fingerprint(manifest,layers,coverage)`로 coverage/math-review의 input_hash를 동일하게 저작한다. source_refs는 `cards:source/snapshots/FILE#pN`, `md:...#pN`, `pdf:...#page=N`(1-based), `figure:...`이며 동결 입력에 실제 존재해야 한다. 원문 인용과 변경된 복습문제 조건이 다른 경우에는 명시된 문제 조건을 설명하고 그 차이를 근거에 적는다.

lesson.json schema1의 steps는 전역 step 순서이며 `{step_id,mode:reasoned|calculation,meaning_notes,source_refs,reason_segment_ids,check_segment_ids,region_ids,annotation_ids}`다. reasoned는 이유가 write 앞에, check는 write 뒤에 있어야 한다. 그래프 focus/annotation은 필요한 경우만 저작한다. calculation은 exemption_reason과 비어 있는 이유/시각 연결 목록을 요구한다.

이전 HTML에 conditions/ask 태그가 모두 없으면 statement_html에 전체 문제 원문을 보존하고 두 분리 필드는 비워 partition_status=author-required로 표시한다. 문장을 자동 분할하거나 질문을 다시 만들지 않는다. PDF의 조건·질문 패널과 전체 statement를 직접 대조한 뒤 source-bound 원고와 coverage를 저작한다. 태그가 한쪽만 빠졌거나 중복되면 손상 문항으로 차단한다.

이전 실행에 동결된 HTML 카드는 기존 `html:...#pN` 참조를 유지한다.
