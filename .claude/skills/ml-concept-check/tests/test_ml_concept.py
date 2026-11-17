import json
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
sys.path.insert(0, str(SKILL / "scripts"))


def test_prepare_real_pack_without_manifest(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SKILL / "scripts/quiz.py"), "--repo", str(REPO),
         "prepare", "1111", "--run", str(tmp_path)],
        text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    scope = json.loads(result.stdout)
    assert scope["slug"] == "Gaussian_Mixture_Models"
    assert scope["review"].endswith(".cards.json")
    assert "s2-responsibility" in scope["topics"]
    assert "s3-next" not in scope["topics"]
    assert scope["stt"]["1111"].endswith("1111 머러기.md")
    assert Path(scope["src"]).is_dir()


def test_new_pack_calls_concept_check_after_publication():
    skill = (REPO / ".claude/skills/ml-review-pack/SKILL.md").read_text()
    publish = skill.index("publish_pack", skill.index("### 8. PDF"))
    followup = skill.index("### 확인문제 자동 생성", publish)
    report = skill.index("### 9. 보고", followup)
    assert "ml-concept-check/SKILL.md" in skill[followup:report]
    assert "확인문제 보류" in skill[followup:report]


def test_fraction_answers_are_equivalent_and_recomputed():
    from validation import check_short

    item = {
        "solution": ["성분의 기여량을 합계로 나눠요."],
        "answer": {"canonical": "2/3", "accepted": ["4/6"]},
        "compute": {"op": "responsibility", "contributions": ["1/5", "1/10"], "component": 1},
    }
    assert check_short(item) == []
    item["answer"]["accepted"] = ["0.66"]
    assert check_short(item)
    item["answer"] = {"canonical": "3/4", "accepted": []}
    assert check_short(item)


def test_publish_without_browser_evidence_keeps_existing_quiz(tmp_path):
    import shutil

    import blind
    from quiz import QuizError, dump, prepare, publish

    repo = tmp_path / "repo"
    shutil.copytree(REPO / "복습노트/1111", repo / "복습노트/1111",
                    ignore=shutil.ignore_patterns("확인문제_*", "자료_확인문제_*"))
    (repo / "STT").mkdir()
    shutil.copy2(REPO / "STT/1111 머러기.md", repo / "STT")
    (repo / "assets").mkdir()
    (repo / "assets/vendor").symlink_to(REPO / "assets/vendor", target_is_directory=True)
    run = tmp_path / "run"
    stage = prepare("1111", run, repo)
    original = repo / "복습노트/1111" / Path(stage["html"]).name
    original.write_text("previous quiz")
    src = Path(stage["src"])
    dump(src / "objectives.json", {"range": stage["range"], "slug": stage["slug"], "objectives": [
        {"id": "o1", "topic_id": "s2-responsibility", "concept": "비율",
         "source": {"date": "1111", "locator": "Part 08"}},
    ]})
    dump(src / "items.json", {"items": [
        {"id": "q1", "objective": "o1", "title": "한 관측", "hint": "전체 합을 구해요.",
         "stem_html": "<p>가중 밀도가 1과 3일 때 첫 성분의 책임도를 구해요.</p>",
         "format": "short", "answer": {"canonical": "1/4", "accepted": []},
         "compute": {"op": "responsibility", "contributions": ["1", "3"], "component": 1},
         "solution": ["기여량 1을 전체 4로 나눠요."]},
    ]})
    from quiz_sources import parse_html, read_json
    from validation import check
    items = read_json(src / "items.json")
    duplicate = next(parse_html(Path(stage["review"]), review=True).find_all(
        lambda node: "problem" in node.classes
    ))
    items["items"][0]["stem_html"] = duplicate.text()
    candidate = src / "items.json"
    original_items = candidate.read_bytes()
    dump(candidate, items)
    assert any("20자 이상 연속" in issue for issue in check(src, stage))
    candidate.write_bytes(original_items)
    answers = run / "answers.md"
    answers.write_text("| q1 | 1/4 | s2-responsibility | |\n")
    blind.record(src, answers, src / "blind-ledger.json", 1)
    with pytest.raises(QuizError, match="browser.json"):
        publish(run, repo)
    assert original.read_text() == "previous quiz"
    assert not (repo / "복습노트/1111/.pack" / src.name).exists()


def test_template_and_interaction_assets_match_documented_digests():
    from quiz_sources import digest

    provenance = (SKILL / "assets/SOURCE.md").read_text()
    for name in ("review-template.html", "review-interaction.css", "review-interaction.js", "review-prompt.js"):
        assert f"`{name}` | `{digest(SKILL / 'assets' / name)}`" in provenance
