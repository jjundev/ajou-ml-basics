"""출제 명세표 검사: 문제 구성이 기출의 요구 구조 목표를 채우는지, 못 채우면 이유가 있는지."""
import copy
import json
import unittest

import _util
from check_blueprint import check, exam_stats

BP = json.loads((_util.REPO / "시험결과" / "출제명세표.json").read_text(encoding="utf-8"))


def manifest(levels, dates=None):
    dates = dates or ["0101"] * len(levels)
    return {
        "sessions": [{"date": d} for d in sorted(set(dates))],
        "sections": [{"id": "s1", "topics": [{"id": "s1-mean"}, {"id": "s1-cov"}]},
                     {"id": "s2", "topics": [{"id": "s2-next"}, {"id": "s2-links"}]}],
        "preview_topic": "s2-next",
        "problems": [{"id": f"p{i + 1}", "level": lv, "date": d, "source": f"MML Exercise 6.{i + 1}"}
                     for i, (lv, d) in enumerate(zip(levels, dates))],
    }


def tags(n, asks=2, last="읽기", chained_ids=("p1",)):
    return {"problems": [{"id": f"p{i + 1}", "asks": asks, "last_ask": last, "chained": f"p{i + 1}" in chained_ids}
                         for i in range(n)], "gaps": {}}


GOOD_M = manifest([1, 1, 2, 2, 2, 2, 2, 2, 3, 3])


class TestExamBlueprint(unittest.TestCase):
    def test_midterm_stats_match_transcript_reading(self):
        s = exam_stats(BP["exams"][0])
        self.assertEqual(s["levels"], [3, 12, 5])
        self.assertEqual(s["chained"], 9)
        self.assertEqual(s["non_calc_last"], 12)
        self.assertEqual(s["lost"], 21)
        self.assertEqual(s["items"], 20)

    def test_every_count_has_level_table(self):
        for n in range(8, 13):
            self.assertEqual(sum(BP["targets"]["level_counts"][str(n)]), n)


class TestCheck(unittest.TestCase):
    def test_good_pack_passes(self):
        self.assertEqual(check(GOOD_M, tags(10), BP), [])

    def test_old_5_4_1_ratio_fails(self):
        errors = check(manifest([1] * 5 + [2] * 4 + [3]), tags(10), BP)
        self.assertTrue(any("levels" in e for e in errors), errors)

    def test_single_ask_majority_fails(self):
        errors = check(GOOD_M, tags(10, asks=1, chained_ids=()), BP)
        self.assertTrue(any("multi_ask" in e for e in errors), errors)

    def test_calc_only_endings_fail(self):
        errors = check(GOOD_M, tags(10, last="계산"), BP)
        self.assertTrue(any("non_calc_last" in e for e in errors), errors)

    def test_no_chained_card_fails(self):
        errors = check(GOOD_M, tags(10, chained_ids=()), BP)
        self.assertTrue(any("chained" in e for e in errors), errors)

    def test_date_without_level2_problem_fails(self):
        m = manifest([1, 1, 2, 2, 2, 2, 2, 2, 3, 3], ["0102", "0102"] + ["0101"] * 8)
        errors = check(m, tags(10), BP)
        self.assertTrue(any("dates" in e and "0102" in e for e in errors), errors)

    def test_session_without_any_problem_fails(self):
        m = copy.deepcopy(GOOD_M)
        m["sessions"].append({"date": "0103"})
        self.assertTrue(any("0103" in e for e in check(m, tags(10), BP)))

    def test_gap_reason_excuses_a_target(self):
        t = tags(10, chained_ids=())
        t["gaps"]["chained"] = "이번 범위 MML 예제에 이어지는 소문항으로 나눌 것이 없음"
        self.assertEqual(check(GOOD_M, t, BP), [])

    def test_empty_gap_reason_does_not_excuse(self):
        t = tags(10, chained_ids=())
        t["gaps"]["chained"] = " "
        self.assertTrue(check(GOOD_M, t, BP))

    def test_unknown_gap_key_fails(self):
        t = tags(10)
        t["gaps"]["typo"] = "이유"
        self.assertTrue(any("typo" in e for e in check(GOOD_M, t, BP)))

    def test_ids_must_match_manifest(self):
        t = tags(10)
        t["problems"].pop()
        self.assertTrue(any("p10" in e for e in check(GOOD_M, t, BP)))

    def test_unknown_last_ask_kind_fails(self):
        t = tags(10)
        t["problems"][0]["last_ask"] = "기타"
        self.assertTrue(any("last_ask" in e for e in check(GOOD_M, t, BP)))

    def test_chained_needs_two_asks(self):
        t = tags(10)
        t["problems"][0]["asks"] = 1
        self.assertTrue(any("p1" in e and "chained" in e for e in check(GOOD_M, t, BP)))

    def test_bool_is_not_an_ask_count(self):
        t = tags(10)
        t["problems"][3]["asks"] = True
        self.assertTrue(any("p4" in e and "asks" in e for e in check(GOOD_M, t, BP)))

    def test_count_outside_table_fails(self):
        errors = check(manifest([2] * 7), tags(7), BP)
        self.assertTrue(any("levels" in e for e in errors), errors)


def self_made_pack(fills="non_calc_last"):
    """10문항 중 p10만 자작. MML만 세면 계산 아닌 끝 요구가 4/10이라 non_calc_last 목표가 비어 있다."""
    m = copy.deepcopy(GOOD_M)
    m["problems"][9]["source"] = "자작 p10"
    t = tags(10, last="계산")
    for r in t["problems"][5:]:
        r["last_ask"] = "읽기"
    t["problems"][9].update(fills=fills, uses=["s1-mean", "s1-cov"])
    return m, t, {"p10": {"status": "pass"}}


class TestSelfMade(unittest.TestCase):
    def test_needed_verified_self_made_passes(self):
        m, t, sc = self_made_pack()
        self.assertEqual(check(m, t, BP, sc), [])

    def test_mml_only_pack_needs_no_self_checks(self):
        self.assertEqual(check(GOOD_M, tags(10), BP, None), [])

    def test_self_made_when_mml_already_meets_target_fails(self):
        m, t, sc = self_made_pack()
        for r in t["problems"][:4]:
            r["last_ask"] = "판정"
        self.assertTrue(any("p10" in e and "필요" in e for e in check(m, t, BP, sc)))

    def test_missing_fills_fails(self):
        m, t, sc = self_made_pack()
        del t["problems"][9]["fills"]
        self.assertTrue(any("p10.fills" in e for e in check(m, t, BP, sc)))

    def test_levels_cannot_be_filled(self):
        m, t, sc = self_made_pack(fills="levels")
        self.assertTrue(any("p10.fills" in e for e in check(m, t, BP, sc)))

    def test_fills_on_mml_problem_fails(self):
        m, t, sc = self_made_pack()
        t["problems"][0]["fills"] = "chained"
        self.assertTrue(any("p1.fills" in e for e in check(m, t, BP, sc)))

    def test_too_many_self_made_fails(self):
        m, t, sc = self_made_pack()
        for i in (7, 8):
            m["problems"][i]["source"] = f"자작 p{i + 1}"
            t["problems"][i].update(fills="non_calc_last", uses=["s1-mean"])
            sc[f"p{i + 1}"] = {"status": "pass"}
        self.assertTrue(any("자작" in e and "2" in e for e in check(m, t, BP, sc)))

    def test_source_must_match_id(self):
        m, t, sc = self_made_pack()
        m["problems"][9]["source"] = "자작 p3"
        self.assertTrue(any("p10" in e and "source" in e for e in check(m, t, BP, sc)))

    def test_missing_self_check_fails(self):
        m, t, _ = self_made_pack()
        for sc in (None, {}, {"p10": {"status": "fail"}}):
            with self.subTest(sc=sc):
                self.assertTrue(any("p10" in e and "검산" in e for e in check(m, t, BP, sc)))

    def test_uses_must_be_taught_topics(self):
        for uses in ([], ["s2-next"], ["s2-links"], ["s9-none"]):
            with self.subTest(uses=uses):
                m, t, sc = self_made_pack()
                t["problems"][9]["uses"] = uses
                self.assertTrue(any("p10.uses" in e for e in check(m, t, BP, sc)))

    def test_dates_fill_needs_level2_on_missing_date(self):
        m = manifest([1, 1, 2, 2, 2, 2, 2, 2, 3, 3], ["0102", "0102"] + ["0101"] * 7 + ["0102"])
        m["problems"][9]["source"] = "자작 p10"
        t = tags(10)
        t["problems"][9].update(fills="dates", uses=["s1-mean"])
        sc = {"p10": {"status": "pass"}}
        self.assertEqual(check(m, t, BP, sc), [])
        m["problems"][9]["date"] = "0101"
        self.assertTrue(any("p10" in e for e in check(m, t, BP, sc)))

    def test_max_self_made_target_exists(self):
        self.assertEqual(BP["targets"]["max_self_made"], 2)


if __name__ == "__main__":
    unittest.main()
