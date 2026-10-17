#!/usr/bin/env python3
"""
Adversarial twins runner (Wave 1, §3.4).

Each pair in fixtures/twins/w1-<pair>-{defective,valid}.md carries an
EXPECT header: `flagged` (verdict must NOT be Production-Ready) or `clean`
(verdict must NOT be Major Rewrite). `#` documentation lines are stripped
before verification — the auditor sees the EXECUTABLE prompt text only
(§3.3), never the fixture's own commentary.

Measures BOTH defect detection AND false accusations on the valid twins.

KNOWN LIMITATIONS (documented, not hidden) — Level-1 lint is lexical by
-design (§3.3 forbids regex semantics). Two defect classes are therefore
`lint-blind`: the EXPECT header says so, and the runner asserts honesty
(banner + clean exit) while RECORDING the verdict instead of demanding a flag:
- Pair B (incompatible JSON clauses): clause-level incompatibility needs
  Level-2 review quoting both clauses.
- Pair D (missing success criterion): needs a Level-2 undefined-criteria
  finding with the exact quote.
- Pair C: verdict-level tie (Needs Fixes / Needs Fixes); split is visible
  only in the red count (defective >= 1 red, valid == 0).
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLI = [sys.executable, str(REPO_ROOT / "scripts" / "prompt_engineer.py")]
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "twins"

PAIRS = ["a", "b", "c", "d"]


def load_fixture(path):
    """Return (expect, executable_text); strip `#` doc lines (not executable)."""
    expect = None
    body = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("# EXPECT:"):
            expect = line.split(":", 1)[1].strip().split()[0]
        elif line.startswith("#"):
            continue
        else:
            body.append(line)
    return expect, "\n".join(body).strip() + "\n"


def verify(text):
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


def parse_result(stdout):
    verdict = re.search(r"^Verdict:\s*(.+)$", stdout, re.MULTILINE).group(1).strip()
    reds = int(re.search(r"(\d+) critical", stdout).group(1))
    return verdict, reds


class TestTwins(unittest.TestCase):
    def test_pair_expectations_hold(self):
        for pair in PAIRS:
            for side in ("defective", "valid"):
                with self.subTest(pair=pair, side=side):
                    path = FIXTURES / f"w1-{pair}-{side}.md"
                    self.assertTrue(path.exists(), f"missing fixture {path.name}")
                    expect, text = load_fixture(path)
                    self.assertIn(expect, ("flagged", "clean", "lint-blind"),
                                  f"{path.name}: bad EXPECT header")
                    result = verify(text)
                    self.assertEqual(result.returncode, 0)
                    self.assertNotIn("Traceback", result.stderr)
                    for banner in ("Structural/lexical checks (static lint):",
                                   "Semantic review: not run",
                                   "Live effectiveness: not measured"):
                        self.assertIn(banner, result.stdout, path.name)
                    verdict, _ = parse_result(result.stdout)
                    if expect == "flagged":
                        self.assertNotEqual(
                            verdict, "Production-Ready",
                            f"{path.name}: defective prompt got a production verdict",
                        )
                    elif expect == "clean":
                        self.assertNotEqual(
                            verdict, "Major Rewrite",
                            f"{path.name}: valid prompt falsely accused",
                        )
                    else:  # lint-blind: record, don't demand
                        print(f"\n[lint-blind] {path.name} verdict: {verdict}")

    def test_pair_a_verdict_split(self):
        """Pair A must split at verdict level: defective strictly worse."""
        _, dt = load_fixture(FIXTURES / "w1-a-defective.md")
        _, vt = load_fixture(FIXTURES / "w1-a-valid.md")
        dv, _ = parse_result(verify(dt).stdout)
        vv, _ = parse_result(verify(vt).stdout)
        self.assertEqual(dv, "Major Rewrite")
        self.assertNotEqual(vv, "Major Rewrite")

    def test_pair_c_red_count_split(self):
        """Pair C splits on red count even though verdicts tie at Needs Fixes."""
        _, dt = load_fixture(FIXTURES / "w1-c-defective.md")
        _, vt = load_fixture(FIXTURES / "w1-c-valid.md")
        _, dreds = parse_result(verify(dt).stdout)
        _, vreds = parse_result(verify(vt).stdout)
        self.assertGreaterEqual(dreds, 1)
        self.assertEqual(vreds, 0)


if __name__ == "__main__":
    unittest.main()
