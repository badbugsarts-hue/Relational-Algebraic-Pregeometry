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


def get_added_files():
    """Get list of added files from git diff. Fail closed on errors."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-status", "--no-renames"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            result = subprocess.run(
                ["git", "diff", "HEAD~1", "--name-status", "--no-renames"],
                capture_output=True, text=True, timeout=30
            )
        if result.returncode != 0:
            print(f"FAIL: git diff exited with code {result.returncode}: {result.stderr.strip()}")
            sys.exit(1)

        added = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t", 1)
            if len(parts) < 2:
                continue
            status, filepath = parts[0].strip(), parts[1].strip()
            if status in ("A", "C"):
                added.append(filepath)
            elif status == "M":
                # Modified files under protected paths are also blocked
                added.append(filepath)
        return added
    except subprocess.TimeoutExpired:
        print("FAIL: git diff timed out")
        sys.exit(1)
    except FileNotFoundError:
        print("FAIL: git not found")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: unexpected error: {e}")
        sys.exit(1)


def check_protected_dirs(files):
    """Check for files under protected directories."""
    violations = []
    for f in files:
        for prefix in PROTECTED_DIR_PREFIXES:
            if f.startswith(prefix):
                if f in ALLOWED_EXCEPTIONS:
                    continue
                # Special case: LOCAL/ exception
                if prefix == "LOCAL/" and f == "LOCAL/uidt-repo.cfg":
                    continue
                violations.append(
                    f"BLOCKED: file under protected path '{prefix}': {f}"
                )
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


def main():
    files = get_added_files()
    if not files:
        print("OK: no files to check")
        sys.exit(0)

    violations = []
    violations.extend(check_protected_dirs(files))
    violations.extend(check_forbidden_filenames(files))

    if violations:
        for v in violations:
            print(v)
        sys.exit(1)
    else:
        print("OK: no protected-path violations found")
        sys.exit(0)


if __name__ == "__main__":
    main()
