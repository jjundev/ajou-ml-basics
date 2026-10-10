# ML 개념 복습영상 멀티코어 렌더 검증

동결 ML 원본 7b2028e82f92962dd12b7f8b76580f6ee7b39682의 127개 파일을 복원하고 EC2 7098e0cc042dab4f2660eebe1fa69c3ebc28dcae의 렌더 부품을 이식했다. ML 수학·출처·selection·독립 revoice·형제 게시 계약은 유지한다.

Apple M5 / physical 10 / 17179869184 bytes. Python 3.14.8, Node v26.4.0, HyperFrames 0.8.137, Chrome 155.0.8059.39, FFmpeg 9.0.2. 고정 CLI: `/Users/hyunjun_macbook_pro/.npm/_npx/702923228c2ce1e6/node_modules/hyperframes/dist/cli.js`. 전역 설치·버전 변경 없음.

정책: 해당 호스트6, 기타/탐지실패2; CLI→유효 저장값→기본값; cpu/browser_gpu auto/fast_capture false, 장면 순차. 옵션만 변경 시 음성/타임라인 보존. 최초 font/composition 보정은 1회 재조립을 요구한다.

## 검증과 수정

- 복원 baseline 88 tests PASS. 최종 개념영상 회귀 120 tests PASS, 스킬 quick_validate PASS.
- 렌더 정책·cache·30fps·손상기록·쌍 교체/interrupt/rollback 실패·detached descendant timeout 검사를 포함한다.
- 실제 Chrome 초기 상태 검사에서 future hide immediateRender가 중간 그래프를 미리 공개하는 [1,1,0]을 재현했다. 시간순으로 earliest from 값을 초기화하고 future immediateRender=false로 보정 후 [1,0,0] PASS.
- mux 내부 pending.pending.mp4 유출을 RED로 재현하고 finally 정리 후 renderer12 tests PASS.
- 별도 최종 검토에서 추가 Critical/Important 없음.

## 실제 영상 비교

SSE oracle points=(0,0),(1,1),(2,2), intercept=0, w=0/1/2, SSE=5/0/5. 실제 ML template/KaTeX/Pretendard, 분수·적분·첨자, 60초/2장면/1800프레임, synthetic PCM만 사용했다. 첫 발화 slot24.4초, 나머지1.7초 각각; dynamic은 첫 slot24초 움직임, 나머지0.6초 reveal.

| 움직임 | workers2 (초) | workers6 (초) | 전체 프레임 | PCM/AAC | 완료 |
|---|---:|---:|---|---|---|
| 0.6초 reveal | 20.277 | 20.581 | True | True/True | True |
| 24초 reveal | 56.688 | 39.928 | True | True/True | True |

시간은 1회 실측이며 다른 회귀 검사/벤치마크와 일부 겹친다. 평균 성능이나 모든 영상의 속도 개선으로 일반화하지 않는다. 짧은 움직임6개가 1.5% 느린 결과도 유지했다.

초기 실험에 추가했던 SVG x 이동은 그래프 영역 래스터 차이가 발생했다. 실험 fixture를 기존 ML author의 opacity reveal로 돌아가 비교했고 GPU 정책·fast capture·프레임 허용오차를 바꾸지 않았다. 임의의 이동 SVG가 모든 환경에서 프레임 동일하다는 보장은 없다. 초기 실패와 수정본 artifact를 모두 보존한다.

실행: `python3 .agents/skills/ml-review-video/tests/render_performance_acceptance.py --destination FRESH_MATERIALS_DIR --hyperframes-entry ABSOLUTE_CLI --motion-duration 0.6` 및 별도 destination의 `--motion-duration 24`. source check/하드자막/전체 decode와 처음·중간·끝 그림을 확인한다.

유료 요청0, 게시없음, live_audio=unverified. 기술 검사를 실제 음성/학습 품질 승인으로 사용하지 않는다. fixture source hash 불변.

## 결과 원문

```json
{
  "static": {
    "technical_complete": true,
    "motion_duration": 0.6,
    "metrics": [
      {
        "workers": 2,
        "seconds": 20.276809750008397,
        "frames": 1800,
        "frame_hash": "784d790c805e2d12c96d7d31b85c05f3b63f9128270790e46e4fefad5e9dcc62",
        "pcm_hash": "db03bc4983b200338fd844d04251fd31dcef6f239dcdfc22b74872980914b4cb",
        "aac_hash": "5b256b66a8c433344084b06a3a958ba895bf363baa240f46bb531b173d4b1c08",
        "master_hash": "44254a0dc914bd3baf6208352033c1860f4e5052b35a2076accc1c6dc3383a38"
      },
      {
        "workers": 6,
        "seconds": 20.580884416995104,
        "frames": 1800,
        "frame_hash": "784d790c805e2d12c96d7d31b85c05f3b63f9128270790e46e4fefad5e9dcc62",
        "pcm_hash": "db03bc4983b200338fd844d04251fd31dcef6f239dcdfc22b74872980914b4cb",
        "aac_hash": "5b256b66a8c433344084b06a3a958ba895bf363baa240f46bb531b173d4b1c08",
        "master_hash": "44254a0dc914bd3baf6208352033c1860f4e5052b35a2076accc1c6dc3383a38"
      }
    ],
    "frames_equal": true,
    "pcm_equal": true,
    "aac_equal": true,
    "source_unchanged": true,
    "paid_requests": 0,
    "published": false,
    "live_audio": "unverified",
    "source_check": {
      "status": "passed",
      "evidence": [
        "verification/source-check-scene-atp.txt",
        "verification/source-check-scene-atp-b.txt",
        "verification/source-check-main.txt"
      ],
      "errors": []
    },
    "captioned_media": {
      "status": "passed",
      "errors": [],
      "probe": {
        "streams": [
          {
            "index": 0,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "High",
            "codec_type": "video",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "mime_codec_string": "avc1.640028",
            "width": 1920,
            "height": 1080,
            "coded_width": 1920,
            "coded_height": 1080,
            "has_b_frames": 2,
            "sample_aspect_ratio": "1:1",
            "display_aspect_ratio": "16:9",
            "pix_fmt": "yuv420p",
            "level": 40,
            "color_range": "tv",
            "color_space": "bt709",
            "color_transfer": "bt709",
            "color_primaries": "bt709",
            "chroma_location": "left",
            "field_order": "progressive",
            "is_avc": "true",
            "nal_length_size": "4",
            "id": "0x1",
            "r_frame_rate": "30/1",
            "avg_frame_rate": "30/1",
            "time_base": "1/15360",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 921600,
            "duration": "60.000000",
            "bit_rate": "61213",
            "bits_per_raw_sample": "8",
            "nb_frames": "1800",
            "extradata_size": 51,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "VideoHandler",
              "encoder": "Lavc63.1.102 libx264"
            }
          },
          {
            "index": 1,
            "codec_name": "aac",
            "codec_long_name": "AAC (Advanced Audio Coding)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_tag_string": "mp4a",
            "codec_tag": "0x6134706d",
            "mime_codec_string": "mp4a.40.2",
            "sample_fmt": "fltp",
            "sample_rate": "24000",
            "channels": 1,
            "channel_layout": "mono",
            "bits_per_sample": 0,
            "initial_padding": 1024,
            "id": "0x2",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/24000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 1440000,
            "duration": "60.000000",
            "bit_rate": "61496",
            "nb_frames": "1408",
            "extradata_size": 5,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "SoundHandler"
            }
          }
        ],
        "format": {
          "filename": "/Users/hyunjun_macbook_pro/.codex/worktrees/ml-render-performance/머신러닝기초/.superpowers/sdd/2026-10-11-ml-review-render-performance/static-corrected/captioned.mp4",
          "nb_streams": 2,
          "nb_programs": 0,
          "nb_stream_groups": 0,
          "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
          "format_long_name": "QuickTime / MOV",
          "start_time": "0.000000",
          "duration": "60.000000",
          "size": "969948",
          "bit_rate": "129326",
          "probe_score": 100,
          "tags": {
            "major_brand": "isom",
            "minor_version": "512",
            "compatible_brands": "isomiso2avc1mp41",
            "encoder": "Lavf63.1.102"
          }
        }
      },
      "decode_exit": 0,
      "decode_stderr": ""
    }
  },
  "dynamic": {
    "technical_complete": true,
    "motion_duration": 24.0,
    "metrics": [
      {
        "workers": 2,
        "seconds": 56.68753070800449,
        "frames": 1800,
        "frame_hash": "7f453d8da4292a3b012c7570a0ae7737e766f547865310be98ddd28ca21d8812",
        "pcm_hash": "db03bc4983b200338fd844d04251fd31dcef6f239dcdfc22b74872980914b4cb",
        "aac_hash": "5b256b66a8c433344084b06a3a958ba895bf363baa240f46bb531b173d4b1c08",
        "master_hash": "bd5dc4963ef896a5caf79feee8612f353be42898ebc0a78692ec40c80d0c9472"
      },
      {
        "workers": 6,
        "seconds": 39.92844383401098,
        "frames": 1800,
        "frame_hash": "7f453d8da4292a3b012c7570a0ae7737e766f547865310be98ddd28ca21d8812",
        "pcm_hash": "db03bc4983b200338fd844d04251fd31dcef6f239dcdfc22b74872980914b4cb",
        "aac_hash": "5b256b66a8c433344084b06a3a958ba895bf363baa240f46bb531b173d4b1c08",
        "master_hash": "bd5dc4963ef896a5caf79feee8612f353be42898ebc0a78692ec40c80d0c9472"
      }
    ],
    "frames_equal": true,
    "pcm_equal": true,
    "aac_equal": true,
    "source_unchanged": true,
    "paid_requests": 0,
    "published": false,
    "live_audio": "unverified",
    "source_check": {
      "status": "passed",
      "evidence": [
        "verification/source-check-scene-atp.txt",
        "verification/source-check-scene-atp-b.txt",
        "verification/source-check-main.txt"
      ],
      "errors": []
    },
    "captioned_media": {
      "status": "passed",
      "errors": [],
      "probe": {
        "streams": [
          {
            "index": 0,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "High",
            "codec_type": "video",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "mime_codec_string": "avc1.640028",
            "width": 1920,
            "height": 1080,
            "coded_width": 1920,
            "coded_height": 1080,
            "has_b_frames": 2,
            "sample_aspect_ratio": "1:1",
            "display_aspect_ratio": "16:9",
            "pix_fmt": "yuv420p",
            "level": 40,
            "color_range": "tv",
            "color_space": "bt709",
            "color_transfer": "bt709",
            "color_primaries": "bt709",
            "chroma_location": "left",
            "field_order": "progressive",
            "is_avc": "true",
            "nal_length_size": "4",
            "id": "0x1",
            "r_frame_rate": "30/1",
            "avg_frame_rate": "30/1",
            "time_base": "1/15360",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 921600,
            "duration": "60.000000",
            "bit_rate": "68909",
            "bits_per_raw_sample": "8",
            "nb_frames": "1800",
            "extradata_size": 51,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "VideoHandler",
              "encoder": "Lavc63.1.102 libx264"
            }
          },
          {
            "index": 1,
            "codec_name": "aac",
            "codec_long_name": "AAC (Advanced Audio Coding)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_tag_string": "mp4a",
            "codec_tag": "0x6134706d",
            "mime_codec_string": "mp4a.40.2",
            "sample_fmt": "fltp",
            "sample_rate": "24000",
            "channels": 1,
            "channel_layout": "mono",
            "bits_per_sample": 0,
            "initial_padding": 1024,
            "id": "0x2",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/24000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 1440000,
            "duration": "60.000000",
            "bit_rate": "61496",
            "nb_frames": "1408",
            "extradata_size": 5,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "SoundHandler"
            }
          }
        ],
        "format": {
          "filename": "/Users/hyunjun_macbook_pro/.codex/worktrees/ml-render-performance/머신러닝기초/.superpowers/sdd/2026-10-11-ml-review-render-performance/dynamic/captioned.mp4",
          "nb_streams": 2,
          "nb_programs": 0,
          "nb_stream_groups": 0,
          "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
          "format_long_name": "QuickTime / MOV",
          "start_time": "0.000000",
          "duration": "60.000000",
          "size": "1027733",
          "bit_rate": "137031",
          "probe_score": 100,
          "tags": {
            "major_brand": "isom",
            "minor_version": "512",
            "compatible_brands": "isomiso2avc1mp41",
            "encoder": "Lavf63.1.102"
          }
        }
      },
      "decode_exit": 0,
      "decode_stderr": ""
    }
  }
}
```

미디어·source-check·render receipts·그림은 이 worktree의 `.superpowers/렌더검증_제작자료/review/{static,static-corrected,dynamic}`에 보존한다. `static`은 처음의 x 이동 실험 실패를 포함하고 최종 수용 결과는 `static-corrected`/`dynamic`이다. CLI worker flag를 임시 제거한 mutation이 FAIL이고 원본 복원 후 CLI11 PASS여서 연결 회귀가 누락을 잡음을 확인했다.
