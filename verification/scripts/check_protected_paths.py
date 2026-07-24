#!/usr/bin/env python3
"""check_protected_paths.py — GOV-001 Scientific Integrity Gate

Block any commit that adds files under protected agent/secret directories or
adds secret/credential filenames.

Per AI_AUDIT_POLICY §7.
Deterministic. No LLM calls. Fail-closed on errors.
"""
import re
import subprocess
import sys

# Protected directory prefixes — files must not be added under these
PROTECTED_DIR_PREFIXES = [
    "UIDT-OS/",
    "LOCAL/",
    ".claude/",
    ".trae/",
    ".kiro/",
    ".antigravity/",
    ".cursor/",
    ".kilo/",
    ".kilocode/",
    ".auxly/",
    ".traycer/",
    ".venv/",
]

# Exception: LOCAL/uidt-repo.cfg is allowed per .gitignore
ALLOWED_EXCEPTIONS = [
    "LOCAL/uidt-repo.cfg",
]

# Forbidden filenames (exact match or pattern)
FORBIDDEN_FILENAMES = [
    ".env",
    ".env.local",
    "credentials.json",
    "config.local.yaml",
]

# Forbidden file extensions
FORBIDDEN_EXTENSIONS = [
    ".key",
    ".pem",
]

from git_diff_range import DiffRangeError, load_changed_paths


def check_protected_dirs(files: list[str]) -> list[str]:
    violations: list[str] = []
    for path in files:
        if path in ALLOWED_EXCEPTIONS:
            continue
        for prefix in PROTECTED_DIR_PREFIXES:
            if path.startswith(prefix):
                violations.append(
                    f"BLOCKED: file under protected path {prefix!r}: {path}"
                )
                break
    return violations


def check_forbidden_filenames(files):
    """Check for forbidden credential/secret filenames."""
    violations = []
    for f in files:
        import os
        basename = os.path.basename(f)

        # Check exact filename matches
        if basename in FORBIDDEN_FILENAMES:
            violations.append(
                f"BLOCKED: forbidden filename '{basename}': {f}"
            )
            continue

        # Check forbidden extensions
        for ext in FORBIDDEN_EXTENSIONS:
            if basename.endswith(ext):
                violations.append(
                    f"BLOCKED: forbidden file extension '{ext}': {f}"
                )
                break

    return violations


def main() -> int:
    try:
        files = load_changed_paths()
    except DiffRangeError as exc:
        print(f"FAIL: {exc}")
        return 1
    violations = [
        *check_protected_dirs(files),
        *check_forbidden_filenames(files),
    ]
    if violations:
        print("\n".join(violations))
        return 1
    print("OK: no protected-path violations found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
