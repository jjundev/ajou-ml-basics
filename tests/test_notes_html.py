#!/usr/bin/env python3
"""
정리노트/복습문제 HTML 계약 테스트.

콘텐츠 태스크는 먼저 COMPLETED_SECTIONS / COMPLETED_PROBLEMS 에 자기 항목을 추가해
테스트를 실패시킨 뒤(RED), 내용을 채워 통과시킨다(GREEN).
"""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from check_notes_html import broken_links, math_delimiter_errors, parse_file  # noqa: E402

NOTE_PATH = ROOT / "복습노트" / "정리노트_0909-0916_When_Models_Meet_Data.html"
REVIEW_PATH = ROOT / "복습노트" / "복습문제_0909-0916_When_Models_Meet_Data.html"
WIDGET_JS_PATH = ROOT / "scripts" / "widget_math.js"
NOTE_HREF = "정리노트_0909-0916_When_Models_Meet_Data.html"

ALLOWED_EXTERNAL_PREFIXES = (
    "https://cdn.jsdelivr.net/npm/katex@0.16.11/",
    "https://cdn.jsdelivr.net/npm/pretendard@1.3.9/",
)

SECTION_IDS = ["s0", "s1", "s2", "s3", "s4", "s5"]
TOPIC_IDS = {
    "s0": ["s0-course"],
    "s1": ["s1-components", "s1-induction", "s1-data", "s1-model", "s1-prob-model", "s1-learning"],
    "s2": ["s2-erm", "s2-affine", "s2-matrix", "s2-risk", "s2-reg"],
    "s3": ["s3-likelihood", "s3-iid", "s3-mle-ls", "s3-map", "s3-map-l2", "s3-fitting"],
    "s4": ["s4-generative", "s4-joint", "s4-posterior", "s4-three-ways", "s4-coin", "s4-predictive"],
    "s5": ["s5-cheatsheet", "s5-prereq", "s5-next", "s5-links"],
}
LAYERED_SECTIONS = {"s1", "s2", "s3", "s4"}  # 이 섹션의 토픽은 eli5/formal/prof 레이어 필수
FIGURE_IDS = {
    "s1": ["fig-pipeline", "fig-induction", "fig-data-vector", "fig-det-vs-prob", "fig-three-phases"],
    "s2": ["fig-neuron", "fig-matrix-packing"],
    "s3": ["fig-log", "fig-factory", "fig-prior-likelihood-posterior", "fig-model-class", "fig-fitting-3"],
    "s4": ["fig-general"],
}
WIDGET_IDS = {
    "s2": ["widget-reg", "reg-degree", "reg-lambda", "reg-plot", "reg-train-mse", "reg-test-mse", "widget-reg-ui"],
    "s4": ["widget-coin", "coin-n", "coin-k", "coin-a", "coin-plot", "coin-ml", "coin-map", "coin-pred", "widget-coin-ui"],
}
SUPP_TOPICS = {"s3-map-l2", "s4-coin"}
FORBIDDEN_OUTSIDE_NEXT = ["d-separation", "Bayes factor", "Bayesian Model Selection", "Directed Graphical", "MCMC"]

REQUIRED_TERMS = {
    "s0-course": ["35%", "20%", "10%", "지도학습", "비지도학습", "강화학습", "전제 과목", "Universal Approximation"],
    "s1-components": ["데이터", "모델", "러닝", "데이터가 부족", "GPU"],
    "s1-induction": ["귀납", "연역", "파란 점", "메인 레슨", "y(t) = x(t) * h(t)"],
    "s1-data": ["볼드", "N \\to \\infty", "\\mathbf{x}_n \\in \\mathbb{R}^D", "clustering", "MBTI", "feature", "PCA", "SVD", "kernel"],
    "s1-model": ["정답은 없", "suppose", "assume", "취사선택", "y = 3x_1 + 5x_2 + 6x_3 + 0.6"],
    "s1-prob-model": ["노이즈", "x=60", "p(y \\mid \\mathbf{x}) = \\mathcal{N}\\big(y \\mid f(\\mathbf{x}), \\sigma^2\\big)", "대령", "MLE"],
    "s1-learning": ["unseen", "such that", "prediction", "training", "model selection", "hyperparameter", "learning rate", "grid search", "gradient descent"],
    "s2-erm": ["Empirical", "Risk", "Minimization", "in terms of", "for all", "\\hat{y}_n \\approx y_n"],
    "s2-affine": ["augmentation", "affine", "원점", "\\boldsymbol{\\theta}^\\top \\mathbf{x}_n", "activation", "sigmoid", "ReLU"],
    "s2-matrix": ["\\in \\mathbb{R}^{N \\times D}", "R_{\\text{emp}}", "(y_n - \\hat{y}_n)^2", "\\|\\mathbf{y} - \\mathbf{X}\\boldsymbol{\\theta}\\|^2", "김밥", "전치"],
    "s2-risk": ["R_{\\text{true}}", "7:3", "validation", "기보", "해 아래"],
    "s2-reg": ["overfitting", "penalty", "regularizer", "\\lambda \\|\\boldsymbol{\\theta}\\|^2", "hyperparameter", "sparse", "\\|\\boldsymbol{\\theta}\\|_1", "Bayesian Optimization"],
    "s3-likelihood": ["likelihood", "그럴듯함", "\\mathcal{L}(\\boldsymbol{\\theta}) = -\\log p(\\mathbf{x} \\mid \\boldsymbol{\\theta})", "단조", "클로즈업", "1보다 클 수", "latent", "\\lambda e^{-\\lambda x}"],
    "s3-iid": ["i.i.d.", "\\prod_{n=1}^{N} p(y_n \\mid \\mathbf{x}_n, \\boldsymbol{\\theta})", "동일한 공장", "추석 선물 세트"],
    "s3-mle-ls": ["\\varepsilon \\sim \\mathcal{N}(0, \\sigma^2)", "\\frac{N}{2}\\log(2\\pi\\sigma^2)", "least squares", "suppose", "delta"],
    "s3-map": ["posterior", "CT", "\\propto", "argmax", "\\boldsymbol{\\theta}_{\\text{MAP}}", "uniform"],
    "s3-map-l2": ["\\mathcal{N}(\\mathbf{0}, b^2 \\mathbf{I})", "\\frac{\\sigma^2}{N b^2}", "나중에"],
    "s3-fitting": ["M^*", "M_{\\boldsymbol{\\theta}^*}", "빨간 거리", "overfitting", "underfitting", "good fitting", "되새김질", "파라미터 개수"],
    "s4-generative": ["generative process", "했을 거야", "노이즈", "c_n = \\mathbf{x}_n^\\top \\boldsymbol{\\theta}"],
    "s4-joint": ["joint", "marginal", "hidden", "latent", "인셉션", "확률 및 랜덤변수"],
    "s4-posterior": ["p(\\mathbf{x}, \\boldsymbol{\\theta}) = p(\\mathbf{x} \\mid \\boldsymbol{\\theta})\\, p(\\boldsymbol{\\theta})", "prior", "모름지기", "marginal likelihood", "\\int p(\\mathbf{x}, \\boldsymbol{\\theta})\\, d\\boldsymbol{\\theta}", "정규화"],
    "s4-three-ways": ["\\boldsymbol{\\theta}_{\\text{ML}}", "\\boldsymbol{\\theta}_{\\text{MAP}}", "Fully Bayesian", "장군"],
    "s4-coin": ["0.2", "0.3125", "\\frac{2}{\\theta} - \\frac{8}{1-\\theta} = 0", "머니볼", "그 사이", "Beta"],
    "s4-predictive": ["posterior predictive", "P(A \\mid \\boldsymbol{\\theta})\\, P(\\boldsymbol{\\theta} \\mid \\mathbf{X})", "조건부 독립", "mixture", "EM"],
    "s5-cheatsheet": ["치트시트", "R_{\\text{emp}}", "\\boldsymbol{\\theta}_{\\text{MAP}}"],
    "s5-prereq": ["Ch.2", "Ch.3", "Ch.5", "Ch.6", "Ch.7"],
    "s5-next": ["d-separation", "Bayes factor", "Linear Regression", "EM"],
    "s5-links": ["Lecture 10", "Lecture 11", "Lecture 12", "복습문제"],
}
S5_LINK_HREFS = [
    "../강의노트/추가%20강의/eli5_lecture10_statistical_inference_part1.html",
    "../강의노트/추가%20강의/eli5_lecture11_statistical_inference_part2.html",
    "../강의노트/추가%20강의/eli5_lecture12_statistical_inference_part3.html",
    "복습문제_0909-0916_When_Models_Meet_Data.html",
]

PROBLEMS = {
    "p1": {"source": "MML Example 8.1", "anchor": "s2-affine", "terms": ["\\mathbb{R}^{D+1}", "원점", "x_n^{(D)}"]},
    "p2": {"source": "MML Example 8.2", "anchor": "s2-matrix", "terms": ["\\|\\mathbf{y} - \\mathbf{X}\\boldsymbol{\\theta}\\|^2", "N \\times (D+1)"]},
    "p3": {"source": "MML Example 8.3", "anchor": "s2-reg", "terms": ["\\lambda \\to \\infty", "(\\mathbf{X}^\\top \\mathbf{X} + N\\lambda \\mathbf{I})", "hyperparameter"]},
    "p4": {"source": "MML Example 8.5", "anchor": "s3-mle-ls", "terms": ["\\frac{N}{2}\\log(2\\pi\\sigma^2)", "least squares"]},
    "p5": {"source": "MML Example 8.6", "anchor": "s3-map-l2", "terms": ["\\frac{\\sigma^2}{N b^2}", "\\frac{1}{2b^2}"]},
    "p6": {"source": "MML Exercise 6.1", "anchor": "s4-joint", "terms": ["0.16", "0.34", "0.26", "0.47", "\\frac{5}{13}", "\\frac{5}{11}", "\\frac{1}{26}", "\\frac{3}{26}"]},
    "p7": {"source": "MML Exercise 6.4", "anchor": "s3-map", "terms": ["\\frac{1}{3}", "0.6", "0.4"]},
    "p8": {"source": "MML Exercise 6.3", "anchor": "s4-coin", "terms": ["\\mathrm{Beta}(\\alpha + k, \\beta + N - k)", "0.3125", "\\frac{1}{3}", "\\frac{2}{10} = 0.2"]},
    "p9": {"source": "MML Exercise 6.12", "anchor": "s4-generative", "terms": ["\\mathcal{N}\\big(\\mathbf{y} \\mid \\mathbf{A}\\mathbf{x} + \\mathbf{b}, \\mathbf{Q}\\big)"]},
    "p10": {"source": "MML Exercise 7.1", "anchor": "s4-coin", "terms": ["-2 + \\sqrt{5}", "-2 - \\sqrt{5}", "6x + 12"]},
}

# 콘텐츠 태스크가 여기에 항목을 추가한다.
COMPLETED_SECTIONS: list[str] = ["s0", "s1", "s2", "s3", "s4", "s5"]
COMPLETED_PROBLEMS: list[str] = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10"]


class _Common:
    path: Path

    @classmethod
    def setUpClass(cls):
        cls.doc = parse_file(cls.path)

    def test_lang_is_korean(self):
        self.assertEqual(self.doc.lang, "ko")

    def test_no_duplicate_ids(self):
        self.assertEqual(self.doc.duplicate_ids, set())

    def test_external_resources_allowlisted(self):
        for url in self.doc.external_resources:
            with self.subTest(url=url):
                self.assertTrue(url.startswith(ALLOWED_EXTERNAL_PREFIXES), url)

    def test_math_delimiters_balanced(self):
        self.assertEqual(math_delimiter_errors(self.doc.body_text), [])

    def test_links_resolve(self):
        self.assertEqual(broken_links(self.doc, self.path.parent), [])


class TestNote(_Common, unittest.TestCase):
    path = NOTE_PATH

    def test_all_section_and_topic_ids_exist(self):
        for sec in SECTION_IDS:
            self.assertIn(sec, self.doc.ids)
            for topic in TOPIC_IDS[sec]:
                with self.subTest(topic=topic):
                    self.assertIn(topic, self.doc.containers)
                    self.assertEqual(self.doc.containers[topic].section, sec)

    def test_widget_math_inline_copy_matches_source(self):
        inline = self.doc.scripts_by_id.get("widget-math", "")
        self.assertEqual(inline.strip(), WIDGET_JS_PATH.read_text(encoding="utf-8").strip())

    def test_scope_forbidden_terms(self):
        texts = {sec: self.doc.section_text.get(sec, "") for sec in SECTION_IDS if sec != "s5"}
        for topic in TOPIC_IDS["s5"]:
            if topic != "s5-next":
                texts[topic] = self.doc.containers[topic].text
        for where, text in texts.items():
            for term in FORBIDDEN_OUTSIDE_NEXT:
                with self.subTest(where=where, term=term):
                    self.assertNotIn(term, text)

    def test_completed_required_terms(self):
        for sec in COMPLETED_SECTIONS:
            for topic in TOPIC_IDS[sec]:
                text = self.doc.containers[topic].text
                for term in REQUIRED_TERMS[topic]:
                    with self.subTest(topic=topic, term=term):
                        self.assertIn(term, text)

    def test_completed_layers(self):
        for sec in COMPLETED_SECTIONS:
            if sec not in LAYERED_SECTIONS:
                continue
            for topic in TOPIC_IDS[sec]:
                with self.subTest(topic=topic):
                    self.assertTrue({"eli5", "formal", "prof"} <= self.doc.containers[topic].child_classes)

    def test_completed_supplement_badges(self):
        for topic in SUPP_TOPICS:
            sec = topic.split("-")[0]
            if sec in COMPLETED_SECTIONS:
                with self.subTest(topic=topic):
                    con = self.doc.containers[topic]
                    self.assertIn("supp", con.child_classes)
                    self.assertIn("📎 보충 · 수업 미유도", con.text)

    def test_completed_figures(self):
        for sec in COMPLETED_SECTIONS:
            for fig in FIGURE_IDS.get(sec, []):
                with self.subTest(fig=fig):
                    self.assertIn(fig, self.doc.ids)
                    self.assertEqual(self.doc.id_section[fig], sec)

    def test_completed_widgets(self):
        for sec in COMPLETED_SECTIONS:
            for wid in WIDGET_IDS.get(sec, []):
                with self.subTest(wid=wid):
                    self.assertIn(wid, self.doc.ids)

    def test_s5_links(self):
        if "s5" not in COMPLETED_SECTIONS:
            self.skipTest("s5 not completed yet")
        hrefs = self.doc.containers["s5-links"].hrefs
        for href in S5_LINK_HREFS:
            with self.subTest(href=href):
                self.assertIn(href, hrefs)


class TestReview(_Common, unittest.TestCase):
    path = REVIEW_PATH

    def test_all_problem_cards_exist(self):
        for pid in PROBLEMS:
            with self.subTest(pid=pid):
                self.assertIn(pid, self.doc.containers)
        self.assertIn("progress-count", self.doc.ids)

    def test_scope_forbidden_terms(self):
        for term in FORBIDDEN_OUTSIDE_NEXT:
            with self.subTest(term=term):
                self.assertNotIn(term, self.doc.body_text)

    def test_completed_problems(self):
        for pid in COMPLETED_PROBLEMS:
            spec = PROBLEMS[pid]
            card = self.doc.containers[pid]
            with self.subTest(pid=pid, check="source"):
                self.assertEqual(card.attrs.get("data-source"), spec["source"])
            with self.subTest(pid=pid, check="anchor"):
                self.assertIn(f"{NOTE_HREF}#{spec['anchor']}", card.hrefs)
            with self.subTest(pid=pid, check="parts"):
                self.assertTrue({"problem", "original", "hint", "solution", "answer", "link-back", "done"} <= card.child_classes)
            for term in spec["terms"]:
                with self.subTest(pid=pid, term=term):
                    self.assertIn(term, card.text)


if __name__ == "__main__":
    unittest.main()
