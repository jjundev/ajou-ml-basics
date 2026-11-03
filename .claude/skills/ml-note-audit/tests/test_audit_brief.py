"""The audit brief keeps its categories and output shape, and every generator calls it."""
import re
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SKILLS = SKILL.parent
BRIEF = (SKILL / "references" / "audit-brief.md").read_text(encoding="utf-8")


class TestAuditBrief(unittest.TestCase):
    def test_six_categories_in_order(self):
        found = re.findall(r"^(\d)\. \*\*", BRIEF, re.M)
        self.assertEqual(found, ["1", "2", "3", "4", "5", "6"])

    def test_output_headers(self):
        for header in ("## Critical", "## Important", "## Minor"):
            self.assertIn(header, BRIEF)

    def test_read_only_and_quote_required(self):
        self.assertIn("파일은 수정하지 않는다", BRIEF)
        self.assertIn("인용할 수 없으면 보고하지 않는다", BRIEF)

    def test_placeholders(self):
        self.assertIn("<대상>", BRIEF)
        self.assertIn("<형제 자료>", BRIEF)

    def test_generators_call_audit(self):
        for name in ("ml-review-pack", "ml-problem-explain", "ml-interactive"):
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("ml-note-audit", text, name)

    def test_review_pack_lite_keeps_audit(self):
        text = (SKILLS / "ml-review-pack" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("6b 설명 감사는 생략하지 않는다", text)
        self.assertIn("### 6b. 설명 감사 (`lite`도 수행)", text)
        self.assertIn("- 설명 감사: Critical n / Important n / 미해결 n", text)


if __name__ == "__main__":
    unittest.main()
