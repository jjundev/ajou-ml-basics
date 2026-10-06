# 머신러닝기초 복습문제 PDF 16:9 설계

## 의도와 확정 범위

전자회로2 `757fa081521008d46542e23d5a1a53112391aed2`의 복습문제 PDF 변경을 ML의 기존 생성 흐름에 적용한다. 분류는 bounded다. 사용자에게 제시한 결정 #1~#5를 유지한다. #6은 후속 writing-plans 호출에서 별도 변경이 없어 grill-yourself의 confirmed by default 규칙에 따라 **기존 PDF 14개 + 향후 생성 모두**로 확정한다. 구현 방법은 아직 선택하지 않았다.

현재 기준은 0909(5), 0914(7), 0916(6), 0921(6), 0923(7), 0928(8), 0930(8)의 47문항이다. 문제지 47쪽과 답안지 54쪽, 총 101쪽의 A4 가로 PDF 14개가 있다. 101쪽은 비교 기준이며 계속 페이지가 필요해졌을 때의 고정 상한은 아니다.

## 완료 동작과 제약

- 기본 복습팩 출력은 1920×1080 CSS px, PDF 1440×810pt의 16:9다.
- 하단 180px(900≤y≤1080)는 흰 자막 예약 영역이다. 텍스트·수식·그림·격자·Hint·제작자 표기를 넣지 않는다.
- EC2의 CSS를 그대로 적용한다: `.page` padding `32px 48px 204px`, 제작자 표기 bottom `190px`, Hint 폭 `144px`/수식 포함 `250px`.
- 화면 글자 크기 보정식은 `(900 / (210 * 72 / 25.4)) / (1920 / 1440)`이다. 기본 본문 10pt는 약 11.34pt가 된다. 비교 기준은 A4를 높이 900px에 맞춘 EC2 표시 관례이며 ML 영상의 현재 표시 동작을 확인했다는 뜻은 아니다.
- 제목·본문·Hint의 고정 pt 값에 같은 보정을 적용한다. 원래 A4 문항별 본문·풀이·display 수식·Hint 수식 축소 배율을 모드별·물리 페이지별로 측정하여 보존한다. 래스터 그림 속 글자는 CSS 보정 대상이 아니므로 별도 가독성 검수한다.
- 공개 생성 진입점 `build_pack`과 CLI 기본값은 `video-16x9`, 명시적 `--layout a4`는 호환한다. 저수준 `render_workbook`의 기존 호출 기본값은 A4로 유지한다.
- 기존 번호·순서·조건·구할 것·풀이·정답·출처를 보존한다. HTML·MD·그림149개의 bytes와 PDF 파일명·기존 노트 링크를 보존한다.
- 넘침은 기존 질문 블록/풀이 단계 경계에서 분할한다. 분할한 페이지에는 그 구성의 A4 배율을 다시 측정한다. 추가 임의 축소나 내용 삭제로 통과시키지 않는다.
- 기존 Chrome·폰트·이미지·KaTeX·DOM 경계 검사를 유지한다. 새 규격 및 자막 영역 검사와 전체 페이지 시각 검수를 추가한다.
- PDF 쌍을 stage에서 검증한 뒤 날짜별로 백업·교체한다. 실패한 날짜는 기존 PDF를 보존한다. OS 수준 다중 파일 원자성은 주장하지 않는다.
- EC2 템플릿·CSS를 해당 커밋에서 ML 내부에 고정 복사하고 SHA256과 출처를 기록한다. 실행 시 EC2 checkout을 요구하지 않는다.
- A4 인쇄용 사본을 추가 배포하지 않는다. 문제 내용 변경·영상 변경·교과서 연습문제 PDF 변경은 제외한다.
- 구현 시 worktree/동시 작업 상태를 다시 확인한다. 현재 분기는 `codex/ml-review-video`다. 사용자 별도 요청 없이 커밋·푸시·merge하지 않는다.

## 구성과 데이터 흐름

실제 스킬 소스는 `.claude/skills/ml-review-pack/`이며 `.agents/skills/ml-review-pack`는 그곳으로 연결된 symlink다. 변경은 실제 소스에만 한다.

`review_pdf_layout.py`가 규격·템플릿 로딩·고정 pt 보정을 담당한다. `review_pdf_render.py`는 기존 리소스 검증과 Chrome 렌더 경로를 공유하면서 A4 typography 측정, 선택 규격 렌더, 자막 침범 검사를 수행한다. `build_review_pdf.py`는 layout 인자를 전달하고 규격/자막 영역/PDF 쌍 검증 근거를 보고서에 기록한다.

흐름은 원본 카드 + 기존 layouts → normalize → 그림 캡처 → 모드별 페이지 후보 → 동일 후보의 A4 측정 → 16:9 렌더 및 경계 검사 → 필요 시 유한 분할·재측정 → 최종 PDF 검사 → validation JSON → 전체 페이지 시각 검수 → 기존 publisher로 날짜별 교체다. `review_pdf_payload.py`와 `review_pdf_pages.py`의 공개 API는 바꾸지 않는다.

## 검증과 오류

비교는 논리 문항 id 및 계속 페이지 대응으로 수행한다. 일반 본문·제목·Hint는 기존 표시 크기 대비 차이 0.1px 이하를 목표로 한다. 본문·풀이·수식에 원래 적용된 축소 배율도 같아야 한다. 모든 문자를 독립 글꼴 span에 대응시키기 어려우면 대응 불가 항목을 기록하고 수식 DOM 배율 대조와 시각 검수로 확인한다. 임의로 문자를 버려 검사를 통과시키지 않는다.

PDF의 마지막 135pt(하단 1/6)에 text bbox·그림 bbox·비백색 도형이 없어야 한다. 흰 배경은 허용한다. DOM의 panel/work/Hint/figure/수식 영역 검사도 유지하며 페이지 영역 및 자막 경계 검사를 보강한다. 무효 layout, 누락 typography 페이지, 리소스 실패, unsplittable overflow는 `ReviewPdfError`로 보고한다.

모든 14개 PDF를 검증하고 PNG로 전체 페이지를 검수한다. 특히 4×4 행렬, 확률표, 방향 그래프, 긴 증명, Hint 부록, 계속 페이지, 필기 공간을 확인한다. 스킬·예습노트·root Python 및 widget JS 회귀를 통과해야 한다. 기존 skip은 실행 통과 수로 세지 않는다.

## 근거

- EC2 `workbook/render.py:18-34`: 보정식과 CSS 주입.
- EC2 `workbook/templates/video-16x9.css:2-14`: 규격·여백·Hint·그림 규칙.
- EC2 `workbook/templates/answer.html:720-762`: 기존 typography 적용 순서.
- ML `scripts/review_pdf_render.py:108-130`: 현재 렌더 및 검증 경로.
- ML `scripts/build_review_pdf.py:22-59`: 현재 A4 검사·페이지 조립·보고서.
- ML `scripts/review_pdf_pages.py:49-75`: 유한 분할 계약.
- ML `tests/test_review_pdf_payload.py:31-37`: 이전 템플릿 SHA 고정 검사.

이번 파일은 설계 기록이다. 구현 승인은 아니다.
