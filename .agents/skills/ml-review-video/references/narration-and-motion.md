# 대본과 화면

디자인 원본은 sibling ml-review-pack/assets의 note-template.html과 review-template.html이다. 이 파일을 수정하지 않는다. snapshot_theme로 HTML/CSS를 보존하고 data-theme=dark를 강제한다. 별도 팔레트나 새로운 카드 디자인을 만들지 않는다. 영상용 크기/배치만 assets/video-layout.css로 조절한다.

manifest.scenes의 template_kind는 note/review다. source/scene-fragments/<scene-id>.html은 해당 템플릿의 topic/layer/tag/badge/figure/문제 클래스를 재사용한다. 긴 본문은 여러 장면으로 분리한다. inline style/script/event/외부 URL은 금지한다. SVG와 이미지는 run 내부 assets에 둔다. 모든 ID는 <scene-id>-로 시작한다.

같은 이름의 .motion.json은 target(#ID), segment_id, kind(reveal/move/count/highlight/path), from/to(GSAP property 객체), duration_s 배열이다. 이동·축적·수량 변화처럼 학습 의미가 있는 움직임을 넣는다. path는 미리 계산한 SVG strokeDashoffset/dasharray 또는 x/y 좌표로 표현한다. 시간 기반 random/interval은 쓰지 않는다.

원고와 SRT는 전체 발화의 용어·수치·조건을 보존한다. caption은 본문 핵심 문장이며 SRT의 대체가 아니다. TTS 실제 PCM 샘플 수가 확정된 후 timing.py가 시간을 만든다. HTML에 하단 고정 자막을 생성하지 않는다. 본문은 자막 안전 영역 위에 배치하고 실제 자막은 렌더 후 narration.srt로 임시 MP4에 굽고 검사 후 접미사 없는 제목의 최종 영상으로 교체한다(SKILL.md "자막 (고정)"). 단어별 타임스탬프를 지어내지 않는다. 학생용 SRT는 전체 발화, 화면 핵심 문장은 본문 박스로 표현한다.

stage_assets에는 fonts/Pretendard-{Regular,SemiBold,Bold}.woff2와 vendor/gsap.min.js가 있는 로컬 asset 폴더를 넘긴다. 기존 복습영상/0915/20260929-legacy/assets를 재사용할 수 있으며 출처/라이선스도 보존한다. 수식이 있으면 local vendor/katex에 katex.min.js, katex.min.css, auto-render.min.js와 fonts를 제공한다. 누락을 네트워크 fallback으로 감추지 않는다.

## 머신러닝 설명과 계산 증거

주제별 동기(문제 → 단순 해법의 한계 → 핵심 아이디어, 15–25초) → 작은 수치 예시 → 화면 변화 → 대응 수식 → 성립 조건·오개념 순서로 설명한다. 기호의 뜻을 화면 점·선·영역과 매핑하고, 수식 원문과 음성 발화를 분리한다. 확률/밀도·독립·차원·부호·단위 조건을 보존한다. KaTeX에는 신뢰되지 않은 명령을 허용하지 않는다. 조립 시 text node의 $…$와 $$…$$를 로컬 KaTeX로 렌더하여 nested 편집 소스에도 같은 수식이 들어간다.

계산은 source/calculations/ 안의 에이전트 작성 Python 스크립트를 실행하고 결과 JSON과 그림을 남긴다. source/math-evidence.json 계약은 schema_version=1, scenes 배열, file_hashes 객체다. scenes는 manifest의 모든 scene_id를 정확히 한 번 포함한다. 각 row는 mode(numeric|qualitative), formula_refs/conditions/axes/units/dimensions(각각 비어 있지 않은 문자열 배열)를 가진다. 정성 장면은 축이 없다는 설명을 해당 배열에 적고 reason으로 숫자를 쓰지 않는 이유를 적는다.

numeric row는 calculation_script와 calculation_result(RUN 상대 경로), states 배열을 가진다. states는 label=start/middle/end 순서의 세 항목이며 각각 figure_path와 values(유한 숫자 값 객체)를 가진다. file_hashes는 모든 참조 파일의 RUN 상대 경로 → SHA256 매핑이다. 예:

```json
{
  "schema_version": 1,
  "scenes": [{
    "scene_id": "scene-regression", "mode": "numeric",
    "formula_refs": ["SSE = sum((y_i-w*x_i)^2)"],
    "conditions": ["절편 0, 점 (0,0),(1,1),(2,2)"],
    "axes": ["x: 입력", "y: 관측/예측"], "units": ["무차원"], "dimensions": ["w: 스칼라"],
    "calculation_script": "source/calculations/example.py",
    "calculation_result": "source/calculations/result.json",
    "states": [
      {"label":"start","figure_path":"assets/start.svg","values":{"w":0,"sse":5}},
      {"label":"middle","figure_path":"assets/middle.svg","values":{"w":1,"sse":0}},
      {"label":"end","figure_path":"assets/end.svg","values":{"w":2,"sse":5}}
    ]
  }],
  "file_hashes": {}
}
```

작성 시 file_hashes의 빈 객체를 실제 다섯 파일의 해시로 채운다. numeric 증거 없이 check/tts가 진행되지 않는다. 계산 스크립트는 검사기가 자동 실행하지 않는다. 직접 실행한 결과·그림 좌표·발화 대응을 coverage.md와 내용 검토에 기록한다. 해시/구조 성공을 수학적 의미 검증으로 대신하지 않는다.

SVG 상태를 계산해 시작·중간·끝을 reveal/highlight/move로 보여준다. 단계별 변화에는 현재 값과 단계임을 표시하고 연속 최적화처럼 오해시키지 않는다. 임의 path morph 엔진을 만들지 않는다.

## 주제별 도입

기존 노트의 s0-why-bayes, s2-motivation처럼 영상의 주제에 해당하는 동기를 먼저 찾는다. 선수 내용이면 selection.json의 context/prerequisite_ids로 연결하고, 주개념 자체의 동기면 해당 requirement에서 설명한다. 특정 why ID를 모든 영상에 강제하지 않는다. 첫 segment·장면에 문제와 한계를 실제로 설명했는지 coverage.md의 의미 검토에서 확인한다. 등록된 선수 ID만으로 도입 내용이 검증되었다고 주장하지 않는다. 도입도 math-evidence.json에 qualitative 장면과 숫자를 쓰지 않는 이유를 기록한다. 새 수치 예시는 설명용으로 표시한다.

## 숫자 자막

text와 subtitle_text는 동일한 전체 발화다. 숫자와 단위 표기만 달라야 하며 문장·조건·기호 뜻을 축약하지 않는다. 새 대본에서 숫자를 발음으로 풀어 썼다면 subtitle_text를 반드시 작성한다. caption은 요약이므로 재사용하지 않는다. 기존 manifest에 필드가 없으면 text를 그대로 사용한다.

```json
{
  "text": "이 일은 마이너스 영 점 오, 삼분의 일, 십이 점 오 퍼센트, 이 밀리초로 설명해요.",
  "subtitle_text": "이 일은 -0.5, 1/3, 12.5%, 2 ms로 설명해요."
}
```

한글 일/이/삼 등을 자동 치환하지 않는다. 값·음수 부호·소수 자릿수·분자/분모·퍼센트·단위를 원자료와 대조하고 coverage.md에 발화 ↔ 표시 대응을 기록한다. 필드 검사는 빈 값·비문자열·줄바꿈을 거부하지만 수학적 동등성까지 증명하지 않는다. TTS는 text만 읽으며 subtitle_text만 바꿔도 PCM 캐시 키는 바뀌지 않는다.

숫자 토큰(-0.5, 1/3, 12.5%, 1.2e-3, 1,000, 2–3)과 뒤에 붙은 단위(예: ms, V, A, Hz, 초)는 줄바꿈의 한 묶음이다. 새 단위를 쓰면 scripts/lib/subtitles.py의 단위 목록과 회귀 테스트를 함께 확장한다. 한 묶음이 길어도 중간에서 쪼개지 말고 화면에서 읽히는지 검토한다. cue 시작·끝은 실측 발화 시간으로 유지하며, 내부 분할은 글자 비중에 따른 근사값이다. 실제 단어 타임스탬프라고 주장하지 않는다. compact 숫자로 분할 시간이 달라질 수 있으므로 최종 영상의 발화·자막 대응을 확인한다.
