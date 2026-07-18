#!/usr/bin/env python3
"""check_evidence_tags.py — GOV-001 Scientific Integrity Gate

Block any diff that:
  1. Introduces [A], [A-], or [B] within three lines of target literals
     (16.339, 49/3, 49 / 3, 17/3000, glueball).
  2. Contains invented evidence classes ([A+], [B+], [B-], [C+], [D+]).

Per AI_AUDIT_POLICY §7.
Deterministic. No LLM calls. Fail-closed on errors.
"""
import re
import subprocess
import sys

# Valid evidence classes
VALID_CLASSES = {"[A]", "[A-]", "[B]", "[C]", "[D]", "[E]"}

# Invented / forbidden classes (regex patterns)
INVENTED_CLASS_PATTERNS = [
    r"\[A\+\]",
    r"\[B\+\]",
    r"\[B-\]",
    r"\[C\+\]",
    r"\[D\+\]",
]

# Strong evidence classes that must not appear near target literals
STRONG_CLASSES = [r"\[A\]", r"\[A-\]", r"\[B\]"]

# Target literals that must not appear near strong evidence classes
TARGET_LITERALS = [
    r"16\.339",
    r"49/3",
    r"49\s*/\s*3",
    r"17/3000",
    r"glueball",
]

PROXIMITY_WINDOW = 3  # lines


def get_diff_lines():
    """Get the staged or HEAD diff lines. Fail closed on errors."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--unified=0", "--no-color"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            # Try HEAD diff as fallback
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
    """Extract added lines with their file and approximate line number."""
    current_file = None
    entries = []
    for line in diff_text.splitlines():
        if line.startswith("diff --git"):
            parts = line.split(" b/")
            current_file = parts[-1] if len(parts) > 1 else "unknown"
        elif line.startswith("+") and not line.startswith("+++"):
            entries.append({"file": current_file, "text": line[1:]})
    return entries


def check_invented_classes(entries):
    """Check for invented evidence classes."""
    violations = []
    for i, entry in enumerate(entries):
        for pattern in INVENTED_CLASS_PATTERNS:
            if re.search(pattern, entry["text"]):
                violations.append(
                    f"BLOCKED: invented evidence class {pattern} in {entry['file']}: {entry['text'].strip()}"
                )
    return violations


def check_proximity(entries):
    """Check for strong evidence classes near target literals."""
    violations = []
    for i, entry in enumerate(entries):
        for cls_pattern in STRONG_CLASSES:
            if re.search(cls_pattern, entry["text"]):
                # Check surrounding lines within window
                window_start = max(0, i - PROXIMITY_WINDOW)
                window_end = min(len(entries), i + PROXIMITY_WINDOW + 1)
                for j in range(window_start, window_end):
                    if j == i:
                        continue
                    for target in TARGET_LITERALS:
                        if re.search(target, entries[j]["text"], re.IGNORECASE):
                            violations.append(
                                f"BLOCKED: {cls_pattern} within {PROXIMITY_WINDOW} lines of "
                                f"'{target}' in {entry['file']}: "
                                f"class line='{entry['text'].strip()}', "
                                f"target line='{entries[j]['text'].strip()}'"
                            )
                # Also check same line
                for target in TARGET_LITERALS:
                    if re.search(target, entry["text"], re.IGNORECASE):
                        violations.append(
                            f"BLOCKED: {cls_pattern} on same line as '{target}' "
                            f"in {entry['file']}: {entry['text'].strip()}"
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
    violations.extend(check_invented_classes(entries))
    violations.extend(check_proximity(entries))

    if violations:
        for v in violations:
            print(v)
        sys.exit(1)
    else:
        print("OK: no evidence-tag violations found")
        sys.exit(0)


if __name__ == "__main__":
    main()
