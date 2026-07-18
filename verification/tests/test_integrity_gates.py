#!/usr/bin/env python3
"""test_integrity_gates.py — Unit tests for GOV-001 Scientific Integrity Gates

Tests for:
  - check_evidence_tags: invented classes, strong classes near targets
  - check_no_gamma_targeting: K_S targeting, target literals in loss/objective contexts
  - check_merge_requirements: missing Claims Table, Reproduction Note, DOI check
  - check_protected_paths: agent dirs, secret filenames, forbidden extensions

Each test uses the module's internal functions directly to avoid git dependency.
"""
import os
import sys
import importlib.util
import pytest

# Import scripts using importlib to avoid package conflicts
_scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")

def _import_script(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(_scripts_dir, name + ".py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

et = _import_script("check_evidence_tags")
gt = _import_script("check_no_gamma_targeting")
mr = _import_script("check_merge_requirements")
pp = _import_script("check_protected_paths")


# ============================================================================
# check_evidence_tags tests
# ============================================================================

class TestEvidenceTags:
    """Tests for evidence tag validation."""

    # --- Negative fixtures (must block) ---

    def test_invented_class_a_plus(self):
        """[A+] is not a valid evidence class and must be blocked."""
        entries = [{"file": "test.md", "text": "This claim is [A+] proven."}]
        violations = et.check_invented_classes(entries)
        assert len(violations) > 0
        assert "invented evidence class" in violations[0]

    def test_invented_class_b_plus(self):
        """[B+] is not a valid evidence class and must be blocked."""
        entries = [{"file": "test.md", "text": "Lattice result [B+]"}]
        violations = et.check_invented_classes(entries)
        assert len(violations) > 0

    def test_invented_class_b_minus(self):
        """[B-] is not a valid evidence class and must be blocked."""
        entries = [{"file": "test.md", "text": "Weak lattice [B-]"}]
        violations = et.check_invented_classes(entries)
        assert len(violations) > 0

    def test_invented_class_c_plus(self):
        """[C+] is not a valid evidence class and must be blocked."""
        entries = [{"file": "test.md", "text": "Calibrated+ [C+]"}]
        violations = et.check_invented_classes(entries)
        assert len(violations) > 0

    def test_invented_class_d_plus(self):
        """[D+] is not a valid evidence class and must be blocked."""
        entries = [{"file": "test.md", "text": "Better prediction [D+]"}]
        violations = et.check_invented_classes(entries)
        assert len(violations) > 0

    def test_proximity_a_near_16339(self):
        """[A] within 3 lines of 16.339 must be blocked."""
        entries = [
            {"file": "test.md", "text": "Claim [A] proven mathematically."},
            {"file": "test.md", "text": "Some intermediate text."},
            {"file": "test.md", "text": "The value is 16.339 GeV."},
        ]
        violations = et.check_proximity(entries)
        assert len(violations) > 0
        assert "16\\.339" in violations[0] or "16.339" in violations[0]

    def test_proximity_a_minus_near_glueball(self):
        """[A-] within 3 lines of 'glueball' must be blocked."""
        entries = [
            {"file": "test.md", "text": "This is [A-] calibrated."},
            {"file": "test.md", "text": "The glueball mass is 1.710 GeV."},
        ]
        violations = et.check_proximity(entries)
        assert len(violations) > 0

    def test_proximity_b_near_49_over_3(self):
        """[B] on same line as 49/3 must be blocked."""
        entries = [
            {"file": "test.md", "text": "[B] The ratio is 49/3 exactly."},
        ]
        violations = et.check_proximity(entries)
        assert len(violations) > 0

    def test_proximity_a_near_17_3000(self):
        """[A] within 3 lines of 17/3000 must be blocked."""
        entries = [
            {"file": "test.md", "text": "Result: 17/3000 correction term."},
            {"file": "test.md", "text": "Line 2"},
            {"file": "test.md", "text": "This is [A] category."},
        ]
        violations = et.check_proximity(entries)
        assert len(violations) > 0

    # --- Positive fixtures (must pass) ---

    def test_valid_class_c(self):
        """[C] is a valid evidence class and must pass."""
        entries = [{"file": "test.md", "text": "This claim is [C] calibrated."}]
        inv = et.check_invented_classes(entries)
        prox = et.check_proximity(entries)
        assert len(inv) == 0
        assert len(prox) == 0

    def test_valid_class_d(self):
        """[D] is a valid evidence class and must pass."""
        entries = [{"file": "test.md", "text": "This prediction is [D]."}]
        inv = et.check_invented_classes(entries)
        prox = et.check_proximity(entries)
        assert len(inv) == 0
        assert len(prox) == 0

    def test_valid_class_e(self):
        """[E] is a valid evidence class and must pass."""
        entries = [{"file": "test.md", "text": "This claim is [E] withdrawn."}]
        inv = et.check_invented_classes(entries)
        assert len(inv) == 0

    def test_a_far_from_target(self):
        """[A] far from any target literal must pass."""
        entries = [
            {"file": "test.md", "text": "Claim [A] proven mathematically."},
            {"file": "test.md", "text": "Line 2"},
            {"file": "test.md", "text": "Line 3"},
            {"file": "test.md", "text": "Line 4"},
            {"file": "test.md", "text": "Line 5"},
            {"file": "test.md", "text": "The value is 16.339 GeV."},
        ]
        violations = et.check_proximity(entries)
        assert len(violations) == 0

    def test_clean_diff_no_evidence(self):
        """A diff without evidence tags must pass."""
        entries = [
            {"file": "README.md", "text": "Updated documentation."},
            {"file": "README.md", "text": "No evidence classes here."},
        ]
        inv = et.check_invented_classes(entries)
        prox = et.check_proximity(entries)
        assert len(inv) == 0
        assert len(prox) == 0


# ============================================================================
# check_no_gamma_targeting tests
# ============================================================================

class TestGammaTargeting:
    """Tests for gamma-targeting detection."""

    # --- Negative fixtures (must block) ---

    def test_ks_delta_gamma(self):
        """K_S = (Delta*/gamma) must be blocked."""
        entries = [{"file": "code.py", "text": "K_S = (Delta*/gamma)"}]
        violations = gt.check_direct_targeting(entries)
        assert len(violations) > 0

    def test_target_16339(self):
        """target = 16.339 must be blocked."""
        entries = [{"file": "code.py", "text": "target = 16.339"}]
        violations = gt.check_literal_in_targeting_context(entries)
        assert len(violations) > 0

    def test_loss_49_3(self):
        """loss using 49/3 must be blocked."""
        entries = [{"file": "code.py", "text": "loss = abs(x - 49/3)"}]
        violations = gt.check_literal_in_targeting_context(entries)
        assert len(violations) > 0

    def test_objective_17_3000(self):
        """objective using 17/3000 must be blocked."""
        entries = [{"file": "code.py", "text": "objective = 17/3000 - result"}]
        violations = gt.check_literal_in_targeting_context(entries)
        assert len(violations) > 0

    def test_kill_switch_16339(self):
        """kill_switch with 16.339 must be blocked."""
        entries = [{"file": "code.py", "text": "kill_switch = abs(gamma - 16.339) / 16.339 > 0.01"}]
        violations = gt.check_literal_in_targeting_context(entries)
        assert len(violations) > 0

    def test_goal_16339(self):
        """goal with 16.339 must be blocked."""
        entries = [{"file": "code.py", "text": "goal = 16.339"}]
        violations = gt.check_literal_in_targeting_context(entries)
        assert len(violations) > 0

    # --- Positive fixtures (must pass) ---

    def test_gamma_in_documentation(self):
        """Mentioning gamma = 16.339 in documentation without targeting context must pass."""
        entries = [{"file": "docs.md", "text": "The calibrated invariant gamma = 16.339 is category [C]."}]
        direct = gt.check_direct_targeting(entries)
        context = gt.check_literal_in_targeting_context(entries)
        assert len(direct) == 0
        assert len(context) == 0

    def test_normal_code(self):
        """Normal code without targeting must pass."""
        entries = [{"file": "code.py", "text": "result = compute_spectral_gap(H)"}]
        direct = gt.check_direct_targeting(entries)
        context = gt.check_literal_in_targeting_context(entries)
        assert len(direct) == 0
        assert len(context) == 0

    def test_49_in_unrelated_context(self):
        """49/3 in unrelated context must pass."""
        entries = [{"file": "code.py", "text": "pages = 49/3  # pagination"}]
        violations = gt.check_literal_in_targeting_context(entries)
        assert len(violations) == 0


# ============================================================================
# check_merge_requirements tests
# ============================================================================

class TestMergeRequirements:
    """Tests for merge requirement validation."""

    # --- Negative fixtures (must block) ---

    def test_empty_pr_body(self):
        """Empty PR body touching protected paths must fail."""
        violations = mr.check_required_sections("")
        assert len(violations) == 3  # all three sections missing

    def test_missing_claims_table(self):
        """PR body without Claims Table must fail."""
        body = "## Reproduction Note\nmp.dps = 80\n## DOI Check\nAll DOIs resolve."
        violations = mr.check_required_sections(body)
        assert any("Claims Table" in v for v in violations)

    def test_missing_reproduction_note(self):
        """PR body without Reproduction Note must fail."""
        body = "## Claims Table\n| claim | class |\n## DOI Check\nAll DOIs resolve."
        violations = mr.check_required_sections(body)
        assert any("Reproduction Note" in v for v in violations)

    def test_missing_doi_check(self):
        """PR body without DOI check must fail."""
        body = "## Claims Table\n| claim | class |\n## Reproduction Note\nmp.dps = 80"
        violations = mr.check_required_sections(body)
        assert any("DOI-Resolvability Check" in v for v in violations)

    # --- Positive fixtures (must pass) ---

    def test_complete_pr_body(self):
        """PR body with all three required sections must pass."""
        body = """## Claims Table
| Claim | Evidence Class |
|-------|---------------|
| Delta = 1.710 GeV | [A] |

## Reproduction Note
Run with mp.dps = 80:
```
python verification/scripts/verify_mass_gap.py
```

## DOI-Resolvability Check
All DOIs verified as resolvable.
"""
        violations = mr.check_required_sections(body)
        assert len(violations) == 0

    def test_alternative_wording(self):
        """PR body with alternative valid wording must pass."""
        body = "Claims table below.\nTo reproduce with 80-digit precision.\nDOI check passed."
        violations = mr.check_required_sections(body)
        assert len(violations) == 0


# ============================================================================
# check_protected_paths tests
# ============================================================================

class TestProtectedPaths:
    """Tests for protected path validation."""

    # --- Negative fixtures (must block) ---

    def test_uidt_os_dir(self):
        """Files under UIDT-OS/ must be blocked."""
        violations = pp.check_protected_dirs(["UIDT-OS/config.yml"])
        assert len(violations) > 0

    def test_claude_dir(self):
        """Files under .claude/ must be blocked."""
        violations = pp.check_protected_dirs([".claude/settings.json"])
        assert len(violations) > 0

    def test_trae_dir(self):
        """Files under .trae/ must be blocked."""
        violations = pp.check_protected_dirs([".trae/rules/custom.md"])
        assert len(violations) > 0

    def test_cursor_dir(self):
        """Files under .cursor/ must be blocked."""
        violations = pp.check_protected_dirs([".cursor/settings.json"])
        assert len(violations) > 0

    def test_antigravity_dir(self):
        """Files under .antigravity/ must be blocked."""
        violations = pp.check_protected_dirs([".antigravity/config.yml"])
        assert len(violations) > 0

    def test_venv_dir(self):
        """Files under .venv/ must be blocked."""
        violations = pp.check_protected_dirs([".venv/lib/python3.10/site.py"])
        assert len(violations) > 0

    def test_local_dir(self):
        """Files under LOCAL/ (except uidt-repo.cfg) must be blocked."""
        violations = pp.check_protected_dirs(["LOCAL/secrets.yml"])
        assert len(violations) > 0

    def test_env_file(self):
        """'.env' file must be blocked."""
        violations = pp.check_forbidden_filenames([".env"])
        assert len(violations) > 0

    def test_env_local_file(self):
        """'.env.local' file must be blocked."""
        violations = pp.check_forbidden_filenames([".env.local"])
        assert len(violations) > 0

    def test_credentials_json(self):
        """'credentials.json' must be blocked."""
        violations = pp.check_forbidden_filenames(["credentials.json"])
        assert len(violations) > 0

    def test_key_extension(self):
        """'.key' files must be blocked."""
        violations = pp.check_forbidden_filenames(["server.key"])
        assert len(violations) > 0

    def test_pem_extension(self):
        """'.pem' files must be blocked."""
        violations = pp.check_forbidden_filenames(["cert.pem"])
        assert len(violations) > 0

    def test_config_local_yaml(self):
        """'config.local.yaml' must be blocked."""
        violations = pp.check_forbidden_filenames(["config.local.yaml"])
        assert len(violations) > 0

    # --- Positive fixtures (must pass) ---

    def test_local_uidt_repo_cfg_exception(self):
        """LOCAL/uidt-repo.cfg is allowed as an exception."""
        violations = pp.check_protected_dirs(["LOCAL/uidt-repo.cfg"])
        assert len(violations) == 0

    def test_normal_verification_file(self):
        """Normal verification file must pass."""
        violations = pp.check_protected_dirs(["verification/scripts/test.py"])
        assert len(violations) == 0

    def test_normal_filename(self):
        """Normal filenames must pass."""
        violations = pp.check_forbidden_filenames(["README.md", "setup.py", "verification/scripts/check.py"])
        assert len(violations) == 0

    def test_docs_file(self):
        """Documentation files must pass."""
        violations = pp.check_protected_dirs(["docs/architecture/bridge.md"])
        assert len(violations) == 0

    def test_clean_diff(self):
        """Clean diff with no protected paths must pass."""
        dirs = pp.check_protected_dirs(["verification/tests/test_foo.py", "README.md"])
        names = pp.check_forbidden_filenames(["verification/tests/test_foo.py", "README.md"])
        assert len(dirs) == 0
        assert len(names) == 0
