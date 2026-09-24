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
# 알려진 차이: 위젯은 스킬 이전에 만들어 .widget-static이 없다.
KNOWN_CODES = {"widget-static-missing"}
LECTURES = find_nfc(REPO, "강의노트")


@unittest.skipUnless(NOTE and REVIEW, "복습노트/의 0909-0916 HTML 없음")
class TestRegression(unittest.TestCase):
    def test_contract_checks_pass(self):
        m = manifest.load(FIXTURES / "manifest-0909-0916.json")
        codes = {p.code for p in check_html.check_pack(m, NOTE, REVIEW)}
        self.assertLessEqual(codes, KNOWN_CODES)

    def test_markdown_has_no_missing_tokens(self):
        # 복습노트/ 옆에 강의노트/를 두어 ../강의노트/ 링크도 그대로 검사한다.
        tmp = Path(tempfile.mkdtemp())
        try:
            pack = tmp / "복습노트"
            pack.mkdir()
            if LECTURES:
                (tmp / "강의노트").symlink_to(LECTURES, target_is_directory=True)
            note, review = copy_nfc(NOTE, pack), copy_nfc(REVIEW, pack)
            (note_md, review_md), figs = html2md.convert_pack(note, review)
            self.assertEqual(figs, 13)
            self.assertEqual(html2md.check_md(note, note_md), [])
            self.assertEqual(html2md.check_md(review, review_md), [])
        finally:
            shutil.rmtree(tmp)

if __name__ == "__main__":
    unittest.main()
