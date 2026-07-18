#!/usr/bin/env python3
"""check_merge_requirements.py — GOV-001 Scientific Integrity Gate

For PRs touching CANONICAL/, LEDGER/CLAIMS.json, core/, modules/, or manuscript/:
require presence of a Claims Table, a Reproduction Note (exact 80-dps command line),
and a DOI-Resolvability check report.

Per AI_AUDIT_POLICY §7.
Deterministic. No LLM calls. Fail-closed on errors.
"""
import re
import subprocess
import sys

# Paths that trigger the merge requirements
PROTECTED_PREFIXES = [
    "CANONICAL/",
    "LEDGER/CLAIMS.json",
    "core/",
    "modules/",
    "manuscript/",
]

# Required sections in the PR body
REQUIRED_SECTIONS = [
    {
        "name": "Claims Table",
        "patterns": [
            r"(?i)claims?\s+table",
            r"(?i)\|\s*claim\s*\|",
            r"(?i)##\s*claims?\s+table",
        ]
    },
    {
        "name": "Reproduction Note",
        "patterns": [
            r"(?i)reproduction\s+note",
            r"(?i)reproduce",
            r"(?i)mp\.dps\s*=\s*80",
            r"(?i)80[- ]d(igit|ps)",
        ]
    },
    {
        "name": "DOI-Resolvability Check",
        "patterns": [
            r"(?i)doi[- ]resolvability",
            r"(?i)doi\s+check",
            r"(?i)citation[- ]check",
        ]
    },
]


def get_changed_files():
    """Get list of changed files from git diff. Fail closed on errors."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            result = subprocess.run(
                ["git", "diff", "HEAD~1", "--name-only"],
                capture_output=True, text=True, timeout=30
            )
        if result.returncode != 0:
            print(f"FAIL: git diff --name-only exited with code {result.returncode}: {result.stderr.strip()}")
            sys.exit(1)
        return [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except subprocess.TimeoutExpired:
        print("FAIL: git diff timed out")
        sys.exit(1)
    except FileNotFoundError:
        print("FAIL: git not found")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: unexpected error: {e}")
        sys.exit(1)


def touches_protected_paths(changed_files):
    """Check if any changed file is under a protected path."""
    for f in changed_files:
        for prefix in PROTECTED_PREFIXES:
            if f.startswith(prefix) or f == prefix.rstrip("/"):
                return True, f, prefix
    return False, None, None


def get_pr_body():
    """Get PR body from environment variable or last commit message."""
    import os
    # Try environment variable first (set by CI)
    pr_body = os.environ.get("PR_BODY", "")
    if pr_body:
        return pr_body

    # Fall back to last commit message
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%B"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass

    return ""


def check_required_sections(pr_body):
    """Check that all required sections exist in the PR body."""
    violations = []
    for section in REQUIRED_SECTIONS:
        found = False
        for pattern in section["patterns"]:
            if re.search(pattern, pr_body):
                found = True
                break
        if not found:
            violations.append(
                f"BLOCKED: missing required section '{section['name']}' in PR body/commit message"
            )
    return violations


def main():
    changed_files = get_changed_files()
    if not changed_files:
        print("OK: no changed files")
        sys.exit(0)

    touches, file_name, prefix = touches_protected_paths(changed_files)
    if not touches:
        print("OK: no protected paths touched, merge requirements not triggered")
        sys.exit(0)

    print(f"INFO: protected path triggered by '{file_name}' (prefix: '{prefix}')")

    pr_body = get_pr_body()
    if not pr_body.strip():
        print("BLOCKED: PR body is empty but protected paths are touched")
        print("BLOCKED: missing required section 'Claims Table' in PR body/commit message")
        print("BLOCKED: missing required section 'Reproduction Note' in PR body/commit message")
        print("BLOCKED: missing required section 'DOI-Resolvability Check' in PR body/commit message")
        sys.exit(1)

    violations = check_required_sections(pr_body)
    if violations:
        for v in violations:
            print(v)
        sys.exit(1)
    else:
        print("OK: all required merge sections present")
        sys.exit(0)


if __name__ == "__main__":
    main()
