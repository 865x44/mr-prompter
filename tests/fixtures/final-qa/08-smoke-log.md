# Final QA — 08 W1/W2 smoke-probe log (recorded actual outputs)

Source: worker wave reports (`wave1-report.md`, `wave2-report.md`,
2026-10-17, executor-recorded). Entries below are the recorded
actual-outputs logs, NOT re-runs: no model-judged PASS, no superiority
claims. Non-rerun entries are marked as such. (Full verbatim probe I/O
lives in the wave sessions; product CLI behavior re-verifiable via the
deterministic twin runners — `scripts/check.sh` green.)

## W1 smoke probes (actual outputs, non-rerun)

- P1 assemble K=1 → compact, no ritual sections, unknowns marked
  (OBSERVED-OK).
- P2 unknown model → explicit unknown, rc 0.
- P3 search/get → pinned rows.
- P4 JSON-shape hook fires only when unbacked (w1-b-valid with fields:
  no finding).
- P5 long-source section retrieved with relevance guidance.
- P6 search+unknown model → degrades to unboosted results, rc 0
  (pre-existing, noted).
- P7 Level-2 demo on w1-a-defective (reviewer-assessment): 2 Critical
  (contradictory output clauses, infallibility promise) + 2 Warning
  (self-override, fieldless JSON) with quotes/fixes; silence on
  w1-d-valid.
- P8/P9 negative inputs → rc 1 clean message, assemble-no-goal →
  unknowns.
- Pipe `BrokenPipe` traces seen only from `| head` truncation, not CLI
  bugs.

## W2 smoke probes (actual outputs, non-rerun)

- P1 K=1 valid — 200-word-changelog→tweet collapses to K=1 (no second
  artifact; recorded contract).
- P2 meaningful K=2 — DB-choice options-table→stress-test→choice
  (artifact consumed).
- P3 redundant K=3 ("research→go deeper→distill") collapses middle (no
  new input/artifact/criterion).
- P4 ledger+revision — P2 explicitly revises H2 with reason
  (supersede-noted, snapshot-compatible).
- P5 data-loss — checker output (R3×3 on w2-a-defective).
- P6 non-prompt failure — truncated tool JSON classified `tool-runtime`,
  prompt blame withheld as insufficient evidence, rerun-with-fixed-payload
  test proposed.
- P7 1-of-3 ambiguous ("concise but complete") — no gate, ambiguity
  finding + pin-and-rerun test.
- P8 subtractive repair on w1-b-defective — DELETE greeting sentence (no
  new rule), diff + preserved JSON-success + regression case
  (greeting-injection probe).
- No downstream suite, no superiority claims.

## Rerun status

All entries above: NON-RERUN (transcribed from the accepted W1/W2 worker
reports; not re-executed in this corrective wave — scope forbids FQA
re-runs). Deterministic twin coverage (W1 4 pairs + W2 4 pairs) stays
green via `scripts/check.sh`.
