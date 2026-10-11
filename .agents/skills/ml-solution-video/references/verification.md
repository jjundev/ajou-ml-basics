# 검증과 보존 게시

verify는 content/math/lesson·전체 페이지 exact-zero 게이트·실측 timeline·page seek·writing/teaching/flow·pacing·HyperFrames·최종 media·전체 SRT·chunk sync와 audio/visual 의미 근거를 검사한다. font/runtime/자산/vendor/code/원문/PCM/trim/대본/출력 SHA에 묶는다. 오래된 검토로 새 결과를 승인하지 않는다.

generic browser는120초, dense teaching만600초다. 모든 원문 공개/주석·완료 chunk probe·forward/back/GSAP oracle을 유지하며 probe를 빼서 timeout을 숨기지 않는다. 픽셀·기하 검사와 실제 의미 검토는 별도다. 최종 media는1920×1080/30fps/24kHz·frame count·A/V 시간·decode를 확인하고 자막 전/후를 대조한다. SRT의 번호·전체 text/개행·실측 시각이 기대값과 같아야 한다. libass box는 WrapStyle2/BorderStyle4/Outline0/Shadow4/FontSize14/MarginV14다.

verification/audio-review.json은 실제 전청크와 최종 MP4를 청취한 경우에만 `{status:passed,mode:live-listened,input_hash,notes,evidence:{relative_path:SHA},chunk_checks:[...]}`다. chunk_checks는 실제 순서대로 segment_id/chunk_id/transcript_match/no_instruction_speech/natural_join/sync_passed/notes를 넣고 네 boolean은 모두true여야 한다. 기계적 sync나 synthetic PCM은 듣기 근거가 아니다. visual-review는 current hash/status/notes/evidence를 포함하고 실제 원본·중간·완성·전환·자막을 대조한다.

청취가 불가능하면 complete=false/live_audio=unverified이며 검토용 영상/기술 보고서만 전달한다. publish/latest는 금지된다. 실제 음성 요청의 key/비용/provider 가용성을 캐시나 설정으로 확인됐다고 표현하지 않는다.

source/inputs→layers→script→voice→timing→composition→render→captions→verify→publish의 fingerprint와 출력 SHA를 state.json에 기록한다. resume-set은 처음 무효인 단계를 반환한다. 수정된 단계부터 다시 실행하고 성공 형제·raw WAV·이전 finals를 지우지 않는다. caption만 수정해도 검토는 갱신하지만 동일 text 음성 cache는 재사용한다.

publish-set은 현재 complete report와 실제 audio/visual 근거·final SHA를 확인하고 안전한 파일명을 만든다. 날짜 범위는 날짜 prefix, 여러 팩은 slug prefix로 충돌을 피한다. `문제풀이영상/<선택범위>/`에는 문항별 MP4와 `<선택범위>_제작자료/`를 둔다. 과제1은 `문제풀이영상/과제1/`이며, 검토용 MP4도 이 폴더에 놓고 미검수 상태를 기록한다. 내부 catalog/README·스냅샷·검토·사용량·cache·이전 버전은 제작자료에 둔다. 성공 문항만 게시하고 실패 형제/기존 파일을 보존한다. 전체 성공만 latest 갱신한다. 교체 journal/backups로 일반 실패를 롤백하며 강제 종료의 원자적 다중 파일 commit을 주장하지 않는다.

회귀 실행:
```bash
PYTHONPATH="$S/scripts:$S/tests" python3 -m unittest discover -s "$S/tests" -v
node "$S/tests/test_writing_runtime.cjs"
node "$S/tests/test_teaching_runtime.cjs"
python3 "$S/tests/ml_acceptance.py" --repo "$REPO" --dest "$SCRATCH" --hyperframes-entry "$HYPERFRAMES"
```
마지막 명령은 실제1007 P2/P3/P8의 고정 source를 scratch에서 사용한다. 기본 synthetic/paid0/completefalse이며 production 게시를 하지 않는다. --live는 실제 음성 실행을 요청받은 경우만 사용하며 청취 승인을 자동으로 쓰지 않는다. 원문은 전후 SHA로 보존을 확인한다. skip/실음성 미검증을 통과 수에 포함하지 않는다.

멀티코어 검증은 workers 2/6의 모든 decoded frame MD5, PCM, AAC와 원자료 SHA를 비교한다. synthetic PCM 결과는 실제 음성 승인과 분리한다. 작업자 설정 변경 시 음성/타임라인 hash 유지, 실패/중단 시 이전 미디어와 기록 보존 및 rollback 잔여 시 재시도 차단을 확인한다. 실행 시간 개선과 저하 모두 기록한다.
