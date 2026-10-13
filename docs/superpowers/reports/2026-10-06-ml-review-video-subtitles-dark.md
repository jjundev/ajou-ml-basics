# 자막·다크모드 업데이트 반영 검증

생명과학 로컬 main의 b87918f(고정 하드 자막·다크모드 강제)와 6f0a515(HTML 하단 자막 제거·별도 자막본)의 변경을 머신러닝 스킬에 반영했다.

- composition에서 하단 .video-caption 생성과 GSAP 타이밍 제거. 머신러닝 로컬 KaTeX와 그래프 상태 기능 유지.
- burn-subtitles CLI, 짧은 SRT 분할, Pretendard Bold TTF, 고정 libass 스타일 추가. 마스터 불변과 별도 <제목>_자막.mp4 출력.
- render_parts의 dark scene entry 검사와 index.html 직접 렌더 금지. mux/verify_media/burn의 배경 밝기 표본 검사 추가.
- 자막 필터 없는 macOS FFmpeg를 위해 libass-capable ffmpeg-full 자동 탐색 추가. ffmpeg-full 설치 과정의 공용 x265 갱신으로 기존 FFmpeg가 실행되지 않아 기본 FFmpeg를 9.0.2로 재설치하여 복구했다. 셸 PATH 설정 파일은 수정하지 않았다.
- 전체 unittest: 87개 PASS. 밝은 영상의 mux·media·burn 실패, 어두운 진입점, 하단 HTML 자막 부재, SRT 분할·고정 스타일·원본 보호 검증 포함. Skill validator PASS.
- 실제 HyperFrames/Chrome/FFmpeg smoke-subtitles-dark: 제작·출판·재개·revoice PASS, 가짜 TTS 6회/유료 요청 0회. OS light/dark 양쪽에서도 브라우저 captionCount=0, 수식·폰트·그래프 상태 검사 PASS.
- 실제 burn-subtitles CLI 출력 검사 PASS. master hash 불변, 해상도·프레임·fps·오디오 스트림 유지, 다크 배경 표본 검사 PASS. 1초 대표 프레임에서 한국어 자막·서체·하단 배치·본문과의 분리를 직접 확인했다.

로컬 ignored .superpowers/sdd/2026-10-06-ml-review-video/에 로그와 검증 프레임을 보존한다. API 키나 .env 내용은 읽어 출력하지 않았고 기존 학습 노트와 실제 복습 영상을 수정하지 않았다. 커밋·푸시 없음.
