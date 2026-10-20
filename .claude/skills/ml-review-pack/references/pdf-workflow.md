# PDF stage workflow

이 절차는 HTML 카드와 정리노트가 `RUN/work/stage/복습노트/<range>/`에 있고 HTML/정답 검증이 끝난 뒤 실행한다. 4단계의 `review_pdf_stage.py`로 상대 경로 구조를 먼저 준비한다. 새 이미지도 이 날짜 stage 폴더의 `.pack/` 아래에 두고 상대 src로 참조한다. PNG 캡처는 원본 HTML 위치를 기준으로 읽는다. 날짜 stage 폴더에는 배포할 파일만 두고 임시 파일은 다른 RUN/work 하위에 둔다. 커밋·푸시는 별도 요청이 있을 때만 한다. 전자회로2 저장소를 실행 의존성으로 요구하지 않는다.

미분 수식이 있으면 `vector-derivative-convention.md`를 전체 읽고 조건·Hint·풀이·생성기 소개·원천 카드/JSON까지 관례를 확인한다. 변경된 원천에서 문제/답안 PDF를 모두 재생성하고 실제 전체 페이지에서 행벡터 식과 양변 전치 단계를 대조한다. HTML 본문만 수정했거나 수치 답만 같은 상태는 동기화 완료가 아니다. 원문 보존 분기는 해당 레퍼런스를 따른다.

```bash
python3 "$SKILL/scripts/build_review_pdf.py" --review "$RUN/work/stage/복습노트/<range>/<복습문제>.html" --build-dir "$RUN/work/pdf" --stage-only --layout video-16x9 --report "$RUN/work/pdf-validation.json"
```

기본 규격은 `video-16x9`: 1920×1080 CSS px, PDF 1440×810pt다. 하단 180px(마지막 135pt)은 완전히 흰 자막 여백이다. 같은 후보의 A4 fitting을 측정해 본문·풀이·display 수식·Hint 수식의 화면 배율을 보존하며, 분할 후보는 다시 측정한다. 임의 추가 축소는 하지 않는다. 명시적인 `--layout a4`는 기존 A4 가로 출력을 유지한다. `validation.json`의 layout·page_size_pt·caption_height_px·typography와 페이지 대응을 확인한다.

과제 PDF는 `--profile homework`로 만든다. 입력 파일명은 `과제<N>_<Slug>.html`, 카드 `data-source`는 `HW<N> Problem <k>`(카드 id `p<k>`와 번호 일치)이며, 출력은 `과제<N>_<Slug>-문제.pdf`/`-답안.pdf`, 배지는 `과제`, 제목은 `머신러닝기초 과제<N>`이다. 프로필을 생략하면 `review` 규칙이 적용되어 과제 파일명은 `invalid review filename`으로 실패한다.

템플릿 두 개와 video CSS는 EC2 `757fa081521008d46542e23d5a1a53112391aed2`의 고정 복사본이다. 실행 중 변경하지 말고 `assets/pdf-template-provenance.json`의 세 SHA256을 검사한다.

기존 비구조화 카드만 수동 `--layouts PATH`가 필요하다. layout의 `source_sha256`는 읽은 HTML bytes와 일치해야 하고 conditions+ask는 원문 문장·수식 순서를 보존해야 한다. 전체 render output 경로와 PDF 해시는 validation JSON에 있다. 실패는 종료코드 1이며 공개 파일을 쓰지 않는다.

다음 Python의 `RUN`, `SKILL`, `REPO`를 환경변수로 넣는다. PDF 쌍을 stage에 복사하고 노트와 manifest 링크를 갱신한다.

```python
import json, os, shutil, sys
from pathlib import Path
run, skill, repo = (Path(os.environ[k]) for k in ('RUN', 'SKILL', 'REPO'))
sys.path.insert(0, str(skill / 'scripts'))
from manifest import PACK_DIR, note_name, review_name, pdf_hrefs
from review_pdf_links import add_pdf_links
from review_pdf_cards import read_cards
from build_review_pdf import digest
m = json.loads((run / 'manifest.json').read_text())
e = json.loads((run / 'work/pdf-validation.json').read_text())
assert e['status'] == 'validated', 'PDF build failed'
stage = run / 'work/stage/복습노트' / m['range']
review = stage / review_name(m)
assert digest(review) == e['source_sha256'], 'stale source'
for mode in ('problems', 'answers'):
    src = Path(e['pdfs'][mode]['path'])
    assert digest(src) == e['pdfs'][mode]['sha256'], 'PDF changed'
    (stage / PACK_DIR).mkdir(exist_ok=True)
    shutil.copy2(src, stage / PACK_DIR / src.name)
note = stage / note_name(m)
note.write_text(add_pdf_links(note.read_text(), m['range'], m['slug'], len(read_cards(review).cards)))
# Use the existing links topic id from this manifest; never invent another topic.
links_topic = next(t['id'] for s in m['sections'] for t in s['topics'] if t['id'].endswith('-links'))
for href in pdf_hrefs(m['range'], m['slug']):
    if not any(link['topic'] == links_topic and link['href'] == href for link in m['links']):
        m['links'].append({'topic': links_topic, 'href': href})
(run / 'manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
```

```bash
python3 "$SKILL/scripts/check_html.py" --manifest "$RUN/manifest.json" --note "$RUN/work/stage/복습노트/<range>/<정리노트>.html" --review "$RUN/work/stage/복습노트/<range>/<복습문제>.html"
python3 "$SKILL/scripts/html2md.py" "$RUN/work/stage/복습노트/<range>/<정리노트>.html" "$RUN/work/stage/복습노트/<range>/<복습문제>.html" --check
```

마지막으로 PyMuPDF/pdftoppm으로 두 PDF의 **모든 페이지**를 PNG로 렌더링해서 검사한다. `validation.json`의 DOM 검사와 PDF 페이지 크기/텍스트 검사만으로 시각 검수를 대신하지 않는다. 기존 팩의 비율 변경은 review/정리노트 HTML·MD·그림과 링크를 보존하고 같은 이름의 PDF 쌍만 백업·교체한다. DOM 자막 경계와 PDF의 마지막 135pt에 텍스트·이미지·비백색 도형이 없는지 검증하고 전체 페이지에서 표·방향 그래프·행렬·긴 증명·Hint·필기 공간을 확인한다.

검수가 모두 통과한 새 팩은 다음으로 배포한다. 상대 경로를 그대로 유지하며 여섯 파일(HTML 2 + `.pack/`의 MD 2·PDF 2)과 그림 모두를 한 배포 요청에 넣는다.

```python
import os, sys
from pathlib import Path
run, skill, repo = (Path(os.environ[k]) for k in ('RUN', 'SKILL', 'REPO'))
sys.path.insert(0, str(skill / 'scripts'))
from manifest import PACK_DIR, load, note_name, review_name, pdf_names
from review_pdf_publish import publish_files
m = load(run / 'manifest.json')
stage = run / 'work/stage/복습노트' / m['range']
public = repo / '복습노트' / m['range']
names = [note_name(m), review_name(m), *(f'{PACK_DIR}/{n}' for n in (Path(note_name(m)).with_suffix('.md').name,
         Path(review_name(m)).with_suffix('.md').name, *pdf_names(m['range'], m['slug'])))]
files = [stage / n for n in names]
# Stage pack holds only deliverables and their local assets; scratch remains elsewhere.
files += [p for p in stage.rglob('*') if p.is_file() and p not in files]
publish_files({public / p.relative_to(stage): p for p in files}, run / 'work/backups')
```

`publish_files`는 모든 stage 파일을 먼저 확인하고 고유 백업 후 교체한다. 일부 교체 실패 시 기존 파일을 복구하고 새 파일을 제거한다. OS 수준의 다중 파일 원자성을 주장하지 않는다. 커널 lock이 같은 공개 폴더의 동시 배포를 막으며 descriptor가 닫히면 해제된다. 살아 있는 lock 파일을 삭제하지 않는다.
