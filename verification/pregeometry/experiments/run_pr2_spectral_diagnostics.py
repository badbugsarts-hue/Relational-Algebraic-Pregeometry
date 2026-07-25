"""Runner for PR-2 spectral graph diagnostics.

Status: [D] purely for software verification.
"""

import json
from pathlib import Path
from mpmath import mp

from verification.pregeometry.null_ensembles import pr0_state_trace
from verification.pregeometry.pr2_protocol import (
    PRECISION_DECIMAL_DIGITS,
    PR2_OUTPUT_SCHEMA,
    PR2_SCHEMA_VERSION,
    assert_no_false_completion,
    evaluate_protocol_components,
    load_frozen_registration,
    serialize_mpf,
)
from verification.pregeometry.spectral_diagnostics import (
    combinatorial_laplacian_spectrum,
    compute_laplacian_lambda_2,
    random_walk_return_probabilities,
    log_slope_diagnostic
)

def run_diagnostics(
    iterations: int = 50,
    seed: int = 42,
    ensemble_size: int = 5,
    max_walk_length: int = 20,
    *,
    project_root: Path = Path("."),
):
    if iterations <= 0:
        raise ValueError("iterations must be positive.")
    print("Generating PR-0 trace...")
    pr0_states = pr0_state_trace(iterations)
    final_pr0_state = pr0_states[-1]

    print("Computing PR-0 spectral diagnostics...")
    with mp.workdps(PRECISION_DECIMAL_DIGITS):
        pr0_spectrum = combinatorial_laplacian_spectrum(final_pr0_state)
        pr0_lambda_2 = compute_laplacian_lambda_2(pr0_spectrum)
        pr0_rw = random_walk_return_probabilities(final_pr0_state, max_walk_length)
        pr0_slope = log_slope_diagnostic(pr0_rw, 5, 15)

    pr0_results = {
        "spectrum": [serialize_mpf(value) for value in pr0_spectrum],
        "laplacian_lambda_2": serialize_mpf(pr0_lambda_2),
        "random_walk_return_probs": [serialize_mpf(value) for value in pr0_rw],
        "log_slope": serialize_mpf(pr0_slope),
    }

    registration, registration_hash = load_frozen_registration()
    protocol = evaluate_protocol_components(
        registration,
        {
            "pr0_toy_graph": "executed",
            "pr1_null_ensemble_graph_states": "missing",
            "seed_stability": "missing",
            "label_permutation_invariance": "missing",
        },
    )
    assert_no_false_completion(protocol)

    results = {
        "schema": PR2_OUTPUT_SCHEMA,
        "schema_version": PR2_SCHEMA_VERSION,
        "registration_sha256": registration_hash,
        "precision": {
            "decimal_digits": str(PRECISION_DECIMAL_DIGITS),
            "stored_values": "decimal strings",
        },
        "protocol": protocol,
        "metadata": {
            "iterations": iterations,
            "seed": seed,
            "ensemble_size": ensemble_size,
            "max_walk_length": max_walk_length,
            "status": "[D]",
            "note": "Prototype software graph diagnostics only. No physical target interpretation.",
        },
        "pr0_toy_graph": pr0_results,
    }

    out_dir = Path(project_root).resolve() / "verification" / "data" / "pregeometry" / "pr2"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "pr2_spectral_diagnostics.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Saved PR-2 spectral diagnostics to {out_file}")
    return results

if __name__ == "__main__":
    run_diagnostics()
