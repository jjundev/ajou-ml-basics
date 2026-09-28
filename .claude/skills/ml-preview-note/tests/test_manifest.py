import copy
import io
import json
from contextlib import redirect_stdout
import unittest

from _util import MINI_RUN

import preview_manifest as pm

BASE = json.loads((MINI_RUN / "manifest.json").read_text(encoding="utf-8"))


def errors_with(mutate):
    m = copy.deepcopy(BASE)
    mutate(m)
    return pm.validate(m)


class TestPreviewManifest(unittest.TestCase):
    def test_fixture_valid(self):
        self.assertEqual(pm.validate(BASE), [])
        self.assertEqual(pm.load(MINI_RUN / "manifest.json")["lecture"], "L99")

    def test_names(self):
        self.assertEqual(pm.note_name(BASE), "예습노트_L99_Mini_Preview.html")
        self.assertEqual(pm.fig_dir_name("L99"), "figures_L99")

    def test_missing_top_level_key(self):
        errs = errors_with(lambda m: m.pop("pdf"))
        self.assertTrue(any("manifest.pdf" in e for e in errs), errs)

    def test_bad_lecture(self):
        errs = errors_with(lambda m: m.update(lecture="L4"))
        self.assertTrue(any("manifest.lecture" in e for e in errs), errs)

    def test_stt_layer_rejected(self):
        errs = errors_with(lambda m: m["sections"][1]["topics"][0]["layers"].append("prof"))
        self.assertTrue(any("알 수 없는 레이어" in e for e in errs), errs)

    def test_concept_topic_needs_eli5_and_formal(self):
        errs = errors_with(lambda m: m["sections"][1]["topics"][0].update(layers=["eli5", "listen"]))
        self.assertTrue(any("eli5와 formal" in e for e in errs), errs)

    def test_slides_format(self):
        for bad in ("12", "s2-3", "s", ""):
            with self.subTest(slides=bad):
                errs = errors_with(lambda m: m["sections"][1]["topics"][0].update(slides=bad))
                self.assertTrue(any(".slides" in e for e in errs), errs)

    def test_s0_topic_may_omit_slides(self):
        self.assertEqual(errors_with(lambda m: m["sections"][0]["topics"][0].update(slides="")), [])
        errs = errors_with(lambda m: m["sections"][0]["topics"][0].update(slides="12"))
        self.assertTrue(any(".slides" in e for e in errs), errs)

    def test_section_ids_in_order(self):
        errs = errors_with(lambda m: m["sections"][0].update(id="s9"))
        self.assertTrue(any("s0이어야 함" in e for e in errs), errs)

    def test_topic_id_prefix(self):
        errs = errors_with(lambda m: m["sections"][1]["topics"][0].update(id="s0-mean"))
        self.assertTrue(any("s1-로 시작" in e for e in errs), errs)

    def test_last_section_needs_cheatsheet_and_links(self):
        errs = errors_with(lambda m: m["sections"][2]["topics"].pop(0))
        self.assertTrue(any("s2-cheatsheet" in e for e in errs), errs)

    def test_single_section_rejected(self):
        errs = errors_with(lambda m: m.update(sections=m["sections"][:1]))
        self.assertTrue(any("2개 이상" in e for e in errs), errs)

    def test_supp_on_summary_topic_rejected(self):
        errs = errors_with(lambda m: m["sections"][2]["topics"][0].update(supp=True))
        self.assertTrue(any(".supp" in e for e in errs), errs)

    def test_link_to_unknown_topic(self):
        errs = errors_with(lambda m: m["links"].append({"topic": "s7-x", "href": "#a"}))
        self.assertTrue(any("없는 토픽" in e for e in errs), errs)

    def test_cli_ok(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = pm.main([str(MINI_RUN / "manifest.json")])
        self.assertEqual((code, out.getvalue().strip()), (0, "OK"))
