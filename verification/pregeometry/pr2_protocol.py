"""Fail-closed PR-2 protocol state, precision persistence, and migration.

Scientific status: [A] only for executed software validation paths.
All interpretation of graph diagnostics remains [D/E].
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping

from mpmath import mp


REGISTRATION_PATH = Path(__file__).with_name("pr2_registration.json")
INCOMPLETE_PROTOCOL = "INCOMPLETE_PROTOCOL"
PROTOTYPE = "prototype"
PR2_OUTPUT_SCHEMA = "uidt-pregeometry-pr2-spectral-graph-diagnostics-v2"
PR2_SCHEMA_VERSION = "2"
PRECISION_DECIMAL_DIGITS = 80
EXPECTED_REGISTRATION_SHA256 = "2797e9db46f689e9f0e16b8b792494e2b2671046a92d8203a7c07e9baca0d386"


def load_frozen_registration(path: Path = REGISTRATION_PATH) -> tuple[dict[str, object], str]:
    """Load the exact registration bytes and return their SHA-256 digest."""
    raw = Path(path).read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != EXPECTED_REGISTRATION_SHA256:
        raise ValueError("Frozen PR-2 registration hash mismatch.")
    registration = json.loads(
        raw.decode("utf-8"),
        parse_float=str,
        parse_int=str,
    )
    if registration.get("registration_kind") != "retrospective":
        raise ValueError("PR-2 registration must disclose its retrospective status.")
    if registration.get("protocol_state") != PROTOTYPE:
        raise ValueError("PR-2 registration must remain prototype.")
    return registration, digest


def evaluate_protocol_components(
    registration: Mapping[str, object],
    component_status: Mapping[str, str],
) -> dict[str, object]:
    """Return a fail-closed protocol state for the declared component map."""
    required = tuple(str(item) for item in registration["required_components"])
    missing = tuple(
        component
        for component in required
        if component_status.get(component) != "executed"
    )
    return {
        "status": INCOMPLETE_PROTOCOL if missing else "registered_components_executed",
        "protocol_state": PROTOTYPE,
        "missing_components": list(missing),
    }


def assert_no_false_completion(protocol: Mapping[str, object]) -> None:
    """Reject complete-status language while any component is missing."""
    missing = tuple(protocol.get("missing_components", ()))
    status = str(protocol.get("status", ""))
    if missing and status != INCOMPLETE_PROTOCOL:
        raise ValueError("Missing PR-2 components require INCOMPLETE_PROTOCOL.")
    if status in {"preregistered_complete", "complete"}:
        raise ValueError("PR-2 cannot emit a complete status from retrospective registration.")


def serialize_mpf(value: mp.mpf, *, digits: int = PRECISION_DECIMAL_DIGITS) -> str:
    """Serialize a protected value as a decimal lexeme, never a native float."""
    if digits != PRECISION_DECIMAL_DIGITS:
        raise ValueError("Protected PR-2 persistence requires exactly 80 decimal digits.")
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        return mp.nstr(mp.mpf(value), n=digits, strip_zeros=False)


def assert_decimal_roundtrip(lexeme: str) -> None:
    """Require stable parse/serialize behavior at the protected precision."""
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        reparsed = mp.mpf(lexeme)
        if serialize_mpf(reparsed) != lexeme:
            raise ValueError("Protected decimal lexeme is not stable at 80-digit precision.")


def migrate_legacy_payload_text(payload_text: str) -> dict[str, object]:
    """Migrate legacy vocabulary while retaining numeric JSON lexemes as strings."""
    payload = json.loads(
        payload_text,
        parse_float=str,
        parse_int=str,
    )
    migrated = _rename_legacy_spectral_gap(payload)
    if not isinstance(migrated, dict):
        raise TypeError("PR-2 payload root must be a JSON object.")
    migrated["schema"] = PR2_OUTPUT_SCHEMA
    migrated["schema_version"] = PR2_SCHEMA_VERSION
    return migrated


def _rename_legacy_spectral_gap(value: object) -> object:
    if isinstance(value, list):
        return [_rename_legacy_spectral_gap(item) for item in value]
    if not isinstance(value, dict):
        return value
    if "spectral_gap" in value and "laplacian_lambda_2" in value:
        raise ValueError("Ambiguous PR-2 vocabulary: legacy and current keys coexist.")
    migrated: dict[str, object] = {}
    for key, item in value.items():
        current_key = "laplacian_lambda_2" if key == "spectral_gap" else key
        migrated[current_key] = _rename_legacy_spectral_gap(item)
    return migrated
