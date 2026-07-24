#!/usr/bin/env python3
"""test_integrity_gates.py — Unit tests for GOV-001 Scientific Integrity Gates

Tests for:
  - check_evidence_tags: invented classes, strong classes near targets
  - check_no_gamma_targeting: K_S targeting, target literals in loss/objective contexts
  - check_merge_requirements: missing Claims Table, Reproduction Note, DOI check
  - check_protected_paths: agent dirs, secret filenames, forbidden extensions

Each test uses the module's internal functions directly to avoid git dependency.
"""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

diff_range = importlib.import_module("git_diff_range")
evidence = importlib.import_module("check_evidence_tags")
gamma = importlib.import_module("check_no_gamma_targeting")
merge = importlib.import_module("check_merge_requirements")
pp = importlib.import_module("check_protected_paths")


def _entry(text: str, line: int = 1) -> dict[str, object]:
    return {"file": "fixture.txt", "line": line, "text": text}


def _git(repo: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _commit(repo: Path, message: str) -> str:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-b", "master")
    _git(tmp_path, "config", "user.name", "Integrity Test")
    _git(tmp_path, "config", "user.email", "integrity@example.invalid")
    (tmp_path / "clean.txt").write_text("clean\n", encoding="utf-8")
    _commit(tmp_path, "base")
    return tmp_path


def _run_gate(
    script: str,
    repo: Path,
    base: str,
    head: str,
    pr_body: str = "",
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update(
        {"BASE_SHA": base, "HEAD_SHA": head, "PR_BODY": pr_body}
    )
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script)],
        cwd=repo,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize(
    "evidence_class",
    ("A+", "B+", "B-", "C+", "D+"),
)
def test_invented_classes_block(evidence_class: str):
    marker = "[" + evidence_class + "]"
    assert evidence.check_invented_classes([_entry(marker)])


def test_strong_class_near_guarded_literal_blocks():
    strong = "[" + "A]"
    guarded = "16" + ".339"
    entries = [_entry(strong, 10), _entry(guarded, 13)]
    assert evidence.check_proximity(entries)


def test_strong_class_in_other_file_does_not_cross_proximity():
    strong = "[" + "A]"
    guarded = "16" + ".339"
    entries = [
        {"file": "one", "line": 1, "text": strong},
        {"file": "two", "line": 1, "text": guarded},
    ]
    assert not evidence.check_proximity(entries)


def test_direct_and_context_targeting_block():
    direct = "K_S = (Delta" + "*/gamma)"
    guarded = "16" + ".339"
    assert gamma.check_direct_targeting([_entry(direct)])
    assert gamma.check_literal_in_targeting_context(
        [_entry("objective = " + guarded)]
    )


def test_required_pr_sections():
    body = (
        "## Claims Table\n| Claim | Class |\n"
        "## Reproduction Note\n80-digit command\n"
        "## DOI Check\nnot applicable with reason\n"
    )
    assert not merge.check_required_sections(body)
    assert merge.check_required_sections("## Claims Table")


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
        violations = pp.check_protected_dirs(
            [".venv/lib/python3.10/site.py"]
        )
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
        violations = pp.check_protected_dirs(
            ["verification/scripts/test.py"]
        )
        assert len(violations) == 0

    def test_normal_filename(self):
        """Normal filenames must pass."""
        violations = pp.check_forbidden_filenames(
            ["README.md", "setup.py", "verification/scripts/check.py"]
        )
        assert len(violations) == 0

    def test_docs_file(self):
        """Documentation files must pass."""
        violations = pp.check_protected_dirs(
            ["docs/architecture/bridge.md"]
        )
        assert len(violations) == 0

    def test_clean_diff(self):
        """Clean diff with no protected paths must pass."""
        dirs = pp.check_protected_dirs(
            ["verification/tests/test_foo.py", "README.md"]
        )
        names = pp.check_forbidden_filenames(
            ["verification/tests/test_foo.py", "README.md"]
        )
        assert len(dirs) == 0
        assert len(names) == 0


def test_poisoned_docstring_is_scanned_in_subprocess(repository: Path):
    base = _git(repository, "rev-parse", "HEAD")
    guarded = "16" + ".339"
    (repository / "poison.py").write_text(
        '"""objective = ' + guarded + '"""\n',
        encoding="utf-8",
    )
    head = _commit(repository, "poison")
    result = _run_gate(
        "check_no_gamma_targeting.py",
        repository,
        base,
        head,
    )
    assert result.returncode != 0
    assert "BLOCKED" in result.stdout


def test_deletion_is_not_hidden_from_path_scanner(repository: Path):
    forbidden = repository / ".env"
    forbidden.write_text("placeholder\n", encoding="utf-8")
    base = _commit(repository, "add path")
    forbidden.unlink()
    head = _commit(repository, "delete path")
    result = _run_gate(
        "check_protected_paths.py",
        repository,
        base,
        head,
    )
    assert result.returncode != 0
    assert "BLOCKED" in result.stdout


def test_rename_is_nul_parsed_and_blocked(repository: Path):
    source = repository / "ordinary.txt"
    source.write_text("content\n", encoding="utf-8")
    base = _commit(repository, "ordinary")
    source.rename(repository / ".env")
    head = _commit(repository, "rename")
    result = _run_gate(
        "check_protected_paths.py",
        repository,
        base,
        head,
    )
    assert result.returncode != 0
    assert "BLOCKED" in result.stdout


def test_empty_range_fails_closed(repository: Path):
    commit = _git(repository, "rev-parse", "HEAD")
    result = _run_gate(
        "check_evidence_tags.py",
        repository,
        commit,
        commit,
    )
    assert result.returncode != 0
    assert "empty PR range" in result.stdout


def test_missing_object_fails_closed(repository: Path):
    base = _git(repository, "rev-parse", "HEAD")
    result = _run_gate(
        "check_evidence_tags.py",
        repository,
        base,
        "0" * 40,
    )
    assert result.returncode != 0
    assert "git cat-file" in result.stdout


@pytest.mark.parametrize(
    "payload",
    (
        b"",
        b"A\0path-without-final-nul",
        b"Q\0path\0",
        b"R100\0only-one-path\0",
    ),
)
def test_malformed_name_status_fails_closed(payload: bytes):
    with pytest.raises(diff_range.DiffRangeError):
        diff_range.parse_name_status_z(payload)
