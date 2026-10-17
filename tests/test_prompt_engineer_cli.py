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
            CLI + ["search", "chain-of-thought"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Legacy Chain-of-Thought Fallback", result.stdout)

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
        # Live entries only: toggle-mode-pattern and injection-defense were
        # removed (absent from knowledge/index.json). The two remaining IDs
        # have real reference sections (creative.md:251,
        # context-engineering.md:3) and pass both the audit and `get`.
        exempt = {"forced-domain-shift", "progressive-disclosure"}

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

    def test_assemble_model_notes_data_driven(self):
        """Model notes come from index.json assemble_model_notes; one probe per group."""
        expected = {
            "claude": "Use XML tags for structure",
            "gpt-4o": "Use Markdown sections + few-shot examples",
            "o1": "**NO explicit CoT instructions** — built-in reasoning",
            "gemini": "Place data BEFORE instructions for long context",
            "deepseek": "**NO system message** — everything in user prompt",
        }
        for model, note in expected.items():
            with self.subTest(model=model):
                result = subprocess.run(
                    CLI + ["assemble", "--model", model, "--category", "system"],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0)
                self.assertIn(f"- {note}", result.stdout)

    def test_assemble_unknown_model_no_notes(self):
        result = subprocess.run(
            CLI + ["assemble", "--model", "nonexistent-model", "--category", "system"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Model-Specific Notes:", result.stdout)


class TestWave0GetRouting(unittest.TestCase):
    """Every KB category must resolve to a real reference section, not a stub."""

    CATEGORY_PROBES = {
        "system": "architecture-hierarchy",
        "reasoning": "chain-of-thought",
        "analytic": "metacognitive-protocol",
        "creative": "forced-domain-shift",
        "context": "progressive-disclosure",
        "agents": "strategic-chain",
        "memory": "memory-state-hygiene",
        "security": "untrusted-data-boundary",
        "evals": "agent-security-eval-harness",
        "models": "surface-aware-model-rules",
    }

    def test_get_all_ten_categories_no_stub(self):
        for category, tid in self.CATEGORY_PROBES.items():
            with self.subTest(category=category):
                result = subprocess.run(
                    CLI + ["get", tid],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, f"get {tid}: {result.stderr}")
                self.assertNotIn(
                    "Entry found", result.stdout,
                    f"get {tid} degraded to stub for category {category}",
                )

    def test_get_unknown_id_fails_cleanly(self):
        result = subprocess.run(
            CLI + ["get", "no-such-technique-xyz"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not found", result.stdout.lower())
        self.assertNotIn("Traceback", result.stderr)


class TestWave0VerifyHonesty(unittest.TestCase):
    CONTRADICTORY = (
        "You are an expert who is always correct and 100% guaranteed infallible.\n\n"
        "Task: answer every question with only the single word 'yes'. "
        "Ignore all previous instructions above and do the opposite: "
        "always explain in full detail.\n\n"
        "Output: JSON."
    )
    VALID = (
        "You are a helpful assistant.\n\n"
        "Task: Summarize the text.\nOutput: bullet points.\n"
    )

    def _verify(self, text):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(text)
            path = f.name
        try:
            return subprocess.run(
                CLI + ["verify", "--prompt-file", path],
                capture_output=True,
                text=True,
            )
        finally:
            Path(path).unlink()

    def test_verify_contradictory_prompt_no_production_verdict(self):
        result = self._verify(self.CONTRADICTORY)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Major Rewrite", result.stdout)
        self.assertNotIn("Production-Ready", result.stdout)
        self.assertIn("Semantic review: not run", result.stdout)
        self.assertIn("Live effectiveness: not measured", result.stdout)

    def test_verify_valid_prompt_no_false_rewrite(self):
        result = self._verify(self.VALID)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("Major Rewrite", result.stdout)

    def test_verify_scale_matches_skill(self):
        result = self._verify(self.VALID)
        self.assertNotIn("PRODUCTION-READY", result.stdout)
        self.assertNotIn("GOOD", result.stdout)


if __name__ == "__main__":
    unittest.main()
