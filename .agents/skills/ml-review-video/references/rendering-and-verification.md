# 렌더와 검증

Python 3.10+, Node, FFmpeg/ffprobe, 로컬 HyperFrames CLI Node entry가 필요하다. HyperFrames entry는 로컬 설치의 package.json bin이 가리키는 Node 파일이다. CLI에 --hyperframes-entry로 절대 경로를 넘긴다. 렌더 버전은 기록하고 이전 run의 도구/템플릿을 몰래 갱신하지 않는다.

CLI는 cpu_backend를 사용하여 CPU 인코딩, browser GPU auto, fast capture false로 장면을 순차 렌더한다. probe_backends는 기존 호출 호환성용으로만 남으며 CLI에서 실행하지 않는다. 각 장면과 마스터 기록에서 실제 command, 설정, 프레임, 출력 SHA와 시간을 확인한다. OS 전역 GPU 설정은 변경하지 않는다.

검증:
1. content: 전체 원문 항목 발견과 발화/문항 판별점 의미 대응 검토.
2. audio: PCM hash/무음/클리핑/길이 검사 + 핵심 수치 직접 청취 또는 예산에 포함한 전사. 표본 검사 범위를 명시.
3. visual: tests/browser_check.mjs로 모든 장면/테마/자막 경계 검사 후 스크린샷을 직접 검토. 템플릿 컴포넌트와 크기 변경만 다른지 비교.
4. source: HyperFrames check를 실제 편집 소스에 실행. timeout은 unverified. MP4 wrapper로 대체 금지.
5. media: ffprobe, 전체 decode, 1920×1080/30fps/mono24k/프레임/스트림.
6. sync: PCM 샘플과 문단 경계, 마지막 audio/video 시간 오차.

verification/reviews.json의 content/audio/visual은 {status,evidence:[run 내부 경로],errors:[],input_hash} 형식이다. input_hash는 verify 모드가 출력하는 현재 review_fingerprint 값이다. 마지막 산출물이 정해진 뒤 검토하고 기록한다. 오래된 검토는 통과하지 않는다. content와 audio의 의미 검토를 기계 성공으로 자동 승인하지 않는다.

node tests/browser_check.mjs RUN PUPPETEER_PACKAGE_JSON CHROME_EXE는 로컬 설치한 puppeteer-core와 Chrome 실행 파일을 사용한다. 각 인자는 절대 경로다. 화면 대표 PNG는 verification/frames에 저장한다.

완료 보고는 검증한 항목과 미확인 항목을 구분한다. report.complete일 때만 latest.json을 갱신한다. 실패 시 이전 최신 결과를 유지한다. 사용자가 명시한 예산이 소진되면 성공한 문단을 보존하고 사용자에게 예산/실패 사유를 알린다. --resume은 처음 미완료 단계부터 다시 수행한다.

수학 검토는 계산 스크립트 실행 결과, 그래프 시작·중간·끝 좌표, 축/단위/차원, 가정·부호·정규화와 음성 발음을 대조한다. source/math-evidence.json은 필수이며 수치 장면의 계산·결과·그림을 해시로 동결한다. 증거 변경은 script/검토 지문을 무효화한다. 정성 장면도 숫자를 사용하지 않는 이유를 기록한다.

브라우저 검사는 분수·적분·첨자·KaTeX 오류·남은 수식 delimiter·수식/축 글자 넘침을 포함한다. 렌더 전 document.fonts.ready를 확인한다. 실제 오디오 청취 검토와 가짜 PCM smoke 검사를 구분한다. smoke 완료는 키의 실제 인증이나 교육 영상의 내용/발음 검증 성공을 의미하지 않는다.

실제 로컬 통합 검사:

```text
python3 SKILL/tests/integration_smoke.py --run SCRATCH --hyperframes-entry LOCAL_HYPERFRAMES_BIN --puppeteer-package-json PUPPETEER_PACKAGE_JSON --chrome CHROME_EXE
```

인자는 절대 경로다. 가짜 키·가짜 TTS·사인파 PCM만 사용하고 실 API transport를 차단한다. 실제 HyperFrames 렌더, Chrome 36개 시간/테마 상태, 시작·중간·끝 그래프, FFmpeg decode/sync, 묶음 publish/resume와 독립 revoice publish를 검사한다. 가짜 API 요청 6회, 유료 요청 0회가 정상 기대값이다.

묶음 영상의 목소리 변경은 독립 RUN/ledger로 수행한다. 원본 scope를 새 요청에 연결하지 않고 source/from-run.json에 원본 출처·파일명·영상 해시를 기록한다. 해당 최종 MP4만 이전버전으로 보존해 교체하고 다른 영상과 latest 항목은 유지한다. 원본이 현재 결과와 다르면 조용히 교체하지 않는다. 전체 복습 신규 제작은 별도 요청이므로 기존 전체 결과를 이전버전으로 보존한다.

## 생명과학 b87918f 업데이트 반영

장면 HTML의 data-theme="dark"를 렌더 전에 검사하고 index.html 직접 렌더는 거부한다. mux, media 검증, 자막 굽기에서 영상의 10/35/60/85% 시점 좌상단 8×8 배경을 샘플링한다. 밝기 80/255 초과나 샘플 추출 실패는 실패다. 이것은 배경 표본 검사이며 모든 픽셀·프레임을 검사했다는 뜻은 아니다.

브라우저는 OS light/dark 양쪽에서 다크 토큰·폰트·수식·넘침을 검사하고 화면 `.video-caption`이 0개인지 확인한다. 하드 자막은 마스터 검증·publish-set 후 임시 파일로 굽고, 검사 후 접미사 없는 제목의 최종 영상으로 교체한다. 검정 반투명 박스 스타일과 교체 순서는 SKILL.md "자막 (고정)"을 따른다. Pretendard Bold TTF로 libass 자막을 굽고 본문과의 겹침을 대표 프레임에서 확인한다. 기본 FFmpeg에 subtitles 필터가 없으면 설치된 macOS ffmpeg-full을 자동 선택한다. Python/tests는 유료 API 없이 실행한다.

최종 날짜 폴더에는 자막본만 남기고 복습영상/README.md·catalog.json은 실제 최종 파일의 경로·크기·SHA256으로 갱신한다. 마스터 검증 지문·review.mp4 링크·latest.json 해시는 자막본에 맞춰 수정하지 않는다. 재검증·revoice·자막 재굽기에는 해당 RUN에서 render로 재생성한 자막 없는 마스터를 쓴다.

멀티코어 검증은 workers 2/6의 모든 decoded frame MD5, PCM, AAC와 원자료 SHA를 비교한다. synthetic PCM 결과는 실제 음성 승인과 분리한다. 작업자 설정 변경 시 음성/타임라인 hash 유지, 실패/중단 시 이전 미디어와 기록 보존 및 rollback 잔여 시 재시도 차단을 확인한다. 실행 시간 개선과 저하 모두 기록한다.
