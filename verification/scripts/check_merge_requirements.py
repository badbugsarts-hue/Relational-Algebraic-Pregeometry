#!/usr/bin/env python3
"""Require governance sections when a PR touches scientific authority paths."""

from __future__ import annotations

import os
import re

from git_diff_range import DiffRangeError, load_changed_paths

PROTECTED_PREFIXES = (
    "CANONICAL/",
    "LEDGER/CLAIMS.json",
    "core/",
    "modules/",
    "manuscript/",
)
REQUIRED_SECTIONS = (
    (
        "Claims Table",
        (
            re.compile(r"claims?\s+table", re.I),
            re.compile(r"\|\s*claim\s*\|", re.I),
        ),
    ),
    (
        "Reproduction Note",
        (
            re.compile(r"reproduction\s+note", re.I),
            re.compile(r"80[- ]d(?:igit|ps)", re.I),
            re.compile(r"mp\.dps\s*=\s*80", re.I),
        ),
    ),
    (
        "DOI-Resolvability Check",
        (
            re.compile(r"doi[- ]resolvability", re.I),
            re.compile(r"doi\s+check", re.I),
            re.compile(r"citation[- ]check", re.I),
        ),
    ),
)


def touches_protected_paths(
    changed_files: list[str],
) -> tuple[bool, str | None, str | None]:
    for path in changed_files:
        for prefix in PROTECTED_PREFIXES:
            if path == prefix.rstrip("/") or path.startswith(prefix):
                return True, path, prefix
    return False, None, None


def check_required_sections(pr_body: str) -> list[str]:
    violations: list[str] = []
    for name, patterns in REQUIRED_SECTIONS:
        if not any(pattern.search(pr_body) for pattern in patterns):
            violations.append(f"BLOCKED: missing required section '{name}'")
    return violations


def main() -> int:
    try:
        changed_files = load_changed_paths()
    except DiffRangeError as exc:
        print(f"FAIL: {exc}")
        return 1
    touches, path, prefix = touches_protected_paths(changed_files)
    if not touches:
        print("OK: no authority path touched")
        return 0
    print(f"INFO: authority path triggered by {path!r} ({prefix!r})")
    pr_body = os.environ.get("PR_BODY", "")
    if not pr_body.strip():
        print("BLOCKED: PR_BODY is missing or empty")
        return 1
    violations = check_required_sections(pr_body)
    if violations:
        print("\n".join(violations))
        return 1
    print("OK: all required merge sections present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
