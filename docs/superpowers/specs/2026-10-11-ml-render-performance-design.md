# 머신러닝기초 풀이·개념 복습영상 멀티코어 렌더 설계

## 확정된 의도

EC2의 멀티코어 렌더 정책을 머신러닝기초 풀이영상 `ml-solution-video`와 개념 복습영상 `ml-review-video` 모두에 적용한다. 사용자 결정 #8은 두 스킬 모두 포함으로 확정됐다. 기존 화면·음성·검토 계약을 유지하면서 작업자 수 설정, 재개, 실패 복구, 실행 기록을 제공한다. 이번 문서는 구현 승인이 아니라 확정된 채팅 설계의 저장본이다.

두 흐름은 독립 실행 가능한 스킬이므로 구현 계획을 두 개로 나눈다. 풀이영상 변경은 bounded, 개념 복습영상은 확인된 과거 구현 복원 후 bounded 변경이다. 공유 런타임 패키지를 새로 도입하지 않는다.

## 현재 근거와 동결 기준

- ML 조사 시 HEAD: `642a17b`. 실행 전 변경 목록과 HEAD를 다시 확인한다.
- 풀이영상은 `scripts/solution_video/media.py:22-48`에서 작업자 2개를 고정하며 파트를 순차 처리한다. `scripts/video.py:140-141`과 `scripts/solution_video/bundle_cli.py:112-114`가 별도 호출 경로다.
- 풀이영상 단계 지문은 `scripts/solution_video/state.py:7-25`에 정의돼 있다. 기존 이식 manifest는 최초 EC2 기준 `eeec3d56513fe9e8a34f45edb05ae1118b08cf62`와 84개 기준 파일을 고정한다.
- 현재 개념 복습영상 디렉터리는 pycache만 남아 있고 실행 소스가 없다. 로컬 Git 객체 `7b2028e82f92962dd12b7f8b76580f6ee7b39682`에서 `.agents/skills/ml-review-video/` 전체 원본을 확인했다. 현재 브랜치 조상이라고 가정하지 않는다.
- EC2 풀이영상 이식 기준: `75a6a581d7b66651d361856fa1bfa35bc85f20b8`의 `.agents/skills/ec2-solution-video/`.
- EC2 개념 복습영상 이식 기준: `7098e0cc042dab4f2660eebe1fa69c3ebc28dcae`의 `.agents/skills/ec2-review-video/`. EC2의 다른 미커밋 변경은 이식하지 않는다.
- 현재 호스트는 Apple M5 / 물리 CPU 10코어 / 메모리 17179869184바이트다. EC2 측정의 속도 개선은 ML의 성능 근거로 사용하지 않는다.

## 전역 계약

- 기본값은 Darwin / Apple M5 / 물리 CPU 10코어 / 메모리 16GiB 이상에서 workers=6, 기타 환경과 탐지 실패에서 workers=2.
- workers는 정수 1–6. bool·실수·문자열·범위 밖 값과 알 수 없는 키는 거부한다.
- 설정은 `source/render-options.json`: `{"schema_version":1,"workers":6,"encoder":"cpu","browser_gpu":"auto","fast_capture":false}`. 다섯 키만 허용한다.
- 우선순위는 CLI `--render-workers` → 유효한 저장값 → 호스트 기본값. 손상된 저장값은 override로 숨기지 않는다. 저장값은 호스트가 달라져도 유지한다.
- 신규 RUN은 설정을 생성한다. 옵션 없는 기존 RUN은 render/revoice 요청 때만 생성하고 resume/resume-set은 파일을 쓰지 않는다.
- CPU 인코딩·브라우저 GPU auto·`--experimental-fast-capture=false`·delivery 1920×1080/30fps 유지. 파트·장면·문항은 순차 처리하고 내부 캡처 작업자만 늘린다.
- 옵션 변경은 render 이후만 무효화한다. 설정 변경 때문에 대본·PCM·타임라인·조립 결과를 갱신하지 않는다. 다른 입력 변경으로 발생한 기존 단계 무효화를 우회하지 않는다.
- ML 풀이영상의 PDF·수학 검토·여러 페이지·연필·자막 계약을 유지한다. 개념 복습영상의 수식·계산·축·단위·차원·시작/중간/끝 증거·다크모드·자막·게시 계약을 유지한다.
- 자동 GPU 인코딩/작업자 대체, 전역 설치·설정 변경, 유료 TTS, 기존 영상 일괄 재생성·자동 게시·push는 제외한다.
- 실패 시 이전 유효 파트/장면과 마스터·기록을 보존한다. 앞서 성공한 파트는 유지할 수 있다. 임시 출력은 검증 후 교체하고 실패 로그를 남긴다.
- 미디어/기록 교체 중 예외·Ctrl+C는 이전 쌍으로 복구한다. 복구 실패 시 `.rollback` 사본 유지·경로 보고·덮어쓰는 재시도 차단. 강제 종료/전원 상실의 다중 파일 원자성은 주장하지 않는다.
- 실험·중간 미디어는 제작자료/scratch 내부에만 보관한다. 실제 음성 청취나 교육 품질 승인으로 synthetic PCM 검사를 사용하지 않는다.

## 풀이영상 구현 계약

`solution_video/render_options.py`는 `detect_hardware() -> dict`, `default_render_options(hardware: dict | None = None) -> dict`, `validate_render_options(options: dict) -> dict`, `load_render_options(run: Path, workers: int | None = None, *, hardware: dict | None = None) -> dict`를 제공한다. EC2의 검증 정책을 복사하고 스킬 내부에서 독립 실행한다.

`render_master(parts: list[dict], timeline: dict, audio: list[dict], run: Path, hyperframes_entry: Path, *, render_options: dict | None = None) -> Path`로 기존 위치 인자를 보존한다. 양쪽 CLI 경로는 재개 검사 전에 옵션을 검증·저장하고 render_master로 전달한다. 반환 JSON에 render_options/render_receipt를 제공하고 render 단계 출력에 마스터와 기록을 모두 등록한다.

파트 임시 출력은 1080p30/예상 프레임 검사 후 교체한다. 마스터는 총 프레임과 mono 24kHz 오디오도 검사한다. `verification/render-receipt.json`은 schema_version/options/parts/master_sha256을 포함하며 각 part는 key/command/elapsed_seconds/output_sha256/frames다. 옵션과 정책 모듈은 render 지문에만 추가한다.

최초 `assets/port-provenance.json`의 기준 커밋·84개 원본 목록은 유지한다. 수정된 항목의 ported_sha256/test_evidence를 갱신하며 이번 동결 출처와 신규 부품은 별도 `assets/render-port-provenance.json`에 기록한다.

## 개념 복습영상 구현 계약

과거 ML 디렉터리만 Git archive로 복원한다. 현재 non-cache 파일이 생겼다면 내용을 비교하고 같은 파일만 유지하며 충돌 파일을 덮어쓰지 않는다. 복원 기준과 파일 SHA 목록을 `assets/restore-provenance.json`에 저장한다. 복원 전후 원자료·다른 스킬·기존 cache는 보존한다.

`lib/render_options.py`는 위 정책과 같은 함수 시그니처를 가지되 ValueError를 사용하는 복습영상 관례를 따른다. `render`와 `revoice` CLI 모두 옵션을 받는다. prepare/prepare-set은 신규 설정을 생성하며 prepare --from-run은 복사한 유효 저장값을 유지한다.

EC2 `lib/render.py`의 `cpu_backend(entry, options) -> dict`, `render_parts(parts, run, backend) -> list[Path]`, `commit_media_receipt(pending, data, media, receipt) -> None`, `mux_with_receipt(parts, audio, timeline, destination, backend, *, captured=None) -> Path`를 이식한다. 기존 probe 인터페이스는 호환용으로 남기되 CLI가 실행하지 않는다. 장면 cache key에는 options/도구 버전/HTML·CSS·JS·폰트·그림/렌더 모듈 해시를 포함한다. 유효 cache hit는 재렌더하지 않는다.

장면 MP4/JSON과 마스터/통합 기록은 쌍으로 검증·교체·복구한다. 시도별 UUID pending을 사용하고 timeout/중단 시 실행한 자식 프로세스 종료·회수 후 정리한다. revoice의 실제 재렌더 장면에 같은 정책을 전달하며 retime만 수행한 창을 캡처 성공으로 기록하지 않는다. 원본 RUN과 형제 게시물을 보존한다.

폰트 준비 전 초기 프레임이 달라지는 EC2 보정도 적용한다. document.fonts.ready 이후 타임라인을 구성·등록하고 composition 모듈 지문을 기록한다. 이 코드 변경에 따른 1회 reassemble은 허용하되 음성은 보존한다. 이후 작업자 설정 변경만으로는 reassemble하지 않는다.

## 완료 검증

두 계획 각각 unit/CLI/재개/복구 회귀와 스킬 검증을 수행한다. 같은 하드웨어 입력에 대해 두 정책이 동일한 옵션을 반환해야 하며 다른 과목 checkout 없이 실행돼야 한다.

풀이영상은 동결한 ML 여러 페이지 문항 composition/PCM으로 2/6개 생산 render_master를 실행한다. 모든 decoded frame hash, PCM, AAC, 원자료 hash를 비교하며 페이지 경계·초기 프레임을 포함한다. 오래된 단계/검토 승인을 복사해 생산 CLI 검사를 통과시키지 않는다.

개념 복습영상은 ML 회귀/SSE 수식·그래프 fixture로 60초/2장면을 저작한다. 기본 0.6초 motion과 24초 motion을 별도로 2/6개 비교하고 모든 프레임·PCM·AAC·원자료 hash·자막·전체 decode를 확인한다. 대표 PNG를 직접 검토하고 개선/저하를 모두 기록한다. 차이가 있으면 허용 오차를 늘리거나 GPU/고속 캡처 정책을 몰래 바꾸지 않고 원인을 해결하거나 미완료로 보고한다.
