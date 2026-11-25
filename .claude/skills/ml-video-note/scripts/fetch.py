#!/usr/bin/env python3
"""영상 링크를 받아 원본 mp4를 ~/Downloads에 받고, 전사용 오디오를 10분 단위로 나눈다.

사용법:
    python3 fetch.py <URL> [--work DIR] [--downloads DIR] [--segment 600]

결과: <work>/meta.json, <work>/audio/partNN.mp3
표준 출력 마지막 줄에 meta.json 경로를 출력한다.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, text=True, **kw)


def slugify(title: str, max_len: int = 60) -> str:
    title = unicodedata.normalize("NFC", title)
    slug = re.sub(r"[^\w]+", "_", title, flags=re.UNICODE).strip("_")
    slug = re.sub(r"_+", "_", slug)
    return (slug[:max_len].rstrip("_")) or "video"


def probe_duration(path: Path) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
              capture_output=True).stdout.strip()
    return float(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--work", help="작업 폴더 (기본: $TMPDIR/ml-video-note/<id>)")
    ap.add_argument("--downloads", default=str(Path.home() / "Downloads"))
    ap.add_argument("--segment", type=int, default=600, help="오디오 분할 길이(초)")
    args = ap.parse_args()

    try:
        info = json.loads(run(["yt-dlp", "-J", "--no-playlist", args.url],
                              capture_output=True).stdout)
    except subprocess.CalledProcessError as e:
        sys.exit(f"[fetch] yt-dlp 메타데이터 조회 실패:\n{e.stderr.strip()[-800:]}")

    vid, title = info["id"], info.get("title") or info["id"]
    work = Path(args.work or Path(tempfile.gettempdir()) / "ml-video-note" / vid)
    (work / "audio").mkdir(parents=True, exist_ok=True)

    downloads = Path(args.downloads).expanduser()
    downloads.mkdir(parents=True, exist_ok=True)
    existing = sorted(downloads.glob(f"*[[]{vid}[]].mp4"))
    if existing:
        video = existing[0]
        print(f"[fetch] 이미 받은 영상 사용: {video}")
    else:
        template = str(downloads / "%(title)s [%(id)s].%(ext)s")
        try:
            run(["yt-dlp", "--no-playlist", "-f",
                 "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/bv*+ba/b",
                 "--merge-output-format", "mp4", "-o", template, args.url])
        except subprocess.CalledProcessError:
            sys.exit("[fetch] yt-dlp 다운로드 실패 (위 오류 참고)")
        found = sorted(downloads.glob(f"*[[]{vid}[]].mp4"))
        if not found:
            sys.exit(f"[fetch] 다운로드 파일을 찾지 못함: {downloads}/*[{vid}].mp4")
        video = found[0]

    for old in (work / "audio").glob("part*.mp3"):
        old.unlink()
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vn", "-ac", "1",
         "-c:a", "libmp3lame", "-b:a", "64k", "-f", "segment",
         "-segment_time", str(args.segment), "-segment_start_number", "1",
         "-reset_timestamps", "1", str(work / "audio" / "part%02d.mp3")])
    parts = sorted(str(p) for p in (work / "audio").glob("part*.mp3"))

    meta = {
        "id": vid,
        "url": info.get("webpage_url") or args.url,
        "title": title,
        "channel": info.get("channel") or info.get("uploader"),
        "duration": probe_duration(video),
        "slug": slugify(title),
        "video": str(video),
        "work": str(work),
        "segment": args.segment,
        "audio_parts": parts,
    }
    meta_path = work / "meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    d = int(meta["duration"])
    print(f"[fetch] {title} ({d // 60}:{d % 60:02d}), 오디오 {len(parts)}개 파트")
    print(meta_path)
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
