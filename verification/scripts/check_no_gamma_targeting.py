#!/usr/bin/env python3
"""check_no_gamma_targeting.py — GOV-001 Scientific Integrity Gate

Block any code that contains gamma-targeting patterns:
  - K_S = (Delta*/gamma), K_S = (Δ*/γ)
  - target = 16.339, target = 49/3, target = 17/3000
  - Use of these literals as loss, objective, goal, or kill_switch thresholds.

Per AI_AUDIT_POLICY §7.
Deterministic. No LLM calls. Fail-closed on errors.
"""
import re
import subprocess
import sys


# Direct targeting patterns
DIRECT_TARGET_PATTERNS = [
    (r"K_S\s*=\s*\(?\s*Delta\s*\*?\s*/\s*gamma\s*\)?", "K_S = (Delta*/gamma)"),
    (r"K_S\s*=\s*\(?\s*[ΔΔ]\s*\*?\s*/\s*[γγ]\s*\)?", "K_S = (Δ*/γ)"),
    (r"K_S\s*=\s*\(?\s*\\?Delta\s*\*?\s*/\s*\\?gamma\s*\)?", "K_S = (\\Delta*/\\gamma)"),
]

# Target literal values
TARGET_LITERALS = [
    (r"16\.339", "16.339"),
    (r"49\s*/\s*3", "49/3"),
    (r"17\s*/\s*3000", "17/3000"),
]

# Context keywords that indicate targeting behavior
TARGETING_CONTEXTS = [
    r"target",
    r"loss",
    r"objective",
    r"goal",
    r"kill[_\s]*switch",
    r"fit[_\s]*target",
    r"desired",
    r"expected[_\s]*value",
]


def get_diff_lines():
    """Get the staged or HEAD diff lines. Fail closed on errors."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--unified=0", "--no-color"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            result = subprocess.run(
                ["git", "diff", "HEAD~1", "--unified=0", "--no-color"],
                capture_output=True, text=True, timeout=30
            )
        if result.returncode != 0:
            print(f"FAIL: git diff exited with code {result.returncode}: {result.stderr.strip()}")
            sys.exit(1)
        return result.stdout
    except subprocess.TimeoutExpired:
        print("FAIL: git diff timed out")
        sys.exit(1)
    except FileNotFoundError:
        print("FAIL: git not found")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: unexpected error running git diff: {e}")
        sys.exit(1)


def parse_diff_added_lines(diff_text):
    """Extract added lines with their file context."""
    current_file = None
    entries = []
    for line in diff_text.splitlines():
        if line.startswith("diff --git"):
            parts = line.split(" b/")
            current_file = parts[-1] if len(parts) > 1 else "unknown"
        elif line.startswith("+") and not line.startswith("+++"):
            entries.append({"file": current_file, "text": line[1:]})
    return entries


def check_direct_targeting(entries):
    """Check for direct K_S targeting patterns."""
    violations = []
    for entry in entries:
        for pattern, desc in DIRECT_TARGET_PATTERNS:
            if re.search(pattern, entry["text"], re.IGNORECASE):
                violations.append(
                    f"BLOCKED: gamma-targeting pattern '{desc}' in {entry['file']}: "
                    f"{entry['text'].strip()}"
                )
    return violations


def check_literal_in_targeting_context(entries):
    """Check for target literals used in targeting contexts."""
    violations = []
    for entry in entries:
        text = entry["text"]
        for lit_pattern, lit_desc in TARGET_LITERALS:
            if re.search(lit_pattern, text):
                for ctx_pattern in TARGETING_CONTEXTS:
                    if re.search(ctx_pattern, text, re.IGNORECASE):
                        violations.append(
                            f"BLOCKED: target literal '{lit_desc}' used in "
                            f"targeting context '{ctx_pattern}' in {entry['file']}: "
                            f"{text.strip()}"
                        )
    return violations


def main():
    diff_text = get_diff_lines()
    if not diff_text.strip():
        print("OK: no diff to check")
        sys.exit(0)

    entries = parse_diff_added_lines(diff_text)
    if not entries:
        print("OK: no added lines in diff")
        sys.exit(0)

    violations = []
    violations.extend(check_direct_targeting(entries))
    violations.extend(check_literal_in_targeting_context(entries))

    if violations:
        for v in violations:
            print(v)
        sys.exit(1)
    else:
        print("OK: no gamma-targeting violations found")
        sys.exit(0)


if __name__ == "__main__":
    main()
