"""One-off: derive the two page templates from the finished 0909-0916 HTML heads.
Usage: python3 build_templates.py <복습노트 dir> <assets out dir>
"""
import os
import re
import sys
import unicodedata

src_dir, out_dir = sys.argv[1], sys.argv[2]
files = {unicodedata.normalize("NFC", f): f for f in os.listdir(src_dir)}


def head_of(name):
    text = open(os.path.join(src_dir, files[name]), encoding="utf-8").read()
    head = text[: text.index("</style>")]
    head = re.sub(r"<title>.*?</title>", "<title>{{PAGE_TITLE}}</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="{{DESCRIPTION}}">', head)
    return head.rstrip() + "\n    [hidden] { display: none !important; }\n  </style>\n</head>\n"


NOTE_BODY = """<body>
  <header class="topbar">
    <div class="topbar-inner">
      <strong>🧸 머러기 정리노트</strong>
      <nav class="toc" aria-label="목차">{{TOC}}</nav>
    </div>
  </header>
  <main>
    <div class="hero">
      <h1>{{TITLE}}</h1>
      <p>{{SUBTITLE}}</p>
      <div class="legend-bar">
        <span class="badge">🧸 쉬운 비유</span><span class="badge">📐 정식 버전</span><span class="badge">🎙️ 교수님 한마디</span>
        <span class="badge">⚠️ 강조 포인트</span><span class="badge supp">📎 보충 · 수업 미유도</span>
      </div>
    </div>
{{SECTIONS}}
  </main>
  <footer>{{FOOTER}}</footer>
{{SCRIPTS}}
</body>
</html>
"""

REVIEW_BODY = """<body>
  <header class="topbar">
    <div class="topbar-inner">
      <strong>📝 머러기 복습문제</strong>
      <nav class="toc" aria-label="목차">{{TOC}}<a href="{{NOTE_HREF}}">정리노트로 ↗</a></nav>
    </div>
  </header>
  <main>
    <div class="hero">
      <h1>{{TITLE}}</h1>
      <p>{{INTRO}}</p>
      <p class="progress">풀었음 <b id="progress-count">0</b> / {{TOTAL}}</p>
    </div>
{{PARTS}}
  </main>
  <footer>{{FOOTER}}</footer>
{{SCRIPTS}}
  <script id="progress-ui">
    (function () {
      const KEY = 'mlb-review-{{RANGE}}-done';
      let saved = {};
      try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { saved = {}; }
      const boxes = Array.from(document.querySelectorAll('input[data-done]'));
      const update = () => { document.getElementById('progress-count').textContent = String(boxes.filter((b) => b.checked).length); };
      boxes.forEach((b) => {
        b.checked = Boolean(saved[b.dataset.done]);
        b.addEventListener('change', () => {
          saved[b.dataset.done] = b.checked;
          try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) { /* 저장 불가 환경: 무시 */ }
          update();
        });
      });
      update();
    })();
  </script>
</body>
</html>
"""

os.makedirs(out_dir, exist_ok=True)
for name, out, body in (
    ("정리노트_0909-0916_When_Models_Meet_Data.html", "note-template.html", NOTE_BODY),
    ("복습문제_0909-0916_When_Models_Meet_Data.html", "review-template.html", REVIEW_BODY),
):
    with open(os.path.join(out_dir, out), "w", encoding="utf-8") as f:
        f.write(head_of(name) + body)
    print(out)
