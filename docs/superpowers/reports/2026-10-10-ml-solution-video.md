# ML 문제풀이 영상 스킬 구현 검증

구현 위치: `.agents/skills/ml-solution-video`. EC2 기준 커밋은 `eeec3d56513fe9e8a34f45edb05ae1118b08cf62`다. 원본 84개 tracked 파일과 TTS 4개 모듈·Pretendard Bold·GSAP의 출처 및 변경 후 SHA를 `assets/port-provenance.json`으로 추적한다. 런타임은 EC2 checkout이나 형제 review-video 스킬을 요구하지 않는다.

## 구현 범위

- 저장된 ML 카드·문제/답안 PDF를 동결하고, 날짜·팩·문항 및 계속 페이지를 구분한다. Hint 부록은 제외한다.
- 원본 SVG glyph·도형·그래프를 보존하며, 페이지별 공개와 하나의 상위 frame clock을 연결한다.
- 전역 단계에 원문 coverage·수학 검토·이유→작성→검산 원고를 묶는다. 기계 검사는 구조와 현재 원문·해시를 검증하며 수학적 진실을 증명하지 않는다.
- spoken-text-only-v1 및 실측 PCM 청크 경계로 음성·기호 자막을 연결한다. 자막 변경 시 동일 발화 캐시를 재사용한다.
- 필기·도형 예산·카메라·발화 주석·필기 지연 검토·현재 상태의 무효화와 재개를 지원한다.
- 실제 전청크 청취와 현재 의미 검토가 없는 결과는 게시하지 않는다. 성공 형제와 이전 결과를 보존하고 게시 교체 실패를 롤백한다.

현재 8개 날짜의 55문항을 확인했다: 0909 5, 0914 7, 0916 6, 0921 6, 0923 7, 0928 8, 0930 8, 1007 8. 이전 HTML의 조건/질문 태그가 없는 경우에는 전체 원문을 보존하고 분리 상태를 author-required로 표시한다. 원본 PDF를 직접 대조한 뒤 저작하며 문장을 자동 분리하지 않는다.

## 검사 결과

독립 검토 수정 및 소프트웨어 캡처 설정 후 전체 Python 회귀(`suite-software.log`, 349.514초): 284개 실행, 실패 0, 선택형 영상 보고서 검사 2개 skip. 따라서 통과 수는 282개다. Node writing/teaching runtime은 6개 assertion 통과, skill-creator quick_validate는 `Skill is valid!`를 확인했다. 마지막 부분 raster 캡처 설정 변경 후 페이지 합성·숨김 변이와 독립 검토 재현 검사 7개를 추가 실행하여 7/7 통과(26.590초)를 확인했다. 이 변경은 tests/bundle_check.mjs 한 파일뿐이며, 제작 코드·자산은 전체 회귀 당시와 byte-for-byte 동일하다. 추가 7회는 전체 회귀 재실행으로 세지 않는다. 별도 테스트로 두 답안 페이지를 묶은 1920×1080/30fps MP4와 자막을 만들고 frame count를 확인했다.

실제 1007 P2/P3/P8은 별도 scratch에서 동결·저작·원본 게이트·TTS 대체 PCM·페이지 합성·HyperFrames 렌더·하드 자막을 실행했다. 원문 SHA는 보존되었고 유료 요청은 0이다. 음성은 명시적인 synthetic PCM이며 `live_audio=unverified`, `complete=false`다. 실제 공급자 인증·발음·전사 일치·자연스러운 연결을 검증했다고 주장하지 않는다. 공개 날짜 폴더와 latest는 갱신하지 않았다.

최종 기술 검사의 상세 상태와 현재 근거 경로는 아래 실행 결과 표에 기록했다. 모든 기술 검사가 현재 코드·입력 해시와 일치함을 확인했다.

## 독립 코드 검토와 수정

독립 검토의 Important 5건을 재현 검사로 확인한 뒤 수정했다.

1. 실패한 export 문항이 batch 대본 검토를 막던 문제: 미준비 실패 문항을 제외하며 복구되면 다시 포함한다.
2. pacing-review가 추가되면 게시가 거부되던 문제: audio/visual 검토를 이름으로 요구하고 모든 현재 검토 SHA를 확인한다.
3. 공개 영역에 걸치는 래스터 풀이가 보일 수 있던 문제: 영역과 교차하는 painted raster를 거부한다. 현재 PDF의 검은 PNG/영휘도 마스크처럼 원본에서 완전히 보이지 않음이 증명되는 경우만 제외한다. 원본 SVG inventory의 bounds·이미지 목록·마스크 판정을 대조하므로 저작 metadata만 바꿔 우회하지 않는다. OCR이나 텍스트 추측을 사용하지 않는다.
4. 명시적 pack 선택에서 중복 identity가 같은 RUN을 덮던 문제: 정규화한 pack identity와 bundle key의 중복을 차단한다.
5. 계속 문제 페이지를 생략하거나 문제 소개에서 답안 원본을 드러낼 수 있던 문제: 모든 문제 페이지의 원문 순서와 page role을 검증한다.

검증 코드 변경을 resume가 추적하지 못하는 항목은 계획의 코드 지문 요구에 따라 Important로 재분류했다. bundle_verify.py와 bundle_check.mjs를 검증 단계 지문에 포함했다. 여섯 재현 검사는 수정 전 실패와 수정 후 통과를 확인했고 전체 회귀도 통과했다. 추가 독립 리뷰를 반복하지 않았다.

독립 검토가 판단하지 않은 항목은 실제 음성 품질, 진행 중이던 전체 픽셀 수용 검사, 모든 수학 풀이의 별도 재풀이였다. 실제 음성은 미검증으로 유지하며, 픽셀 수용 검사는 실행 결과로만 판정한다. 수학 검토는 고정 원문에 대한 작성자 근거와 기계적 구조 검사를 구분한다.

## 실행 중 판단과 한계

- 격리된 worktree에서 구현했다. 원래 과목 폴더에 반영할 때는 새 스킬과 이번 보고서만 복사하며 기존 과목 자료·스킬·자격 증명은 덮지 않는다. 두 작업 공간의 중복본이 남을 수 있다.
- 커밋 요청이 없으므로 커밋 단계는 보류했다. merge/push는 실행하지 않는다. 미커밋 변경과 scratch 근거를 보존한다.
- 수용 검사는 필기 시간에 맞춘 synthetic PCM으로 기술 동기화만 확인한다. 실제 음성 품질은 이후 실제 청취가 필요하다.
- 이전 HTML의 조건/질문 구분은 추측하지 않았다. 저작자는 전체 원문과 PDF 패널을 확인해야 한다.
- 마지막 읽기 전용 리뷰는 실행 중인 수용 검사와 겹쳐 진행했다. 리뷰 후 변경은 재현 검사와 전체 회귀로 검증하며 수용 결과도 현재 코드 기준으로 다시 확인한다.
- 래스터 예외는 원본에서 영휘도 마스크/영투명도가 증명되는 경우만 허용한다. 이 판정이 잘못되면 선공개 위험이 있으므로 원본 inventory와 해시에 묶는다.
- 검증만 바뀐 scratch 실행에서는 재저작 후 실제 렌더 입력(HTML/JS/CSS/이미지), 타임라인, PCM이 이전과 byte-for-byte 동일함을 확인해 기존 encode를 유지했다. 생산 CLI의 단계 무효화 규칙은 바꾸지 않았다.

- 캡처 준비 전 첫 프레임의 미세한 raster 차이가 있었으므로 독립/상위 화면의 전체 glyph·이미지 표면을 먼저 준비한다. 준비만으로 P3 한 프레임의 6픽셀에서 최대 1단계 채널 차이가 남아 소프트웨어 캡처(`--disable-gpu`)로 정확 비교를 고정했다. 소프트웨어 캡처만으로 P8 f3808/3809의 차이가 남았다. ID를 정규화한 SVG DOM·clip 좌표·화면 bounds는 동일했으며 연속 캡처도 안정적이었다. Chrome 부분 raster 갱신을 끄면 같은 25개 probe가 세 번 모두 차이 0이므로 `--disable-gpu --disable-partial-raster`로 캡처 환경을 고정했다. 제작 렌더러나 원문은 바꾸지 않았다. GPU 또는 Chrome 내부 구현의 정확한 원인이라고 단정하지 않는다. 모든 계획된 프레임을 그대로 비교하며 decoded RGBA 허용 오차는 0이다. 하드웨어에만 생기는 raster 차이는 이 정확 비교의 범위 밖이며 실제 encode·상태·geometry·core 화면 검사는 별도로 유지한다. 숨김 CSS 변이도 계속 실패하는지 검사한다.
- 실행 중 EC2 HEAD는 `1208d3c`(23:16 멀티코어 렌더 병합)로 바뀌었다. 승인 설계는 HEAD 자동 갱신을 금지하고 `eeec3d5`를 고정하므로 이번 이식은 그 기준을 유지한다. 새 멀티코어 설정까지 반영했다고 주장하지 않는다.
- 커밋되지 않은 worktree와 무시된 scratch 근거는 삭제하지 않는다. 이후 별도 정리 전까지 임시 영상의 디스크 사용량이 남는다.

- 동시에 실행한 소프트웨어 캡처에 긴 지연이 생겨 수용 검사를 순차 실행으로 전환했다. 단독 P2의 전체 state 검사와 25개 화면 비교는 8.670초, 차이 0으로 완료됐다. 제작 CLI의 비교 지점과 허용 오차를 줄이지 않았으며 검증 시간은 길어질 수 있다.

## 실행 결과 표

| 문항 | 기술 검사 | 전체 화면 비교 | 프레임 수 | 현재 검사 근거 |
|---|---|---|---|---|
| P2 | 13/13 통과 | 2094개, 차이 0 | 3872 | [검사 결과](</Users/hyunjun_macbook_pro/.codex/worktrees/ml-solution-video/머신러닝기초/.superpowers/sdd/2026-10-10-ml-solution-video/acceptance-final/문제풀이영상/1007/1007_제작자료/실행/20261010-212359-413e865a/videos/problem-a7acd5c2175a7cb5/verification/report.json>) · [페이지 비교](</Users/hyunjun_macbook_pro/.codex/worktrees/ml-solution-video/머신러닝기초/.superpowers/sdd/2026-10-10-ml-solution-video/acceptance-final/문제풀이영상/1007/1007_제작자료/실행/20261010-212359-413e865a/videos/problem-a7acd5c2175a7cb5/verification/page-order.json>) |
| P3 | 13/13 통과 | 2850개, 차이 0 | 4153 | [검사 결과](</Users/hyunjun_macbook_pro/.codex/worktrees/ml-solution-video/머신러닝기초/.superpowers/sdd/2026-10-10-ml-solution-video/acceptance-final/문제풀이영상/1007/1007_제작자료/실행/20261010-212359-413e865a/videos/problem-37572b9500ab80f1/verification/report.json>) · [페이지 비교](</Users/hyunjun_macbook_pro/.codex/worktrees/ml-solution-video/머신러닝기초/.superpowers/sdd/2026-10-10-ml-solution-video/acceptance-final/문제풀이영상/1007/1007_제작자료/실행/20261010-212359-413e865a/videos/problem-37572b9500ab80f1/verification/page-order.json>) |
| P8 | 13/13 통과 | 3404개, 차이 0 | 5484 | [검사 결과](</Users/hyunjun_macbook_pro/.codex/worktrees/ml-solution-video/머신러닝기초/.superpowers/sdd/2026-10-10-ml-solution-video/acceptance-final/문제풀이영상/1007/1007_제작자료/실행/20261010-212359-413e865a/videos/problem-26f7f4198f344928/verification/report.json>) · [페이지 비교](</Users/hyunjun_macbook_pro/.codex/worktrees/ml-solution-video/머신러닝기초/.superpowers/sdd/2026-10-10-ml-solution-video/acceptance-final/문제풀이영상/1007/1007_제작자료/실행/20261010-212359-413e865a/videos/problem-26f7f4198f344928/verification/page-order.json>) |

총 8348개 probe를 누락 없이 검사했다. 세 결과 모두 `technical_complete=true`, `complete=false`, `live_audio=unverified`다. 최종 미디어는 1920×1080/30fps/mono24kHz이며 원문 4개 파일 SHA가 초기 값과 동일하다.

[수용 검사 전체 결과](</Users/hyunjun_macbook_pro/.codex/worktrees/ml-solution-video/머신러닝기초/.superpowers/sdd/2026-10-10-ml-solution-video/acceptance-final/acceptance.json>) · [전체 회귀 로그](</Users/hyunjun_macbook_pro/.codex/worktrees/ml-solution-video/머신러닝기초/.superpowers/sdd/2026-10-10-ml-solution-video/suite-software.log>) · [최종 캡처 설정 회귀 로그](</Users/hyunjun_macbook_pro/.codex/worktrees/ml-solution-video/머신러닝기초/.superpowers/sdd/2026-10-10-ml-solution-video/final-capture-regression.log>)

직접 확인한 최종 MP4의 중간 프레임과 native/필기 단계 PNG는 worktree scratch에 보존했다. 실음성 또는 영상의 교육 품질 승인으로 사용하지 않는다.

## 과목 폴더 반영

새 스킬 117개 non-cache 파일과 이 보고서를 원래 머신러닝기초 폴더에 복사했다. 기존 대상이 없음을 확인했고 코드·자산·보고서는 worktree와 byte-for-byte 동일하다. 기존 과목 자료·스킬·자격 증명을 덮지 않았다. 과목 폴더에서 `test_ml_port test_ml_sources` 8/8 통과(1.836초), `quick_validate`의 `Skill is valid!`를 확인했다. 커밋·stage·merge·push는 하지 않았다. 미커밋 worktree와 scratch 근거는 보존한다.

## 후속 Git 반영 요청

위 Git 상태는 구현 검증 당시의 기록이다. 이후 사용자의 “커밋해줘. 메인에” 요청에 따라 새 스킬·설계·구현 계획·검증 보고서를 main 브랜치의 커밋 대상으로 확정했다. 푸시는 요청 범위에 포함하지 않는다. worktree와 scratch 검증 근거는 보존한다.
