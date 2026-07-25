#!/usr/bin/env python3
r"""Parser-aware census for RAP manuscript evidence markers.

The scanner counts semantic ``\catmark{...}`` calls, records source identity
and exact locations, and fails closed for malformed calls or unknown
qualifiers. TeX comments, escaped pseudo-invocations, command definitions, and
verbatim-like environments are excluded. Git comparisons always load the
actual base and head blobs supplied by the caller.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

LEGAL_CLASSES = ("A-", "A", "B", "C", "D", "E")
VERBATIM_ENVS = ("verbatim", "Verbatim", "lstlisting", "minted")
SPACING_RE = re.compile(r"(?:\\[,;:!]|\\quad|\\qquad|\\\s|\s)+")
PENDING_RE = re.compile(r"^(?:pending|\\(?:text|mathrm)\{\s*pending\s*\})$")
DEFINITION_BRACED_RE = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand)\s*\{\s*$"
)
DEFINITION_UNBRACED_RE = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand)\s*$"
)
FULL_SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")


class CensusError(ValueError):
    """Raised when a catmark or source identity is invalid."""


@dataclass(frozen=True)
class Occurrence:
    evidence_class: str
    qualifier: str | None
    line: int
    column: int
    raw_argument: str


def git_blob_id(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload, usedforsecurity=False).hexdigest()


def _mask_verbatim(text: str) -> str:
    masked = text
    for env in VERBATIM_ENVS:
        begin = rf"\\begin\{{{re.escape(env)}\}}"
        end = rf"\\end\{{{re.escape(env)}\}}"
        if len(re.findall(begin, masked)) != len(re.findall(end, masked)):
            raise CensusError(f"Unbalanced verbatim-like environment: {env}")
        pattern = re.compile(f"{begin}.*?{end}", flags=re.DOTALL)
        masked = pattern.sub(
            lambda match: "\n" * match.group(0).count("\n"),
            masked,
        )
    return masked


def _strip_comments(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines(keepends=True):
        cut = None
        for index, character in enumerate(line):
            if character != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                cut = index
                break
        if cut is None:
            out.append(line)
        else:
            newline = "\n" if line.endswith("\n") else ""
            out.append(line[:cut] + newline)
    return "".join(out)


def _balanced_argument(text: str, open_brace: int) -> tuple[str, int]:
    depth = 0
    cursor = open_brace
    start = open_brace + 1
    while cursor < len(text):
        character = text[cursor]
        if character == "\\":
            cursor += 2
            continue
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return text[start:cursor], cursor + 1
        cursor += 1
    raise CensusError(f"Unclosed \\catmark argument at byte offset {open_brace}")


def _classify(argument: str) -> tuple[str, str | None]:
    raw = argument.strip()
    for evidence_class in LEGAL_CLASSES:
        if not raw.startswith(evidence_class):
            continue
        if evidence_class == "A" and raw.startswith("A-"):
            continue
        suffix = raw[len(evidence_class) :]
        normalized = SPACING_RE.sub("", suffix)
        if normalized == "":
            return evidence_class, None
        if PENDING_RE.fullmatch(normalized):
            return evidence_class, "pending"
        raise CensusError(f"Unknown qualifier in \\catmark{{{argument}}}")
    raise CensusError(f"Unknown evidence class in \\catmark{{{argument}}}")


def _is_escaped(text: str, command_start: int) -> bool:
    preceding = 0
    cursor = command_start - 1
    while cursor >= 0 and text[cursor] == "\\":
        preceding += 1
        cursor -= 1
    return preceding % 2 == 1


def _is_command_definition(
    text: str, command_start: int, command_end: int
) -> bool:
    line_start = text.rfind("\n", 0, command_start) + 1
    prefix = text[line_start:command_start]
    suffix = text[command_end:]
    if DEFINITION_BRACED_RE.search(prefix):
        return bool(re.match(r"\s*\}\s*(?:\[\s*\d+\s*\])?", suffix))
    if DEFINITION_UNBRACED_RE.search(prefix):
        return bool(re.match(r"\s*(?:\[\s*\d+\s*\])?", suffix))
    return False


def scan(text: str) -> list[Occurrence]:
    prepared = _strip_comments(_mask_verbatim(text))
    occurrences: list[Occurrence] = []
    command = "\\catmark"
    position = 0
    while True:
        index = prepared.find(command, position)
        if index < 0:
            break
        command_end = index + len(command)
        if _is_escaped(prepared, index):
            position = command_end
            continue
        if command_end < len(prepared) and (
            prepared[command_end].isalpha() or prepared[command_end] == "@"
        ):
            position = command_end
            continue
        if _is_command_definition(prepared, index, command_end):
            position = command_end
            continue
        cursor = command_end
        while cursor < len(prepared) and prepared[cursor].isspace():
            cursor += 1
        if cursor >= len(prepared) or prepared[cursor] != "{":
            raise CensusError(
                f"Malformed \\catmark at byte offset {index}: missing '{{'"
            )
        argument, end = _balanced_argument(prepared, cursor)
        evidence_class, qualifier = _classify(argument)
        line = prepared.count("\n", 0, index) + 1
        previous_newline = prepared.rfind("\n", 0, index)
        column = index - previous_newline
        occurrences.append(
            Occurrence(
                evidence_class=evidence_class,
                qualifier=qualifier,
                line=line,
                column=column,
                raw_argument=argument,
            )
        )
        position = end
    return occurrences


def report_payload(label: str, payload: bytes) -> dict[str, object]:
    text = payload.decode("utf-8")
    source_sha256 = hashlib.sha256(payload).hexdigest()
    source_blob = git_blob_id(payload)
    classes: Counter[str] = Counter()
    qualifiers: Counter[str] = Counter()
    rows: list[dict[str, object]] = []
    for occurrence in scan(text):
        classes[occurrence.evidence_class] += 1
        if occurrence.qualifier:
            qualifiers[
                f"{occurrence.evidence_class}:{occurrence.qualifier}"
            ] += 1
        row = asdict(occurrence)
        row.update(
            {
                "file": label,
                "source_sha256": source_sha256,
                "source_blob": source_blob,
            }
        )
        rows.append(row)
    return {
        "source": {
            "file": label,
            "sha256": source_sha256,
            "git_blob_sha1": source_blob,
            "bytes": len(payload),
        },
        "classes": {
            evidence_class: classes.get(evidence_class, 0)
            for evidence_class in LEGAL_CLASSES
        },
        "qualifiers": dict(sorted(qualifiers.items())),
        "total": len(rows),
        "occurrences": rows,
        "malformed": [],
    }


def report(paths: Iterable[Path]) -> dict[str, object]:
    path_list = list(paths)
    if len(path_list) != 1:
        raise CensusError("Exactly one source file is required per census report")
    path = path_list[0]
    return report_payload(path.as_posix(), path.read_bytes())


def _location_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        row["evidence_class"],
        row["qualifier"],
        row["line"],
        row["column"],
        row["raw_argument"],
    )


def compare_payloads(
    base_label: str,
    base_payload: bytes,
    head_label: str,
    head_payload: bytes,
) -> dict[str, object]:
    base = report_payload(base_label, base_payload)
    head = report_payload(head_label, head_payload)
    base_locations = Counter(_location_key(row) for row in base["occurrences"])
    head_locations = Counter(_location_key(row) for row in head["occurrences"])

    def expand(counter: Counter[tuple[object, ...]]) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for key, count in sorted(counter.items(), key=lambda item: repr(item[0])):
            evidence_class, qualifier, line, column, raw_argument = key
            rows.extend(
                {
                    "evidence_class": evidence_class,
                    "qualifier": qualifier,
                    "line": line,
                    "column": column,
                    "raw_argument": raw_argument,
                }
                for _ in range(count)
            )
        return rows

    count_delta = {
        evidence_class: head["classes"][evidence_class]
        - base["classes"][evidence_class]
        for evidence_class in LEGAL_CLASSES
    }
    added = expand(head_locations - base_locations)
    removed = expand(base_locations - head_locations)
    return {
        "base": base,
        "head": head,
        "conservation": {
            "count_delta": count_delta,
            "counts_equal": all(delta == 0 for delta in count_delta.values()),
            "locations_equal": not added and not removed,
            "same_count_locations_changed": (
                all(delta == 0 for delta in count_delta.values())
                and bool(added or removed)
            ),
            "added_occurrences": added,
            "removed_occurrences": removed,
        },
    }


def _git_payload(revision: str, path: str) -> bytes:
    if not FULL_SHA_RE.fullmatch(revision):
        raise CensusError(f"Git revision must be a full 40-hex SHA: {revision}")
    verify = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}^{{commit}}"],
        capture_output=True,
    )
    if verify.returncode != 0:
        raise CensusError(f"Unavailable Git commit: {revision}")
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        capture_output=True,
    )
    if completed.returncode != 0:
        raise CensusError(
            f"Unavailable source at {revision}:{path}: "
            f"{completed.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return completed.stdout


def write_locations(path: Path, result: dict[str, object]) -> None:
    fields = (
        "file",
        "line",
        "column",
        "raw_argument",
        "evidence_class",
        "qualifier",
        "source_blob",
        "source_sha256",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result["occurrences"])


def validate_baseline(
    result: dict[str, object], baseline_path: Path
) -> list[str]:
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if result["source"]["git_blob_sha1"] != baseline.get("git_blob_sha1"):
        errors.append("baseline source blob mismatch")
    if result["source"]["sha256"] != baseline.get("sha256"):
        errors.append("baseline SHA-256 mismatch")
    if result["classes"] != baseline.get("classes"):
        errors.append("baseline class census mismatch")
    if result["qualifiers"] != baseline.get("qualifiers"):
        errors.append("baseline qualifier census mismatch")
    return errors


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--expect-e", type=int)
    parser.add_argument("--baseline-manifest", type=Path)
    parser.add_argument("--locations-csv", type=Path)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--git-base")
    parser.add_argument("--git-head")
    parser.add_argument("--git-path")
    parser.add_argument("--base-locations-csv", type=Path)
    parser.add_argument("--head-locations-csv", type=Path)
    parser.add_argument("--require-conservation", action="store_true")
    args = parser.parse_args(argv)
    try:
        git_mode = any((args.git_base, args.git_head, args.git_path))
        if git_mode:
            if not all((args.git_base, args.git_head, args.git_path)):
                raise CensusError(
                    "--git-base, --git-head, and --git-path are jointly required"
                )
            if args.files:
                raise CensusError("File arguments cannot be mixed with Git mode")
            result = compare_payloads(
                f"{args.git_base}:{args.git_path}",
                _git_payload(args.git_base, args.git_path),
                f"{args.git_head}:{args.git_path}",
                _git_payload(args.git_head, args.git_path),
            )
            if args.base_locations_csv:
                write_locations(args.base_locations_csv, result["base"])
            if args.head_locations_csv:
                write_locations(args.head_locations_csv, result["head"])
            if args.baseline_manifest:
                baseline_errors = validate_baseline(
                    result["base"], args.baseline_manifest
                )
                if baseline_errors:
                    result["baseline_errors"] = baseline_errors
            if args.require_conservation and (
                not result["conservation"]["counts_equal"]
                or not result["conservation"]["locations_equal"]
            ):
                result["conservation_errors"] = [
                    "base/head evidence-marker conservation failed"
                ]
        else:
            result = report(args.files)
            if args.locations_csv:
                write_locations(args.locations_csv, result)
            if args.expect_e is not None and result["classes"]["E"] != args.expect_e:
                if args.output_json:
                    args.output_json.parent.mkdir(parents=True, exist_ok=True)
                    args.output_json.write_text(
                        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8",
                    )
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return 1
            if args.baseline_manifest:
                baseline_errors = validate_baseline(result, args.baseline_manifest)
                if baseline_errors:
                    result["baseline_errors"] = baseline_errors
                    if args.output_json:
                        args.output_json.parent.mkdir(parents=True, exist_ok=True)
                        args.output_json.write_text(
                            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8",
                        )
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                    return 1
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        CensusError,
    ) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), flush=True)
        return 2

    serialized = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    if result.get("baseline_errors") or result.get("conservation_errors"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
