"""0909~0916 복습팩(스킬 이전에 손으로 만든 결과물)이 일반화된 도구에서도 통과하는지 확인한다."""

from pathlib import Path
import shutil
import tempfile
import unittest

from _util import FIXTURES, REPO, copy_nfc, find_nfc

import check_html
import html2md
import manifest

PACK = find_nfc(REPO, "복습노트")
NOTE = find_nfc(PACK, "정리노트_0909-0916_When_Models_Meet_Data.html") if PACK else None
REVIEW = find_nfc(PACK, "복습문제_0909-0916_When_Models_Meet_Data.html") if PACK else None
# 알려진 차이: 위젯은 스킬 이전이라 .widget-static이 없고, 추가강의 링크는 폴더 이동으로 깨져 있다.
KNOWN_CODES = {"widget-static-missing", "broken-link"}


@unittest.skipUnless(NOTE and REVIEW, "복습노트/의 0909-0916 HTML 없음")
class TestRegression(unittest.TestCase):
    def test_contract_checks_pass(self):
        m = manifest.load(FIXTURES / "manifest-0909-0916.json")
        codes = {p.code for p in check_html.check_pack(m, NOTE, REVIEW)}
        self.assertLessEqual(codes, KNOWN_CODES)

    def test_markdown_has_no_missing_tokens(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            note, review = copy_nfc(NOTE, tmp), copy_nfc(REVIEW, tmp)
            (note_md, review_md), figs = html2md.convert_pack(note, review)
            self.assertEqual(figs, 13)
            self.assertEqual(html2md.check_md(note, note_md), [])
            self.assertEqual(html2md.check_md(review, review_md), [])
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
