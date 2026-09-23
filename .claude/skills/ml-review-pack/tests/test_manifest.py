import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

from _util import FIXTURES, MINI_RUN

import manifest


def mini() -> dict:
    return json.loads((MINI_RUN / "manifest.json").read_text(encoding="utf-8"))


class TestManifest(unittest.TestCase):
    def test_mini_manifest_is_valid(self):
        self.assertEqual(manifest.validate(mini()), [])

    def test_regression_manifest_is_valid(self):
        manifest.load(FIXTURES / "manifest-0909-0916.json")

    def test_missing_top_level_key(self):
        m = mini()
        del m["problems"]
        self.assertIn("manifest.problems: list 필요", manifest.validate(m))

    def test_bad_range_and_slug(self):
        m = mini()
        m["range"], m["slug"] = "9/21", "한글"
        errors = manifest.validate(m)
        self.assertTrue(any(e.startswith("manifest.range") for e in errors))
        self.assertTrue(any(e.startswith("manifest.slug") for e in errors))

    def test_problem_anchor_must_be_topic(self):
        m = mini()
        m["problems"][0]["anchor"] = "s9-nope"
        self.assertIn("problems[0].anchor: 없는 토픽: s9-nope", manifest.validate(m))

    def test_duplicate_id(self):
        m = mini()
        m["sections"][0]["topics"][1]["id"] = "s1-mean"
        self.assertTrue(any("중복 id: s1-mean" in e for e in manifest.validate(m)))

    def test_unknown_layer(self):
        m = mini()
        m["sections"][0]["topics"][0]["layers"].append("fun")
        self.assertTrue(any("알 수 없는 레이어" in e for e in manifest.validate(m)))

    def test_preview_topic_must_exist(self):
        m = copy.deepcopy(mini())
        m["preview_topic"] = "s9"
        self.assertIn("preview_topic: 토픽 id가 아님: s9", manifest.validate(m))

    def test_load_raises_on_invalid(self):
        m = mini()
        m["parts"] = []
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(json.dumps(m, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(manifest.ManifestError) as cm:
                manifest.load(path)
        self.assertIn("problems[0].part: 없는 part: partA", str(cm.exception))

    def test_cli(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(manifest.main([str(MINI_RUN / "manifest.json")]), 0)
        self.assertEqual(out.getvalue().strip(), "OK")

    def test_non_dict_top_level(self):
        for value in ([], "x", 3, None):
            self.assertEqual(manifest.validate(value), ["manifest: JSON 객체 필요"])

    def test_non_dict_list_item_is_reported_and_skipped(self):
        m = mini()
        m["problems"].insert(0, "oops")
        m["sessions"].append(7)
        m["sections"][0]["topics"].append(None)
        errors = manifest.validate(m)
        self.assertIn("problems[0]: 객체 필요", errors)
        self.assertIn(f"sessions[{len(m['sessions']) - 1}]: 객체 필요", errors)
        self.assertTrue(any(e.endswith(": 객체 필요") and e.startswith("sections[0].topics[") for e in errors))

    def test_non_string_layer_is_reported(self):
        m = mini()
        m["sections"][0]["topics"][0]["layers"].append(["eli5"])
        self.assertTrue(any("layers" in e for e in manifest.validate(m)))

    def test_load_invalid_json_raises_manifest_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(manifest.ManifestError):
                manifest.load(path)
            with self.assertRaises(manifest.ManifestError):
                manifest.load(Path(tmp) / "missing.json")

    def test_cli_invalid_manifest_exits_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "manifest.json"
            bad.write_text("[]", encoding="utf-8")
            for arg in (bad, Path(tmp) / "missing.json"):
                with contextlib.redirect_stdout(io.StringIO()) as out, \
                        contextlib.redirect_stderr(io.StringIO()) as err:
                    self.assertEqual(manifest.main([str(arg)]), 1)
                self.assertTrue(out.getvalue().strip())
                self.assertNotIn("Traceback", out.getvalue() + err.getvalue())

    def test_cli_usage_exits_2(self):
        for argv in ([], ["a", "b"]):
            with contextlib.redirect_stdout(io.StringIO()), \
                    contextlib.redirect_stderr(io.StringIO()) as err:
                self.assertEqual(manifest.main(argv), 2)
            self.assertIn("사용법", err.getvalue())

    def test_term_lists_require_nonempty_strings(self):
        for bad in (0.2, 3, None, "", ["x"]):
            with self.subTest(bad=bad):
                m = mini()
                m["problems"][0]["terms"].append(bad)
                m["sections"][0]["topics"][0]["required_terms"].append(bad)
                m["forbidden_outside_preview"].append(bad)
                errors = manifest.validate(m)
                for where in ("problems[0].terms[", "sections[0].topics[0].required_terms[", "forbidden_outside_preview["):
                    self.assertTrue(any(e.startswith(where) and "빈 문자열이 아닌 문자열 필요" in e for e in errors), (where, errors))

    def test_quoted_number_term_is_valid(self):
        m = mini()
        m["problems"][0]["terms"].append("0.2")
        self.assertEqual(manifest.validate(m), [])

    def test_level_rejects_bool(self):
        for value in (True, False):
            with self.subTest(value=value):
                m = mini()
                m["problems"][0]["level"] = value
                self.assertIn("problems[0].level: int 필요", manifest.validate(m))

    def test_names(self):
        m = mini()
        self.assertEqual(manifest.note_name(m), "정리노트_0101-0102_Mini_Test.html")
        self.assertEqual(manifest.review_name(m), "복습문제_0101-0102_Mini_Test.html")
        self.assertEqual(manifest.fig_dir_name("0101-0102"), "figures_0101-0102")


if __name__ == "__main__":
    unittest.main()
