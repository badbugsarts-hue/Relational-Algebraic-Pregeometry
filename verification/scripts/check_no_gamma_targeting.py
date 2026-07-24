#!/usr/bin/env python3
"""Block target-shaped assignments in added PR content."""

from __future__ import annotations

import re

from git_diff_range import AddedLine, DiffRangeError, load_added_lines

DIRECT_TARGET_PATTERNS = (
    re.compile(r"K_S\s*=\s*\(?\s*Delta\s*\*?\s*/\s*gamma\s*\)?", re.I),
    re.compile(r"K_S\s*=\s*\(?\s*Δ\s*\*?\s*/\s*γ\s*\)?", re.I),
    re.compile(r"K_S\s*=\s*\(?\s*\\Delta\s*\*?\s*/\s*\\gamma\s*\)?", re.I),
)
TARGET_LITERALS = (
    re.compile(r"16\.339"),
    re.compile(r"49\s*/\s*3"),
    re.compile(r"17\s*/\s*3000"),
)
TARGETING_CONTEXTS = (
    re.compile(r"target", re.I),
    re.compile(r"loss", re.I),
    re.compile(r"objective", re.I),
    re.compile(r"goal", re.I),
    re.compile(r"kill[_\s]*switch", re.I),
    re.compile(r"fit[_\s]*target", re.I),
    re.compile(r"desired", re.I),
    re.compile(r"expected[_\s]*value", re.I),
)


def _value(entry: AddedLine | dict[str, object], key: str, default: object) -> object:
    if isinstance(entry, AddedLine):
        return getattr(entry, key)
    return entry.get(key, default)


def check_direct_targeting(
    entries: list[AddedLine] | list[dict[str, object]],
) -> list[str]:
    violations: list[str] = []
    for entry in entries:
        text = str(_value(entry, "text", ""))
        if any(pattern.search(text) for pattern in DIRECT_TARGET_PATTERNS):
            violations.append(
                f"BLOCKED: direct target-shaped assignment at "
                f"{_value(entry, 'file', 'unknown')}:"
                f"{_value(entry, 'line', 0)}"
            )
    return violations


def check_literal_in_targeting_context(
    entries: list[AddedLine] | list[dict[str, object]],
) -> list[str]:
    violations: list[str] = []
    for entry in entries:
        text = str(_value(entry, "text", ""))
        if not any(pattern.search(text) for pattern in TARGET_LITERALS):
            continue
        if any(pattern.search(text) for pattern in TARGETING_CONTEXTS):
            violations.append(
                f"BLOCKED: guarded literal used in targeting context at "
                f"{_value(entry, 'file', 'unknown')}:"
                f"{_value(entry, 'line', 0)}"
            )
    return violations


def main() -> int:
    try:
        entries = load_added_lines()
    except DiffRangeError as exc:
        print(f"FAIL: {exc}")
        return 1
    violations = [
        *check_direct_targeting(entries),
        *check_literal_in_targeting_context(entries),
    ]
    if violations:
        print("\n".join(violations))
        return 1
    print("OK: no gamma-targeting violations found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
