#!/usr/bin/env python3
"""영상 화면을 읽기 위한 프레임 묶음(3x3 시트)과 핵심 장면 그림을 만든다.

사용법:
    python3 sheets.py sheets <work>/meta.json [--interval N]
        → <work>/sheets/sNN.png, <work>/sheets/sheets.json (시트·칸 → 초)
    python3 sheets.py frame <work>/meta.json --at 93,144 --names a,b --out <figures 폴더>
        → 지정 시각의 프레임을 960px 폭 PNG로 저장

로컬 ffmpeg에 drawtext 필터가 없을 수 있으므로 시각은 그림에 쓰지 않고 sheets.json으로 계산한다.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

COLS = ROWS = 3
MAX_SHEETS = 40


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def fmt(sec: float) -> str:
    s = int(round(sec))
    return f"{s // 60:02d}:{s % 60:02d}"


def cmd_sheets(meta: dict, interval: int | None) -> None:
    dur = meta["duration"]
    per = COLS * ROWS
    if not interval:
        interval = max(6, math.ceil(dur / (MAX_SHEETS * per)))
    out = Path(meta["work"]) / "sheets"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("s*.png"):
        old.unlink()
    ffmpeg("-i", meta["video"], "-vf",
           f"fps=1/{interval},scale=640:-2,tile={COLS}x{ROWS}:padding=4:color=white",
           str(out / "s%02d.png"))
    files = sorted(out.glob("s*.png"))
    # ffmpeg fps 필터는 가장 가까운 프레임으로 반올림하므로 마지막 반 칸은 나오지 않는다.
    n_frames = min(int(dur / interval + 0.5), len(files) * per)
    sheets = []
    for i, f in enumerate(files):
        cells = [k * interval for k in range(i * per, min((i + 1) * per, n_frames))]
        sheets.append({"file": str(f), "cells": cells,
                       "range": f"{fmt(cells[0])}–{fmt(cells[-1])}" if cells else ""})
    index = {"interval": interval, "cols": COLS, "rows": ROWS,
             "order": "row-major (왼→오, 위→아래)", "sheets": sheets}
    (out / "sheets.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[sheets] 간격 {interval}초, 프레임 {n_frames}장, 시트 {len(files)}장 → {out}/sheets.json")
    for s in sheets:
        print(f"  {Path(s['file']).name}: {s['range']}")


def cmd_frame(meta: dict, at: str, names: str | None, out: str) -> None:
    times = [float(t) for t in at.split(",") if t.strip()]
    labels = names.split(",") if names else [f"frame_{int(t):04d}" for t in times]
    if len(labels) != len(times):
        sys.exit("[sheets] --at 과 --names 개수가 다릅니다.")
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for t, name in zip(times, labels):
        path = out_dir / f"{name.strip()}.png"
        ffmpeg("-ss", str(t), "-i", meta["video"], "-frames:v", "1", "-vf", "scale=960:-2", str(path))
        print(f"[frame] {fmt(t)} → {path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sheets")
    s.add_argument("meta")
    s.add_argument("--interval", type=int)
    f = sub.add_parser("frame")
    f.add_argument("meta")
    f.add_argument("--at", required=True, help="초 단위, 쉼표 구분")
    f.add_argument("--names", help="파일 이름(확장자 제외), 쉼표 구분")
    f.add_argument("--out", required=True)
    args = ap.parse_args()
    meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
    if args.cmd == "sheets":
        cmd_sheets(meta, args.interval)
    else:
        cmd_frame(meta, args.at, args.names, args.out)
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())
