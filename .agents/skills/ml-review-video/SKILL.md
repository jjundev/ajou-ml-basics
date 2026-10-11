---
name: ml-review-video
description: 완성된 머신러닝기초 복습노트에서 수식·그래프·확률 변화의 애니메이션이 이해에 도움이 되는 부분을 골라 주제별 한국어 복습 영상을 만든다. 복습 영상 제작·영상 복습·기존 영상 재개·목소리 교체 또는 /ml-review-video 호출에 사용한다. 정리노트와 문제 작성은 ml-review-pack을 사용한다.
---

# 머신러닝기초 복습 영상

수업을 이미 들은 학생을 위한 주제별 애니메이션 복습 영상이다. **노트 전체 읽기 → 영상이 필요한 부분 선정 → 학습 질문별 묶기 → 대본·수식·장면 → 음성·렌더 → 검증·전달**을 자동 완주한다. 선정한 주제가 N개면 영상도 N개다. 통합 영상은 명시적 전체 복습 요청에만 만든다.

기본: ml-review-pack HTML 템플릿 스냅샷, 다크모드(고정, 라이트 렌더 금지), Pretendard, 한국어 Vertex AI Aoede, 1920×1080 30fps. 길이는 주제별 1–3분 목표지만 설명에 필요한 유도·조건을 누락하지 않고 연장한다. 비용 상한은 기본 null, 요청별 사용량 ledger를 유지한다. 예산은 사용자 지정 시만 설정한다. 모델/공급자/음성을 자동 대체하지 않는다.

SKILL은 이 파일의 폴더, REPO는 머신러닝기초 저장소 루트다. RUN과 BATCH는 prepare 계열 명령의 반환값이다. Python 명령의 SKILL/REPO/RUN/CONFIG/PLAN을 실제 절대 경로로 펼친다. 원자료·기존 노트·기존 템플릿을 수정하지 않는다. STT에서 노트를 만드는 일은 ml-review-pack이 담당한다.

인자: MMDD, MMDD-MMDD, 노트 폴더, --review, --resume, --revoice --voice NAME. 날짜가 없으면 가장 최근 복습노트 폴더를 택하고 선택한 범위를 알린다. 복습노트가 없으면 먼저 ml-review-pack 실행이 필요하다고 알린다.

## 준비와 인증

REPO의 STT/, 강의노트/, 교과서/Mathematics_for_Machine_Learning.pdf와 `.agents/skills/ml-review-pack`을 확인한다. Unicode 이름은 실제 검색 결과를 사용한다.

API 키는 프로젝트 루트 `.env`를 사용한다. 최초 설치 시 `python3 SKILL/scripts/setup_env.py --source /Users/hyunjun_macbook_pro/Documents/Univ/생명과학/.env --destination REPO/.env`로 복사한다. 이미 설치한 파일은 매번 다시 복사하지 않는다. 동일 바이트는 재사용, 다른 파일은 덮어쓰지 않고 충돌을 보고한다. 권한 0600과 Git 제외를 확인한다. `.env` 내용·키·키 해시는 출력하거나 제작자료·스냅샷·fixture·커밋에 넣지 않는다. [음성·인증·예산](references/voice-and-budget.md)을 따른다.

prepare/prepare-set/tts에 `--env-file REPO/.env`를 전달한다. 명시 파일의 GOOGLE_API_KEY → GEMINI_API_KEY 순서로 사용한다. 명시 파일에 키가 없으면 다른 셸 키로 대체하지 않는다. 키는 config.json에 넣지 않고 env_file 경로만 기록한다.

렌더 자산은 `SKILL/assets/runtime`에 fonts/와 vendor/를 포함한다. 다른 과목 폴더 없이 동작한다. HyperFrames CLI Node entry와 FFmpeg/ffprobe는 로컬 설치 경로를 확인한다.

## 절차

1. **전체 읽기·선정.** HyperFrames entry skill을 읽고 기존 의도/디자인으로 복습 explainer workflow를 사용한다. [선정·묶음](references/selection-and-batches.md)에 따라 정리노트 HTML/MD·복습문제·그림을 읽는다. 장마감은 있으면 참고한다. 예고는 기본 선정에서 제외한다. 전체 개념과 선정/비선정 이유·학습 질문·선수 개념·상태 변화를 selection.json에 남긴다. `plan-check RANGE --repo REPO --selection PLAN` → `prepare-set RANGE --repo REPO --selection PLAN --env-file REPO/.env` 순서로 실행한다. --review이면 prepare-set에도 붙인다.
2. **출처와 내용 범위.** [출처·coverage](references/sources-and-coverage.md)에 따라 영상별 requirement와 발화 대응을 manifest.json과 source/coverage.md에 남긴다. 필요 시 STT·강의노트·MML 쪽으로 대조한다. 원문 수치·조건·독립 가정을 바꾸지 않는다. 새 수치 예시는 설명용으로 표시한다.
3. **수식·대본·장면.** [대본·수학·화면](references/narration-and-motion.md)에 따라 주제별로 왜 필요한가(문제 → 단순 해법의 한계 → 핵심 아이디어)를 15–25초로 연 뒤 작은 예시 → 상태 변화 → 대응 수식 → 조건/오개념 순서로 작성한다. 원문에 있는 동기를 해당 영상에 연결하고 노트 전체의 공통 동기를 모든 영상에 강제하지 않는다. manifest의 segments/scenes, source/scene-fragments의 HTML/motion JSON, source/math-evidence.json을 작성한다. 계산 스크립트를 실행해 결과와 시작·중간·끝 그림을 연결한다. `check --run RUN` 통과가 TTS 전제다. --review이면 전체 선정·장면을 묶어 한 번 검토한다.
4. **음성.** `tts --run RUN --env-file REPO/.env`로 생성한다. --review에서 승인된 경우 --approve-review를 추가한다. 기호 원문 대신 대본의 자연스러운 한국어 발화를 읽고 선수 개념·조건·단위를 보존한다.
5. **실측·화면 조립.** `assemble --run RUN --pack REPO/.agents/skills/ml-review-pack --assets-from SKILL/assets/runtime`. 템플릿을 동결하고 실측 PCM으로 타이밍을 맞춘다. 수식은 로컬 KaTeX로 조립 시 렌더하여 단독 장면과 편집 소스에 모두 포함한다. 넘치면 장면을 나눈다.
6. **렌더.** `render --run RUN --hyperframes-entry LOCAL_HYPERFRAMES_BIN`. CPU 인코딩과 browser GPU auto로 장면을 순차 렌더하고 PCM을 결합한다. OS 전역 GPU 설정은 변경하지 않는다.
7. **검증.** [검증](references/rendering-and-verification.md)에 따라 모든 장면을 브라우저·대표 이미지로 확인하고 수식/그래프/축/단위/조건, 음성 발음, SRT, 편집 소스와 최종 MP4를 검토한다. reviews.json에 현재 input_hash와 실제 근거를 기록하고 `verify --run RUN --hyperframes-entry LOCAL_HYPERFRAMES_BIN`을 실행한다. 내용의 정확성을 ID나 해시 검사만으로 주장하지 않는다. 하드 자막본은 마스터 검증·전달 후 별도 검사한다.
8. **전달·재개.** 모든 선정 RUN이 검증된 뒤 `publish-set --batch BATCH`. 이어서 "자막 (고정)" 절에 따라 모든 영상에 하드 자막을 굽고 접미사 없는 제목으로 교체한 뒤 목록을 갱신한다. 일부 실패 시 완료된 영상과 음성을 보존한다. `resume-set --batch BATCH` 또는 기존 단일 `resume --run RUN`이 알려주는 첫 미완료 단계부터 재개한다.

## 자막 (고정)

화면 안에는 하단 고정 문구(`.video-caption`)를 넣지 않는다. 핵심 문장은 장면의 "꼭 기억해요" 박스로만 보여 준다. 자막은 렌더 후 **하드 자막**으로 굽는다. 검증(`verify`)과 `publish-set`은 자막 없는 마스터로 수행하고, 그 뒤 날짜 폴더에는 **자막본만 남긴다.** 자막본의 파일명에는 `_자막` 같은 접미사를 붙이지 않고 영상 제목 그대로(`<영상 제목>.mp4`) 둔다.

```text
python3 SKILL/scripts/video.py burn-subtitles --video "<제목>.mp4" --srt RUN/narration.srt --output "<제목>_자막.mp4"
```

`burn-subtitles`는 입력 파일을 덮어쓰지 않으므로 임시 이름(`_자막`)으로 만든다. 자막본 검사(`status: passed`)와 대표 프레임 확인이 끝나면 자막 없는 `<제목>.mp4`를 지우고 `<제목>_자막.mp4`를 `<제목>.mp4`로 바꾼다. 같은 이름의 파일이 이미 있으면 덮어쓰지 말고 멈춘다. 모든 영상을 바꾼 뒤 `복습영상/README.md`·`catalog.json`의 경로·크기·SHA256을 실제 남은 파일 기준으로 갱신한다.

모양은 Pretendard 굵게 흰 글자, 하단 중앙, 검정 약 70% 불투명 박스(패딩 `Outline=4`)다. 설정은 `scripts/lib/subtitles.py`에 고정했으며 사용자가 바꾸라고 하지 않는 한 건드리지 않는다.

- 폰트 Pretendard Bold(`assets/fonts/Pretendard-Bold.ttf`, 영상 본문과 동일 서체). libass는 woff2를 읽지 못하므로 TTF를 쓴다. 맑은 고딕 등 시스템 폰트로 대체하지 않는다.
- 하단 중앙, 흰 글씨·검정 반투명 박스, FontSize 14, MarginV 22(1080p에서 하단 약 80px 위). 화면 하단의 박스·본문과 겹치지 않는다.
- narration.srt의 긴 문단 자막은 문장·쉼표 단위(한 줄 약 34자 이하)로 쪼개고 글자 수 비례로 시간을 나눈다. 시간은 글자 수 비례이며 정확한 단어 타이밍이 아니므로 대표 프레임과 재생으로 확인한다.
- 긴 문장은 두 줄로 줄바꿈한다.
- 재인코딩은 libx264 crf 18, 오디오는 복사한다.
- 마스터를 지운 뒤에는 제작자료의 `review.mp4` 링크와 latest.json의 영상 해시가 남은 자막본과 맞지 않는다. 이는 의도된 상태이며 제작자료를 자막본에 맞춰 고치지 않는다. 자막본은 검증 지문의 대상이 아니다.
- 목소리 교체·재검증·자막 재굽기에 마스터가 필요하면 해당 RUN에서 `render`를 다시 실행해 마스터를 재생성한다(음성 캐시를 재사용하므로 TTS 유료 요청은 없다). 자막본을 `--source-run`이나 자막 재굽기 입력으로 쓰지 않는다(자막이 이중으로 들어간다).

FFmpeg subtitles/libass 필터가 필요하다. macOS 기본 빌드에 없으면 로컬 ffmpeg-full을 자동 선택하며 사용자 PATH는 변경하지 않는다. 없으면 구체적인 의존성 오류를 보고한다.

## 선정 기준

계수에 따른 회귀선·잔차·손실, 사전/가능도/사후분포, 주변화의 가중 합, 점구름·공분산·아핀 변환처럼 움직임이 특정 혼동을 해결하는 부분을 고른다. 최적화는 배운 범위에서만 다룬다. 단순 정의·목록·비교표는 독립 영상으로 만들지 않는다. 선수 개념은 해당 영상 안에서 짧게 설명한다. 한 학습 질문에 필요한 수식 유도와 상태 변화는 하나로 묶고 같은 주개념을 중복 선정하지 않는다.

0개면 선정 기록과 이유만 전달하며 TTS/MP4를 생성하지 않는다. 기본 자동 실행에서는 선정 목록·이유·예상 길이를 알리고 진행한다. --review일 때만 사용자 검토를 기다린다.

## 고정 출력

`복습영상/<날짜 또는 기간>/`에 하드 자막을 구운 자연스러운 한국어 제목의 최종 MP4 N개와 `<기간>_제작자료/` 하나를 둔다. 제작자료/실행/<실행ID>/ 안에 selection.json·batch.json·원자료 스냅샷·공용 ledger를, videos/<주제ID>/ 안에 대본·자막·시간표·계산 증거·HTML·음성·검증을 보관한다. publish-set이 최종 영상을 내보내고 RUN/review.mp4를 상대 링크로 만든다. 그 뒤 "자막 (고정)" 절에 따라 마스터를 자막본으로 교체한다. 날짜 폴더에는 자막 없는 마스터와 `_자막` 접미사 파일을 남기지 않는다. 임의로 RUN을 이동하지 않는다.

같은 기간 재제작 시 기존 영상과 링크를 이전버전으로 보존한다. 전체 성공 전 latest를 바꾸지 않는다. 파일명 충돌·선정 변경·검증 실패를 조용히 덮어쓰지 않는다. 명시적 커밋 요청 때만 해당 결과를 커밋하고 인증은 제외한다.

## 목소리 변경과 전체 복습

전체 복습은 `prepare --repo REPO RANGE --env-file REPO/.env`에서 원문 전체 범위를 manifest로 등록한다. 단일 전체 복습과 목소리 교체 결과도 "자막 (고정)" 절에 따라 자막본으로 전달한다. 목소리만 변경할 때는 `prepare --repo REPO --from-run OLD_RUN --voice NAME --env-file REPO/.env`로 별도 RUN을 만든다. tts → assemble → `revoice --run RUN --source-run OLD_RUN --hyperframes-entry LOCAL_HYPERFRAMES_BIN` → 검증. OLD_RUN의 마스터가 자막본으로 교체되었으면 revoice 전에 OLD_RUN에서 render로 자막 없는 마스터를 재생성한다. 기존 문단 경계로 재타이밍하고 내용/그림/가독성 변화 시 장면을 다시 렌더한다. 원본과 이전버전을 보존한다. 목소리 교체는 독립 RUN/ledger로 관리하며 해당 MP4만 교체하고 같은 날짜의 다른 영상과 최신 목록 항목을 유지한다. 단일 전체 복습도 제작자료/실행 안에 준비하며 verify 완료 시 제목 MP4를 전달한다.

회귀 검사: `python3 -m unittest discover -s SKILL/tests -v`. 가짜 API와 로컬 PCM을 사용하며 비용은 발생하지 않는다. 실제 인증 성공과 완성된 학습 영상 검증은 제작 요청에서 별도로 확인한다.

## 숫자 자막

segments.text는 자연스러운 한국어 전체 발화, caption은 본문 핵심 문장이다. 숫자 발화를 표시할 때는 segments.subtitle_text에 숫자·단위만 표기한 전체 발화의 한 줄 문자열을 명시한다. 예: text="영 점 오입니다.", subtitle_text="0.5입니다.". SRT는 subtitle_text를 사용하고 없으면 text를 보존한다. 핵심 문장 caption을 전체 자막 대신 쓰지 않는다. 음성은 text만 읽으며 subtitle_text 변경은 동일 음성 캐시를 재사용한다. 한글 일/이 등을 전역 치환하지 않는다. [숫자 작성·검토·분할 규칙](references/narration-and-motion.md#숫자-자막)을 따른다.

## 멀티코어 렌더 정책

새 RUN의 기본은 schema2 workers=auto다. 검증된 Apple M5/물리 10코어/16GiB 이상 macOS에서 900프레임(30초) 이상 장면의 동작 비중이 50%를 넘으면 6개, 나머지는 2개를 선택한다. from/to가 달라지는 동작 구간을 실측 타임라인에 맞춰 합산하며 겹친 구간은 한 번만 센다. 정보 누락·미검증 장비는 2개, 손상 정보는 오류다. 메타데이터 기반 휴리스틱이며 모든 장면의 최적 속도를 보장하지 않는다.

render/revoice --render-workers auto 또는 1..6 → 유효한 저장값 → auto 기본값 순이다. 기존 schema1 숫자는 그대로 유지하고 auto를 명시할 때만 schema2로 전환한다. 손상 설정은 override로 숨기지 않는다. CPU 인코딩·browser GPU auto·fast capture false와 순차 장면 처리를 유지한다. source/render-options.json과 verification/render-receipt.json에 설정·실제 작업자·선택 이유·동작 비율을 보존한다. resume/resume-set은 옵션을 생성하지 않으며 prepare --from-run은 저장값을 유지한다. 정책 변경은 render 이후만 무효화하여 음성과 타임라인을 유지한다. 장면 캐시는 동작 메타데이터·선택 결과·폰트·HTML·도구·설정 변경을 감지한다. 마스터와 기록을 함께 복구하고 .rollback이 남으면 재교체를 차단한다. 중단/timeout은 실행한 자식 프로세스를 종료·회수한 후 pending을 정리한다.
