import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from _util import MINI_RUN

import assemble
import check_html


class TestPrimitives(unittest.TestCase):
    def test_adjacent_inline_math_in_list_items_is_not_display_math(self):
        doc = check_html.parse_html('<html lang="ko"><body><ol><li>$a$</li><li>$b$</li></ol></body></html>')
        self.assertEqual(check_html.math_delimiter_errors(doc.body_text), [])

    def test_unbalanced_inline_math(self):
        self.assertEqual(check_html.math_delimiter_errors("a $x b"), ["unbalanced $ (inline math)"])

    def test_widget_without_static(self):
        src = '<html lang="ko"><body><div class="widget" id="w1"><h4>x</h4></div></body></html>'
        problems = check_html.check_common(check_html.parse_html(src), src, Path("x.html"))
        self.assertEqual([p.code for p in problems], ["widget-static-missing"])

    def test_leftover_slot_and_external(self):
        src = '<html lang="ko"><head><script src="https://cdn.tailwindcss.com"></script></head><body>{{TOC}}</body></html>'
        codes = sorted(p.code for p in check_html.check_common(check_html.parse_html(src), src, Path("x.html")))
        self.assertEqual(codes, ["external", "leftover-slot"])


class TestPack(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.run = self.tmp / "run"
        shutil.copytree(MINI_RUN, self.run)
        self.m = json.loads((self.run / "manifest.json").read_text(encoding="utf-8"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def codes(self):
        note, review = assemble.assemble(self.run, self.tmp / "out")
        return sorted(p.code for p in check_html.check_pack(self.m, note, review))

    def edit(self, rel: str, old: str, new: str):
        path = self.run / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def test_mini_pack_passes(self):
        self.assertEqual(self.codes(), [])

    def test_missing_required_term(self):
        self.edit("sections/s1.html", "무게중심", "가운데")
        self.assertEqual(self.codes(), ["missing-term"])

    def test_forbidden_term_outside_preview(self):
        self.edit("sections/s1.html", "분산은 흩어진 정도예요.", "분산은 d-separation과 무관해요.")
        self.assertEqual(self.codes(), ["forbidden-term"])

    def test_missing_layer(self):
        self.edit("sections/s1.html", '<div class="layer prof"><span class="layer-title">🎙️ 교수님 한마디</span><p>"평균부터 봐요." (0101 01:00)</p></div>', "")
        self.assertEqual(self.codes(), ["missing-layer"])

    def test_missing_supp_badge(self):
        self.edit("sections/s1.html", '<span class="badge supp">📎 보충 · 수업 미유도</span>', "")
        self.assertEqual(self.codes(), ["missing-supp"])

    def test_card_anchor_and_source(self):
        self.edit("cards/p1.html", "{{NOTE_HREF}}#s1-mean", "{{NOTE_HREF}}#s1-var")
        self.edit("cards/p1.html", 'data-source="MML Example 6.1"', 'data-source="MML Ex 6.1"')
        self.assertEqual(self.codes(), ["card-anchor", "card-source"])

    def test_card_missing_hint(self):
        self.edit("cards/p1.html", '<details class="hint"><summary>💡 힌트</summary>더해서 개수로 나눈다.</details>', "")
        self.assertEqual(self.codes(), ["card-parts"])

    def test_widget_static_required(self):
        self.edit("sections/s1.html", 'class="widget-static"', 'class="widget-snap"')
        self.assertEqual(self.codes(), ["widget-static-missing"])

    def test_cli_exit_codes(self):
        note, review = assemble.assemble(self.run, self.tmp / "out")
        args = ["--manifest", str(self.run / "manifest.json"), "--note", str(note), "--review", str(review)]
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(check_html.main(args), 0)
            self.assertEqual(check_html.main([str(note), str(review)]), 0)
            note.write_text(note.read_text(encoding="utf-8").replace('lang="ko"', 'lang="en"'), encoding="utf-8")
            self.assertEqual(check_html.main(args), 1)
        self.assertIn("[lang]", out.getvalue())


if __name__ == "__main__":
    unittest.main()
