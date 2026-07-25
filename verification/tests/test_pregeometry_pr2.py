"""Static and deterministic tests for PR-2 spectral graph diagnostics.

Status: [A] for software invariant checks.
"""

import json
from pathlib import Path
import subprocess
import sys

from mpmath import mp
from verification.pregeometry.null_ensembles import pr0_state_trace
from verification.pregeometry.pr2_protocol import (
    INCOMPLETE_PROTOCOL,
    EXPECTED_REGISTRATION_SHA256,
    PRECISION_DECIMAL_DIGITS,
    assert_decimal_roundtrip,
    assert_no_false_completion,
    evaluate_protocol_components,
    load_frozen_registration,
    migrate_legacy_payload_text,
    serialize_mpf,
)
from verification.pregeometry.spectral_diagnostics import (
    combinatorial_laplacian_spectrum,
    compute_laplacian_lambda_2,
    random_walk_return_probabilities
)
from verification.pregeometry.observer_stability import verify_relabeling_invariance

def test_spectral_diagnostics_deterministic():
    """Ensure spectral properties are fully deterministic for PR-0 trace."""
    state = pr0_state_trace(15)[-1]
    
    spectrum_1 = combinatorial_laplacian_spectrum(state)
    spectrum_2 = combinatorial_laplacian_spectrum(state)
    
    # Must be exactly identical
    assert len(spectrum_1) == len(spectrum_2)
    for v1, v2 in zip(spectrum_1, spectrum_2):
        assert v1 == v2
        
    laplacian_lambda_2 = compute_laplacian_lambda_2(spectrum_1)
    assert laplacian_lambda_2 >= 0

def test_random_walk_probs_deterministic():
    """Ensure random walk return probabilities are fully deterministic."""
    state = pr0_state_trace(15)[-1]
    
    rw_1 = random_walk_return_probabilities(state, 5)
    rw_2 = random_walk_return_probabilities(state, 5)
    
    assert len(rw_1) == len(rw_2) == 5
    for v1, v2 in zip(rw_1, rw_2):
        assert v1 == v2

def test_observer_relabeling_invariance():
    """Ensure spectral gap and spectrum are invariant under node relabeling."""
    state = pr0_state_trace(20)[-1]
    is_invariant = verify_relabeling_invariance(state, seed=42)
    assert is_invariant is True

def test_no_forbidden_terms_in_api():
    """Ensure the API of spectral diagnostics does not leak physical target terms."""
    from verification.pregeometry import spectral_diagnostics
    
    source = open(spectral_diagnostics.__file__).read()
    forbidden = ["16.339", "dimension", "mass gap", "metric"]
    
    for f in forbidden:
        assert f not in source.lower(), f"Forbidden physical term '{f}' found in spectral_diagnostics.py"


def test_retrospective_registration_is_fail_closed_and_hash_stable():
    registration_1, digest_1 = load_frozen_registration()
    registration_2, digest_2 = load_frozen_registration()
    assert digest_1 == digest_2
    assert digest_1 == EXPECTED_REGISTRATION_SHA256
    protocol = evaluate_protocol_components(
        registration_1,
        {"pr0_toy_graph": "executed"},
    )
    assert protocol["status"] == INCOMPLETE_PROTOCOL
    assert protocol["missing_components"]
    assert_no_false_completion(protocol)


def test_80_digit_decimal_roundtrip():
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        lexeme = serialize_mpf(mp.sqrt(mp.mpf(2)))
    assert_decimal_roundtrip(lexeme)
    assert len([char for char in lexeme if char.isdigit()]) == PRECISION_DECIMAL_DIGITS


def test_lower_precision_is_rejected():
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        value = mp.sqrt(mp.mpf(2))
    try:
        serialize_mpf(value, digits=30)
    except ValueError as exc:
        assert "exactly 80" in str(exc)
    else:
        raise AssertionError("Lower protected precision was not rejected.")


def test_80_digit_cross_process_roundtrip():
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        lexeme = serialize_mpf(mp.sqrt(mp.mpf(2)))
    script = (
        "from verification.pregeometry.pr2_protocol import assert_decimal_roundtrip;"
        "import sys;"
        "assert_decimal_roundtrip(sys.argv[1]);"
        "print(sys.argv[1])"
    )
    completed = subprocess.run(
        [sys.executable, "-c", script, lexeme],
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stdout.strip() == lexeme


def test_legacy_migration_preserves_numeric_lexemes_and_renames_vocabulary():
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        lexeme = serialize_mpf(mp.sqrt(mp.mpf(2)))
    payload = json.dumps({"spectral_gap": lexeme, "count": 7})
    migrated = migrate_legacy_payload_text(payload)
    assert migrated["laplacian_lambda_2"] == lexeme
    assert migrated["count"] == "7"
    assert "spectral_gap" not in migrated


def test_protected_sources_have_no_native_float_conversion_or_legacy_key():
    root = Path(__file__).resolve().parents[2]
    protected = (
        root / "verification" / "pregeometry" / "spectral_diagnostics.py",
        root / "verification" / "pregeometry" / "pr2_protocol.py",
        root / "verification" / "pregeometry" / "experiments" / "run_pr2_spectral_diagnostics.py",
        root / "verification" / "pregeometry" / "reports" / "write_pr2_report.py",
    )
    legacy_vocabulary = "spectral" + "_gap"
    for path in protected:
        source = path.read_text(encoding="utf-8")
        assert "float(" not in source
        if path.name != "pr2_protocol.py":
            assert legacy_vocabulary not in source
