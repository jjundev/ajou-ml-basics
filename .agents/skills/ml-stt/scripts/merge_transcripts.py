#!/usr/bin/env python3
"""
Merge segmented STT markdown files into a master transcript for ml-stt.

Outputs to STT/<NAME>.md with header:
# <NAME> 전체 오디오 전사본
- **총 세그먼트**: N개 파트 (각 약 10분)
- **파트 목록**: ...
---
## Part 01
...
"""

import argparse
import os
from pathlib import Path
import re
import sys
import unicodedata


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def merge_transcripts(
    target_dir: str,
    prefix: str = "",
    segment_seconds: int = 600,
    keep_parts: bool = False,
    output_file: str = "",
    out_file: str = "",
    timestamps: bool = False,
    speakers: list[str] | str | None = None,
) -> str:
    target_dir = os.path.abspath(target_dir)
    output_path_candidate = output_file or out_file
    pattern = re.compile(rf"^{re.escape(prefix)}.*part(\d+)\.md$" if prefix else r"^.*part(\d+)\.md$")
    timestamp_pattern = re.compile(r"^(\d{1,2}):(\d{2})$")

    part_files = []
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory does not exist: {target_dir}", file=sys.stderr)
        return ""

    for f in os.listdir(target_dir):
        m = pattern.match(nfc(f))
        if m:
            part_files.append((int(m.group(1)), f))

    if not part_files:
        print(f"Error: No matching part markdown files found in {target_dir}", file=sys.stderr)
        return ""

    part_files.sort(key=lambda x: x[0])

    if output_path_candidate:
        output_path = os.path.abspath(output_path_candidate)
    elif prefix:
        output_path = os.path.join(target_dir, f"{prefix}.md")
    else:
        output_path = os.path.join(target_dir, "transcript.md")

    # Ensure parent dir exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    part_names_str = ", ".join(p[1] for p in part_files)
    header_title = f"{prefix or os.path.basename(target_dir)} 전체 오디오 전사본"
    full_content = [
        f"# {header_title}\n\n",
        f"- **총 세그먼트**: {len(part_files)}개 파트 (각 약 {segment_seconds // 60}분)\n",
        f"- **파트 목록**: {part_names_str}\n\n",
        "---\n\n",
    ]

    for part_num, p_file in part_files:
        offset_seconds = (part_num - 1) * segment_seconds
        part_path = os.path.join(target_dir, p_file)
        if timestamps:
            start_min = (part_num - 1) * (segment_seconds // 60)
            full_content.append(f"## Part {part_num:02d} ({start_min:02d}:00 ~ )\n\n")
        else:
            full_content.append(f"## Part {part_num:02d}\n\n")

        with open(part_path, "r", encoding="utf-8") as pf:
            lines = pf.readlines()

        content_lines = []
        skip_header = True
        for line in lines:
            line_str = line.strip()
            if skip_header and (line_str.startswith("#") or not line_str):
                continue
            skip_header = False

            tm = timestamp_pattern.match(line_str)
            if tm:
                if timestamps:
                    mins = int(tm.group(1))
                    secs = int(tm.group(2))
                    total_secs = offset_seconds + (mins * 60) + secs
                    new_mins = total_secs // 60
                    new_secs = total_secs % 60
                    content_lines.append(f"{new_mins:02d}:{new_secs:02d}\n")
                else:
                    # Strip timestamp line when timestamps is False
                    continue
            else:
                content_lines.append(line)

        body = "".join(content_lines).strip()
        if body:
            full_content.append(body + "\n\n")

    raw_text = "".join(full_content)
    cleaned_text = re.sub(r"\n{3,}", "\n\n", raw_text).strip() + "\n"

    with open(output_path, "w", encoding="utf-8") as out:
        out.write(cleaned_text)

    print(f"Master transcript successfully created: {output_path}")

    # Validate speaker roster if provided
    if speakers:
        if isinstance(speakers, str):
            speaker_list = [s.strip() for s in speakers.split(",") if s.strip()]
        else:
            speaker_list = [s.strip() for s in speakers if s.strip()]

        allowed = set(speaker_list) | {"화자?"}
        label_pattern = re.compile(r"^\*\*(.+?):\*\*", re.MULTILINE)
        found = set(label_pattern.findall(cleaned_text))
        unknown = sorted(found - allowed)
        if unknown:
            print(
                "Warning: speaker labels not in roster: " + ", ".join(repr(u) for u in unknown),
                file=sys.stderr,
            )

    # Auto-cleanup of intermediate files unless keep_parts is specified
    if not keep_parts and os.path.isfile(output_path) and os.path.getsize(output_path) > 0:
        cleaned_count = 0
        output_abs = os.path.abspath(output_path)
        for f in os.listdir(target_dir):
            fn = nfc(f)
            is_chunk_md = bool(re.search(r"_part\d+\.md$", fn))
            is_chunk_mp3 = bool(re.search(r"_part\d+\.mp3$", fn))
            is_chunk_mp4 = bool(re.search(r"_part\d+_temp\.mp4$", fn))

            if prefix:
                matches_prefix = fn.startswith(prefix)
            else:
                matches_prefix = True

            if matches_prefix and (is_chunk_md or is_chunk_mp3 or is_chunk_mp4):
                fpath = os.path.join(target_dir, f)
                if os.path.abspath(fpath) == output_abs:
                    continue
                try:
                    os.remove(fpath)
                    cleaned_count += 1
                except OSError as e:
                    print(f"Warning: Failed to delete intermediate file {f}: {e}", file=sys.stderr)

        print(f"Cleaned up {cleaned_count} intermediate chunk files.")
        if os.path.basename(target_dir).startswith("_temp_"):
            try:
                remaining = [f for f in os.listdir(target_dir) if f != ".DS_Store"]
                if not remaining:
                    ds_store = os.path.join(target_dir, ".DS_Store")
                    if os.path.exists(ds_store):
                        os.remove(ds_store)
                    os.rmdir(target_dir)
                    print(f"Removed empty temporary directory: {target_dir}")
            except OSError:
                pass

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Merge segmented transcripts for ml-stt")
    parser.add_argument("--dir", required=True, help="Directory containing part files")
    parser.add_argument("--prefix", default="", help="Prefix of the part files (e.g. 1005 머러기)")
    parser.add_argument("--out", default="", help="Final output file path")
    parser.add_argument("--segment-seconds", type=int, default=600, help="Segment length in seconds (default: 600)")
    parser.add_argument("--keep-parts", action="store_true", help="Preserve intermediate part files")
    parser.add_argument("--timestamps", action="store_true", help="Include continuous MM:SS timestamps")
    parser.add_argument("--speakers", default="", help="Comma-separated allowed speaker labels")

    args = parser.parse_args()
    merge_transcripts(
        target_dir=args.dir,
        prefix=args.prefix,
        segment_seconds=args.segment_seconds,
        keep_parts=args.keep_parts,
        output_file=args.out,
        timestamps=args.timestamps,
        speakers=args.speakers,
    )


if __name__ == "__main__":
    main()
