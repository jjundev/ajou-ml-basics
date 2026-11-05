# 기존 인터랙티브 연결 복원

기본 팩 발행 및 문제설명 처리 뒤, ml-interactive/scripts/relink.cjs와 날짜의 .pack/자료_인터렉티브_*/가 있을 때 실행한다. 신규 자료는 자동 생성하지 않는다.

```powershell
node .agents/skills/ml-interactive/scripts/relink.cjs REPO '1014' --dry-run
node .agents/skills/ml-interactive/scripts/relink.cjs REPO '1014'
node .agents/skills/ml-interactive/scripts/relink.cjs REPO '1014'
```

REPO와 날짜/range는 실제 대상으로 바꾼다. dry-run으로 문맥을 확인한 뒤 적용하고 재실행은 unchanged여야 한다. 링크는 `target="_self"`로 현재 탭에서 연다. 새 링크에는 `rel`을 추가하지 않고 기존 링크의 `rel`과 그 밖의 속성은 보존한다. PC·모바일에서 링크 클릭으로 현재 탭의 목적지에 이동하고 뒤로 가기로 정리노트에 돌아오는지, 안내가 보이는지 확인한다. SECTION_MISSING은 새 설명을 읽고 metadata를 갱신하거나 구체적 skipped로 보고한다. NO_LINK_METADATA는 기존 자료 내용을 읽어 명세부터 작성한다. 페이지 끝에 임의로 붙이지 않는다. 미설치·자료 없음은 기본 팩 성공을 막지 않는다. 오류를 문제설명 검토와 분리해 보고한다. 링크 때문에 html2md.py를 재실행하지 않는다.
