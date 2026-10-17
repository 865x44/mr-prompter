#!/usr/bin/env python3
"""
Chain twins runner (Wave 2, §4.3). Total with W1: 8 pairs.

Fixtures in fixtures/twins/w2-<pair>-{defective,valid}.md use a minimal
typed-link format (own test-side convention, NOT a product schema):

    P<n>:      executable step text (only P/HANDOFF/USES/TRACKED/EVIDENCE
    HANDOFF:   lines are parsed; `#` doc lines and SUMMARY-style metadata
    USES:      are ignored — executable text is the source of truth)
    TRACKED:
    EVIDENCE:

Deterministic rules (typed link/schema errors — machine-checkable):
  R1: steps numbered contiguously P1..PK.
  R2: every USES token resolves to an artifact from an EARLIER step's
      HANDOFF, or to an id declared in EVIDENCE.
  R3: every HANDOFF artifact is consumed by a LATER step's USES or is
      preserved in a TRACKED line (rejected-but-tracked).

Logic errors (premature convergence, fake "independent" verification with no
external evidence, silent filtering) are SEMANTIC — see w2-c-defective.md,
EXPECT: lint-blind. Same honesty discipline as W1: record, don't demand.
"""

import re
import unittest
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "twins"
PAIRS = ["a", "b", "c", "d"]


def parse_pack(path):
    """Return (expect, steps, violations). steps: list of dicts."""
    expect = None
    steps = []
    current = None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("# EXPECT:"):
            expect = line.split(":", 1)[1].strip().split()[0]
            continue
        if line.startswith("#") or not line:
            continue
        m = re.match(r"^P(\d+):\s*(.*)$", line)
        if m:
            current = {"n": int(m.group(1)), "handoff": [], "uses": [],
                       "tracked": [], "evidence": []}
            steps.append(current)
            continue
        m = re.match(r"^(HANDOFF|USES|TRACKED|EVIDENCE):\s*(.*)$", line, re.IGNORECASE)
        if m and current is not None:
            key = m.group(1).lower()
            toks = [t.strip() for t in re.split(r",", m.group(2)) if t.strip()]
            # TRACKED entries carry "(reason)"; keep the leading id token.
            if key == "tracked":
                toks = [re.split(r"\s+", t, 1)[0] for t in toks]
            current[key].extend(toks)
    violations = check(steps)
    return expect, steps, violations


def check(steps):
    violations = []
    if [s["n"] for s in steps] != list(range(1, len(steps) + 1)):
        violations.append("R1: step numbering not contiguous P1..PK")
    declared = {}  # artifact -> producing step n
    evidence_ids = set()
    for s in steps:
        for tok in s["uses"]:
            if tok not in declared and tok not in evidence_ids:
                violations.append(
                    f"R2: step P{s['n']} USES undeclared '{tok}'")
        for tok in s["handoff"]:
            declared.setdefault(tok, s["n"])
        evidence_ids.update(s["evidence"])
    consumed_or_tracked = set()
    for s in steps:
        consumed_or_tracked.update(s["uses"])
        consumed_or_tracked.update(s["tracked"])
    for art, producer in declared.items():
        if art not in consumed_or_tracked:
            violations.append(
                f"R3: artifact '{art}' from P{producer} never consumed nor tracked")
    return violations


class TestChainTwins(unittest.TestCase):
    def test_pair_expectations_hold(self):
        for pair in PAIRS:
            for side in ("defective", "valid"):
                with self.subTest(pair=pair, side=side):
                    path = FIXTURES / f"w2-{pair}-{side}.md"
                    self.assertTrue(path.exists(), f"missing {path.name}")
                    expect, steps, violations = parse_pack(path)
                    self.assertIn(expect, ("flagged", "clean", "lint-blind"),
                                  f"{path.name}: bad EXPECT")
                    self.assertGreaterEqual(len(steps), 2, f"{path.name}: need K>=2")
                    if expect == "flagged":
                        self.assertGreaterEqual(
                            len(violations), 1,
                            f"{path.name}: defective pack passed link check")
                    elif expect == "clean":
                        self.assertEqual(
                            violations, [],
                            f"{path.name}: valid pack flagged: {violations}")
                    else:
                        print(f"\n[lint-blind] {path.name}: "
                              f"{len(violations)} link violations (semantic fraud "
                              f"needs Level-2 review)")

    def test_pairs_split_on_violation_presence(self):
        """Every non-blind pair splits: defective violates, valid does not."""
        for pair in ("a", "b", "d"):
            with self.subTest(pair=pair):
                _, _, dv = parse_pack(FIXTURES / f"w2-{pair}-defective.md")
                _, _, vv = parse_pack(FIXTURES / f"w2-{pair}-valid.md")
                self.assertGreaterEqual(len(dv), 1)
                self.assertEqual(vv, [])

    def test_fusion_ready_variant_no_paste_tokens(self):
        """Fusion-ready chain packs must contain no unresolved [PASTE tokens."""
        # Negative probe: human-transfer placeholder is detected
        human_transfer_sample = (
            "P1: extract criteria\n"
            "HANDOFF: E1\n"
            "P2: From evidence pack E1:\n[PASTE E1 HERE]\n"
            "USES: E1\n"
        )
        self.assertRegex(
            human_transfer_sample,
            r"\[PASTE\b",
            "Human-transfer pack expected to have [PASTE token",
        )

        # Fusion-ready contract: no [PASTE tokens allowed in prompt body/chain steps
        fusion_ready_sample = (
            "P1: extract criteria\n"
            "HANDOFF: E1\n"
            "P2: From evidence pack E1 above: apply hard constraint.\n"
            "USES: E1\n"
        )
        self.assertNotRegex(
            fusion_ready_sample,
            r"\[PASTE\b",
            "Fusion-ready pack must not contain [PASTE tokens",
        )

        # Assert all valid twin fixtures satisfy the Fusion-ready token rule
        for pair in PAIRS:
            valid_path = FIXTURES / f"w2-{pair}-valid.md"
            content = valid_path.read_text(encoding="utf-8")
            self.assertNotRegex(
                content,
                r"\[PASTE\b",
                f"{valid_path.name} contains forbidden [PASTE token for Fusion-ready variant",
            )


if __name__ == "__main__":
    unittest.main()
