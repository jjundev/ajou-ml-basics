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

    def test_adjacent_inline_math_in_term_list_is_not_display_math(self):
        # 페이지 요약의 용어 목록(dt/dd)에서 수식이 이어져도 $$로 붙지 않는다
        doc = check_html.parse_html('<html lang="ko"><body><dl><dt>$a$</dt><dd>$b$</dd></dl></body></html>')
        self.assertEqual(check_html.math_delimiter_errors(doc.body_text), [])

    def test_unbalanced_inline_math(self):
        self.assertEqual(check_html.math_delimiter_errors("a $x b"), ["unbalanced $ (inline math)"])

    def test_deriv_rows_need_one_display_formula_and_visible_note(self):
        ok = ('<ol class="deriv"><li><div class="deriv-eq">$$a=b$$</div>'
              '<div class="deriv-why"><p>정의</p><details><summary>자세히</summary><p>x</p></details></div></li></ol>')
        self.assertEqual(check_html.deriv_row_errors(ok), [])
        bad = ('<ol class="deriv">'
               '<li><div class="deriv-eq">$$a$$ $$b$$</div><div class="deriv-why"><p>둘</p></div></li>'
               '<li><div class="deriv-eq">$$c$$</div><div class="deriv-why">'
               '<details><summary>자세히</summary><p>숨김</p></details></div></li></ol>')
        errs = check_html.deriv_row_errors(bad)
        self.assertEqual(len(errs), 2)
        self.assertIn("수식 2개", errs[0])
        self.assertIn("보이는 주석 없음", errs[1])
        src = f'<html lang="ko"><body>{bad}</body></html>'
        codes = [p.code for p in check_html.check_common(check_html.parse_html(src), src, Path("x.html"))]
        self.assertEqual(codes.count("deriv-row"), 2)

    def test_deriv_rows_inside_outer_details_keep_visible_notes(self):
        # 선택 보충 details 안에 놓인 ol.deriv: 바깥 details는 주석을 숨긴 것으로 보지 않는다
        nested = ('<details><summary>선택 보충</summary><ol class="deriv">'
                  '<li><div class="deriv-eq">$$a=b$$</div><div class="deriv-why"><p>정의</p></div></li>'
                  '<li><div class="deriv-eq">$$c$$</div><div class="deriv-why">'
                  '<details><summary>자세히</summary><p>숨김</p></details></div></li></ol></details>')
        errs = check_html.deriv_row_errors(nested)
        self.assertEqual(len(errs), 1)
        self.assertIn("line 1", errs[0])
        self.assertIn("보이는 주석 없음", errs[0])

    def test_plain_ordered_lists_are_not_deriv_rows(self):
        self.assertEqual(check_html.deriv_row_errors('<ol class="steps"><li>no math</li></ol>'), [])

    def test_widget_without_static(self):
        src = '<html lang="ko"><body><div class="widget" id="w1"><h4>x</h4></div></body></html>'
        problems = check_html.check_common(check_html.parse_html(src), src, Path("x.html"))
        self.assertEqual([p.code for p in problems], ["widget-static-missing"])

    def test_leftover_slot_and_external(self):
        src = '<html lang="ko"><head><script src="https://cdn.tailwindcss.com"></script></head><body>{{TOC}}</body></html>'
        codes = sorted(p.code for p in check_html.check_common(check_html.parse_html(src), src, Path("x.html")))
        self.assertEqual(codes, ["external", "leftover-slot"])

    def external_codes(self, head: str, body: str = "") -> list[str]:
        src = f'<html lang="ko"><head>{head}</head><body>{body}</body></html>'
        return [p.code for p in check_html.check_common(check_html.parse_html(src), src, Path("x.html"))]

    def test_remote_resources_on_any_tag_are_external(self):
        cases = [
            ("", '<img src="https://evil.com/x.png" alt="">'),
            ("", '<iframe src="https://evil.com/frame"></iframe>'),
            ('<link rel="preload" href="https://evil.com/f.woff2" as="font">', ""),
            ('<style>@import url("https://x/y.css");</style>', ""),
            ('<script src="//cdn.example.com/a.js"></script>', ""),
        ]
        for head, body in cases:
            with self.subTest(head=head, body=body):
                self.assertEqual(self.external_codes(head, body), ["external"])

    def test_relative_and_allowed_resources_are_not_external(self):
        head = ('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">'
                '<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>')
        self.assertEqual(self.external_codes(head, '<img src="figures_0101-0102/a.svg" alt="">'), [])


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

    def test_stt_timestamps_block_note_publication(self):
        markers = (
            "(1102 P04 09:03)", "(0909 02:27)", "(0928 Part 01 ~03:00)",
            "(1028 P01 08:34 – P02 00:36)", "(0909 05:41, 06:29)",
            "(주변 학교, 1028 P03 06:30)", "(수업 70:23에서도 언급)",
            "(1102&nbsp;P04&nbsp;09:03)",
        )
        self.edit("sections/s1.html", "평균부터 봐요.", "평균부터 봐요. " + " ".join(markers))
        note, review = assemble.assemble(self.run, self.tmp / "out")
        for problems in (check_html.check_pack(self.m, note, review), check_html.check_file(note)):
            self.assertEqual([p.code for p in problems], ["stt-timestamp"] * len(markers))
            self.assertTrue(all(p.where.startswith(f"{note.name}:") for p in problems))

    def test_ordinary_times_and_review_html_are_allowed(self):
        self.edit("sections/s1.html", "평균부터 봐요.", "평균부터 봐요. (09:03) 2:3")
        self.edit("cards/p1.html", "더해서 개수로 나눈다.", "더해서 개수로 나눈다. (1102 P04 09:03)")
        self.assertEqual(self.codes(), [])

    def test_recording_parts_without_times_block_both_publication_paths(self):
        markers = (
            '(1104 Parts 06–07)', '<cite>1104 전사 Part 02</cite>',
            '(1014 Part 02; 정확한 시각 없음)', 'Part 03에서는 복습했어요.',
            '(1104&nbsp;<em>Parts</em> 06–07)', '(1104 P06)',
            '(1104\n<span>Part</span> 06)', '(Part 12)',
        )
        for marker in markers:
            with self.subTest(marker=marker):
                note, review = assemble.assemble(self.run, self.tmp / 'out')
                note.write_text(note.read_text().replace('평균부터 봐요.', '평균부터 봐요. ' + marker))
                for problems in (check_html.check_pack(self.m, note, review), check_html.check_file(note)):
                    self.assertIn('stt-location', [p.code for p in problems])
                    self.assertTrue(all(p.where.startswith(f'{note.name}:') for p in problems))

    def test_editorial_history_blocks_note_publication(self):
        remarks = (
            '픽셀 수는 수업 중 여러 수치가 구두로 언급됐고, 여기서는 MNIST 규격을 사용했어요.',
            '수업 중 분모를 다르게 말했다가 정정했어요.',
            '수업 중 같은 값이라고 말했지만 일반적으로 달라요.',
            'STT의 g는 z예요.', '이번 전사에서는 시작하지 않았어요.',
            '전사에 없는 세부 시간은 붙이지 않았어요.',
            '수업에서 X로 적었다가 정정했어요.',
            'STT에 분·초가 없어 인용은 Part로 표시해요.',
            '슬라이드의 두 번째 성분은 오타예요.',
            '시각은 각 녹음 파트 시작 기준의 추정값이에요.',
            'TA1 s13의 표기는 여기의 분산으로 바로잡았어요.',
        )
        for remark in remarks:
            with self.subTest(remark=remark):
                note, review = assemble.assemble(self.run, self.tmp / 'out')
                note.write_text(note.read_text().replace('평균부터 봐요.', '평균부터 봐요. ' + remark))
                for problems in (check_html.check_pack(self.m, note, review), check_html.check_file(note)):
                    self.assertIn('editorial-history', [p.code for p in problems])

    def test_reader_text_is_checked_with_source_line_numbers(self):
        note, _ = assemble.assemble(self.run, self.tmp / 'out')
        note.write_text('<html lang="ko"><body>\n<!-- (1104 Part 06) -->\n'
                        '<script>const evidence = "(1104 Part 06)";</script>\n'
                        '<p>(1104&nbsp;<em>Parts</em>\n06–07)</p>\n'
                        '<p>STT의 <span>g</span>는 z예요.</p></body></html>')
        problems = check_html.check_file(note)
        self.assertEqual([(p.code, p.where) for p in problems], [
            ('stt-location', f'{note.name}:4'), ('editorial-history', f'{note.name}:6'),
        ])

    def test_lecture_titles_sources_and_mathematical_corrections_are_allowed(self):
        text = ('Lecture02(Part 2), PCA Part1, Statistical Inference Part 1. '
                '가정에 따라 사후분포를 보정해요. 일반적으로 PD와 DP는 달라요. '
                '출처: 수업 녹음 전사(1104), MML 10.1장, Lecture05 s14. '
                '(09:03) 비율 2:3')
        self.edit('sections/s1.html', '평균부터 봐요.', '평균부터 봐요. ' + text)
        self.edit('cards/p1.html', '더해서 개수로 나눈다.', '더해서 개수로 나눈다. (1104 Parts 06–07) STT의 g')
        self.assertEqual(self.codes(), [])

    def test_missing_required_term(self):
        self.edit("sections/s1.html", "무게중심", "가운데")
        self.assertEqual(self.codes(), ["missing-term"])

    def test_forbidden_term_outside_preview(self):
        self.edit("sections/s1.html", "분산은 흩어진 정도예요.", "분산은 d-separation과 무관해요.")
        self.assertEqual(self.codes(), ["forbidden-term"])

    def test_missing_layer(self):
        self.edit("sections/s1.html", '<div class="layer prof"><span class="layer-title">교수님 말씀</span><p>"평균부터 봐요."</p></div>', "")
        self.assertEqual(self.codes(), ["missing-layer"])

    def test_missing_supp_badge(self):
        self.edit("sections/s1.html", '<span class="badge supp">보충 · 수업에서 유도하진 않았어요</span>', "")
        self.assertEqual(self.codes(), ["missing-supp"])

    def test_missing_sum(self):
        self.edit("sections/s1.html", '<div class="sum" hidden>\n          <p class="sum-lead">평균은', '<div class="summary" hidden>\n          <p class="sum-lead">평균은')
        self.assertEqual(self.codes(), ["missing-sum"])

    def test_sum_not_required_without_summary_panel(self):
        # 요약 패널이 없는 예전 템플릿으로 만든 팩은 .sum을 요구하지 않는다.
        self.edit("sections/s1.html", '<div class="sum" hidden>\n          <p class="sum-lead">평균은', '<div class="summary" hidden>\n          <p class="sum-lead">평균은')
        note, review = assemble.assemble(self.run, self.tmp / "out")
        note.write_text(note.read_text(encoding="utf-8").replace('id="sum-for"', 'id="old-panel"'), encoding="utf-8")
        self.assertEqual([p.code for p in check_html.check_pack(self.m, note, review)], [])

    def test_card_source(self):
        self.edit("cards/p1.html", 'data-source="MML Example 6.1"', 'data-source="MML Ex 6.1"')
        self.assertEqual(self.codes(), ["card-source"])

    def test_card_missing_hint(self):
        self.edit("cards/p1.html", '<details class="hint"><summary>힌트 보기</summary>더해서 개수로 나눈다.</details>', "")
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
