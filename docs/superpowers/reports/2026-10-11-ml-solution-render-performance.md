# ML 풀이영상 멀티코어 렌더 검증

EC2 75a6a581d7b66651d361856fa1bfa35bc85f20b8의 독립 정책·미디어 복구 부품을 ML 단일/여러 페이지 bundle CLI에 연결했다. 최초 이식 commit eeec3d56513fe9e8a34f45edb05ae1118b08cf62와 84개 baseline 목록은 보존하고 현재 port hash만 갱신했다. 별도 render-port-provenance에 추가 이식 근거가 있다.

Apple M5/physical10/16GiB에서는 기본6, 기타/탐지실패2; --render-workers 정수1..6. CPU 인코딩/browser GPU auto/fast capture false; 파트/문항 순차, 내부 capture workers만 변경한다. config/음성/타임라인/조립을 작업자 변경으로 갱신하지 않는다. 손상 저장값 override 거부, resume-set 옵션 생성없음.

최종 검토가 찾은 upgrade 입력 지문 문제는 정확히 검토한 bundle_cli 신버전 SHA를 구버전 입력 의미 SHA로 정규화하여 수정했다. 알 수 없는 파일 변경은 실제 SHA로 무효화하고 출력/hash 검사도 유지한다. 구버전 파일→신버전 보존/다른 수정 무효화 검사를 RED→GREEN으로 확인했다.

## 실제 비교

동결 1007 Product_of_Gaussians P2 RUN: `.codex/worktrees/ml-solution-video/머신러닝기초/.superpowers/sdd/2026-10-10-ml-solution-video/acceptance-final/문제풀이영상/1007/1007_제작자료/실행/20261010-212359-413e865a/videos/problem-a7acd5c2175a7cb5`. 문제 원본1페이지+답안 원본1페이지의 서로 다른 page_id와 화면 전환을 검증했다. 여러 답안 continuation page를 실렌더한 것으로 주장하지 않는다(continuation/seek 경로는 기존 bundle 회귀 검사가 담당). 원본 전체3872프레임/129.07초를 모두 비교했다.

HyperFrames 0.8.137 (`/Users/hyunjun_macbook_pro/.npm/_npx/702923228c2ce1e6/node_modules/hyperframes/dist/cli.js`), Chrome155.0.8059.39, Node26.4.0, Python3.14.8, FFmpeg9.0.2. 전역 업그레이드 없음.

실행: `python3 .agents/skills/ml-solution-video/tests/render_performance_acceptance.py --fixture FROZEN_RUN --destination FRESH_MATERIALS_DIR --hyperframes-entry ABSOLUTE_CLI`. 생산 render_master를 두 번 순차 호출했다. 세부 옵션/command/hash는 각 render-receipt.json에 저장한다.

workers2 198.004s → workers6 167.030s (15.6% 감소). source check, render/mux, 전체 frame MD5/AAC 추출을 포함한 1회 시간이며 일부 다른 테스트와 겹친다. 일반 성능 개선율로 사용하지 않는다.

모든 decoded frame MD5, PCM, AAC 및 master SHA가 동일하고 fixture hash가 변하지 않았다. FFmpeg의 전체 프레임 decode, 별도 하드자막 burn/full decode, 처음·중간·끝 및 caption PNG를 확인했다. PDF 화면·수식·연필·카메라 규약을 바꾸지 않았다. 실제 음성은 검증하지 않았고 유료 요청0/게시없음/live_audio=unverified다.

기본 회귀284 tests PASS(2 기존 skip). 최종 추가 검사와 Node/skill 결과는 최종 검증 결과 절에 기록한다.

```json
{
  "technical_complete": true,
  "metrics": [
    {
      "workers": 2,
      "frames": 3872,
      "frame_hash": "20407d9ac16e02468540403e9578b1c8d129beec3a11e6b9b51e0d8c2f099c14",
      "pcm_hash": "db3139f208c662dc86f6d2727b09fef8a57d950396ebcc1acf94b97061a83a0a",
      "aac_hash": "cb063ee7886c7493ac6da032467bbf918e8d084b169922c29486f8426caa839a",
      "master_hash": "c9df78a0c10acdebf94add148daa04d125dcaeab536a47e747c57099aca0be91",
      "seconds": 198.00417724999716
    },
    {
      "workers": 6,
      "frames": 3872,
      "frame_hash": "20407d9ac16e02468540403e9578b1c8d129beec3a11e6b9b51e0d8c2f099c14",
      "pcm_hash": "db3139f208c662dc86f6d2727b09fef8a57d950396ebcc1acf94b97061a83a0a",
      "aac_hash": "cb063ee7886c7493ac6da032467bbf918e8d084b169922c29486f8426caa839a",
      "master_hash": "c9df78a0c10acdebf94add148daa04d125dcaeab536a47e747c57099aca0be91",
      "seconds": 167.03042037499836
    }
  ],
  "frames_equal": true,
  "pcm_equal": true,
  "aac_equal": true,
  "source_unchanged": true,
  "paid_requests": 0,
  "published": false,
  "live_audio": "unverified"
}
```

검증 미디어와 초기/중간/끝·자막 PNG는 이 worktree의 `.superpowers/렌더검증_제작자료/solution/acceptance`에 보존한다. 구형/신형 RUN 지문 검사, CLI 양 경로, media15, policy6, state12, 입력guard4, provenance2 및 Node runtime6 검사를 수행했다. 독립 코드 검토의 Important 두 건(업그레이드 지문/중첩 pending)은 RED→GREEN으로 수정했다.

## 최종 검증 결과

`python3 -m unittest discover -s .agents/skills/ml-solution-video/tests -v`: Ran313 tests in445.426s, OK(skipped=2); 기존 opt-in 렌더 skip을 유지했다. 프레임 비교는 별도 real acceptance로 실행했다. `node --test .../test_writing_runtime.cjs .../test_teaching_runtime.cjs`:6 PASS. 두 스킬 quick_validate: Skill is valid! provenance mismatch0, git diff --check clean. Python/Pillow/SWIG deprecation warnings는 기존 검사에서 관찰되며 이번 변경으로 수정하지 않았다.

Ruling: 최종 CLI/state/provenance와 수용 harness/report는 함께 커밋해 manifest가 참조하는 새 파일을 빠뜨리지 않는다. 검토 diff가 커지지만 실행 계약은 변하지 않는다.
