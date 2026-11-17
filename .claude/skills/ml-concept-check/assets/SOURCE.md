# 자구알 원본

고정한 자구알 커밋은 `2b384389fd3a88c99c6a6d951903736196ebd63c`이다.

| 원본 (자구알 저장소 상대 경로) | 파일 | SHA-256 |
|---|---|---|
| `.agents/skills/ds-review-pack/assets/review-template.html` | `review-template.html` | `a4ab46b5dd70f6d50748f6b47ffa11a17eb7a7aa4124fb07d2bc06e1b4cbacab` |
| `.agents/skills/ds-concept-check/assets/review-interaction.css` | `review-interaction.css` | `5700e02b9a686b4c2af0b00a3deee81a8531a52c5c1bd2ec5f1e6bb1e44ab37f` |
| `.agents/skills/ds-concept-check/assets/review-interaction.js` | `review-interaction.js` | `654facf47d19f68f4c0e9ed5a87b03333c9d70aedfe17e15353fae22fcbb20f5` |
| `.agents/skills/ds-concept-check/assets/review-prompt.js` | `review-prompt.js` | `344d3a7bc4ffad6eb84c9e2fa6951185de42a6feb28d2ce5a9793d203606ef45` |

템플릿에는 문제 목록의 채점 아이콘 변경을 반영했다. 원본 템플릿의 SHA-256은 `345324b7d1cdcbfadd2e538c4a871d92597bbceb946abbb7bf793d95b68b5a93`이다. 나머지 세 파일은 원본과 같다. 빌드 시 자구알의 슬롯 채우기와 상호작용 연결을 적용하며, 글꼴과 수식은 ML 저장소의 공용 `assets/vendor` 경로에서 읽는다. `quiz_interaction.py`, `quiz_render.py`, `blind.py`, `browser_check.py`는 자구알의 동작을 ML 입력 경로와 문항 규칙에 맞춰 연결한다.

복기창은 원본 모듈로 열고, ML 연결 코드에서 복사되는 제목·튜터 과목명·자료명을 설정한다. 자동 복사와 수동 복사에서 같은 문구를 사용한다.
