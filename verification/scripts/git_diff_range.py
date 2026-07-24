#!/usr/bin/env python3
"""Fail-closed Git range loading for scientific-integrity checks."""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass

SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
HUNK_RE = re.compile(rb"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
ALL_STATUS_FILTER = "ACDMRTUXB"
ADDED_CONTENT_FILTER = "ACMRTUXB"


class DiffRangeError(RuntimeError):
    """Raised when the requested PR range cannot be inspected exactly."""


@dataclass(frozen=True)
class Change:
    status: str
    paths: tuple[str, ...]


@dataclass(frozen=True)
class AddedLine:
    file: str
    line: int
    text: str


def _run_git(arguments: list[str]) -> bytes:
    try:
        result = subprocess.run(
            ["git", *arguments],
            check=False,
            capture_output=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise DiffRangeError(f"git execution failed: {exc}") from exc
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise DiffRangeError(
            f"git {' '.join(arguments)} exited {result.returncode}: {stderr}"
        )
    return result.stdout


def _decode(value: bytes, context: str) -> str:
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DiffRangeError(f"non-UTF-8 {context}: {exc}") from exc


def require_range() -> tuple[str, str]:
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "")
    if not SHA_RE.fullmatch(base) or not SHA_RE.fullmatch(head):
        raise DiffRangeError(
            "BASE_SHA and HEAD_SHA must be explicit 40-character hexadecimal SHAs"
        )
    if base.lower() == head.lower():
        raise DiffRangeError("unexpectedly empty PR range: BASE_SHA equals HEAD_SHA")
    for label, value in (("BASE_SHA", base), ("HEAD_SHA", head)):
        _run_git(["cat-file", "-e", f"{value}^{{commit}}"])
        actual_sha = _decode(
            _run_git(["rev-parse", f"{value}^{{commit}}"]),
            label,
        ).strip()
        if actual_sha.lower() != value.lower():
            raise DiffRangeError(f"{label} did not resolve to the supplied commit")
    changes = load_changes(base, head)
    if not changes:
        raise DiffRangeError("unexpectedly empty PR range")
    return base, head


def parse_name_status_z(payload: bytes) -> list[Change]:
    if not payload or not payload.endswith(b"\0"):
        raise DiffRangeError("malformed NUL-delimited name-status payload")
    fields = payload[:-1].split(b"\0")
    changes: list[Change] = []
    cursor = 0
    while cursor < len(fields):
        status = _decode(fields[cursor], "status field")
        cursor += 1
        if not re.fullmatch(r"[ACDMRTUXB](?:\d{1,3})?", status):
            raise DiffRangeError(f"malformed Git status field: {status!r}")
        path_count = 2 if status[0] in {"R", "C"} else 1
        if cursor + path_count > len(fields):
            raise DiffRangeError(f"truncated path record for status {status}")
        paths = tuple(
            _decode(field, "path field")
            for field in fields[cursor : cursor + path_count]
        )
        if any(not path for path in paths):
            raise DiffRangeError(f"empty path in status record {status}")
        cursor += path_count
        changes.append(Change(status=status, paths=paths))
    return changes


def load_changes(base: str, head: str) -> list[Change]:
    payload = _run_git(
        [
            "diff",
            "--name-status",
            "-z",
            "--find-renames",
            "--find-copies",
            f"--diff-filter={ALL_STATUS_FILTER}",
            base,
            head,
            "--",
        ]
    )
    return parse_name_status_z(payload)


def _parse_added_patch(payload: bytes) -> list[AddedLine]:
    binary_notice = b"Binary" + b" files "
    binary_patch = b"GIT" + b" binary patch"
    if binary_notice in payload or binary_patch in payload:
        raise DiffRangeError("binary added content cannot be inspected")
    entries: list[AddedLine] = []
    current_file: str | None = None
    new_line: int | None = None
    for raw_line in payload.splitlines():
        if raw_line.startswith(b"diff --git "):
            current_file = None
            new_line = None
            continue
        if raw_line.startswith(b"+++ "):
            path = _decode(raw_line[4:], "patch path")
            if path == "/dev/null":
                current_file = None
            elif path.startswith("b/"):
                current_file = path[2:]
            else:
                raise DiffRangeError(f"malformed patch path: {path!r}")
            continue
        if raw_line.startswith(b"@@ "):
            match = HUNK_RE.match(raw_line)
            if not match or current_file is None:
                raise DiffRangeError("malformed unified-diff hunk")
            new_line = int(match.group(1))
            continue
        if new_line is None:
            continue
        if raw_line.startswith(b"+"):
            entries.append(
                AddedLine(
                    file=current_file or "",
                    line=new_line,
                    text=_decode(raw_line[1:], "added line"),
                )
            )
            new_line += 1
        elif raw_line.startswith(b"-"):
            continue
        elif raw_line.startswith(b" "):
            new_line += 1
        elif raw_line == rb"\ No newline at end of file":
            continue
        else:
            raise DiffRangeError("malformed unified-diff content")
    return entries


def load_added_lines() -> list[AddedLine]:
    base, head = require_range()
    payload = _run_git(
        [
            "diff",
            "--no-ext-diff",
            "--no-color",
            "--unified=3",
            f"--diff-filter={ADDED_CONTENT_FILTER}",
            base,
            head,
            "--",
        ]
    )
    return _parse_added_patch(payload)


def load_changed_paths() -> list[str]:
    base, head = require_range()
    paths: list[str] = []
    for change in load_changes(base, head):
        paths.extend(change.paths)
    return paths
