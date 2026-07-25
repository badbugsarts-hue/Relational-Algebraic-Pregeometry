from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
ENV_LOCK = ROOT / "environment" / "texlive.lock.json"
SOURCE_LOCK = ROOT / "environment" / "manuscript-source.lock.json"
BUILD_SCRIPT = ROOT / "scripts" / "build_manuscript.sh"


class Prov002LockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.environment = json.loads(ENV_LOCK.read_text(encoding="utf-8"))
        cls.source = json.loads(SOURCE_LOCK.read_text(encoding="utf-8"))

    def test_image_reference_uses_platform_manifest_digest(self) -> None:
        digest = self.environment["platform_manifest_digest"]
        self.assertRegex(digest, r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(
            self.environment["image_reference"],
            f"{self.environment['registry']}/{self.environment['repository']}@{digest}",
        )
        self.assertEqual(self.environment["architecture"], "amd64")
        self.assertEqual(self.environment["os"], "linux")

    def test_index_config_and_package_locks_are_immutable(self) -> None:
        self.assertRegex(
            self.environment["index_digest"], r"^sha256:[0-9a-f]{64}$"
        )
        self.assertRegex(
            self.environment["config_digest"], r"^sha256:[0-9a-f]{64}$"
        )
        package_lock = self.environment["package_lock"]
        self.assertEqual(
            package_lock["manifest_digest"],
            self.environment["platform_manifest_digest"],
        )
        self.assertEqual(
            package_lock["config_digest"], self.environment["config_digest"]
        )

    def test_canonical_source_matches_both_locks(self) -> None:
        completed = subprocess.run(
            ["git", "-C", ROOT, "hash-object", "--", self.source["path"]],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.stdout.strip(), self.source["git_blob_sha1"])
        blob = subprocess.run(
            [
                "git",
                "-C",
                ROOT,
                "cat-file",
                "blob",
                self.source["git_blob_sha1"],
            ],
            check=True,
            capture_output=True,
        ).stdout
        self.assertEqual(
            hashlib.sha256(blob).hexdigest(), self.source["git_blob_sha256"]
        )
        self.assertEqual(
            self.source["commit"], "c8daae119b8699e665c462c06e8580b6e34f831a"
        )

    def test_positive_and_negative_fixtures_are_real_tex_sources(self) -> None:
        fixture_root = ROOT / "verification" / "tests" / "fixtures" / "prov002"
        positive = (fixture_root / "positive.tex").read_text(encoding="utf-8")
        negative = (fixture_root / "negative.tex").read_text(encoding="utf-8")
        self.assertIn(r"\begin{document}", positive)
        self.assertIn(r"\end{document}", positive)
        self.assertIn(r"\ThisCommandMustRemainUndefined", negative)
        self.assertNotIn(r"\ThisCommandMustRemainUndefined", positive)

    def test_build_script_is_digest_bound_and_fail_closed(self) -> None:
        script = BUILD_SCRIPT.read_text(encoding="utf-8")
        self.assertIn('image_ref="$(read_lock "${environment_lock}" image_reference)"', script)
        self.assertIn("--platform linux/amd64", script)
        self.assertIn("--network none", script)
        self.assertIn("--read-only", script)
        self.assertIn("git -C", script)
        self.assertIn("sha256sum", script)
        self.assertIn("exit 69", script)
        self.assertIn("git_blob_sha256", script)
        self.assertIn("platform_manifest_digest", script)
        self.assertNotIn(":latest", script)
        self.assertIsNone(re.search(r"docker\s+run.*:[Ll]atest", script))

    def test_build_output_boundary_is_explicit(self) -> None:
        script = BUILD_SCRIPT.read_text(encoding="utf-8")
        self.assertIn("verification/data/pregeometry", script)
        self.assertIn("Build outputs are forbidden", script)

    def test_negative_lock_fixtures_are_mismatched(self) -> None:
        fixture_root = ROOT / "verification" / "tests" / "fixtures" / "prov002"
        wrong_source = json.loads(
            (fixture_root / "wrong-source-lock.json").read_text(encoding="utf-8")
        )
        wrong_image = json.loads(
            (fixture_root / "wrong-image-lock.json").read_text(encoding="utf-8")
        )
        self.assertNotEqual(
            wrong_source["git_blob_sha256"], self.source["git_blob_sha256"]
        )
        self.assertNotEqual(
            wrong_image["image_reference"].split("@", 1)[1],
            wrong_image["platform_manifest_digest"],
        )


if __name__ == "__main__":
    unittest.main()
