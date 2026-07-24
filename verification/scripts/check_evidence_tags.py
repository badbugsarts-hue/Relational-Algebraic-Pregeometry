#!/usr/bin/env python3
"""Block forbidden evidence classes and target-adjacent strong classes."""

from __future__ import annotations

import re

from git_diff_range import AddedLine, DiffRangeError, load_added_lines

INVENTED_CLASS_PATTERNS = (
    re.compile(r"\[A\+\]"),
    re.compile(r"\[B\+\]"),
    re.compile(r"\[B-\]"),
    re.compile(r"\[C\+\]"),
    re.compile(r"\[D\+\]"),
)
STRONG_CLASSES = (
    re.compile(r"\[A\]"),
    re.compile(r"\[A-\]"),
    re.compile(r"\[B\]"),
)
TARGET_LITERALS = (
    re.compile(r"16\.339", re.IGNORECASE),
    re.compile(r"49\s*/\s*3", re.IGNORECASE),
    re.compile(r"17\s*/\s*3000", re.IGNORECASE),
    re.compile(r"glueball", re.IGNORECASE),
)
PROXIMITY_WINDOW = 3


def _field(entry: AddedLine | dict[str, object], name: str, fallback: object) -> object:
    if isinstance(entry, AddedLine):
        return getattr(entry, name)
    return entry.get(name, fallback)


def check_invented_classes(
    entries: list[AddedLine] | list[dict[str, object]],
) -> list[str]:
    violations: list[str] = []
    for entry in entries:
        text = str(_field(entry, "text", ""))
        path = str(_field(entry, "file", "unknown"))
        line = int(_field(entry, "line", 0))
        for pattern in INVENTED_CLASS_PATTERNS:
            if pattern.search(text):
                violations.append(
                    f"BLOCKED: invented evidence class at {path}:{line}"
                )
    return violations


def check_proximity(
    entries: list[AddedLine] | list[dict[str, object]],
) -> list[str]:
    normalized: list[tuple[str, int, str]] = []
    for index, entry in enumerate(entries, start=1):
        normalized.append(
            (
                str(_field(entry, "file", "unknown")),
                int(_field(entry, "line", index)),
                str(_field(entry, "text", "")),
            )
        )
    violations: list[str] = []
    for path, line, text in normalized:
        if not any(pattern.search(text) for pattern in STRONG_CLASSES):
            continue
        for other_path, other_line, other_text in normalized:
            if path != other_path or abs(line - other_line) > PROXIMITY_WINDOW:
                continue
            if any(pattern.search(other_text) for pattern in TARGET_LITERALS):
                violations.append(
                    f"BLOCKED: strong evidence class within "
                    f"{PROXIMITY_WINDOW} lines of a guarded literal at "
                    f"{path}:{line}"
                )
                break
    return violations


def main() -> int:
    try:
        entries = load_added_lines()
    except DiffRangeError as exc:
        print(f"FAIL: {exc}")
        return 1
    violations = [
        *check_invented_classes(entries),
        *check_proximity(entries),
    ]
    if violations:
        print("\n".join(violations))
        return 1
    print("OK: no evidence-tag violations found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
