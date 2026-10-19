# Source visual review

Reviewer: /root/summary (actual visual inspection plus current source.json comparison)
Status: pass

MML PDF 91 (book85) Example3.10, PDF93–94 (book87–88) Example3.11의 실제 페이지를 source-pages.png로 시각 확인했어요. Example3.10의 회색 상자는 투영행렬, 특정 벡터의 투영, 재투영 불변 설명까지 포함하며 그 뒤 eigenvector Remark는 상자 밖이에요. Example3.11의 회색 상자는 좌표, 투영, 오차, 행렬과 잔차 직교/P²=P 확인까지 포함해요. 원 예제의 상자 밖 정리나 새 질문을 가져오지 않았어요.

현재 source.json의 모든 조건 행렬·벡터를 work/problem-data.json의 허가된 수치변형과 원소별 대조했어요. p1/p5는 원 숫자이고 나머지는 같은 3차원/기저 열 개수를 유지한 수치변형이에요. a–c 또는 a–d 소문항은 원 상자 안의 계산과 확인을 문제로 바꾼 것이에요. source.json의 figures_html은 8문항 모두 비어 있으며 실제 원 카드도 별도 문항 그림이 없어요. 교과서의 본문 Figure3.11은 문항에 필수인 주어진 그림이 아니므로 누락된 조건이 아니에요.

| 문항 | 방향/기저 | 입력 | 소문항 | 대조 |
|---|---|---|---|---|
| p1 | [[1], [2], [2]] | [1, 1, 1] | a,b,c | 일치 |
| p2 | [[1], [0], [0]] | [2, 3, 1] | a,b,c | 일치 |
| p3 | [[0], [1], [0]] | [3, 2, 1] | a,b,c | 일치 |
| p4 | [[1], [1], [1]] | [3, 3, 3] | a,b,c | 일치 |
| p5 | [[1, 0], [1, 1], [1, 2]] | [6, 0, 0] | a,b,c,d | 일치 |
| p6 | [[1, 0], [0, 1], [0, 0]] | [2, 3, 4] | a,b,c,d | 일치 |
| p7 | [[1, 0], [1, 1], [1, 2]] | [0, 6, 0] | a,b,c,d | 일치 |
| p8 | [[1, 1], [2, 0], [0, 1]] | [1, 2, 3] | a,b,c,d | 일치 |

현재 source.json SHA256: f4bdbcb94bb2c5d4dbaf1510d780161c3bcc9310179c53420ac2ed4d580f0645

수치변형 자료 SHA256: 487b4ffa43cd72b05da6cf6503524730c3c1db4f095cc5bb904ad9175b255b9c

시각 근거: /tmp/ml-review-pack-20261019/1019/work/source-pages.png (MML PDF91,93–94 포함). 이번 검토는 원문·조건·소문항·그림 대조이며 해설 내용과 브라우저 검토를 대신하지 않아요.
