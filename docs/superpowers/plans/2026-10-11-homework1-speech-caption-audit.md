# 과제1 실제 발화·자막 재검증 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 수정 커밋의 과제1 25편을 실제 MP4 음성으로 독립 전사하고 744개 자막의 내용·시간·화면 대응을 근거와 함께 보고한다.

**Architecture:** 현재 checkout은 유지하고 고정 커밋에서 필요한 입력만 별도 snapshot으로 추출한다. 독립 ASR와 문항별 의미 검토, 기계적 시간 검사, 실제 자막 화면 검토를 별도 결과로 합친다. 기존 제작·검수 코드를 수정하지 않고 실제 청취 없는 ASR 결과는 공식 음성 승인과 구분한다.

**Tech Stack:** Windows PowerShell, Python 3.14/unittest, Git subprocess bytes, FFmpeg/FFprobe, 기존 Vertex Express HTTP transport, JSON/Markdown, 에이전트의 이미지 검사 도구.

**Spec:** `docs/superpowers/specs/2026-10-11-homework1-speech-caption-audit-design.md`. 실행자는 이 명세와 계획을 모두 읽는다.

## Global Constraints

- 대상은 `c566d8905bf915e50c7f10ad617800fbc0a923e2`의 P1–P25 MP4 25편과 자막 cue 744개다.
- 현재 브랜치·미커밋 변경·현재 MP4·기존 WAV·원본 PDF·공식 verification/report.json·publish/latest를 변경하지 않는다.
- Git 바이너리는 Python subprocess의 bytes로 추출한다. PowerShell 텍스트 파이프와 파일 리다이렉션을 통한 MP4 추출을 하지 않는다.
- 저장된 macOS 절대 경로는 사용하지 않는다. 커밋의 상대 listing 경로와 RUN 경로를 검증하여 새 snapshot 아래에 매핑한다.
- ASR 입력에는 MP4에서 추출한 음성과 일반 전사 지침만 넣는다. 기대 원고·자막·speech-pairs를 제공하지 않는다.
- 후보 ASR 모델은 `gemini-2.5-flash`, 기존 Vertex Express 전송 경로다. 실제 인증·모델·음성 입력 가능 여부는 P1 최초 전사 성공 전까지 미확인이다.
- 최초 전사 실패 시 전체 전사를 시작하지 않는다. 자동 모델 대체·새 계정 설정·전역 패키지 설치·TTS 재합성을 하지 않는다.
- 새 ASR 요청은 순차 실행하며 실행당 최대 50회다. 성공 결과는 음성 SHA·모델·지침·요청 설정에 묶어 재사용한다. 가격과 예상 비용을 추정하지 않는다.
- 숫자·부호·분수·변수·행열·조건·단위를 보존한다. 한글 일/이/삼 등의 전역 숫자 치환을 하지 않는다.
- SRT 반올림 오차 ≤1ms, 영상 경계 오차 ≤1프레임이다. 이는 시간 계산 검사 기준이며 ASR 시각 정확도나 실제 발화 동기화의 증명이 아니다.
- ASR 근거만으로 `mode=live-listened`, `complete=true`, `live_audio=verified`를 기록하지 않는다. 직접 청취 근거가 없으면 `complete=false`, `live_audio=unverified`다.
- 검증 결과는 별도 재검증 폴더에 보존하며 불일치와 미확인 구간을 모두 보고한다. 수정·재합성·머지·push는 이번 작업 범위에 포함하지 않는다.

## Review Focus

1. 현재 25편은 수정 전 버전이다. 잘못된 MP4, 누락·중복 문항, 경로 이탈과 snapshot 변조를 Task 1에서 거부한다.
2. 원고를 전사 모델에 보여 주는 확인 편향, 빈 응답·출력 잘림·인증 실패·잘못된 캐시 재사용을 Task 2에서 거부한다.
3. `−1/3`와 `1/3`, x/y, 2행3열/3행2열, 조건 생략을 같은 뜻으로 처리하지 않는다. Task 3에서 정확한 불일치·미확인 근거를 검사한다.
4. SRT가 맞더라도 MP4에 구버전 자막이 구워져 있을 수 있다. Task 4에서 실제 모든 cue 화면과 시간 경계를 검사한다.
5. 24편 성공/1편 실패, 오래된 검토 증거, ASR만으로 실제 청취 완료 주장, 검증 중 원본 변경을 Task 5에서 완료 판정에 반영한다.

---

## 파일 구조, 인터페이스와 실행 위치

계획 안의 약어: `A=문제풀이영상/과제1/과제1_제작자료`, `D=A/speech_caption_audit`, `O=A/재검증/20261011-c566d89`. 약어는 아래 설명을 짧게 하기 위한 것이며 실제 셸 명령에는 전체 경로를 쓴다. O가 이미 있으면 덮어쓰지 않고 새 접미사 폴더로 `--output`을 지정한다.

| 파일 | 책임 |
|---|---|
| 새 `D/__init__.py` | 독립 검사 패키지 표시; 내용은 빈 문자열 |
| 새 `D/target.py` | binary snapshot, 목록·경로·SHA 검증, 시작·종료 원본 hash |
| 새 `D/asr.py` | MP4 음성 추출, blind ASR, 응답 검사·캐시·요청 제한 |
| 새 `D/compare.py` | cue/원고/SRT 식별, 전사 diff, 문항별 수학 의미 검토 입력 |
| 새 `D/evidence.py` | 실제 cue 화면 추출, 시간 검사, 검토 근거와 SHA 연결 |
| 새 `D/cli.py` | prepare/smoke/transcribe/inspect/report 명령과 부분 실패 보고 |
| 새 `D/tests/test_target.py` | 잘못된 버전·바이너리·경로·중복 회귀 |
| 새 `D/tests/test_asr.py` | 기대 원고 비노출·실패·캐시·제한 회귀 |
| 새 `D/tests/test_compare.py` | 음수·분수·변수·행열·생략과 불확실성 회귀 |
| 새 `D/tests/test_evidence.py` | 실시간 경계와 실제 MP4 프레임 근거 회귀 |
| 새 `D/tests/test_report.py` | 부분 실패·오래된 증거·허위 청취·원본 변경 회귀 |
| 생성 `O/targets.json`, `O/progress.json` | 고정 입력과 단계별 상태 |
| 생성 `O/snapshot/`, `O/audio/`, `O/asr/`, `O/frames/` | 실제 검사 입력·전사·화면 근거 |
| 생성 `O/reviews/`, `O/report.json`, `O/report.md` | 문항별 실제 검토 판단과 최종 보고 |
| 생성 `O/.gitignore` | `/snapshot/`, `/audio/`, `/frames/`만 무시; 기존 캐시 ignore를 바꾸지 않음 |

인증 loader import를 위해 실행 때만 기존 review-video scripts를 PYTHONPATH에 추가한다. 새 패키지는 기존 solution-video 제작 모듈의 write/verify 실행을 호출하지 않는다.

```powershell
$env:PYTHONPATH = "$PWD/문제풀이영상/과제1/과제1_제작자료;$PWD/.agents/skills/ml-review-video/scripts"
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -v
```

`targets.json` 계약: `{schema_version:1,commit,original_hashes:{relative_path:sha256},items:[{problem_id,video,manifest,timeline,srt,report,expected_sha256}]}`. items 경로는 O에 상대적이다. 원본 목록 파일과 제작 원고·SRT 및 현재 MP4는 original_hashes에 포함한다. 각 item의 video SHA는 수정 커밋 listing의 sha256와 같아야 한다.

`reviews/Pn.json` 계약: `{problem_id,video_sha256,transcript_sha256,content_checks:[{segment_id,chunk_id,observed_text,caption_text,status,notes,transcript_span:[start,end],extra_asr_evidence:[]}],screen_checks:[{segment_id,chunk_id,status,observed_caption,frame_sha256,notes}],listening:{status:'unverified',mode:'unavailable',notes}}`. status는 passed/failed/unverified 중 하나다. transcript_span은 원시 ASR transcript의 문자 offset이며 실재하는 구간만 허용한다. 실제 읽어 검토한 후에만 reviews 파일을 작성한다. 자동 초안은 `review-drafts`에 놓고 final reviews로 복사하지 않는다.

### Task 1: 고정 커밋 입력을 별도 snapshot으로 추출

**Files:** Create `D/__init__.py`, `D/target.py`, `D/tests/test_target.py`; generates `O/targets.json`, `O/snapshot`.

**Interfaces:**
- Consumes: repo `Path`, commit `str`, 새 output `Path`.
- Produces: `blob(repo: Path, commit: str, path: str) -> bytes`; `sha(data: bytes) -> str`; `safe_relative(base: str, value: str) -> str`; `prepare(repo: Path, output: Path, commit: str) -> dict`; `check_target(output: Path, item: dict) -> None`; `original_hashes(repo: Path) -> dict[str,str]`.
- prepare는 O가 이미 존재하면 FileExistsError, commit에 문항이 누락되거나 SHA/경로/744 cue 계약이 틀리면 ValueError. 부분 snapshot은 보존하고 targets.json을 생성하지 않는다.

- [ ] **Step 1: 실패 테스트를 작성한다.** 아래와 함께 0바이트 blob·26개 목록·P1 중복·P25 누락을 각각 거부하는 prepare 테스트를 작성한다. prepare의 `blob` 호출은 unittest.mock.patch로 이 테스트의 작은 Git fixture 응답에 연결한다; 실제 25개 영상 대신 bytes를 사용하며 총 cue 수만 744로 구성한다.

```python
import unittest
from speech_caption_audit.target import sha, safe_relative
class TargetTests(unittest.TestCase):
    def test_binary_bytes_are_preserved(self):
        self.assertNotEqual(sha(b'\x00\xff\r\n'), sha(b'\x00\xff\n'))
    def test_relative_listing_path(self):
        self.assertEqual(safe_relative('과제1/제작자료', '../01.mp4'), '과제1/01.mp4')
    def test_escape_and_absolute_rejected(self):
        for p in ('../../secret', '/secret', 'C:/secret', '//server/share'):
            with self.subTest(path=p), self.assertRaises(ValueError):
                safe_relative('과제1/제작자료', p)
```

- [ ] **Step 2: 해당 테스트를 실행하여 새 모듈 import 실패를 확인한다.**

prepare의 누락·중복·변조 테스트에는 다음 전체 fixture 생성기를 사용한다. Task 1의 테스트 파일에 추가하고 호출 때 `target.blob`을 `lambda repo,commit,path: files[path]`, `target.original_hashes`를 빈 dict로 patch한다. 경로 안전성은 위의 실제 safe_relative 테스트에서 별도로 검사한다.

```python
def make_snapshot_fixture():
    import json
    a = '문제풀이영상/과제1/과제1_제작자료'
    files, items, problems = {}, [], {}
    def put(path, value):
        files[path] = json.dumps(value, ensure_ascii=False).encode('utf-8')
    for i in range(1,26):
        pid, run = f'P{i}', f'실행/20261011-130113-6f93daa8/videos/problem-{i}'
        video, n = f'문제풀이영상/과제1/{i:02d}.mp4', 24 if i==1 else 30
        raw = b'\x00\xffbinary-video-' + str(i).encode('ascii')
        files[video] = raw
        chunks = [{'id':f'c{j}','text':'값입니다.','caption_text':'값입니다.'} for j in range(n)]
        put(f'{a}/{run}/source/manifest.json',
            {'problem_id':pid,'segments':[{'id':'s1','text':' '.join(c['text'] for c in chunks),'chunks':chunks}]})
        cues = [{'segment_id':'s1','chunk_id':c['id'],'caption_text':c['caption_text'],
                 'start_sample':j*24000,'end_sample':(j+1)*24000} for j,c in enumerate(chunks)]
        put(f'{a}/{run}/source/timeline.json',
            {'rate':24000,'fps':30,'total_frames':n*30,'caption_cues':cues})
        srt = '\n'.join(f'{j+1}\n00:00:{j:02d},000 --> 00:00:{j+1:02d},000\n값입니다.\n' for j in range(n))
        files[f'{a}/{run}/renders/captions.srt'] = srt.encode('utf-8')
        put(f'{a}/{run}/verification/report.json', {'final_sha256':sha(raw)})
        items.append({'problem_id':pid,'path':f'../{i:02d}.mp4','run':run,'sha256':sha(raw)})
        problems[pid] = {'segments':{'s1':{'chunks':chunks}}}
    put(f'{a}/검토영상_목록.json', {'items':items})
    put(f'{a}/speech-pairs.json', {'schema_version':1,'problems':problems})
    return files
```

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from speech_caption_audit.target import prepare
def test_missing_duplicate_and_bad_hash():
    import json
    key = '문제풀이영상/과제1/과제1_제작자료/검토영상_목록.json'
    for mode in ('missing','duplicate','bad-hash'):
        files = make_snapshot_fixture()
        listing = json.loads(files[key])
        if mode == 'missing':
            listing['items'].pop()
        elif mode == 'duplicate':
            listing['items'][-1]['problem_id'] = 'P1'
        else:
            listing['items'][0]['sha256'] = '0'*64
        files[key] = json.dumps(listing).encode('utf-8')
        with TemporaryDirectory() as td, patch('speech_caption_audit.target.blob',
                side_effect=lambda repo,commit,path: files[path]), \
                patch('speech_caption_audit.target.original_hashes', return_value={}):
            case = unittest.TestCase()
            with case.assertRaises(ValueError):
                prepare(Path(td), Path(td)/'snapshot-out', 'c566d8905bf915e50c7f10ad617800fbc0a923e2')
```

이 테스트 함수는 TargetTests의 메서드로 옮겨 unittest discover에 포함한다. make_snapshot_fixture는 그 파일의 module-level helper다. binary 보존의 성공 테스트도 같은 fixture로 prepare를 호출하고 첫 video의 read_bytes가 files 값과 같은지 assert한다.

```powershell
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -p test_target.py -v
```

- [ ] **Step 3: bytes 추출과 입력 계약을 구현한다.** 다음 primitives를 작성한다. `prepare`는 commit listing을 읽고 정확히 P1–P25인지 검사한 뒤 MP4 및 각 RUN의 `source/manifest.json`, `source/timeline.json`, `renders/captions.srt`, `verification/report.json`만 추출한다. speech-pairs.json도 동결한다. RUN은 A 아래 `실행/20261011-130113-6f93daa8/videos/`로 제한한다. manifest.problem_id와 목록 ID의 실제 필드 구조를 읽어 대응시키고, 타임라인 fps=30/rate=24000, 총 cue=744, cue identity 순서 유일성을 검사한다. snapshot 영상 SHA가 listing과 report.final_sha256 모두에 일치해야 한다. 원본 현재 파일·대본·SRT·목록 SHA를 relative path로 기록하고 마지막에 targets.json을 쓴다.

```python
import hashlib, posixpath, re, subprocess
from pathlib import Path
def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
def blob(repo: Path, commit: str, path: str) -> bytes:
    data = subprocess.check_output(['git', 'show', f'{commit}:{path}'], cwd=repo)
    if not data:
        raise ValueError('empty Git blob')
    return data
def safe_relative(base: str, value: str) -> str:
    if value.startswith(('/', '\\')) or '\\' in value or re.match(r'^[A-Za-z]:', value):
        raise ValueError('absolute or non-POSIX path')
    result = posixpath.normpath(posixpath.join(base, value))
    root = base.split('/')[0]
    if not result.startswith(root + '/'):
        raise ValueError('path escaped target root')
    return result
def check_target(output: Path, item: dict) -> None:
    video = (output / item['video']).resolve()
    if not video.is_relative_to(output.resolve()):
        raise ValueError('snapshot path escape')
    if sha(video.read_bytes()) != item['expected_sha256']:
        raise ValueError('target SHA mismatch')
```

`prepare`의 영상 저장 루프에는 다음 처리를 사용한다.

```python
# listing/items는 커밋의 검토영상_목록.json을 JSON으로 읽은 값이다.
ids = [x['problem_id'] for x in listing['items']]
if len(ids) != 25 or set(ids) != {f'P{i}' for i in range(1, 26)}:
    raise ValueError('expected exactly P1-P25')
for row in listing['items']:
    video_path = safe_relative('문제풀이영상/과제1/과제1_제작자료', row['path'])
    raw = blob(repo, commit, video_path)
    if sha(raw) != row['sha256']:
        raise ValueError('committed listing/video mismatch')
    dest = output / 'snapshot' / video_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
```

- [ ] **Step 4: 테스트 통과와 실제 추출 검사를 실행한다.** 실제 명령은 Task 5 CLI가 완성된 뒤 동일 prepare 함수를 사용한다. 이 단계에서는 Python으로 prepare 함수를 직접 호출해 25개 영상 hash 및 744개 cue를 출력하고 snapshot 파일과 기존 영상 하나씩 hash가 다름을 확인한다. 새 output 존재 여부를 먼저 검사한다.

```powershell
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -p test_target.py -v
python -c "from pathlib import Path;from speech_caption_audit.target import prepare;r=prepare(Path.cwd(),Path('문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89'),'c566d8905bf915e50c7f10ad617800fbc0a923e2');print(len(r['items']))"
```

- [ ] **Step 5: 이번 도구와 테스트만 선별 커밋한다.** 생성 MP4와 기존 미커밋 파일은 stage하지 않는다.

```powershell
git add -- '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/__init__.py' '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/target.py' '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests/test_target.py'
git diff --cached --stat
git commit -m 'feat(audit): freeze corrected homework video inputs'
```

### Task 2: 원고를 모르는 독립 ASR와 P1 가용성 게이트

**Files:** Create `D/asr.py`, `D/tests/test_asr.py`; generates `O/audio`, `O/asr`, `O/progress.json`.

**Interfaces:**
- Consumes: Task 1 item/output 및 `lib.vertex_tts.load_key`, `live_transport`.
- Produces: `extract_audio(video: Path, dest: Path, start: float | None = None, end: float | None = None) -> Path`; `payload(audio: bytes) -> dict`; `decode(response: dict) -> str`; `transcribe(audio: Path, dest: Path, model: str, transport, counter: dict) -> dict`.
- transcript receipt: `{audio_sha256,model,prompt_sha256,config_sha256,transcript,transcript_sha256,usage,mode:'independent-asr'}`. counter의 구조는 `{'requests':0}`다. API 오류는 비밀을 포함하지 않는 상태 코드/분류만 기록한다.

- [ ] **Step 1: 실패 테스트를 작성한다.** 기대 원고를 전달할 인자를 만들지 않는다. 아래 테스트와 함께 50회 이후 호출 0회, 캐시의 model/음성 hash/prompt 변경 시 재호출, 빈 transcript 및 잘린 JSON 거부를 각각 테스트한다.

```python
import unittest, json
from speech_caption_audit.asr import payload, decode
class ASRTests(unittest.TestCase):
    def test_request_has_only_audio_and_generic_instruction(self):
        p = payload(b'RIFF-test')
        parts = p['contents'][0]['parts']
        self.assertEqual(len(parts), 2)
        self.assertEqual(parts[1]['inlineData']['mimeType'], 'audio/wav')
        self.assertNotIn('첫 행의 일', json.dumps(p, ensure_ascii=False))
    def test_empty_and_truncated_responses_rejected(self):
        for text, finish in [('{"transcript":""}', 'STOP'), ('{}', 'MAX_TOKENS')]:
            r = {'candidates':[{'finishReason':finish,'content':{'parts':[{'text':text}]}}]}
            with self.subTest(finish=finish), self.assertRaises(ValueError):
                decode(r)
```

- [ ] **Step 2: 새 모듈 import 실패를 확인한다.**

```powershell
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -p test_asr.py -v
```

- [ ] **Step 3: MP4 음성 추출과 blind payload/응답 검사를 구현한다.** 전체 영상은 FFmpeg `-i video -vn -ac 1 -ar 16000 -c:a pcm_s16le dest.wav`로 추출한다. 출력이 이미 있으면 원본 video SHA에 연결된 receipt가 맞을 때만 재사용한다. 부분 재전사는 `-ss max(0,start-0.25)`와 `-t end-start+0.5`를 입력 전 옵션으로 사용하고 실제 종료를 영상 길이로 제한한다. 이 ±0.25초는 문맥 확보이며 정렬 허용오차가 아니다. WAV와 FFprobe의 audio duration 차이가 0.1초를 넘으면 거부한다. HTTP payload가 16MiB를 넘으면 호출하지 않고 payload-too-large로 기록한다.

```python
import base64, json
PROMPT = ('첨부 음성을 처음부터 끝까지 그대로 전사하세요. 한국어 수학 설명입니다. '
          '숫자와 기호는 들리는 발음대로 쓰고, 발화를 생략하거나 설명을 추가하지 마세요. '
          '불명확한 말은 [불명확]으로 표시하세요. '
          'JSON 객체 하나로만 답하세요: {"transcript":"발화 전문"}.')
CONFIG = {'temperature':0, 'maxOutputTokens':16384, 'responseMimeType':'application/json'}
def payload(audio: bytes) -> dict:
    return {'contents':[{'role':'user','parts':[
        {'text':PROMPT}, {'inlineData':{'mimeType':'audio/wav',
                                     'data':base64.b64encode(audio).decode('ascii')}}]}],
        'generationConfig':CONFIG}
def decode(response: dict) -> str:
    candidates = response.get('candidates', [])
    if len(candidates) != 1 or candidates[0].get('finishReason') != 'STOP':
        raise ValueError('incomplete ASR response')
    text = ''.join(p.get('text','') for p in candidates[0].get('content',{}).get('parts',[])
                   if not p.get('thought',False))
    result = json.loads(text)
    transcript = result.get('transcript')
    if not isinstance(transcript,str) or not transcript.strip():
        raise ValueError('missing transcript')
    return transcript
```

`transcribe`는 Task 1 sha를 사용해 audio/prompt/CONFIG hash를 만든다. 네 캐시 키가 일치하고 transcript hash가 정확할 때만 dest를 재사용한다. `counter['requests'] >= 50`이면 transport를 호출하기 전에 ValueError. 실제 호출 직전에 counter를 증가시킨다. CLI는 progress.json의 누적 요청 수에서 counter를 시작하고 transport wrapper가 네트워크 호출 직전에 증가한 수를 progress.json에 저장하게 한다. smoke·전체 전사·의심 구간 재전사·중단 후 재개가 동일 O의 최대 50회를 공유하며 실패 요청도 포함한다. decode 성공 후 receipt를 `.pending.json`에 쓰고 os.replace한다. 인증 키, 요청 헤더, HTTP 오류 본문을 쓰지 않는다. usageMetadata의 숫자 필드만 보존하고 실제 가격 정보가 없으면 비용은 null이다.

캐시·호출 제한 테스트는 ASRTests의 메서드로 다음을 넣는다.

```python
def test_cache_and_request_limit(self):
    from pathlib import Path
    from tempfile import TemporaryDirectory
    from unittest.mock import Mock
    from speech_caption_audit.asr import transcribe
    r = {'candidates':[{'finishReason':'STOP','content':{'parts':[
        {'text':'{"transcript":"전치는 행을 열로 옮깁니다."}'}]}}]}
    transport = Mock(return_value=r)
    with TemporaryDirectory() as td:
        audio, dest = Path(td)/'input.wav', Path(td)/'receipt.json'
        audio.write_bytes(b'RIFF-test')
        counter = {'requests':0}
        first = transcribe(audio,dest,'candidate-a',transport,counter)
        second = transcribe(audio,dest,'candidate-a',transport,counter)
        self.assertEqual(first,second)
        self.assertEqual(transport.call_count,1)
        transcribe(audio,dest,'candidate-b',transport,counter)
        self.assertEqual(transport.call_count,2)
        with self.assertRaises(ValueError):
            transcribe(audio,Path(td)/'new.json','candidate-b',transport,{'requests':50})
        self.assertEqual(transport.call_count,2)
```

- [ ] **Step 4: mock 테스트 통과 후 실제 P1 한 편만 blind ASR한다.** 기존 load_key와 live_transport를 호출하는 실제 smoke 명령을 Task 5에 구현한다. 이 단계에서는 같은 함수로 다음 코드를 실행한다. 실제 요청 성공/응답 STOP/nonempty transcript를 확인하되 원고 대비 의미 검증은 Task 3에서 한다. 실패하면 api-unavailable 근거를 저장하고 다음 live 작업을 중단한다.

```python
from pathlib import Path
from lib.vertex_tts import load_key, live_transport
from speech_caption_audit.asr import transcribe
o = Path('문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89')
transcribe(o/'audio/P1.wav', o/'asr/P1.json', 'gemini-2.5-flash',
           live_transport(load_key(Path.cwd()/'.env'), 'gemini-2.5-flash'), {'requests':0})
```

P1.wav는 Task 1의 P1 video에 extract_audio를 적용하여 만든다. 경로·extract 명령·video SHA·WAV SHA를 receipt에 남긴다. 모델이 실패하면 키 값을 출력하거나 다른 모델을 시도하지 않는다.

- [ ] **Step 5: mock 테스트를 다시 실행하고 코드·테스트만 커밋한다.**

```powershell
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -p test_asr.py -v
git add -- '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/asr.py' '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests/test_asr.py'
git commit -m 'feat(audit): transcribe delivered audio independently'
```

### Task 3: 전사·원고·수학 자막 대응을 문항별 검토

**Files:** Create `D/compare.py`, `D/tests/test_compare.py`; generates `O/review-drafts`, `O/reviews`.

**Interfaces:**
- Consumes: 고정 manifest/timeline/SRT, ASR receipt, 실제 검토자가 작성한 reviews 계약.
- Produces: `normal(text: str) -> str`; `diff_transcript(expected: str, observed: str) -> list[dict]`; `cue_rows(manifest: dict, timeline: dict) -> list[dict]`; `validate_content_review(rows: list[dict], review: dict, transcript: str, video_sha: str, transcript_sha: str) -> str`.
- cue_rows 결과 `{segment_id,chunk_id,text,caption_text,start_sample,end_sample,rate}`. manifest의 chunk_id와 timeline caption_cues의 순서가 정확히 일치해야 한다. validate는 passed/failed/unverified를 반환하며 빈 note·중복 identity·범위 밖 transcript_span·hash 불일치는 ValueError.

- [ ] **Step 1: 실패 테스트를 작성한다.** 문자 차이를 자동 동일 의미로 만들지 않는 최소 회귀는 다음과 같다. validate 테스트에는 `observed_text='일 삼분의 일'`, caption_text='−1/3', status='failed', notes='음수 발화가 없음'을 넣고 failed를 기대한다. `[불명확]`이 있는 관측 또는 status 미입력은 unverified를 기대한다.

```python
import unittest
from speech_caption_audit.compare import diff_transcript, normal
class CompareTests(unittest.TestCase):
    def test_critical_changes_are_not_erased(self):
        for expected, observed in [('마이너스 삼분의 일','삼분의 일'),
                                   ('엑스의 노름','와이의 노름'),
                                   ('이 행 삼 열','삼 행 이 열'),
                                   ('독립일 때 성립합니다','성립합니다')]:
            with self.subTest(expected=expected):
                self.assertTrue(diff_transcript(expected, observed))
    def test_numbers_are_not_globally_replaced(self):
        self.assertNotEqual(normal('이 행'), normal('2 행'))
```

- [ ] **Step 2: import 실패를 확인한다.**

```powershell
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -p test_compare.py -v
```

- [ ] **Step 3: 차이 후보 추출과 검토 계약을 구현한다.** 다음 코드를 사용하고 normal을 의미 판정에 사용하지 않는다. 정확한 문자열 대응도 ASR 관측의 문자열 대응일 뿐 실제 음성 청취가 아니다.

```python
import difflib, unicodedata
def normal(text: str) -> str:
    return ' '.join(unicodedata.normalize('NFC', text).split())
def diff_transcript(expected: str, observed: str) -> list[dict]:
    a, b = normal(expected), normal(observed)
    return [{'kind':tag, 'expected':a[i:j], 'observed':b[k:l],
             'expected_span':[i,j], 'observed_span':[k,l]}
            for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes()
            if tag != 'equal']
```

cue_rows는 manifest.segments[].chunks와 timeline.caption_cues를 `(segment_id,chunk_id)`로 연결하고 set 비교와 순서 비교를 모두 한다. `speech-pairs.json`의 수식 표기를 참조해 원고 발음↔기호 대응을 검토하되 ASR 입력으로 사용하지 않는다. review-drafts에는 모든 cue의 기대값만 기록하고 status를 unverified로 둔다. 실제 읽은 transcript의 raw offset을 확인한 뒤 reviews를 작성한다. 정규화된 diff offset을 raw transcript_span으로 복사하지 않는다.

숫자 표기만 바뀐 경우도 reviewer가 해당 문맥의 수치·분모·부호·행열을 확인해 notes에 근거를 적는다. ASR이 잘못 인식했을 가능성이 있으면 passed 또는 영상 오류로 단정하지 않고 unverified로 둔다. 필요하면 Task 2 extract_audio로 해당 cue 전후 0.25초를 포함한 actual MP4 clip을 만들고 blind 재전사한다. extra_asr_evidence에 clip/response SHA를 기록한다. 정정 판단은 두 전사 결과와 화면 문맥을 함께 설명하며 새로운 전사를 직접 청취라고 부르지 않는다.

- [ ] **Step 4: 테스트 통과와 실제 P1 의미 대조를 수행한다.** P1의 intro/reason/write/check/final 전체를 검토한다. 특히 행렬 원소 (1,−2,3)/(0,4,5), 전치의 행열 순서, 검산 설명의 누락 여부를 본다. ASR이 원고 밖 지시문을 말한 것으로 전사했으면 extra-speech issue를 추가한다. 전사 전문에서 어느 cue에도 연결되지 않은 말도 보고한다. diff의 delete/insert/replace마다 해결 근거 또는 미확인을 기록한다.

```powershell
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -p test_compare.py -v
```

- [ ] **Step 5: 코드와 테스트를 선별 커밋한다.**

```powershell
git add -- '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/compare.py' '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests/test_compare.py'
git commit -m 'feat(audit): preserve semantic speech-caption review evidence'
```

### Task 4: 실제 MP4의 자막과 기계적 시간 경계 확인

**Files:** Create `D/evidence.py`, `D/tests/test_evidence.py`; generates `O/frames`, `O/reviews`의 screen_checks.

**Interfaces:**
- Consumes: 고정 video/timeline/SRT 및 Task 3 cue_rows.
- Produces: `cue_time(row: dict, fps: int = 30) -> dict`; `capture(video: Path, row: dict, dest: Path) -> dict`; `validate_screen_review(rows: list[dict], review: dict, frame_receipts: list[dict]) -> str`; `timing_checks(timeline: dict, srt: Path, video: Path) -> dict`.
- capture receipt `{segment_id,chunk_id,video_sha256,frame_sha256,time_seconds,path}`. timing_checks는 SRT 전문과 samples→milliseconds·프레임 duration을 각각 비교하고 actual_spoken_sync는 unverified로 둔다.

- [ ] **Step 1: 시간 경계와 구버전 자막 근거 거부 테스트를 작성한다.** validate_screen_review는 실제 프레임의 hash가 다르거나 하나의 cue라도 검사 기록이 없으면 passed가 될 수 없다. 구버전 텍스트를 observed_caption에 넣고 failed로 기록한 review를 failed로 반환하는 테스트도 작성한다.

```python
import unittest
from speech_caption_audit.evidence import cue_time
class EvidenceTests(unittest.TestCase):
    def test_sample_boundary_rounding(self):
        r = cue_time({'start_sample':24001,'end_sample':48001,'rate':24000})
        self.assertLessEqual(r['start_error_ms'], 1)
        self.assertAlmostEqual(r['middle_seconds'], 1.5, places=3)
    def test_invalid_interval_rejected(self):
        with self.assertRaises(ValueError):
            cue_time({'start_sample':100,'end_sample':90,'rate':24000})
```

- [ ] **Step 2: import 실패를 확인한다.**

```powershell
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -p test_evidence.py -v
```

- [ ] **Step 3: cue 시간과 실제 frame 추출을 구현한다.** 다음 계산을 사용한다. 캡처는 생성한 자막 이미지가 아니라 대상 MP4의 실제 프레임이어야 한다.

```python
import subprocess
from pathlib import Path
def cue_time(row: dict, fps: int = 30) -> dict:
    lo, hi, rate = row['start_sample'], row['end_sample'], row['rate']
    if not (isinstance(lo,int) and isinstance(hi,int) and 0 <= lo < hi and rate > 0):
        raise ValueError('invalid cue interval')
    middle = (lo+hi)/(2*rate)
    return {'middle_seconds':round(middle*fps)/fps,
            'start_error_ms':abs(round(lo*1000/rate)-lo*1000/rate),
            'end_error_ms':abs(round(hi*1000/rate)-hi*1000/rate)}
def capture(video: Path, row: dict, dest: Path) -> dict:
    from .target import sha
    dest.parent.mkdir(parents=True, exist_ok=True)
    t = cue_time(row)['middle_seconds']
    subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(video),
                    '-frames:v','1','-vf','crop=iw:240:0:ih-240','-y',str(dest)],check=True)
    return {'segment_id':row['segment_id'],'chunk_id':row['chunk_id'],
            'video_sha256':sha(video.read_bytes()),'frame_sha256':sha(dest.read_bytes()),
            'time_seconds':t,'path':str(dest)}
```

timing_checks는 SRT index/start/end/text를 파싱하여 timeline caption_cues와 일대일 대응한다. 텍스트는 줄바꿈만 제거해 비교하고 숫자·기호는 보존한다. 끝 시각 반올림 오차 ≤1ms, video duration과 total_frames/30 차이 ≤1/30초를 검사한다. SRT 텍스트가 줄별 wrap되어 있으면 기대 caption_text와 공백 join 비교를 사용한다. 각 cue 중간 프레임 외에 첫/마지막 cue 및 내용 diff 의심 cue의 시작·끝 전후 한 프레임을 캡처한다. 1프레임 이내 cue는 middle을 강제로 통과시키지 않고 시각 검사 미확인으로 기록한다.

- [ ] **Step 4: actual P1 screenshot을 직접 읽고 screen_checks를 작성한다.** 원본 해상도 이미지를 이미지 검사 도구로 열어 intro·행렬 원소·기호·check·final의 모든 cue를 대조한다. cue별 이미지 직접 조회 또는 2열×4행 contact sheet를 사용하되 읽기 어려우면 원본 crop으로 돌아간다. 프레임을 만들었다는 이유만으로 passed를 쓰지 않는다. 화면 텍스트가 축약·잘림·부호 누락이면 failed와 실제 관측을 적는다. 직접 청취 도구가 없으므로 체감 음성 동기화는 unverified다.

```powershell
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -p test_evidence.py -v
```

- [ ] **Step 5: 새 코드와 테스트만 커밋한다.**

```powershell
git add -- '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/evidence.py' '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests/test_evidence.py'
git commit -m 'feat(audit): verify burned captions against measured cues'
```

### Task 5: 25편 실행, 부분 실패 보존, 최종 근거 보고

**Files:** Create `D/cli.py`, `D/tests/test_report.py`; generates `O/progress.json`, `O/report.json`, `O/report.md`, `O/.gitignore`; Update 이번 계획의 완료 checkbox와 검증 결과 메모.

**Interfaces:**
- Consumes: Tasks 1–4 함수와 고정 targets/reviews/ASR/frame receipts.
- Produces: `rollup(items: list[dict], originals_unchanged: bool) -> dict`; `main(argv: list[str] | None = None) -> int`.
- CLI: `prepare --repo --commit --output`; `smoke --repo --output --env-file`; `transcribe --repo --output --env-file`; `inspect --output`; `report --repo --output`.
- prepare→smoke→transcribe→inspect→report 순서. smoke가 passed이고 hash가 현재 snapshot과 같아야 transcribe 진행. inspect는 실제 cue 검사 자료/초안만 만들며 의미·화면 검토를 자동 승인하지 않는다. report는 검토 완료 기록을 검증해 읽는다.

- [ ] **Step 1: 실패·미확인·허위 청취 회귀 테스트를 작성한다.**

```python
import unittest
from speech_caption_audit.cli import rollup
class ReportTests(unittest.TestCase):
    def test_partial_and_asr_only_never_mean_complete(self):
        good = {'content_status':'passed','screen_status':'passed',
                'mechanical_timing_status':'passed','listening_status':'unverified'}
        rows = [dict(good,problem_id=f'P{i}',cue_count=1) for i in range(1,25)]
        r = rollup(rows, True)
        self.assertFalse(r['complete'])
        self.assertEqual(r['live_audio'], 'unverified')
        self.assertIn('P25', r['missing_problems'])
    def test_original_mutation_is_failure(self):
        self.assertEqual(rollup([], False)['original_preservation'], 'failed')
```

P1을 25회 중복해도 통과하지 않는 테스트, transcript/MP4/frame hash가 달라진 검토를 거부하는 테스트, 청취 근거가 없는 `mode='live-listened'` 입력을 거부하는 테스트를 각각 추가한다.

```python
def test_duplicate_ids_are_not_full_coverage(self):
    row = {'problem_id':'P1','cue_count':30,'content_status':'passed',
           'screen_status':'passed','mechanical_timing_status':'passed',
           'listening_status':'unverified'}
    r = rollup([dict(row) for _ in range(25)],True)
    self.assertFalse(r['unique_problem_ids'])
    self.assertEqual(r['content_status'],'unverified')
```

허위 청취 모드를 입력하는 경우는 rollup이 아니라 `report`가 reviews 계약을 읽는 위치에서 ValueError로 처리한다. 근거 hash는 Task 3/4 validator가 검사한다. 각 validator가 거부한 리뷰를 report에서는 해당 문항 unverified와 오류 이유로 보존한다.

- [ ] **Step 2: import 실패를 확인한다.**

```powershell
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -p test_report.py -v
```

- [ ] **Step 3: CLI와 보고서 상태 집계를 구현한다.** argparse subcommands를 앞 계약 그대로 만든다. 단계별 예외를 해당 problem_id/status/reason에 기록하고 성공한 형제의 ASR/cache를 유지한다. 인증 실패가 반복되거나 counter 제한이면 남은 문제는 unverified로 기록하고 요청을 멈춘다. raw 예외 본문이나 키를 progress에 쓰지 않는다.

```python
def rollup(items: list[dict], originals_unchanged: bool) -> dict:
    ids = [r['problem_id'] for r in items]
    expected = {f'P{i}' for i in range(1,26)}
    unique = len(ids) == len(set(ids))
    missing = sorted(expected-set(ids), key=lambda x:int(x[1:]))
    count = sum(r.get('cue_count',0) for r in items)
    def axis(key: str) -> str:
        values = [r.get(key,'unverified') for r in items]
        if 'failed' in values:
            return 'failed'
        return 'passed' if unique and not missing and len(ids)==25 and count==744 and all(v=='passed' for v in values) else 'unverified'
    return {'report_generated':True,'target_count':len(ids),'cue_count':count,
            'missing_problems':missing,'unique_problem_ids':unique,
            'content_status':axis('content_status'),'screen_status':axis('screen_status'),
            'mechanical_timing_status':axis('mechanical_timing_status'),
            'actual_spoken_sync':'unverified', 'complete':False,'live_audio':'unverified',
            'original_preservation':'passed' if originals_unchanged else 'failed'}
```

현재 도구의 청취 불가 조건을 전제로 rollup은 complete=false를 유지한다. 실제 청취 가능한 도구가 새로 제공되면 이 계획을 임의로 확대하지 말고 실제 청취 근거 계약을 검토한 뒤 그 기능의 별도 범위를 정한다. existing audio-review/report/latest를 이 도구가 갱신하지 않는다.

report.md는 입력 commit/SHA, 25편·744cue의 처리 수, 네 축의 판정, 실패·미확인 구간 표, 실제 사용 모델/요청 수/usage/비용 null, 원본 보존, 수행하지 않은 직접 청취를 포함한다. 불일치 구간 표는 문항·SRT시각·원고·전사·자막·근거 상대경로를 열로 갖는다. 보고서 자체 생성 성공을 전체 영상 통과로 표현하지 않는다.

- [ ] **Step 4: mock 테스트 통과 후 실제 25편을 순차 검사한다.** 아래 명령은 이미 준비된 O에 실행한다. P1 smoke에서 기존 성공 receipt가 있으면 재과금하지 않는다. 모든 의미·화면 검토는 실제 ASR/스크린샷을 읽은 뒤 수행하고 reviews를 작성한다.

```powershell
python -m unittest discover -s '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests' -v
python -m speech_caption_audit.cli smoke --repo . --output '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89' --env-file .env
python -m speech_caption_audit.cli transcribe --repo . --output '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89' --env-file .env
python -m speech_caption_audit.cli inspect --output '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89'
```

inspect 후 실제 검토 순서: P1을 완성한 뒤 P2–P25를 순차 처리한다. P2 x/y/0, P4–P8 행렬·음수·분수, P11 Jacobian 행열, P12 −4/5, P16 N, P19 MAP 수치, P22 다중 페이지, P23 4/3, P24 5/2, P25 역공분산 계수는 별도 notes를 쓴다. 모든 일반 설명·intro·check·final도 누락 없이 대조한다. 이름만 기록한 중요 구간 표로 전체 검토를 대신하지 않는다.

- [ ] **Step 5: 최종 보고와 보존 검사를 수행한다.** 새 ASR/hash/화면 근거 및 reviews를 다시 읽고 report 명령을 실행한다. 사용자에게 핵심 불일치/미확인과 직접 청취 미수행을 간단히 보고한다. 첫 원본 hash와 현재 hash가 다르면 보존 failed로 보고하고 해당 변경을 되돌리려 하지 않는다.

```powershell
python -m speech_caption_audit.cli report --repo . --output '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89'
git status --short
```

- [ ] **Step 6: 검증 도구와 보고서만 선별 커밋한다.** 새 snapshot/audio/frames는 커밋하지 않고 O/.gitignore로 제외한다. transcript와 reviews/report는 검사 근거로 보존한다. 인증·HTTP payload·키·대용량 MP4를 stage하지 않는다. 기존 untracked tmp와 문제설명 자료도 stage하지 않는다.

```powershell
git add -- '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/cli.py' '문제풀이영상/과제1/과제1_제작자료/speech_caption_audit/tests/test_report.py'
git add -- '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89/.gitignore' '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89/targets.json' '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89/progress.json' '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89/asr' '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89/reviews' '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89/report.json' '문제풀이영상/과제1/과제1_제작자료/재검증/20261011-c566d89/report.md'
git diff --cached --stat
git commit -m 'docs(audit): report independent homework speech-caption evidence'
```

## 계획 자체 검토와 실행 인계

- 명세 범위 → Task 1은 버전·입력, Task 2는 실제 음성 전사, Task 3은 원고·수학 의미, Task 4는 화면·시간, Task 5는 전체 범위·부분 실패·보존·보고를 담당한다.
- 의심 구간 재전사는 Task 2의 start/end extract와 transcribe, Task 3의 extra_asr_evidence로 연결된다. 모델 시각을 실측 단어 시각으로 사용하지 않는다.
- 직접 청취 불가와 전사 provider 미확인은 서로 다른 조건이다. provider 실패 시 speech 검증 미실행, provider 성공 시 ASR 근거 대조 완료와 청취 미확인을 함께 기록한다.
- 실제 데이터로 전체 검증을 수행하는 마지막 단계 이전의 unit test는 fake transport와 작은 fixture만 사용한다. 유료 요청을 테스트마다 보내지 않는다.
- 기획 단계에서 실행한 것은 Git/해시/설치 SDK/기존 소스의 읽기 전용 검사다. ASR, FFmpeg 추출, 신규 코드 테스트, 영상 청취, 화면 재검증은 아직 실행하지 않았다.
- 권장 실행 방법은 Native다. 다섯 단계가 동일 snapshot과 검토 근거 계약을 공유하고, 미디어·수학 판정이 많아 한 실행자가 문맥을 유지하는 편이 효율적이다. 구현 후 한 번의 독립 최종 검토에서 근거·상태 표현을 확인한다.
