#!/usr/bin/env python3
"""Monday Morning Punchlines -- entry program.

Writes one joke about Monday mornings to the output directory's
entry.txt for the judge to read. Standard library only, no network,
no input files, deterministic output: the same joke, the same bytes,
every run.

The output directory is taken from MAKEFUN_OUTPUT_DIR first, then
OUTPUT_DIR, then the grader's default /output, so the entry works
both in the sandbox harness and in a local run.
"""

import os

LINE = "Monday morning my bed sent a calendar invite for 6am. I declined. We'll reschedule for Friday."

MAX_CHARS = 200


def resolve_output_dir() -> str:
    """Pick where entry.txt goes.

    MAKEFUN_OUTPUT_DIR wins, then OUTPUT_DIR, then the grader's
    default /output. An empty variable counts as unset, so a stray
    empty export can never send the entry to a relative path.
    """
    for var in ("MAKEFUN_OUTPUT_DIR", "OUTPUT_DIR"):
        value = os.environ.get(var)
        if value:
            return value
    return "/output"


def _check_length(entry: str) -> None:
    # len() counts Unicode code points, which is what the gate's
    # "1 to 200 characters" means -- not bytes. This entry is pure
    # ASCII, so code points and bytes agree here, but the check stays
    # correct if the joke ever gains a non-ASCII character.
    if not 1 <= len(entry) <= MAX_CHARS:
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(entry)}"
        )


def _check_single_line(entry: str) -> None:
    if not entry.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")


def validate(entry: str) -> None:
    """Fail loudly if the entry ever stops meeting the gate.

    The gate requires UTF-8 text of 1 to 200 characters, not only
    whitespace, and the brief requires a single short funny line.
    Each rule is its own check so a failure names the rule it broke.
    """
    _check_length(entry)
    _check_single_line(entry)


def write_entry(path: str, entry: str) -> None:
    """Write the entry with no trailing newline, creating the
    output directory if the harness has not made it yet."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry)


def verify_written(path: str, entry: str) -> None:
    """Read the file back and refuse to pass on any mismatch, so a
    bad write can never silently reach the judge."""
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != entry:
        raise ValueError("entry.txt does not match the entry line")


def main() -> int:
    validate(LINE)
    output_path = os.path.join(resolve_output_dir(), "entry.txt")
    write_entry(output_path, LINE)
    verify_written(output_path, LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
