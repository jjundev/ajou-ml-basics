#!/usr/bin/env python3
"""meta.json의 오디오 파트를 Gemini API(Vertex AI, API 키 방식)로 병렬 전사하고 하나의 md로 합친다.

사용법:
    python3 transcribe.py <work>/meta.json --repo <저장소 루트> [--out STT/<slug>.md]
                          [--model gemini-3.5-flash] [--hints "용어1, 용어2"]

- 키: 환경변수 GOOGLE_API_KEY, 없으면 <repo>/.env 에서 읽는다. 키 값은 절대 출력하지 않는다.
- 모델: --model 을 먼저 시도하고, 404·빈 응답이면 FALLBACK 순서로 넘어간다.
- 셸에서 "$m:generateContent"처럼 쓰면 zsh가 ":g"를 수식어로 해석하므로, API 호출은 이 스크립트로만 한다.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DEFAULT_MODEL = "gemini-3.5-flash"
FALLBACK = ["gemini-3.5-flash", "gemini-3.1-pro-preview", "gemini-2.5-flash"]
ENDPOINT = "https://aiplatform.googleapis.com/v1/publishers/google/models/{model}:generateContent"

PROMPT = """You are a verbatim speech-to-text transcription agent.
Audio source: the video "{title}"{channel}. This is part {idx} of {total} (each part is about {seg} minutes).
{hints}
Instructions:
1. Transcribe ALL spoken words verbatim in the original spoken language, from start to finish.
   Do not skip, summarize, translate, or omit anything.
2. Group 2-4 sentences per paragraph, separated by a blank line. No timestamps.
3. When a technical term sounds ambiguous, prefer the correct domain term.
4. Output only the transcript text: no heading, preface, or commentary.
"""


class ModelUnavailable(Exception):
    pass


def load_key(repo: Path) -> str:
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    env = repo / ".env"
    if not key and env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith(("GOOGLE_API_KEY=", "GEMINI_API_KEY=")):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    if not key:
        sys.exit("[transcribe] GOOGLE_API_KEY가 없습니다. 저장소 .env에 GOOGLE_API_KEY=... 를 넣어 주세요.")
    return key


def call(model: str, key: str, audio: Path, prompt: str) -> tuple[str, str]:
    body = {
        "contents": [{"role": "user", "parts": [
            {"inlineData": {"mimeType": "audio/mpeg",
                            "data": base64.b64encode(audio.read_bytes()).decode()}},
            {"text": prompt}]}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 32768},
    }
    req = urllib.request.Request(ENDPOINT.format(model=model), data=json.dumps(body).encode(),
                                 method="POST", headers={"Content-Type": "application/json",
                                                         "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="ignore")[:300]
        if e.code == 404:
            raise ModelUnavailable(f"{model}: 404")
        if e.code in (401, 403):
            sys.exit(f"[transcribe] 인증/권한 오류 HTTP {e.code}. .env의 GOOGLE_API_KEY가 "
                     f"Vertex AI용 키인지 확인해 주세요.\n{msg}")
        try:
            status = json.loads(msg + "}}" if msg.count("{") > msg.count("}") else msg)["error"]["status"]
        except Exception:
            status = msg.split("\n")[0][:80]
        raise RuntimeError(f"HTTP {e.code} {status}")
    cands = d.get("candidates") or []
    if not cands:
        raise ModelUnavailable(f"{model}: 후보 없음 {json.dumps(d.get('promptFeedback', {}))[:200]}")
    text = "".join(p.get("text", "") for p in cands[0].get("content", {}).get("parts", []))
    if not text.strip():
        raise ModelUnavailable(f"{model}: 빈 응답 (finishReason={cands[0].get('finishReason')})")
    return text.strip(), cands[0].get("finishReason", "")


def transcribe_part(idx: int, total: int, audio: Path, key: str, models: list[str],
                    meta: dict, hints: str, out_dir: Path) -> dict:
    channel = f' by {meta["channel"]}' if meta.get("channel") else ""
    prompt = PROMPT.format(title=meta["title"], channel=channel, idx=idx, total=total,
                           seg=meta.get("segment", 600) // 60,
                           hints=f"Domain vocabulary hints: {hints}\n" if hints else "")
    errors = []
    for model in models:
        for attempt in range(3):
            try:
                text, finish = call(model, key, audio, prompt)
                (out_dir / f"part{idx:02d}.md").write_text(text + "\n", encoding="utf-8")
                note = f" (앞선 실패: {' | '.join(errors)})" if errors else ""
                print(f"[transcribe] part{idx:02d}: {model} finish={finish} "
                      f"words={len(text.split())}{note}")
                return {"idx": idx, "model": model, "finish": finish, "text": text}
            except ModelUnavailable as e:
                errors.append(str(e))
                break  # 다음 모델로
            except Exception as e:  # 429·5xx·네트워크 오류는 쉬었다가 같은 모델로 재시도
                errors.append(f"{model} try{attempt + 1}: {e}")
                # 429(사용량 한도)는 회복에 30초 이상 걸리는 경우가 많아 더 길게 쉰다.
                time.sleep((30 if "429" in str(e) else 10) * (attempt + 1))
    print(f"[transcribe] part{idx:02d}: 실패 — {' | '.join(errors)}", file=sys.stderr)
    return {"idx": idx, "model": None, "finish": "FAILED", "text": None, "errors": errors}


def fmt(sec: float) -> str:
    s = int(round(sec))
    return f"{s // 60:02d}:{s % 60:02d}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("meta")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", help="기본: <repo>/STT/<slug>.md")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--hints", default="", help="쉼표로 구분한 도메인 용어")
    ap.add_argument("--workers", type=int, default=2, help="동시 요청 수 (429가 잦으면 1)")
    args = ap.parse_args()

    meta_path = Path(args.meta)
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    repo = Path(args.repo).resolve()
    key = load_key(repo)
    models = [args.model] + [m for m in FALLBACK if m != args.model]
    parts = [Path(p) for p in meta["audio_parts"]]
    out_dir = Path(meta["work"]) / "transcript"
    out_dir.mkdir(parents=True, exist_ok=True)

    def job(ia):
        time.sleep(5 * (ia[0] - 1))  # 동시 요청이 몰려 429가 나지 않도록 시작 시각을 엇갈림
        return transcribe_part(ia[0], len(parts), ia[1], key, models, meta, args.hints, out_dir)

    with ThreadPoolExecutor(max_workers=min(args.workers, len(parts))) as ex:
        results = list(ex.map(job, enumerate(parts, start=1)))

    seg, dur = meta.get("segment", 600), meta["duration"]
    used = sorted({r["model"] for r in results if r["model"]})
    failed = [r["idx"] for r in results if not r["text"]]
    lines = [f"# {meta['title']} 전체 오디오 전사본", "",
             f"- **원본 영상**: {meta['url']} (약 {fmt(dur)})",
             f"- **채널**: {meta.get('channel') or '-'}",
             f"- **전사 방식**: {', '.join(used) or '실패'} (Vertex AI API), 원어 축어 전사",
             f"- **총 세그먼트**: {len(parts)}개 파트 (각 약 {seg // 60}분)"]
    if failed:
        lines.append(f"- **전사 실패 파트**: {', '.join(f'Part {i:02d}' for i in failed)}")
    lines += ["", "---", ""]
    for r in results:
        start, end = (r["idx"] - 1) * seg, min(r["idx"] * seg, dur)
        model_note = f" · {r['model']}" if len(used) > 1 and r["model"] else ""
        lines += [f"## Part {r['idx']:02d} ({fmt(start)}–{fmt(end)}){model_note}", "",
                  r["text"] or "> ⚠️ 이 구간은 전사에 실패했습니다.", ""]

    out = Path(args.out) if args.out else repo / "STT" / f"{meta['slug']}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    meta.update({"transcript": str(out), "transcribe_models": used, "transcribe_failed": failed})
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    words = sum(len(r["text"].split()) for r in results if r["text"])
    print(f"[transcribe] 저장: {out} ({words} words)")
    return 1 if failed else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
