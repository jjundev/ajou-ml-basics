# ml-review-video 검증 결과

2026-10-06, codex/ml-review-video 브랜치. 커밋·푸시 없음.

- `python3 -m unittest discover -s .agents/skills/ml-review-video/tests -v`: 79개 통과.
- skill-creator quick_validate.py: Skill is valid.
- 실제 0930 source discovery: note-html/note-md/questions-html/questions-md/figure, 28개, 누락 없음.
- 프로젝트 .env: 복사 완료, 권한 0600, Git 제외, 키 로딩 확인. 내용·키·키 해시를 보고하지 않음. 실제 API 인증은 미검증.
- HyperFrames 0.8.137, Node 24, Chrome, FFmpeg: 실제 1920×1080/30fps 렌더, 전체 decode, 소스 check, 오디오 동기화 통과.
- 선형회귀 예시: 절편 0, 점 (0,0),(1,1),(2,2), w=0/1/2의 SSE=5/0/5를 계산 스크립트와 상태 그림으로 확인.
- 브라우저: light/dark 환경 36개 시간/테마 표본에서 로컬 font·수식·가로 넘침·자막 검사 통과. 발화 중간에 start/middle/end 그래프가 각각 단독 표시됨. 최종 end 프레임도 직접 확인.
- prepare-set → check → fake tts → assemble → render → browser → verify → publish-set → resume-set 통과.
- 묶음 영상 → 독립 prepare --from-run → Charon fake tts → assemble → 실제 revoice → browser → verify → 단일 전달 통과. 이전 영상 링크/해시 유지.
- 가짜 TTS 요청 6회, 유료 요청 0회. PCM은 사인파 테스트 신호이므로 실제 한국어 발음/음성 품질/키 인증 성공을 증명하지 않는다.
- 독립 검토에서 발견한 batch revoice 예산 경로, HTML 엔티티 수식 누락, 형제 영상 보존 문제를 각각 실패 재현 후 수정하고 회귀 검사 추가.

인증 파일을 검증 산출물로 복사하지 않았다. 실제 강의 내용의 학습 영상은 별도 제작 요청에서 생성·의미·발음 검토한다.
