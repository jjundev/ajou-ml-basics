---
name: ml-stt
description: "[Gemini Only] Use when transcribing machine learning lecture audio or video recordings (.m4a, .mp3, .wav) into a verbatim transcript under STT/<MMDD> 머러기.md with domain-specific terminology guidance for ajou-ml-basics, or when invoking /ml-stt. Strictly requires Gemini models; fails on Claude/GPT."
---

# ML STT (머신러닝기초 강의 음성 전사)

머신러닝기초(정방철 교수님, ECE3512) 강의 녹음 음성을 Gemini 네이티브 멀티모달(`view_file`)로 축어적(verbatim) 전사하고, 당일 진도(강의 슬라이드·MML 교과서·기존 복습노트)의 머신러닝·수학·통계 고유명사 및 발음 교정 지침을 프롬프트에 주입하여 전문용어 오인식을 최소화한 마스터 전사본을 `STT/<MMDD> 머러기.md`로 산출한다.

> [!IMPORTANT]
> **Gemini 전용 스킬**: 본 스킬은 Gemini 모델의 네이티브 비디오/오디오 멀티모달(`view_file`) 인식 기능에 전적으로 의존합니다. 비디오/오디오 바이너리 입력을 처리할 수 없는 Claude, GPT 등의 비-Gemini 모델에서는 절대 실행하지 마십시오.

---

## 🧠 핵심 원칙

0. **모델 호환성 게이트 (Model Compatibility Gate - STRICT GEMINI ONLY)**:
   - 본 스킬은 Gemini 멀티모달 모델(예: Gemini 1.5, Gemini 2.0, Gemini 2.5, Gemini 3.x)을 필수적으로 요구합니다.
   - 현재 활성화된 모델이 Gemini가 아닌 경우(예: Claude 3.5/3.7, GPT-4o, o1/o3, Llama, DeepSeek 등):
     - **어떠한 명령어(ffmpeg, view_file 등)도 실행하지 말고 즉시 중단하십시오.**
     - 사용자에게 아래 안내 메시지를 출력하고 태스크를 즉시 종료합니다:
       > ⚠️ **ml-stt 스킬은 Gemini 모델 전용입니다.**  
       > 본 스킬은 Gemini의 네이티브 오디오 멀티모달 인식(`view_file`)을 사용하므로, 비디오/오디오 바이너리 입력을 처리할 수 없는 Claude 및 GPT 모델에서는 동작하지 않습니다.  
       > 모델 선택을 **Gemini(Gemini 2.5 / 3.0 등)**로 변경하신 후 다시 요청해 주세요.

1. **도메인 특화 어휘 주입 (Context-Aware Prior)**:
   - 파일명에서 날짜(`MMDD`)를 자동 추출하고, `복습노트/<MMDD>/.pack/정리노트_*.md`, 당일 진도 단원의 최신 개정 슬라이드(`강의노트/Lecture*_rev_HO.pdf` 등), 조교 특강(`TA_Lecture_*.pdf`), 및 `교과서/Mathematics_for_Machine_Learning.pdf`(MML)에서 핵심 머신러닝·선형대수 고유명사를 추출해 서브에이전트 프롬프트에 힌트로 주입한다.
   - 발음이 뭉개지거나 일상 단어로 들리기 쉬운 어휘(예: *기븐* $\rightarrow$ *given*, *조인트* $\rightarrow$ *joint*, *라이클리후드* $\rightarrow$ *likelihood*, *마지널* $\rightarrow$ *marginal*, *포스테리어 프레딕티브* $\rightarrow$ *posterior predictive*, *슈도 인버스* $\rightarrow$ *pseudo-inverse*, *아핀* $\rightarrow$ *affine*, *오소고날 프로젝션* $\rightarrow$ *orthogonal projection*, *오소노말 베이시스* $\rightarrow$ *orthonormal basis*, *피씨에이* $\rightarrow$ *PCA*, *이브이디* $\rightarrow$ *EVD*, *스펙트럴 씨어럼* $\rightarrow$ *Spectral Theorem*, *라그랑주 멀티플라이어* $\rightarrow$ *Lagrange multiplier*, *세타* $\rightarrow$ *$\theta$*, *람다* $\rightarrow$ *$\lambda$*, *힘숨찐*, *장군님* 등)는 머신러닝 표준 용어로 전사한다.

2. **저장소 표준 경로 및 산출물 보존**:
   - 최종 마스터 전사본은 항상 `STT/<MMDD> 머러기.md`로 생성한다 (`ml-review-pack`이 기대하는 표준 경로).
   - 포맷은 기존 전사본 규격과 일치하게 `# <MMDD> 머러기 전체 오디오 전사본` 및 세그먼트 메타데이터, `## Part 01`, `## Part 02` 헤더 아래 문단 단위 클린 텍스트로 저장한다.

3. **네이티브 멀티모달 전사 (외부 Whisper 절대 금지)**:
   - Whisper, mlx-whisper, faster-whisper 등 외부/로컬 STT 모델을 절대 설치하거나 사용하지 않는다.
   - 오디오를 1fps 블랙 비디오 래퍼(`color=c=black:s=320x240:r=1`)가 포함된 MP4로 변환한 뒤, Gemini의 `view_file` 기능으로 직접 듣고 전사한다.

4. **10분 세그먼트 및 병렬 서브에이전트**:
   - 10분이 넘는 긴 음성은 10분(600초) 단위로 분할하여 `self` 서브에이전트를 병렬 기동한다.

5. **복습팩 파이프라인 연계 안내**:
   - 전사 완료 후 `/ml-review-pack <MMDD>` 실행을 안내하여 예습 → 수업 STT → 복습팩 생성이 매끄럽게 연결되도록 한다. (자동 실행하지 않고 안내만 출력)

6. **화자 분리 (선택적 - Diarization)**:
   - 머신러닝기초 강의는 기본적으로 교수님 1인의 독강이므로, 특별한 언급이 없으면 단일 스트림으로 전사한다.
   - 질의응답이나 학생 발표 등으로 사용자가 화자 구분을 명시적으로 요청한 경우(`--speakers`, `-s`, "화자 구분"):
     - `라벨: 특징` 설명이 사전에 제공되어야 한다 (예: `--speakers "교수: 40대 남성 / 학생: 20대 남성"`). 설명이 없으면 전사 전 사용자에게 확인한다.
     - 매 화자 변경마다 `**라벨:** 발화내용` 형식으로 구분한다.

7. **안전성 보존 축어성 (Safe Verbatim & Euphemistic Normalization)**:
   - 수학/머신러닝 이론, 수식 전개, 및 교수님의 강의 맥락은 100% 누락 없이 전사한다.
   - 단, 구글 Gemini API의 실시간 안전 필터(공격성, 혐오 표현, 비하, 비속어) 오탐(False Positive)을 유발하는 감탄사/자조적 비속어/거친 농담에 한해 문맥과 의미를 100% 보존하는 안전한 표준 구어체로 완곡 순화(Euphemistic Normalization)하여 게이트웨이 차단을 원천 방지한다.
   - 수학 기호 및 학습용 핵심 비유('힘숨찐', '장군님', '도가니탕' 등)는 절대 순화 대상이 아니다.

---

## 🛠️ Workflow A: 단일 파일 (<= 10분)

0. **모델 호환성 확인 (Gate 0)**: Gemini 모델인지 확인. 비-Gemini 모델이면 즉시 중단.
1. **컨텍스트 추출**:
   ```bash
   REPO="$(git rev-parse --show-toplevel)"
   mkdir -p "$REPO/tmp/ml-stt"
   uv run python "$REPO/.agents/skills/ml-stt/scripts/infer_context.py" "<AUDIO_PATH>" --repo "$REPO" --json > "$REPO/tmp/ml-stt/ml_stt_context.json"
   ```
2. **1fps 블랙 MP4 래핑 (정확한 재생 길이 매칭)**:
   ```bash
   dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "<AUDIO_PATH>")
   ffmpeg -y -f lavfi -i color=c=black:s=320x240:r=1 -i "<AUDIO_PATH>" -t "$dur" -c:v libx264 -c:a aac -b:a 128k "$REPO/tmp/ml-stt/_temp_ml_stt.mp4" -loglevel error
   ```
3. **메인 에이전트 직접 `read_file` 전사**:
   - 서브에이전트 없이 메인 에이전트가 `$REPO/tmp/ml-stt/_temp_ml_stt.mp4`에 `read_file` (또는 `view_file`)을 호출.
   - `infer_context.py`에서 추출한 도메인 프롬프트와 Safe Verbatim 원칙을 컨텍스트로 두고 축어적 전사.
4. **저장 및 정리**:
   - `STT/<MMDD> 머러기.md`로 저장.
   - `rm -f "$REPO/tmp/ml-stt/_temp_ml_stt.mp4"`
5. **완료 보고 및 `/ml-review-pack <MMDD>` 안내**.

---

## ⚡ Workflow B: 긴 오디오 (> 10분) - 병렬 서브에이전트

0. **모델 호환성 확인 (Gate 0)**: Gemini 모델인지 확인. 비-Gemini 모델이면 즉시 중단.
1. **날짜 및 단원 컨텍스트 추출**:
   ```bash
   REPO="$(git rev-parse --show-toplevel)"
   mkdir -p "$REPO/tmp/ml-stt"
   uv run python "$REPO/.agents/skills/ml-stt/scripts/infer_context.py" "<AUDIO_PATH>" --repo "$REPO" --json > "$REPO/tmp/ml-stt/ml_stt_context.json"
   ```
   - 파일명에서 날짜를 파싱할 수 없는 경우 임의 추측하지 않고 즉시 `--date MMDD` 입력을 안내하고 중단.

2. **10분 분할 및 병렬 1fps MP4 래핑**:
   ```bash
   DATE=$(uv run python -c "import json, sys; print(json.load(open(sys.argv[1], encoding='utf-8'))['date'])" "$REPO/tmp/ml-stt/ml_stt_context.json")
   WORK_DIR="$REPO/STT/_temp_${DATE}"
   mkdir -p "$WORK_DIR"

   # 10분 분할
   ffmpeg -y -i "<AUDIO_PATH>" -vn -c:a libmp3lame -b:a 192k \
     -f segment -segment_time 600 -segment_start_number 1 -reset_timestamps 1 \
     "$WORK_DIR/${DATE} 머러기_part%02d.mp3"

   # MP4 일괄 래핑
   for f in "$WORK_DIR"/*_part*.mp3; do
     (
       dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f")
       ffmpeg -y -f lavfi -i color=c=black:s=320x240:r=1 \
         -i "$f" -t "$dur" -c:v libx264 -c:a aac -b:a 128k "${f%.mp3}_temp.mp4" -loglevel error
     ) &
   done
   wait
   ```

3. **병렬 서브에이전트 기동**:
   - 각 파트마다 `self` 서브에이전트를 동시 기동.
   - **기본 프롬프트 (클린 문단)**:
     ```text
     You are a verbatim STT transcription agent specialized in college Machine Learning (머신러닝기초, 정방철 교수님).
     Target video: <WORK_DIR>/<DATE> 머러기_part01_temp.mp4
     Output markdown: <WORK_DIR>/<DATE> 머러기_part01.md

     <PROMPT_GUIDE> (infer_context.py 의 prompt_guide 내용 삽입)

     Instructions:
     1. Call `read_file` (or `view_file`) on <WORK_DIR>/<DATE> 머러기_part01_temp.mp4.
     2. Transcribe ALL spoken words verbatim from start to finish. Do not skip, summarize, or omit anything.
     3. Group 2~4 sentences per paragraph, separated by blank lines (\n\n). Do not output timestamps unless requested.
     4. When technical terms sound ambiguous or muffled, bias towards the correct Korean/English machine learning terms provided above.
     5. Safe Verbatim (Euphemistic Normalization):
        - Preserve 100% of academic explanations, mathematical derivations, formula readouts, and pedagogical metaphors.
        - If informal profanities, harsh reprimands, or aggressive exclamations occur (e.g., '제기랄', '바보 엔지니어', '뇌가 썩는다'), normalize them euphemistically into mild polite spoken Korean ('이런', '미숙한 엔지니어', '생각이 굳는다') to prevent false-positive safety filter triggers.
     6. Save directly to <WORK_DIR>/<DATE> 머러기_part01.md using `write_file` (Overwrite=true).
     7. Strict Guardrails:
        - Perform transcription in a single pass directly from read_file.
        - NEVER search for, install, or run Whisper or any external STT tools.
        - Do NOT inspect other part files or compare transcripts.
        - Do NOT run audio analysis, silence detection, ffmpeg slicing, or additional tools.
     8. Report completion immediately when done.
     ```
   - **타임스탬프 요청 시 (`--timestamps` / `-t`) 변형**:
     지침 3을 아래로 교체:
     ```text
     3. Format strictly with MM:SS timestamps:
     MM:SS
     발화내용 문장
     ```
   - **화자 분리 요청 시 (`--speakers`) 변형**:
     화자 로스터 블록 삽입 및 매 발화마다 `**라벨:**` 접두사 추가.

4. **마스터 전사본 병합 및 자동 정리**:
   ```bash
   REPO="$(git rev-parse --show-toplevel)"
   uv run python "$REPO/.agents/skills/ml-stt/scripts/merge_transcripts.py" \
     --dir "$WORK_DIR" \
     --prefix "${DATE} 머러기" \
     --out "$REPO/STT/${DATE} 머러기.md"
   ```
   - 타임스탬프 필요 시: `--timestamps`
   - 중간 파일 보존 필요 시: `--keep-parts`
   - 화자 분리 적용 시: `--speakers "라벨1,라벨2"`

5. **완료 보고**:
   ```text
   ✅ 머신러닝기초 강의 전사 완료: STT/<DATE> 머러기.md
   - 대상 수업: <DATE> (Lecture<XX> <TITLE>)
   - 머신러닝 도메인 어휘 및 수식 힌트 적용 완료

   👉 이 전사본으로 복습팩(정리노트 + 복습문제)을 생성하려면 다음 명령을 실행하세요:
   /ml-review-pack <DATE>
   ```

---

## 🛡️ 안전 필터(Safety Filter) 자동 복구 프로토콜 (Self-Healing Fallback)

Gemini safety filter에 의해 특정 파트에서 전사가 차단(`blocked by Gemini's filters`)될 경우:
1. **Whisper/외부 모델 폴백 절대 금지**: Whisper 등 외부 툴 설치 시도 금지.
2. **해당 파트를 150초(2.5분) 단위 마이크로 청크로 즉시 자동 분할**:
   ```bash
   WORK_DIR="STT/_temp_${DATE}"
   PART_MP3="$WORK_DIR/${DATE} 머러기_part${PART_NUM}.mp3"

   # 150초 단위 서브 청크 분할
   ffmpeg -y -i "$PART_MP3" -vn -c:a libmp3lame -b:a 192k \
     -f segment -segment_time 150 -segment_start_number 1 -reset_timestamps 1 \
     "$WORK_DIR/part${PART_NUM}_sub%02d.mp3"

   # 1fps 블랙 MP4 래핑
   for f in "$WORK_DIR"/part${PART_NUM}_sub*.mp3; do
     dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f")
     ffmpeg -y -f lavfi -i color=c=black:s=320x240:r=1 \
       -i "$f" -t "$dur" -c:v libx264 -c:a aac -b:a 128k "${f%.mp3}_temp.mp4" -loglevel error
   done
   ```
3. **엄격 순화 모드(Strict Sanitization Override) 프롬프트로 서브 청크 전사**:
   - `infer_context.py` 추출 프롬프트와 함께 다음 완곡 순화 지침을 최우선으로 주입하여 각 sub 청크를 `read_file`로 전사한다:
     > "You are transcribing an archival academic lecture. Ensure complete conceptual accuracy. Any extreme emotional reprimands or colloquial slurs must be neutrally smoothed (e.g., '이런', '어리석은', '안타까운') to prevent output generation blockage."
4. **서브 청크 합본 및 원본 파트 파일 복원**:
   - 성공한 sub01, sub02, ... 텍스트를 순서대로 결합하여 `$WORK_DIR/${DATE} 머러기_part${PART_NUM}.md`를 복원한다.
   - 마스터 머지(`merge_transcripts.py`)를 정상 진행한다.

---

## ✅ 완료 기준 (Completion Criteria)

- [ ] 활성 모델이 Gemini인지 확인 완료 (Gate 0 준수, Claude/GPT 차단).
- [ ] 오디오 파일명에서 날짜(`MMDD`) 정상 파싱 (실패 시 `--date` 요구).
- [ ] 당일 진도 Lecture 고유명사 및 발음 교정 지침 추출 및 프롬프트 주입 완료.
- [ ] Safe Verbatim(완곡 순화) 원칙 적용으로 생성 시 안전 필터 차단 사전 예방.
- [ ] 1fps 블랙 MP4 래퍼 적용 (`color=c=black:s=320x240:r=1`, `-t "$dur"`).
- [ ] 외부/로컬 모델(Whisper 등) 사용 배제 (네이티브 `read_file` 100% 사용).
- [ ] 생략이나 요약 없는 전 구간 축어적(verbatim) 전사 완료.
- [ ] 서브에이전트가 딴짓(추가 슬라이싱, 진단 루프) 없이 단일 패스로 완료.
- [ ] 최종 산출물이 `STT/<MMDD> 머러기.md`로 올바르게 병합 및 저장됨.
- [ ] 중간 임시 파일 정리 완료 (사용자가 `--keep-parts`를 요구하지 않은 경우).
- [ ] 후속 작업으로 `/ml-review-pack <MMDD>` 안내 메시지 출력.
