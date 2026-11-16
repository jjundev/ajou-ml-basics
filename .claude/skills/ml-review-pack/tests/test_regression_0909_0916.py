"""0909·0914·0916 날짜별 복습팩의 HTML 구조와 Markdown 변환을 검사한다."""

from pathlib import Path
import tempfile
import unittest

from _util import REPO, copy_nfc, find_nfc

import check_html
import html2md
from manifest import pdf_names
from review_sources import html_name, source_markup


PACKS = {
    "0909": {
        "slug": "Data_Models_Learning",
        "links_topic": "s4-links",
        "topics": {
            "s1-vectors": ("벡터",),
            "s2-induction": ("귀납", "연역"),
            "s3-three-phases": ("prediction", "training", "model selection"),
        },
        "sources": ["MML Example 9.1"] + ["MML Exercise 2.4"] * 4,
        "figures": 15,
    },
    "0914": {
        "slug": "ERM_and_MLE",
        "links_topic": "s5-links",
        "topics": {
            "s1-affine": ("원점",),
            "s2-squared": ("김밥",),
            "s4-mle-ls": ("최소제곱",),
        },
        "sources": [f"MML Example 8.{n}" for n in range(1, 6)]
        + ["MML Exercise 3.3", "MML Exercise 7.1"],
        "figures": 18,
    },
    "0916": {
        "slug": "MAP_and_Generative_Models",
        "links_topic": "s4-links",
        "topics": {
            "s1-map": ("prior", "posterior"),
            "s2-joint": ("joint", "marginal"),
            "s3-coin": ("0.3125",),
        },
        "sources": ["MML Example 8.6"] + ["MML Exercise 6.1"] * 4 + ["MML Exercise 6.3"],
        "figures": 19,
    },
}


class TestRegression(unittest.TestCase):
    def required_path(self, parent, name):
        path = find_nfc(parent, name)
        self.assertIsNotNone(path, f"복습팩 검사에 필요한 경로 없음: {parent / name}")
        return path

    def setUp(self):
        self.packs_dir = self.required_path(REPO, "복습노트")

    def pack_sources(self, date, slug):
        pack = self.packs_dir / date
        note = self.required_path(pack, f"정리노트_{date}_{slug}.html")
        review = self.required_path(pack / ".pack", f"복습문제_{date}_{slug}.cards.json")
        return note, review

    def work_review(self, source, folder):
        result = folder / html_name(source)
        result.write_text('<html lang="ko"><body><main><header class="hero"><h1>복습문제</h1></header>'
                          + source_markup(source)
                          + '</main></body></html>', encoding="utf-8")
        return result

    def test_contract_checks_pass(self):
        for date, spec in PACKS.items():
            with self.subTest(date=date):
                note, review = self.pack_sources(date, spec["slug"])
                sections = {}
                for topic, terms in spec["topics"].items():
                    section = topic.split("-", 1)[0]
                    sections.setdefault(section, []).append({
                        "id": topic,
                        "required_terms": terms,
                        "layers": ["eli5", "formal", "prof"],
                        "supp": False,
                    })
                contract = {
                    "sections": [
                        {"id": section, "topics": topics}
                        for section, topics in sections.items()
                    ],
                    "preview_topic": None,
                    "forbidden_outside_preview": [],
                    "links": [{
                        "topic": spec["links_topic"],
                        "href": pdf_names(date, spec['slug'])[0],
                    }],
                    "problems": [
                        {"id": f"p{number}", "source": source, "terms": []}
                        for number, source in enumerate(spec["sources"], start=1)
                    ],
                }
                with tempfile.TemporaryDirectory() as directory:
                    folder = Path(directory)
                    (folder / ".pack").symlink_to(review.parent, target_is_directory=True)
                    issues = check_html.check_pack(contract, note, self.work_review(review, folder))
                self.assertEqual([str(issue) for issue in issues], [])

    def test_markdown_has_no_missing_tokens(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packs = root / "복습노트"
            packs.mkdir()
            (root / "강의노트").symlink_to(
                self.required_path(REPO, "강의노트"), target_is_directory=True
            )
            # 0916 정리노트에서 링크하는 후속 강의 자료.
            (packs / "0928").symlink_to(self.packs_dir / "0928", target_is_directory=True)

            for date, spec in PACKS.items():
                with self.subTest(date=date):
                    note, review = self.pack_sources(date, spec["slug"])
                    pack = packs / date
                    output = pack / ".pack"
                    output.mkdir(parents=True)
                    staged_note = copy_nfc(note, pack)
                    staged_review = self.work_review(review, pack)
                    for name in pdf_names(date, spec["slug"]):
                        (pack / name).symlink_to(self.required_path(note.parent, name))
                    (note_md, review_md), figures = html2md.convert_pack(staged_note, staged_review)
                    self.assertEqual(figures, spec["figures"])
                    self.assertEqual(html2md.check_md(staged_note, note_md), [])
                    self.assertEqual(html2md.check_md(staged_review, review_md), [])
