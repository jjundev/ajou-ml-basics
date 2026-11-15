---
name: ml-solution-video
description: 머신러닝기초 복습문제의 문제·답안 PDF 원본을 보존하며 연필 공개, 한국어 설명, 수학 기호 자막을 넣은 문항별 풀이 영상을 만든다. 날짜 또는 문항을 지정한 문제풀이 영상·재개·대본 검토 요청과 /ml-solution-video에 사용한다.
---

# 머신러닝기초 문제풀이 영상

저장된 복습문제 문항 원고(`.cards.json`)와 MD와 문제·답안 PDF를 사용한다. 원본 조건·그래프·행렬·기호·수치·줄바꿈을 바꾸지 않는다. 새 문제, 대체 유도, 원본에 없는 그래프를 만들지 않는다. PDF의 native glyph outlines를 공개하며 KaTeX 재조판이나 OCR을 쓰지 않는다. 내용 충돌은 해당 문항을 차단하고 보고한다.

## 호출

- `/ml-solution-video 1007`: 날짜의 모든 문항, 문항당 MP4 하나.
- `/ml-solution-video 1007 --problems P2,P3`: 일부 문항.
- `/ml-solution-video 0930-1007 --problems 0930:P1,1007:P1`: 날짜를 포함한 식별자.
- `--pack SLUG`: 같은 날짜 여러 팩 또는 선택 경계를 가로지르는 팩을 명시한다.
- `--review`: 현재 batch 대본을 묶어 한 번 검토한다. 수정되면 승인은 무효다.
- `--writing-mode typing`: typing 선택. 기본은 pencil이다.

날짜는 MMDD 또는 MMDD-MMDD이며 양끝을 포함한다. 여러 날짜의 P1은 별도 문항이다. 같은 날짜 여러 팩은 추측하지 않는다. 카드별 계속 페이지를 모두 묶고 Hint 부록은 제외한다. 모호한 PDF 대응은 `--page-map JSON`으로 명시한다.

## 실행 흐름

스킬 폴더를 S, 반환된 문항 실행 폴더를 RUN으로 둔다. Python에는 PyMuPDF/Pillow, Node에는 로컬 HyperFrames와 puppeteer-core, Chrome, GSAP, libass FFmpeg가 필요하다. 설치 경로는 실제 실행 때 확인한다. 없는 패키지를 전역 자동 설치하지 않는다. `ML_PUPPETEER_CORE_PACKAGE`는 package.json 경로, `ML_CHROME`, `ML_FFMPEG`는 실행 파일 경로다. TTS/cache/budget, GSAP와 Pretendard Bold는 이 스킬 내부에 포함한다.

1. `python3 "$S/scripts/video.py" prepare 1007 --repo "$PWD" [--problems P2,P3] [--pack SLUG] [--page-map FILE] [--review]`. 문항 원고·MD·PDF·사용한 그림을 동결하고 페이지별 후보 SVG/native PNG를 만든다. 유료 요청은 0이다.
2. [PDF와 원문 대응](references/pdf-and-coverage.md)을 읽는다. 동결 원문·native PNG·후보 SVG를 직접 대조하고 `source/map.json`을 저작한다. `extract --run RUN`은 답안의 모든 페이지에 exact-zero 공개 검사를 실행한다.
3. `source/manifest.json`, `coverage.json`, `math-review.json`, `lesson.json`을 저작한다. 이유→작성→검산 순서를 사용한다. 이유에 불필요한 그래프 표시를 강제하지 않는다. focus/annotations는 필요할 때만 저작한다. `check --run RUN`이 현재 원문·단계·해시·자막을 검증한다. 기계 검사는 수학적 진실을 증명하지 않는다.
4. [음성과 타이밍](references/narration-and-timing.md)을 읽는다. `tts --run RUN [--env-file FILE] [--config FILE] [--approve-review]`가 원고만 합성한다. 키는 환경에서만 읽고 출력·설정·커밋에 넣지 않는다. 성공 청크와 raw WAV를 보존한다.
5. `retime --run RUN [--writing-config FILE]`은 기존 PCM과 검토된 수동 trim으로 타이밍을 다시 만든다. 대본 text가 바뀌면 tts를 먼저 실행한다. 자막만 바꾸면 동일 text 청크 WAV를 캐시에서 재사용한다.
6. `assemble --run RUN --runtime "$S/assets/runtime/vendor/gsap.min.js"`, `render --run RUN --hyperframes-entry /ABS/dist/cli.js`, `captions --run RUN`을 실행한다. 페이지별 렌더러를 한 상위 frame clock으로 구동하며 페이지 경계·seek를 검증한다.
7. [검증과 게시](references/verification.md)를 읽는다. 실제 음성의 모든 청크와 최종 영상을 청취·확인하고 현재 해시에 audio/visual-review를 기록한다. `verify --run RUN --hyperframes-entry ...`와 `publish-set --batch BATCH`를 실행한다. 실제 청취가 없으면 complete=false/live_audio=unverified다. synthetic PCM으로 의미 검토를 승인하지 않는다.
8. `resume-set --batch BATCH`로 처음 무효인 단계를 찾는다. 실패 문항·성공 형제·이전 결과를 보존하며 같은 RUN에서 재개한다.

prepare/extract/check는 유료 서비스를 부르지 않는다. 저작이 덜 됐으면 author-required와 누락 파일을 반환한다. 경고는 원문 대조 대상이며 별도 승인 단계를 추가하지 않는다. 입력·WAV·trim·주석·폰트·코드·출력이 바뀌면 관련 단계와 현재 검증 근거를 무효화한다.

## 고정 제작 계약

1920×1080, 30fps, 흰 PDF, 하단 180px 자막 영역이다. 1440×810pt PDF 전체를 맞추며 1920×900으로 다시 줄이지 않는다. A4는 원본 비율로 호환한다. 그래프·조건·Hint는 원본에 남긴다.

연필은 초당 7.5글자, 화면상 160px다. 저작한 writing_units의 줄·영역·청크에 따라 native glyph를 공개한다. 실제 한글·수학 획순 복원이 아니다. 본문/label 최소 26px, 카메라 전환 12프레임이며 작성 중에는 고정한다. 긴 줄은 의미 청크로 나눈다. 도형 draw 예산은 `min(90,max(18,ceil(W/H×glyph_interval)))`이고 clip 조각에 폭으로 배분하며 합계를 보존한다. 60프레임 초과 필기 지연과 음성 공백에는 현재 hash의 명시적 pacing 근거가 필요하다.

Vertex AI Express / gemini-2.5-flash-tts / Aoede / ko-KR / mono PCM 24kHz 16bit를 기본으로 한다. 공급자·모델을 자동 대체하지 않는다. 예산 기본 null, 요청 동시성2/최대 시도4다. TTS에는 spoken-text-only-v1 원고만 보낸다. direction/“원고:”/caption을 읽히지 않는다.

모든 신규 segment에 pcm-chunks-v1 `{id,text,caption_text}`를 저작한다. 표시용 숫자·θ/φ/Σ/전치·첨자·분수는 직접 적는다. 한글 숫자를 전역 치환하지 않는다. cue는 최대 두 줄/줄당34자이며 보호된 수식이 넘치면 저작을 고친다. 임의 연결 무음·자동 에너지 절단·단어 내부 강제 정렬을 하지 않는다. SRT는 실측 샘플 경계, 오차1ms/영상 경계1프레임이다. libass는 `WrapStyle2, BorderStyle4, Outline0, Shadow4`, Pretendard Bold14/Alignment2/MarginV14를 유지한다.

주석은 2–12px의 화면상 일정 굵기이며 기본3px다. 저작 시 보조4/중요6/결과8px를 권한다. page/source hash와 이미 공개된 영역에 묶으며 future solution focus를 거부한다. chunk_id+offset으로 측정된 발화 안에 move8+draw를 끝낸다. 원본 필기·주석은 한 연필을 공유하고 최종 hold에는 숨긴다.

## 저장과 검증 경계

`문제풀이영상/<선택범위>/`에는 자연스러운 제목의 최종 MP4와 `<선택범위>_제작자료/`만 둔다. 과제1은 `문제풀이영상/과제1/`에 생성한다. 검토용 영상도 선택범위 폴더 바로 아래에 두되 음성 검수 상태를 명시하고 publish/latest 승인을 대신하지 않는다. 모든 원고·캐시·검증·이전 버전은 제작자료 안에 둔다. 범위 영상은 날짜, 여러 팩은 slug도 파일명에 넣는다. 전체 성공일 때만 latest를 바꾼다. 게시 교체 실패는 journal로 롤백하며 강제 종료 상황의 원자적 다중 파일 갱신을 주장하지 않는다.

EC2 기준은 `eeec3d56513fe9e8a34f45edb05ae1118b08cf62`다. `assets/port-provenance.json`에 84개 원본 파일과 6개 자체 부품의 SHA·이식 위치·검사 대응을 기록한다. 런타임은 다른 과목 checkout을 요구하지 않는다. `tests/ml_acceptance.py`는 1007 P2/P3/P8의 고정 좌표 검사를 위해 `2e09a745`의 PDF를 scratch로 복사하고 현재 문항 원고와 당시 문항 조각의 동등성을 확인하며 기본 synthetic/paid0/게시 차단이다. 다른 날짜의 저작 템플릿으로 좌표를 재사용하지 않는다.

## 멀티코어 렌더 정책

render는 CPU 인코딩, browser GPU auto, fast capture false를 유지하며 파트·문항을 순차 처리한다. Apple M5/물리 10코어/16GiB 이상 macOS는 내부 작업자 6개, 나머지·탐지 실패는 2개다. `render --render-workers 1..6`은 유효한 저장값보다 우선하며, 손상된 저장 설정은 거부한다. 설정은 `source/render-options.json`, 실행 기록은 `verification/render-receipt.json`에 보존한다. 신규 RUN은 기본값을 저장하고, 기존 RUN은 render에서만 생성하며 resume-set은 설정을 쓰지 않는다. 작업자 변경은 render 이후만 무효화하여 음성·대본·타임라인·composition을 보존한다. 실패 시 이전 마스터/기록을 복구하며 남은 `.rollback` 파일은 확인 전 재교체를 차단한다.
