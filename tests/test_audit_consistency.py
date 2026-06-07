#!/usr/bin/env python3
"""
Tests for the consistency audit script itself.
"""

import subprocess
import sys
import os
import shutil
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIT = [sys.executable, str(REPO_ROOT / "scripts" / "audit_consistency.py")]


class TestAuditConsistency(unittest.TestCase):
    def run_audit(self, repo_root=REPO_ROOT, extra_env=None):
        env = dict(os.environ)
        env["AUDIT_REPO_ROOT"] = str(repo_root)
        if extra_env:
            env.update(extra_env)
        return subprocess.run(AUDIT, capture_output=True, text=True, env=env)

    def test_audit_exits_zero(self):
        """Current repository audit must pass cleanly."""
        result = self.run_audit()
        self.assertEqual(
            result.returncode, 0,
            f"Audit must exit 0 for current repo. stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
        self.assertIn("Audit PASSED", result.stdout)

    def test_audit_exits_nonzero_on_drift(self):
        """A fabricated count drift must cause nonzero exit."""
        import json
        index_path = REPO_ROOT / "knowledge" / "index.json"
        original = json.loads(index_path.read_text(encoding="utf-8"))
        # Temporarily corrupt stats to trigger failure
        corrupted = dict(original)
        corrupted["stats"] = dict(original.get("stats", {}))
        corrupted["stats"]["techniques"] = 999
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, dir=index_path.parent
        ) as f:
            json.dump(corrupted, f)
            tmp_path = f.name
        try:
            result = self.run_audit(extra_env={"AUDIT_INDEX_OVERRIDE": Path(tmp_path).name})
            self.assertNotEqual(
                result.returncode, 0,
                "Audit must fail when stats drift"
            )
            self.assertIn("FAIL:", result.stdout)
        finally:
            Path(tmp_path).unlink()

    def test_audit_exits_nonzero_on_published_claim_drift(self):
        """A published claim drift must fail even when index stats remain unchanged."""
        with tempfile.TemporaryDirectory() as tmp:
            copied_repo = Path(tmp) / "repo"
            shutil.copytree(REPO_ROOT, copied_repo, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            readme = copied_repo / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8").replace(
                    "| Session archetypes | 6 |",
                    "| Session archetypes | 999 |",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_audit(copied_repo)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("README.md table claims 999 session_archetypes", result.stdout)


if __name__ == "__main__":
    unittest.main()
