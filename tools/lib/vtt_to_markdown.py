#!/usr/bin/env python3
"""Convert a WebVTT subtitle file to clean markdown with sparse [mm:ss] anchors.

Usage:
    python tools/lib/vtt_to_markdown.py --input path/to/captions.vtt > out.md
    python tools/lib/vtt_to_markdown.py --self-test
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass


CUE_TIMESTAMP_RE = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2})\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}"
)
INLINE_TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class Cue:
    start_seconds: int
    text: str


def parse_vtt(vtt_text: str) -> list[Cue]:
    """Parse VTT text → list of per-line cues, deduped across cues.

    YouTube auto-captions emit rolling-window cues where each block repeats
    the previous line plus a new line. Deduping at the line level (not the
    whole-cue level) flattens the rolling window into unique content.
    """
    cues: list[Cue] = []
    seen_lines: set[str] = set()
    lines = vtt_text.splitlines()
    i = 0
    while i < len(lines):
        m = CUE_TIMESTAMP_RE.match(lines[i])
        if not m:
            i += 1
            continue
        start = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        i += 1
        while i < len(lines) and lines[i].strip() != "":
            clean = INLINE_TAG_RE.sub("", lines[i]).strip()
            clean = re.sub(r"\s+", " ", clean)
            i += 1
            if not clean or clean in seen_lines:
                continue
            seen_lines.add(clean)
            cues.append(Cue(start_seconds=start, text=clean))
    return cues


def format_timestamp(total_seconds: int) -> str:
    return f"[{total_seconds // 60:02d}:{total_seconds % 60:02d}]"


def cues_to_markdown(cues: list[Cue], paragraph_gap_seconds: int = 60) -> str:
    """Group cues into paragraphs; emit [mm:ss] anchor on each paragraph start."""
    if not cues:
        return ""
    paragraphs: list[tuple[int, list[str]]] = []
    current_start = cues[0].start_seconds
    current_buf: list[str] = []
    last_start = cues[0].start_seconds

    for cue in cues:
        if current_buf and cue.start_seconds - current_start >= paragraph_gap_seconds:
            paragraphs.append((current_start, current_buf))
            current_start = cue.start_seconds
            current_buf = []
        current_buf.append(cue.text)
        last_start = cue.start_seconds
    if current_buf:
        paragraphs.append((current_start, current_buf))

    out_lines: list[str] = []
    for start, buf in paragraphs:
        text = " ".join(buf)
        text = re.sub(r"\s+", " ", text).strip()
        out_lines.append(f"{format_timestamp(start)} {text}")
    return "\n\n".join(out_lines) + "\n"


def convert(vtt_text: str) -> str:
    return cues_to_markdown(parse_vtt(vtt_text))


def self_test() -> int:
    sample = """WEBVTT

00:00:00.000 --> 00:00:03.000
Bom dia a todos,

00:00:03.000 --> 00:00:06.000
sejam muito bem-vindos à teleconferência.

00:00:06.000 --> 00:00:09.000
sejam muito bem-vindos à teleconferência.

00:01:05.000 --> 00:01:08.000
<c>Começando pelos destaques</c> do trimestre.
"""
    out = convert(sample)
    expected = (
        "[00:00] Bom dia a todos, sejam muito bem-vindos à teleconferência.\n\n"
        "[01:05] Começando pelos destaques do trimestre.\n"
    )
    if out != expected:
        sys.stderr.write("SELF-TEST FAIL\n")
        sys.stderr.write(f"--- got ---\n{out!r}\n")
        sys.stderr.write(f"--- want ---\n{expected!r}\n")
        return 1
    print("SELF-TEST OK")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", help="Path to .vtt file. Reads stdin if omitted.")
    ap.add_argument("--self-test", action="store_true", help="Run inline self-test and exit.")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            vtt_text = f.read()
    else:
        vtt_text = sys.stdin.read()
    sys.stdout.write(convert(vtt_text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
