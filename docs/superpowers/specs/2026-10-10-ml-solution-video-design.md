# 머신러닝기초 PDF 문제풀이 영상 설계

## 확정 의도와 범위

EC2의 PDF 원본 공개·연필·음성·자막 제작 흐름을 ML용 독립 `ml-solution-video`로 옮긴다. architectural 작업이다. 기존 답안의 문장·수식·수치·줄바꿈·순서·배치를 유지하면서 조건 → 기호·규칙의 이유 → 해당 원문 필기 → 결과 확인을 설명한다.

대화의 결정 #0=A(독립 포트)를 유지한다. #8=PDF 원본 공개+설명·주석, #9=날짜의 모든 문제는 후속 계획 요청에서 변경하지 않아 confirmed by default다. 이번 문서와 계획 작성은 실행 승인이 아니다. 실행 방법은 계획 검토 후 정한다.

- 스킬 위치: `/Users/hyunjun_macbook_pro/Documents/Univ/머신러닝기초/.agents/skills/ml-solution-video`.
- 입력: 저장된 복습문제 HTML·MD, 문제/답안 PDF 쌍, 참조 그림. 정리노트·STT·강의노트·MML 교과서는 설명 근거가 실제 필요할 때 읽고 사용한 부분과 파일만 동결한다.
- 날짜만 지정하면 해당 팩 모든 문항. `--problems P2,P8`은 단일 팩에서 선택한다. 범위에서 `1007:P2`를 지원한다. 팩이 모호하면 `--pack SLUG`로 명시하도록 후보를 제공한다. 서로 다른 날짜의 P1을 합치지 않는다.
- 날짜 범위는 시작·끝 포함이다. 범위형 팩은 기간이 완전히 포함될 때 선택하고 경계에 걸친 팩은 명시적 `--pack` 없이 조용히 일부 날짜로 해석하지 않는다. 연도 없는 MMDD의 연말을 넘는 범위는 지원하지 않는다.
- 호출의 날짜 선택은 필수다. 기존 노트 생성 스킬을 자동 호출하지 않는다.
- 출력은 문항별 MP4. 새 문제·답안·대체 유도·원본에 없는 그래프를 생성하지 않는다. 기존 입력·과목 스킬·다른 과목 파일을 수정하지 않는다.

## 기준과 실제 확인한 상태

포트 소스 저장소는 `/Users/hyunjun_macbook_pro/Documents/Univ/전자회로2`다. 이 경로는 구현 때 git blob을 읽는 용도이며 새 스킬 실행 의존성이 아니다.

EC2 고정 커밋은 `eeec3d56513fe9e8a34f45edb05ae1118b08cf62`(2026-10-10, fix(ec2-video): improve circuit ink and captions)다. 최신 HEAD로 자동 바꾸지 않는다. 해당 커밋의 `.agents/skills/ec2-solution-video/` 추적 파일 84개와 review-video의 필요한 TTS/cache/budget·폰트·GSAP 부품을 파일별 SHA256과 원 경로로 기록하여 포트한다. 실행 중 EC2 checkout 또는 EC2 review-video를 요구하지 않는다.

현재 ML `ml-review-video`에는 캐시만 있고 SKILL.md/실행 소스가 없다. 이를 실행 의존성 또는 구현 근거로 쓰지 않는다. 실제 `ml-review-pack`은 `.claude/skills/ml-review-pack`이며 `.agents`의 경로는 symlink다. 이 스킬도 수정하지 않는다.

현재 ML 복습문제 HTML은 0909/0914/0916/0921/0923/0928/0930/1007의 55문항이다. 1007은 P1–P8, 답안 PDF는 본문 8쪽+Hint 부록 1쪽이다. P3은 그래프 읽기, P2는 수치·차원 확인, P8은 긴 완전제곱식 유도다. 현재 샘플의 계속 페이지 존재를 주장하지 않는다. PDF 생성기의 PageSlice/continuation 계약이 있으므로 향후 계속 페이지를 지원한다.

## 원본과 데이터 계약

HTML 카드의 id=`pN`, h3 제목, `data-source=MML Example/Exercise ...`, 조건·질문·풀이 단계·정답을 읽는다. 지원된 저장 HTML을 직접 파싱하며 JS 실행 결과를 원문으로 삼지 않는다. MD의 해당 문항과 수식·조건·답을 대조한다. 누락 MD, 누락 PDF, HTML/PDF/MD의 의미 충돌은 해당 문항을 중단한다.

문항 내부 key는 `range:slug:Pn`, pack_id는 `range:slug`다. 공개 problem_id는 Pn이다. 선택자는 NFC 비교, 숫자 비교로 P02/P2/p2를 P2로 정규화하되 원본 표제는 보존한다. 같은 pack/card의 중복 발견은 오류다. 파일명이 다른 같은 팩을 내용이 같다는 이유로 자동 병합하지 않는다.

ProblemBundle은 문제/답안 페이지를 각각 순서 있는 목록으로 가진다. 각 PageRef는 id, role, snapshot, page_index(0-based), width_pt, height_pt, continuation(1-based)를 가진다. 문제/답안 페이지 수는 달라도 된다. 제목·문항 badge·MML 출처를 함께 대조하고 Hint 부록은 제외한다. 계속 페이지를 놓치거나 중복시키지 않는다. 자동 대응이 불명확하면 `--page-map JSON`의 명시 대응을 검증한다. 사용자 지정도 출처·해시·페이지 범위·중복을 검사한다.

각 답안 페이지는 자체 PageMap과 SVG/native PNG/glyph/shape 목록을 가진다. 페이지 내 local ID는 재사용할 수 있고 전역 step/segment/glyph/shape 참조는 `page_id::local_id`로 식별한다. 배열이나 PDF paint order를 의미 순서로 자동 추정하지 않는다. glyph·shape·분수선·근호선·첨자·답 상자 모두 한 번씩 대응한다. 중간 페이지의 마지막 단계는 일반 풀이이며 문항 전체 최종 단계만 answer다.

입력은 RUN 내부 `source/snapshots/`로 SHA256 동결하고 원 경로/해시/도구 버전을 inputs.json에 기록한다. 절대 실행 경로와 무관한 스냅샷 상대 경로를 직렬화한다. 같은 내용 해시여도 과목·팩·문항 identity는 합치지 않는다. 외부 경로를 가리키는 이미지, 경로 탈출, 스냅샷 손상은 실패한다.

## 내용 검토와 교육 흐름

`coverage.json`은 모든 전역 step의 PDF 원문, MD 대조, source_refs, meaning_review를 기록한다. source_refs는 `html:<snapshot>#pN`, `md:<snapshot>#pN`, `pdf:<snapshot>#page=N`(1-based), `figure:<snapshot>`를 사용한다. snapshot은 동결 입력의 상대 경로이고 참조 anchor/페이지 범위를 확인한다. `math-review.json`은 같은 순서로 variables/dimensions/assumptions/derivation/numeric_checks/visual_checks/source_refs/meaning_review를 가진다. dimensions/derivation/numeric_checks/visual_checks는 `{applicable: bool, evidence: str}`이며 해당하지 않는 경우에도 이유가 비어 있으면 실패한다. 실제 계산·차원 자료가 필요한 단계에 applicable=false를 넣어 회피할 수 없으며 의미 검토에서 확인한다.

수학 검토는 변수·행렬 차원, 전치, 부호, 독립성·조건부 확률·가역성 등 적용 가정, 분산/표준편차, 평균/공분산, 정규화·상수 생략 범위, 숫자 계산을 다룬다. 그래프는 축·범례·음영·함수와 관측 노이즈의 구분을 확인한다. 자동 검사는 검토의 누락/해시/대응을 검사하며 임의 수학의 진실을 자동 증명했다고 주장하지 않는다.

`lesson.json`은 모든 step 순서와 mode=`reasoned|calculation`, reason/check segment, page/region/annotation 참조, meaning_notes, source_refs를 가진다. 핵심 규칙을 적용하는 reasoned 단계는 먼저 이유를 설명한다. 강조 표시는 필요한 경우만 만들고 새 계산을 추가하지 않는다. 제목·후속 계산 단계는 exemption_reason으로 불필요한 왕복을 피한다.

PDF·MD 충돌, 스캔/풀이 이미지, 해석 불가능한 도형/클립, 원문 누락은 해당 문항 실패다. 마지막 전체 화면을 원본 래스터로 교체해 공개 오류를 숨기지 않는다. 내용·SVG 게이트가 현재 입력에서 통과하기 전에는 유료 요청이 0이어야 한다.

## 화면·필기 계약

- 1920×1080/30fps, 기본 원본 PDF 1440×810pt, 하단 180px(900≤y≤1080) 자막 영역.
- 16:9 PDF 전체를 1920×1080에 맞춘다. 1920×900으로 다시 축소하지 않는다. 원본을 재조판하지 않는다.
- A4 가로는 기존 profile의 비율 유지·상단 900px content fit으로 호환하며 별도 PDF 생성은 하지 않는다.
- 신규 기본 pencil, 7.5 chars/sec, 연필 길이 160px. typing은 명시 선택할 수 있다. 배경음·필기·타이핑 소리는 없다.
- writing_units로 의미상 줄·가로 band·chunk를 저작한다. 같은 줄 안 첨자·위첨자·분수·근호의 원래 위치를 유지한다. 실제 획순을 복원했다고 주장하지 않는다.
- 본문·label 최소 26px, 카메라 이동 12프레임. 전체 줄과 실제 연필 여백이 들어온 뒤 작성하며 해당 chunk 동안 구도를 고정한다. 긴 줄은 의미 경계로 나눈다.
- 원본 도형별 작성 프레임은 `min(90,max(18,ceil(W/H×글자간격프레임)))`, clip 폭으로 배분, 조각당 최소 1프레임. 예산보다 조각 수가 많으면 실패한다.
- 글자 없는 도형 chunk는 페이지 전체와 연필 여백을 맞춘다. 글자 26px 검사를 도형-only 구도에 잘못 적용하지 않는다.
- focus는 조건·수식·행렬·표·그래프·이미 공개한 단계 중 원문 영역을 참조한다. 아직 공개되지 않은 풀이를 focus/주석으로 누설하지 않는다. 회로 전용 상단-only 제약은 제거하되 자막 영역 침범·원문 가림은 금지한다.
- 주석은 arrow/underline/ellipse/짧은 label. 원본 필기와 같은 연필을 공유한다. `stroke_width_px` 유한수 2–12, 생략값 3, 저작 기본 보조 4/중요 관계 6/결과 강조 8px. 역할 색은 #1565C0/#C45100/#237A43/#8E348E를 ML 의미에 배정하고 위치·기호로도 구별한다.
- 선 굵기는 확대와 무관하게 유지한다. 카메라에 굵은 선 반경·화살촉·label·연필을 포함한다. glyph alias Δ/∆는 실제 폰트 glyph ID가 같을 때만 허용하고 저작 기호는 보존한다.
- 주석은 `chunk_id`의 실측 시작 기준 offset_frames를 사용한다. 같은 segment에서 legacy/청크 오프셋을 혼용하지 않는다. move8프레임+작성은 해당 청크 음성 안, 카메라 복귀 전(segment end−13) 완료한다. 넘치면 저작 오류이며 임의 무음을 늘리지 않는다.
- 설명 중 주석은 누적/명시 hide_at을 지원하며 다음 풀이 복귀 시 정리한다. 최종 각 페이지 전체 hold에 연필·커서·주석을 숨긴다. 임의 forward/backward/GSAP seek에서 같은 공개 상태가 나온다.

## 음성·자막 계약

- 기본 Vertex AI Express / gemini-2.5-flash-tts / Aoede / ko-KR / mono PCM 24kHz/16bit. 자동 공급자·모델 대체 없음. 공급자의 현재 가용성은 실행 시 실제 응답으로 확인한다.
- 예산 상한 기본 null, 요청 전체 공용 usage ledger. 요청 재시도 최대 4회, 기본 동시 요청 2. 키는 환경/명시 env 파일에서만 읽고 출력·동결·Git 저장하지 않는다.
- `spoken-text-only-v1`: 읽을 text만 전송하며 direction·“원고:”·caption_text를 입력에 넣지 않는다. EC2의 회로 발음 사전은 ML 기호 저작으로 교체한다.
- 모든 신규 segment는 `caption_timing=pcm-chunks-v1`의 `{id,text,caption_text}` 청크를 가진다. 부모 text/caption_text는 청크 공백 연결과 같다. 일부 청크 누락을 legacy로 자동 처리하지 않는다.
- 성공 raw WAV/영수증을 재사용한다. 연결은 raw PCM 샘플 그대로, 임의 무음 없음. SRT 오차 ≤1ms, 영상 cue 경계 ≤1프레임. 단어 단위 강제 정렬을 주장하지 않는다.
- 실청취로 확인한 긴 무음만 raw_sha256/start_sample/end_sample/reason의 chunk-trims.json으로 수동 절단한다. raw WAV를 보존하고 retime 전 검증한다.
- text는 한국어 발음, caption_text는 원문의 숫자·기호·대소문자·첨자·전치·부호·분수·괄호를 보존한다. 한글 숫자를 전역 자동 치환하지 않는다.
- 문장 온점·수식/괄호 밖 쉼표에서 cue 교체. cue 최대 두 줄/줄당 34자. 설명/수식 경계 → 일반 공백 → 괄호 밖 연산 경계 순으로 줄바꿈한다. 중첩 괄호·식별자·소수·분수·부호는 보호한다. 긴 연산자는 다음 항과 같은 줄이다. 안전한 배치가 없으면 저작 오류이며 글자 축소/자동 축약으로 통과시키지 않는다.
- 표시용 온점 보정은 저장 text/WAV를 바꾸지 않는다. 불균형 괄호·LaTeX 원문·지원되지 않는 종결은 TTS 전 오류다. 숫자/연산 표기 검사 error/warning 구분·segment/span 근거·유료 요청 전 경고 출력은 계승한다.
- libass `WrapStyle=2, BorderStyle=4, Outline=0, Shadow=4`, Pretendard Bold/FontSize14/Alignment2/MarginV14. cue 전체의 균일 박스와 지정 개행을 유지한다.
- 자막만 바꾸면 같은 WAV·청크 실측 시작/끝을 재사용한다. 현재 내용 검토·timeline/SRT/final 검증은 갱신한다. writing/retime 변경도 유료 재합성 없이 실행한다.

## 단계·검증·저장

`prepare → extract → check → tts → assemble → render → captions → verify → publish-set`; `retime`, `resume-set`을 지원한다. 상태 단계는 inputs/layers/script/voice/timing/composition/render/captions/verify/publish다. 모든 페이지·review·주석·폰트·adapter·코드·출력 해시를 stage 지문에 포함해 최초 무효 단계로 재개한다. 깨진 캐시를 삭제하지 않고 이유를 보고한다.

`--review`는 batch 전체 현재 대본 지문에 한 번 승인, 기본 호출에는 승인 단계를 추가하지 않는다. synthetic PCM은 기술검사에만 쓰며 audio_meaning/publish를 승인하지 않는다. 실제 청크별 transcript_match/no_instruction_speech/natural_join/sync_passed와 최종 MP4 청취·시각 근거가 모두 있어야 complete=true다. 미청취는 complete=false/live_audio=unverified의 검토용 결과다.

음성 종료 후 필기 지연 >60프레임(2초)은 현재 hash의 writing_lags 명시 검토가 필요하다. 필기 중 무음과 완성 화면 hold를 구분한다. 70–85% 음성 밀도는 저작 가이드이며 자동 의미 승인 기준이 아니다.

정적 SVG original/empty/partial/complete 비교는 정확한 pixel/non-target/hidden leak=0이다. setContent·공개 변경 후 두 requestAnimationFrame 뒤 캡처하며 정적 게이트에만 disable-gpu를 적용한다. 다른 렌더에 적용하거나 허용 오차를 늘리지 않는다. 주석 검사는 glyph 상태·청크별 안정 완료 프레임·역방향/GSAP seek·별도 화면 기대값을 검사하고 teaching browser만 600초, 다른 browser는 기존 120초를 유지한다. SRT cue 번호/전체 text/개행/PCM 시각을 기대 SRT와 완전히 대조한다.

최종 출력은 `문제풀이영상/<selector>/<문항 ID — 자연스러운 제목>.mp4`, 범위에는 날짜 prefix를 넣는다. 여러 팩에는 slug도 넣어 중복을 막는다. 지원자료·WAV·raw/master/SRT/HTML/SVG/검증/usage와 같은 제목의 이전 결과는 `<selector>_제작자료/실행/<run_id>/videos/<safe_key>/`에 둔다. _자막 접미사 없음. catalog/README는 실제 SHA256, latest는 전체 성공 때만 갱신한다. 일부 실패 시 검증된 문항만 게시할 수 있으나 실패 문항·기존 파일·형제 결과를 보존한다. 공개 폴더에는 최종 MP4와 제작자료 폴더만 둔다.

## 검증 완료 조건과 제외

새 skill validator, Python/JS 회귀, 페이지별 원본 게이트, ML CLI 전체 흐름, 수치·그래프·긴 유도의 실제 PDF scratch 수용 검사를 수행한다. 계속 페이지/A4/같은 P번호/Hint 부록/손상 스냅샷/부분 실패/자막-only·retime 캐시를 검사한다. 실음성 검증이 없으면 제작기 기술 완료와 영상 교육 품질 완료를 구분한다. 구현 계획에 유료 호출·영상 공개·커밋·푸시를 자동 승인하는 효과는 없다.

원본 PDF 재생성, 기존 review-video 복원, 외부 사이트 게시, 스캔 OCR, 실제 필기 획순, 별도 음성-only 교체 기능은 제외한다.
