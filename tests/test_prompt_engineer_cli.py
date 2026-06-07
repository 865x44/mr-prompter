#!/usr/bin/env python3
"""
Regression tests for scripts/prompt_engineer.py CLI.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLI = [sys.executable, str(REPO_ROOT / "scripts" / "prompt_engineer.py")]


class TestSearch(unittest.TestCase):
    def test_search_chain_of_thought(self):
        result = subprocess.run(
            CLI + ["search", "chain of thought"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Chain of Thought", result.stdout)

    def test_search_no_results(self):
        result = subprocess.run(
            CLI + ["search", "xyznonexistent"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0, "search with no results should exit non-zero")
        self.assertIn("No results found", result.stdout)


class TestList(unittest.TestCase):
    def test_list_reasoning(self):
        result = subprocess.run(
            CLI + ["list", "--category", "reasoning"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("chain-of-thought", result.stdout)
        self.assertIn("tree-of-thought", result.stdout)


class TestGet(unittest.TestCase):
    def test_get_strategic_chain(self):
        result = subprocess.run(
            CLI + ["get", "strategic-chain"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Strategic Prompt Chain", result.stdout)
        # Must NOT begin with Chain of Thought content
        lines = result.stdout.splitlines()
        first_content_line = None
        for line in lines:
            if line.strip() and not line.startswith("---") and not line.startswith("Category:"):
                first_content_line = line
                break
        self.assertIsNotNone(first_content_line)
        self.assertNotIn("Chain of Thought", first_content_line)

    def test_get_not_found(self):
        result = subprocess.run(
            CLI + ["get", "does-not-exist"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0, "get for missing ID should exit non-zero")
        self.assertIn("not found", result.stdout.lower())

    def test_get_all_techniques(self):
        """Every technique ID should be retrievable or have a known exemption."""
        import json
        with open(REPO_ROOT / "knowledge" / "index.json") as f:
            index = json.load(f)

        # Known exemptions: techniques without reference sections
        exempt = {"forced-domain-shift", "toggle-mode-pattern", "injection-defense", "progressive-disclosure"}

        for t in index.get("techniques", []):
            tid = t["id"]
            result = subprocess.run(
                CLI + ["get", tid],
                capture_output=True,
                text=True,
            )
            if tid in exempt:
                # Exempt techniques may fail gracefully
                self.assertIn(
                    result.returncode, [0, 1],
                    f"get {tid} should exit 0 or 1, got {result.returncode}"
                )
            else:
                self.assertEqual(
                    result.returncode, 0,
                    f"get {tid} should succeed. stderr: {result.stderr}"
                )


class TestVerify(unittest.TestCase):
    def test_verify_no_input(self):
        result = subprocess.run(
            CLI + ["verify"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0, "verify with no input should exit non-zero")
        self.assertIn("No prompt provided", result.stdout)

    def test_verify_missing_file(self):
        result = subprocess.run(
            CLI + ["verify", "--prompt-file", "/does/not/exist"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        # Should not traceback
        self.assertNotIn("Traceback", result.stderr)

    def test_verify_valid_prompt(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("You are a helpful assistant.\\n\\nTask: Summarize the text.\\nOutput: bullet points.\\n")
            path = f.name
        try:
            result = subprocess.run(
                CLI + ["verify", "--prompt-file", path],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("AUDIT RESULT", result.stdout)
        finally:
            Path(path).unlink()


class TestAssemble(unittest.TestCase):
    def test_assemble_basic(self):
        result = subprocess.run(
            CLI + ["assemble", "--model", "claude", "--category", "system"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Prompt Assembly Scaffold", result.stdout)


if __name__ == "__main__":
    unittest.main()
