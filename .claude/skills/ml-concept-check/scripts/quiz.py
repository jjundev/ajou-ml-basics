"""Stage, validate, and publish a concept check for an existing ML review pack."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import quote

from quiz_sources import REPO, SKILL, QuizError, digest, dump, load_items, read_json, source_scope
import blind
import browser_check
import quiz_interaction
import quiz_render
import validation
from assemble import fill
from review_pdf_publish import publish_files
from review_pdf_types import ReviewPdfError

BRAND = '<strong class="brand">복습문제</strong>'
ARTIFACTS = ("objectives.json", "items.json", "blind-ledger.json", "browser.json")


def stage_paths(run, scope):
    stem = f"확인문제_{scope['range']}_{scope['slug']}"
    stage = run / "stage"
    day = stage / "복습노트" / scope["range"]
    return stage, day / f"{stem}.html", day / ".pack" / f"자료_{stem}"


def prepare(range_, run, repo=REPO, manifest=None):
    run = run.resolve()
    scope = source_scope(repo.resolve(), range_, manifest)
    stage, html, src = stage_paths(run, scope)
    vendor = repo.resolve() / "assets/vendor"
    required = ("katex/katex.min.css", "katex/katex.min.js", "katex/contrib/auto-render.min.js",
                "pretendard/pretendard.css")
    if any(not (vendor / name).is_file() for name in required):
        raise QuizError(f"오프라인 수식·글꼴 자원이 없습니다: {vendor}")
    run.mkdir(parents=True, exist_ok=True)
    if (run / "scope.json").exists() or stage.exists():
        raise QuizError(f"이미 준비된 RUN입니다. 기존 실행을 이어가거나 새 RUN을 쓰세요: {run}")
    src.mkdir(parents=True)
    (stage / "assets").mkdir()
    (stage / "assets/vendor").symlink_to(vendor, target_is_directory=True)
    note = Path(scope["note"])
    (html.parent / note.name).symlink_to(note)
    scope.update(src=str(src), html=str(html))
    dump(run / "scope.json", scope)
    return scope


def read_scope(run):
    scope = read_json(run / "scope.json")
    for name, sha in scope["hashes"].items():
        path = Path(name)
        if not path.is_file() or digest(path) != sha:
            raise QuizError(f"준비 이후 근거가 바뀌었습니다. 새 RUN에서 시작하세요: {path}")
    return scope


def check(src, scope):
    issues = validation.check(src, scope)
    if issues:
        raise QuizError("\n".join(issues))


def render_page(src, scope, asset_root):
    doc, items = load_items(src)
    objectives = {objective["id"]: objective for objective in doc["objectives"]}
    note = Path(scope["note"]).name
    cards = "".join(quiz_render.card_html(item, objectives[item["objective"]], number, note)
                    for number, item in enumerate(items, 1))
    range_ = scope["range"]
    title = f"{range_} 확인문제 — 이번 수업 개념 확인"
    template = (SKILL / "assets/review-template.html").read_text(encoding="utf-8")
    if template.count(BRAND) != 1:
        raise QuizError("자구알 원본 템플릿에서 상단 바 위치를 찾을 수 없습니다")
    page = fill(template, {
        "ASSET_ROOT": asset_root,
        "PAGE_TITLE": f"머신러닝기초 확인문제 {range_}",
        "DESCRIPTION": title, "TITLE": title,
        "TOC": '<a href="#check">확인</a>', "NOTE_HREF": quiz_render.esc(note),
        "INTRO": f"이번 수업에서 처음 배운 개념을 {len(items)}문항으로 확인해요. 답하면 바로 채점돼요.",
        "PARTS": f'<section id="check"><h2>확인문제</h2>{cards}</section>',
        "FOOTER": "<p>출처 · 정방철 교수님 머신러닝기초 수업과 정리노트.</p>",
        "SCRIPTS": "", "RANGE": f"{range_}-확인",
    })
    return quiz_interaction.install(page.replace(BRAND, '<strong class="brand">확인문제</strong>'),
                                    f"확인문제_{range_}_{scope['slug']}")


def build(run):
    scope = read_scope(run)
    stage, html, src = stage_paths(run, scope)
    check(src, scope)
    asset_root = quote(Path(os.path.relpath(stage / "assets/vendor", html.parent)).as_posix(), safe="/")
    html.write_text(render_page(src, scope, asset_root), encoding="utf-8")
    return html


def check_blind(src):
    issues = blind.status(src, src / "blind-ledger.json")
    if issues:
        raise QuizError("\n".join(issues))


def verify(run, shots=None):
    html = build(run)
    scope = read_scope(run)
    stage, _, src = stage_paths(run, scope)
    check_blind(src)
    report_path = src / "browser.json"
    report_path.unlink(missing_ok=True)
    hashes = {name: digest(src / name) for name in ARTIFACTS[:-1]}
    report = browser_check.check(html, report_path, shots, src=src, serve_root=stage)
    if any(digest(src / name) != sha for name, sha in hashes.items()) or digest(html) != report["sha256"]:
        raise QuizError("브라우저 검사 도중 입력 또는 HTML이 바뀌었습니다")
    report["inputs"] = hashes
    dump(report_path, report)
    if report["status"] != "pass":
        raise QuizError("\n".join(report["failures"]))
    return report


def publish(run, repo=REPO):
    scope = read_scope(run)
    _, html, src = stage_paths(run, scope)
    check(src, scope)
    check_blind(src)
    report = read_json(src / "browser.json")
    expected_runs = {f"{width}x{height} {theme}" for width, height in browser_check.VIEWPORTS
                     for theme in browser_check.THEMES}
    runs = report.get("runs", [])
    if (report.get("status") != "pass" or report.get("failures") != [] or len(runs) != len(expected_runs)
            or {entry["label"] for entry in runs if entry["failures"] == []} != expected_runs
            or report.get("sha256") != digest(html)
            or report.get("inputs") != {name: digest(src / name) for name in ARTIFACTS[:-1]}):
        raise QuizError("현재 HTML·근거에 대한 브라우저 검사가 필요합니다. verify를 실행하세요")
    day = repo.resolve() / "복습노트" / scope["range"]
    if Path(scope["note"]).parent.resolve() != day.resolve():
        raise QuizError("준비한 복습팩과 발행할 저장소가 다릅니다")
    asset_root = quote(Path(os.path.relpath(repo.resolve() / "assets/vendor", day)).as_posix(), safe="/")
    if html.read_text(encoding="utf-8") != render_page(src, scope, asset_root):
        raise QuizError("검증한 HTML과 최종 발행 경로에서 다시 렌더한 결과가 다릅니다")
    targets = {day / ".pack" / src.name / name: src / name for name in ARTIFACTS}
    targets[day / html.name] = html
    publish_files(targets, run / "backups")
    return day / html.name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("prepare", "check", "build", "verify", "publish"):
        sub = commands.add_parser(command)
        sub.add_argument("--run", type=Path, required=True)
        if command == "prepare":
            sub.add_argument("range")
            sub.add_argument("--manifest", type=Path)
        if command == "verify":
            sub.add_argument("--shots", type=Path)
    args = parser.parse_args()
    run = args.run.resolve()
    try:
        match args.command:
            case "prepare":
                print(json.dumps(prepare(args.range, run, args.repo, args.manifest), ensure_ascii=False, indent=2))
            case "check":
                scope = read_scope(run)
                check(stage_paths(run, scope)[2], scope)
                print("OK")
            case "build":
                print(build(run))
            case "verify":
                report = verify(run, args.shots)
                print(f"browser: pass · 실행 {len(report['runs'])}회")
            case "publish":
                print(publish(run, args.repo))
    except (ValueError, OSError, ReviewPdfError, RuntimeError, ImportError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
