# 정리노트에 인터렉티브 자료 연결

## 연결할 곳 고르기

정리노트 HTML의 설명과 자료의 제목·모드·단계·관찰 가능한 장면을 읽는다. 단어 일치만으로 연결하지 않는다. 같은 폴더의 대응 노트가 기본이고, 다른 폴더 연결은 그 설명과 자료가 실제로 맞을 때만 한다. 여러 노트가 있으면 실제로 대응하는 노트만 선택한다.

관련 `article.topic` 또는 `section`의 고유 ID를 `sectionId`로 쓴다. 기본 삽입 위치는 절 안 첫 `.layer.formal` 뒤, 없으면 첫 `.layer.eli5` 뒤, 둘 다 없으면 제목 뒤다. 다른 설명·그림·위젯 바로 뒤가 더 적절하면 그 블록의 기존 고유 ID를 `anchorId`로 지정한다. 블록은 닫는 태그가 있는 div/figure 등의 컨테이너여야 한다. 원본에 새 ID를 추가하지 않는다.

안내는 한 문장으로 **어떤 과정을 재생하거나 무엇을 비교·조작할지** 말한다. 예: `데이터 개수와 사전분산에 따른 사후분포 변화를 ` + `사전분포와 사후분포 실험` 링크 + `에서 비교해 보세요.`. 실제로 없는 조작 기능은 안내하지 않는다. 페이지 끝 목록이나 숨긴 요약 블록에만 연결하지 않는다.

## 명세와 실행

`RUN/note-links.json`은 노트별로 모은 UTF-8 JSON이다. 경로는 실제 절대 경로를 사용하고 Windows에서는 역슬래시를 JSON에서 이스케이프하거나 `/`로 쓴다. 아래 경로는 자신의 `noteHtml`과 `save.cjs` 출력의 `html` 실제 경로로 교체한다.

```json
{
  "notes": [{
    "note": "/absolute/정리노트.html",
    "links": [{
      "sectionId": "s1-match",
      "html": "/absolute/인터렉티브_01_사전분포와_사후분포.html",
      "label": "사전분포와 사후분포 실험",
      "before": "데이터 개수와 사전분산에 따른 사후분포 변화를 ",
      "after": "에서 비교해 보세요."
    }]
  }]
}
```

- `note`: resolve의 `noteHtml`에서 고른 기존 노트의 실제 경로.
- `html`: 검증·저장한 자료의 실제 경로. 기존 자료 연결 요청에서는 기존 파일 경로.
- `sectionId`: 설명이 있는 article/section의 고유 ID.
- `anchorId`: 선택 사항. 같은 절 안의 블록 ID로 삽입 위치를 지정한다.
- `before`, `label`, `after`: 일반 텍스트. 도구가 HTML 이스케이프한다.

```bash
node "$SKILL/scripts/link-notes.cjs" "$RUN/note-links.json" --dry-run
node "$SKILL/scripts/link-notes.cjs" "$RUN/note-links.json"
```

새 링크는 노트 기준 상대 경로를 세그먼트별 URL 인코딩하고 `target="_blank" rel="noopener noreferrer"`를 쓴다. 안내 문장은 자연스럽게 마무리하고 `(새 탭)` 같은 표시 문구는 붙이지 않는다. `data-ml-interactive` 표식으로 안내를 식별하며 재실행 시 같은 절의 같은 목적지 링크를 중복하지 않는다. 기존 목적지 링크가 해당 절 안에 있으면 문구를 유지하고 새 탭 속성만 보정한다. 다른 절·페이지 끝 링크는 해당 절의 안내를 대체하지 않는다.

## 결과와 실패

출력은 `{notes:[{note, changed, results:[{sectionId,html,status,reason?}]}]}`이다.

| status | 의미 |
|---|---|
| added | 설명 뒤 안내·링크 추가 |
| updated | 기존 링크의 새 탭 속성 보정 |
| unchanged | 같은 절의 링크가 이미 올바름 |
| skipped | 연결하지 않고 reason 보고 |

`NOTE_MISSING`, `TARGET_MISSING`, `TARGET_INVALID`, `LINK_INVALID`, `SECTION_MISSING`, `SECTION_AMBIGUOUS`, `SECTION_INVALID`, `ANCHOR_MISSING`, `ANCHOR_AMBIGUOUS`, `ANCHOR_INVALID`는 해당 연결만 건너뛴다. 자료를 삭제하거나 문맥이 다른 곳에 연결하지 않는다. JSON 문법·명세 형식 오류나 파일 쓰기 실패는 종료 코드 1이다. 실패한 쓰기는 경로·권한을 확인하고 같은 명세로 재시도한다.

노트가 없거나 대응 절을 결정할 수 없는 자료는 명세에 억지로 넣지 않고 보고에 이유를 적는다. dry-run은 디스크를 수정하지 않는다. 실제 실행 후 모든 링크의 파일 존재를 확인하고 다시 실행해 `changed: false`를 확인한다. 브라우저에서 안내 문맥과 새 탭 열기·원래 노트 유지를 검증한다.

## 기존 자료 연결

연결만 요청했을 때는 생성·검토·저장 절차로 새 번호를 만들지 않는다. 요청한 날짜·주제·전체 범위의 기존 노트와 자료를 읽고 위 명세를 만들어 실행한다. 전체 요청에서는 `복습노트/` 아래 기존 `인터렉티브_*.html`·`3D모형_*.html`가 모두 연결되었거나 연결 불가 이유가 보고되었는지 대조한다.


## 저장된 명세와 재연결

각 .pack/자료_인터렉티브_NN_이름/note-links.json은 {v:1,links:[{note,html,sectionId,label,before,after,anchorId?}]}다. note/html은 repo-relative forward slash 경로다. 절대 경로와 저장소 밖 경로는 거절한다. relink.cjs REPO 날짜/주제/전체 [--dry-run]는 해당 날짜만 복원하며 metadata 없는 자료는 NO_LINK_METADATA, 깨진 JSON은 METADATA_INVALID로 보고한다.
link-notes CLI의 RUN manifest는 {notes:[{note:absolute,links:[...]}]}다. 이 runtime 명세와 저장 명세를 혼동하지 않는다. 실제 쓰기는 옆의 UUID 임시 파일에 exclusive write→rename이며 실패하면 원 노트 bytes를 유지하고 임시 파일을 제거한다.
