"""Report generator for PR-2 spectral graph diagnostics.

Status: [D] purely for software verification.
"""

import json
from pathlib import Path

from mpmath import mp

from verification.pregeometry.pr2_protocol import INCOMPLETE_PROTOCOL


def _display_decimal(lexeme: str) -> str:
    """Round for display only; stored protected values remain untouched."""
    with mp.workdps(80):
        return mp.nstr(mp.mpf(lexeme), n=7)


def write_report(*, project_root: Path = Path(".")):
    output_dir = Path(project_root).resolve() / "verification" / "data" / "pregeometry" / "pr2"
    data_file = output_dir / "pr2_spectral_diagnostics.json"
    if not data_file.exists():
        print("Data file not found. Run experiments/run_pr2_spectral_diagnostics.py first.")
        return

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f, parse_float=str, parse_int=str)
    if data["protocol"]["status"] != INCOMPLETE_PROTOCOL:
        raise ValueError("Retrospective PR-2 report must disclose INCOMPLETE_PROTOCOL.")

    report_lines = [
        "# PR-2 Spectral Graph Diagnostics Report",
        "",
        "> **Protocol status:** INCOMPLETE_PROTOCOL. Only the PR-0 toy-graph component is present; no null-ensemble comparison is reported.",
        "",
        "> **Boundary:** All spectral quantities are exclusively graph diagnostics [D] and carry no physical interpretation.",
        "",
        "## Configuration",
        f"- **Iterations:** {data['metadata']['iterations']}",
        f"- **Seed:** {data['metadata']['seed']}",
        f"- **Walk Length:** {data['metadata']['max_walk_length']}",
        f"- **Registration SHA-256:** `{data['registration_sha256']}`",
        "",
        "## PR-0 Toy Graph Diagnostics",
        f"- **Laplacian lambda_2 (algebraic connectivity):** {_display_decimal(data['pr0_toy_graph']['laplacian_lambda_2'])}",
        f"- **Log-Slope (Window 5-15):** {_display_decimal(data['pr0_toy_graph']['log_slope'])}",
        "",
        "### Random Walk Return Probabilities",
        "```text"
    ]

    for i, p in enumerate(data['pr0_toy_graph']['random_walk_return_probs']):
        report_lines.append(f"Step {i+1:2d}: {_display_decimal(p)}")

    report_lines.append("```")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("Status: prototype / INCOMPLETE_PROTOCOL / [D] graph diagnostic.")

    out_file = output_dir / "pr2_report.md"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"Report written to {out_file}")

if __name__ == "__main__":
    write_report()
