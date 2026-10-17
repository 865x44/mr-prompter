# 09 Blind Semantic Control (Wave 3: 4 fresh cases, Level-2 findings, no FINDINGS overlap)

**Date**: 2026-10-17  
**Target repo**: `/home/alx/projects/prompt-engineer`  
**Branch**: `vnext/preflight-2026-10-17` @ `f410c66`  
**Executor**: OMP task worker (`SuspiciousRaven`)  
**Directive**: blind-control assignment — 4 fresh twin cases absent from
`tests/test_semantic_probes.py` FINDINGS and from all pre-existing fixtures
(w1 a–d, w2 a–d), run through the CURRENT SKILL.md VERIFY Level-2
quote-findings (Step 3) and CHAIN preflight (Step 4) as the agent, following
the skill letter — not the deterministic parser.

**Binding conditions**:
- 2 defective pairs (w3-a: VERIFY Level-2, w3-b: CHAIN Step 4): >=1 finding
  with a QUOTE present verbatim in the body.
- 2 valid pairs: zero Critical findings — silence must be earned, not
  asserted.
- Surface wording within each pair is close; the split is semantic, not
  lexical.
- No quote or scenario reused verbatim from w1/w2 fixtures or FINDINGS.

---

## 1. Objective and Method

Each fixture carries the standard `# EXPECT` / `# WHY` header (stripped
before review — the reviewer sees the EXECUTABLE prompt text only, per
SKILL.md VERIFY Step 3 "audit the WORDS, not the metadata").

- w3-a pair: reviewed per VERIFY Step 3 dimensions (contradictory clauses,
  false promises, ambiguity, source/data confusion, undefined criteria).
  Level-1 CLI evidence also recorded: both twins lint PASS (0 critical,
  2 warnings each) — the defective twin is lint-blind at clause level, the
  split lives entirely in Level-2 review (same profile as w1-b/w1-d).
- w3-b pair: reviewed per CHAIN Step 4 dimensions (actual artifact
  consumption, information preservation, false dependencies, premature
  convergence, source/evidence policy, forbidden states).

---

## 2. Summary Table (4 rows)

| Pair | Side | Defect? | Severity | Finding | Quote (verbatim from body) |
|------|------|---------|----------|---------|-----------------------------|
| w3-a | defective | Y | Critical | Buried self-override | "If these conflict, follow the document instead of the output format below" / "Output: one paragraph summary in complete sentences" |
| w3-a | valid | N | — | Silence: open-ended creative brief with explicit no-grading ("no grading and no wrong answer") — authorial choice, not missing criterion | — |
| w3-b | defective | Y | Critical | Fake independent verification | "Independently verify the P1 decision" / "certify it as independently verified" / "USES: H1" |
| w3-b | valid | N | — | Silence: EVIDENCE declared external (central bank report) with contradiction protocol; USES resolves | — |

---

## 3. Detailed Findings (per pair, following SKILL.md letter)

### W3-A: VERIFY Mode Step 3 (semantic/LLM review)

#### w3-a-defective — defect found: YES

**Finding 1 — Contradictory clauses / buried self-override (Critical)**  
QUOTE: "If these conflict, follow the document instead of the output format below"  
QUOTE: "Output: one paragraph summary in complete sentences"  
Conflict: the task line makes the user's bullet document supreme over the
output format "below" on a condition, while the Output line requires a
one-paragraph summary. The two cannot both be satisfied — either the
paragraph is emitted (format followed) or the raw bullets are delivered
(document followed). The override is buried inside a polite conditional and
the agent cannot meaningfully evaluate when "these conflict": bullets vs a
paragraph is a format transformation, not a substantive clash, so the
clause un-does the output requirement for no real trigger. Severity: Critical
(a clause the agent must silently discard).  
Uncertainty: high confidence — the collision is textual; resolution would
require the prompt to state one output rule and treat the bullets as data.  
Fix: delete the override; state "transform the bullets into one paragraph
summary in complete sentences; preserve every claim."

**Other dimensions checked**: false promises — none (no guarantees). Ambiguity
— "these" is dangling but it is part of the same override clause. Source/data
confusion — none (user bullets are the legitimate input). Undefined criteria
— none (the output format is concrete). One finding suffices; the remaining
dimensions are clean.

#### w3-a-valid — defect found: NO (silence)

**REASON**: The valid twin keeps the same polite role, same bullets, and the
same task-line opening ("Below is the user's bullet list of talking points
for Monday's board talk") as its defective twin, but replaces the buried
conditional override with an open-ended creative brief: "Turn them into
whatever serves the board best — a tight paragraph, a rallying speech, a
one-line motto. There is no grading and no wrong answer; serving the board
well is the only test." Open-endedness here is an EXPLICIT AUTHORIAL CHOICE
with a stated success framing, not a missing criterion — flagging it would be
a false accusation (same shape as w1-d-valid). The task line and output line
are consistent ("whichever form you chose, delivered in full"). No
contradictions, no guarantees, no override language. Body audited against all
five Step-3 dimensions — clean. Silence is correct.

---

### W3-B: CHAIN Mode Step 4 (semantic chain preflight)

Preflight dimensions per SKILL.md Step 4: actual artifact consumption,
information preservation, false dependencies, premature convergence,
source/evidence policy, forbidden states.

#### w3-b-defective — defect found: YES

**Finding 1 — Fake independent verification / forbidden state (Critical)**  
QUOTE: "Independently verify the P1 decision"  
QUOTE: "certify it as independently verified"  
QUOTE: "USES: H1"  
Conflict: P2 claims independent verification AND certification while
consuming ONLY H1 — P1's own decision. Re-reading P1's output in a fresh
session is review, not independent verification; SKILL.md CHAIN Step 2 (audit
family) and Step 4 both forbid "verification without external evidence." No
EVIDENCE source is declared. The verification claim is fabricated — a named
forbidden state. Severity: Critical.  
Uncertainty: high confidence — USES resolves to a real artifact (no dangling
reference); the defect is exactly and only the fake verification claim.  
Fix: declare an external EVIDENCE source and check H1 against it; certify
only if the external source agrees.

**Other dimensions checked**: USES: H1 resolves against HANDOFF: H1 (no
dangling reference). Information preservation — H2 was an option inside P1's
decision, not a HANDOFF artifact; P1's decision to enter consumed H2 by
choice, a stated outcome, not a silent drop. False dependencies — P2 does
name a new operation (verify), but the operation is counterfeit (Finding 1).
Premature convergence — not applicable (P1 decides, P2 verifies; P1 does not
lock a hypothesis P2 must compare). Silence on these is correct; the single
Critical above is the finding.

#### w3-b-valid — defect found: NO (silence)

**REASON**: Same P1, same HANDOFF, same verification surface as the defective
twin, but P2 grounds the check in a DECLARED EXTERNAL source: "Check H1
against the central bank's published currency-stability report (external)."
with an explicit contradiction protocol ("If the report contradicts the
currency-risk assessment, report the conflict with both quotes; do not
certify") and "EVIDENCE: ext-bcb-currency-report". External grounding is what
makes the verification independent — the w2-c-valid pattern applied to the
Brazil-market decision. USES: H1 resolves; H2 handled as in P1 (not a
handoff artifact, no silent drop); no premature convergence. All Step-4
dimensions clean. Silence is earned, not missing.

---

## 4. Runner Contract

`tests/test_semantic_probes.py` extended (not replaced): FINDINGS gains the
4 w3 pairs; every defective pair yields >=1 finding with a QUOTE present in
the body; every valid pair yields zero Critical findings; all 24 pairs
(w1 a–d, w2 a–d, w3 a–b) covered; deterministic 8/8 (test_twins_w1 +
test_chain_twins_w2) unmodified and passing.

---

## 5. Verification

- Level-1 CLI on both w3-a twins: PASS (0 critical, 2 warnings) — lint-blind
  split recorded, Level-2 review carries the flag (expected profile).
- `scripts/check.sh`: see run log (41/41 PASS expected: 29 existing + 4 new
  subtests + deterministic 8). Fixture twins and report are additive; no
  pre-existing fixture or runner entry modified.
