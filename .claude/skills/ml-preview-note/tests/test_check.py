from contextlib import redirect_stdout
import io
from pathlib import Path
import shutil
import tempfile
import unittest

from _util import MINI_RUN

import preview_assemble as pa
import preview_check as pc
import preview_manifest as pm


class TestPreviewCheck(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.run = self.tmp / "run"
        shutil.copytree(MINI_RUN, self.run)
        self.m = pm.load(self.run / "manifest.json")

    def tearDown(self):
        self._tmp.cleanup()

    def patch(self, sid, old, new):
        p = self.run / "sections" / f"{sid}.html"
        text = p.read_text(encoding="utf-8")
        self.assertIn(old, text)
        p.write_text(text.replace(old, new, 1), encoding="utf-8")

    def problems(self):
        note = pa.assemble(self.run, self.tmp / "out")
        return pc.check_preview(self.m, note)

    def codes(self):
        return {(p.code, p.where) for p in self.problems()}

    def test_fixture_passes(self):
        self.assertEqual(self.problems(), [])

    def test_missing_required_term(self):
        self.patch("s1", r"$\sigma^2 = ", "$s = ")
        self.assertIn(("missing-term", "s1-var"), self.codes())

    def test_slide_tag(self):
        self.patch("s1", "L99 s2–3", "L99 s2")
        self.assertIn(("slide-tag", "s1-mean"), self.codes())

    def test_supp_label(self):
        self.patch("s1", "교과서 보충", "보충")
        self.assertIn(("missing-supp", "s1-var"), self.codes())

    def test_stt_layer(self):
        self.patch("s1", '<div class="layer listen">',
                   '<div class="layer prof"><span class="layer-title">교수님 말씀</span><p>가</p></div><div class="layer listen">')
        self.assertIn(("stt-layer", "s1-mean"), self.codes())

    def test_eli5_sentences(self):
        self.patch("s1", "평균은 시소의 무게중심이에요.", "평균은 시소의 무게중심이에요. 두 번째 문장이에요. 세 번째 문장이에요.")
        self.assertIn(("eli5-long", "s1-mean"), self.codes())

    def test_figcaption_not_counted_as_sentence(self):
        self.patch("s1", "평균은 시소의 무게중심이에요.", "평균은 시소의 무게중심이에요. 두 번째 문장이에요.")
        self.assertNotIn(("eli5-long", "s1-mean"), self.codes())

    def test_eli5_sentences_without_periods(self):
        self.patch("s1", '<p class="lead">평균은 시소의 무게중심이에요.</p>',
                   '<p class="lead">첫 문장이에요</p><p>둘째 문장이에요</p><p>셋째예요</p>')
        self.assertIn(("eli5-long", "s1-mean"), self.codes())

    def test_inline_markup_does_not_split_sentence(self):
        self.patch("s1", "평균은 시소의 무게중심이에요.", "평균은 0.<b>5</b>예요. 둘째 문장이에요.")
        self.assertNotIn(("eli5-long", "s1-mean"), self.codes())

    def test_slide_tag_exact_match(self):
        self.patch("s0", "L99 s1</span>", "L99 s12</span>")
        self.assertIn(("slide-tag", "s0-vector"), self.codes())

    def test_s0_topic_without_slides(self):
        self.m["sections"][0]["topics"][0]["slides"] = ""
        self.patch("s0", '<div class="tags"><span class="tag slide">L99 s1</span></div>', "")
        self.assertEqual(self.problems(), [])

    def test_listen_items(self):
        self.patch("s1", "<li>무게중심 비유가 나오면 위 식과 연결해 보세요.</li>", "<li>가</li><li>나</li><li>다</li>")
        self.assertIn(("listen-long", "s1-mean"), self.codes())

    def test_topic_too_long(self):
        self.patch("s0", "열벡터예요.</p>", "열벡터예요.</p><p>" + "가" * 700 + "</p>")
        self.assertIn(("topic-long", "s0-vector"), self.codes())

    def test_math_not_counted(self):
        self.patch("s0", "열벡터예요.</p>", "열벡터예요.</p><p>$$" + "x_n + " * 300 + "x$$</p>")
        self.assertNotIn(("topic-long", "s0-vector"), self.codes())

    def test_summary_panel_not_counted(self):
        self.patch("s0", '<p class="sum-lead">벡터는 숫자 묶음이에요.</p>', '<p class="sum-lead">' + "가" * 700 + "</p>")
        self.assertNotIn(("topic-long", "s0-vector"), self.codes())

    def test_helpers(self):
        self.assertEqual(pc.visible_chars("가 나 $x^2$ $$y$$ 다"), 3)
        self.assertEqual(pc.sentences(" 하나예요. 둘이에요? 셋 "), 3)
        self.assertEqual(pc.sentences("값은 0.5예요."), 1)

    def test_cli(self):
        note = pa.assemble(self.run, self.tmp / "out")
        with redirect_stdout(io.StringIO()):
            code = pc.main(["--manifest", str(self.run / "manifest.json"), "--note", str(note)])
        self.assertEqual(code, 0)
