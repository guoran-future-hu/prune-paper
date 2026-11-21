#!/usr/bin/env python3
"""
Split a markdown academic paper into three files:
  -pruned.md   — body before the reference section
  -reference.md — the reference/bibliography section
  -appendix.md  — everything after the reference section

Logic: find the reference heading, split there. Everything after the
reference list (next same/higher‑level heading → EOF) goes to appendix.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^(#+)\s+(.*)")

# Reference / bibliography headings — case-insensitive
REF_RE = re.compile(
    r"^(?:\d+\.?\s*)?(?:"
    r"References?(?:\s+(?:and|&)\s+Notes?)?|"
    r"Bibliography|Bibliograph(?:ic|y)\s+References?|Selected\s+Bibliography|"
    r"Works?\s+[Cc]ited|Literature\s+[Cc]ited|"
    r"Citations?|Sources?|"
    r"Notes?(?:\s+(?:and|&)\s+References?)?|"
    r"Reference\s+List|Reference\s+Notes?|"
    r"Further\s+Reading"
    r")\s*$",
    re.IGNORECASE,
)


def parse_headings(lines: list[str]) -> list[dict]:
    """Return list of {idx, level, text} for every heading line."""
    headings = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m:
            headings.append({
                "idx": i,
                "level": len(m.group(1)),
                "text": m.group(2).strip(),
            })
    return headings


def find_ref(headings: list[dict]) -> int | None:
    """Return index into `headings` of the reference heading, or None."""
    for i, h in enumerate(headings):
        if REF_RE.match(h["text"]):
            return i
    return None


def section_end(headings: list[dict], start_i: int, level: int) -> int | None:
    """Line index of first heading after `start_i` that ends the section.

    Ends at next heading whose level <= `level`. For level-1 (H1) references,
    also ends at level-2 headings (standard section level in papers).
    Returns None if section runs to EOF."""
    cutoff = max(level, 2)
    for i in range(start_i + 1, len(headings)):
        if headings[i]["level"] <= cutoff:
            return headings[i]["idx"]
    return None


def split_paper(input_path: Path, stem: str | None = None) -> dict:
    if stem is None:
        stem = input_path.stem

    text = input_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    headings = parse_headings(lines)

    ref_hi = find_ref(headings)

    if ref_hi is None:
        # No references found — everything stays in -pruned
        parent = input_path.parent
        pruned_path = parent / f"{stem}-pruned.md"
        ref_path = parent / f"{stem}-reference.md"
        appdx_path = parent / f"{stem}-appendix.md"

        pruned_path.write_text(text, encoding="utf-8")
        ref_path.write_text("<!-- No reference section found -->\n", encoding="utf-8")
        appdx_path.write_text("<!-- No appendix (no reference section to split after) -->\n", encoding="utf-8")

        return {
            "pruned_path": pruned_path,
            "ref_path": ref_path,
            "appdx_path": appdx_path,
            "report": (
                f"Input:  {input_path} ({len(lines)} lines)\n"
                f"pruned: {pruned_path} ({len(lines)} lines)\n"
                f"ref:    {ref_path} (0 lines)\n"
                f"appdx:  {appdx_path} (0 lines)\n\n"
                "⚠ No reference section detected. Entire paper left in -pruned.md."
            ),
        }

    ref_start = headings[ref_hi]["idx"]
    ref_level = headings[ref_hi]["level"]
    ref_end = section_end(headings, ref_hi, ref_level)  # next same/higher heading

    # ── Three-way split ──────────────────────────────────────────
    # -pruned:   everything BEFORE the reference heading
    # -reference: reference heading → next same/higher heading (or EOF)
    # -appendix:  everything AFTER the reference section ends

    pruned_content = "".join(lines[:ref_start])

    if ref_end is None:
        # References go to EOF, no appendix
        ref_content = "".join(lines[ref_start:])
        appdx_content = "<!-- No appendix (reference section runs to EOF) -->\n"
        ref_lines = len(lines) - ref_start
        appdx_lines = 0
    else:
        ref_content = "".join(lines[ref_start:ref_end])
        appdx_content = "".join(lines[ref_end:])
        ref_lines = ref_end - ref_start
        appdx_lines = len(lines) - ref_end

    parent = input_path.parent
    pruned_path = parent / f"{stem}-pruned.md"
    ref_path = parent / f"{stem}-reference.md"
    appdx_path = parent / f"{stem}-appendix.md"

    pruned_path.write_text(pruned_content, encoding="utf-8")
    ref_path.write_text(ref_content, encoding="utf-8")
    appdx_path.write_text(appdx_content, encoding="utf-8")

    report = [
        f"Input:  {input_path} ({len(lines)} lines)",
        f"pruned: {pruned_path} ({len(lines[:ref_start])} lines)",
        f"ref:    {ref_path} ({ref_lines} lines)",
        f"appdx:  {appdx_path} ({appdx_lines} lines)",
    ]

    return {
        "pruned_path": pruned_path,
        "ref_path": ref_path,
        "appdx_path": appdx_path,
        "report": "\n".join(report),
    }


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <paper.md> [output_stem]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    stem = sys.argv[2] if len(sys.argv) > 2 else None
    result = split_paper(input_path, stem)
    print(result["report"])


if __name__ == "__main__":
    main()
