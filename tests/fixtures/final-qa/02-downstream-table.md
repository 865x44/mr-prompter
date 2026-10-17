# Final QA — downstream results (FQA-1 live telemetry; FQA-3/FQA-4 inputs frozen)

Sources: `live` = free-tier live harness (`omp -p`, sha-pinned prompt bytes)
with provider-reported telemetry = PRIMARY. `simulated` = early muse spot
(no telemetry, executor-as-model) = LOW WEIGHT, kept in a separate section
and never mixed into verdicts. Dead tier:
`opencode-go/step-5-preview-free` → 400 Model unavailable (1 probe,
not re-probed) — LIMITATION.

## FQA-1 downstream — live (fixed prompts × 3 inputs × live tiers)

Harness: `/tmp/fqa1_run2.py` (extraction = concatenated `text_delta` in
contentIndex order; `text_end` truncates at first thinking→text boundary).
Raw evidence: `/tmp/fqa1-raw2/` (`.prompt.txt` + `.jsonl` + `.rec.json` per
cell), verdicts: `/tmp/fqa1-raw2/score.json`. Re-run:
`python3 /tmp/fqa1_run2.py /tmp/fqa1-raw2` (executor-local, no repo writes).

| Run | muse-spark-1.3 live | gemini-3.8-flash live |
|---|---|---|
| A×INPUT-1 all-clear | PASS (in 3988/out 696/$0.00054/6.7s) | FAIL (a: `Uncertain:` dropped) |
| A×INPUT-2 version trap | PASS (v2.4.0 verbatim-only/$0.00055) | PASS (retry after thinking-loop stall) |
| A×INPUT-3 ambiguous | PASS (both verbatim/$0.00063) | FAIL (a: `Added+Fixed` dropped; 12k reasoning tokens) |
| B×INPUT-1 all-clear | PASS ($0.00055) | FAIL (a: `Uncertain:` dropped) |
| B×INPUT-2 version trap | PASS ($0.00055) | PASS |
| B×INPUT-3 ambiguous | PASS ($0.00048) | PASS (116s wall) |
| Lane totals | 6/6 PASS both lanes | A 1/3, B 2/3, TOTAL 3/6 (fails lane-invariant) |

Observed FAILs STAY FAIL in the primary experiment. No run invented a
version/date/header; no ambiguous line ever guessed into Added/Fixed — on
ANY tier, EITHER lane. Old/new downstream delta on FQA-1: ZERO (honest
result, not a loss).

Cost (17 runs = 12 live + 5 controls): live muse $0.0033 total
(~$0.00055/run, ~7s); live gemini $0.134 total (~$0.022/run,
reasoning-dominated 29.6k/34.5k reasoning/out tokens); controls $0.011
(C1–C5 thinking-OFF gemini + tools-ON muse, see HYPOTHESIS below).

## HYPOTHESIS — thinking/streaming artifact (NOT merged into verdicts)

Status: hypothesis, harness-artifact explanation for the 3 live gemini
FAILs. NOT a verdict override: the FAILs above stand as observed.

Supporting evidence (recorded, not hidden):
- Thinking-OFF controls (gemini, stub tools neutralized, `--thinking off`):
  C1/C2 (A-lane INPUT-1/INPUT-3) and C4/C5 (B-lane INPUT-1/INPUT-3) all
  sections present, 20–26 out tokens, ~5s wall. C3 (muse, tools ENABLED)
  confirms `--no-tools` did not change the muse behavior.
- Raw control evidence: `/tmp/fqa1-ctrl/` (`.prompt.txt` + `.jsonl` +
  `.rec.json` per cell), harness `/tmp/fqa1-ctrl.py`.
- Method caveat: gemini `text_end` truncates at the first
  thinking→text boundary; extraction used concatenated `text_delta` in
  contentIndex order (executor finding — earlier gemini harness readings
  may be wrong).

## Simulated spot (early muse, NO telemetry — low weight, separate)

- muse-tier results labelled `simulated` in the pilot draft were
  executor-as-model spots with no provider telemetry. They are LOW
  WEIGHT and are NOT mixed into the live table above.
- The live `muse-spark-1.3-contributor` rows (6/6 PASS, telemetry exact)
  supersede the simulated spot for verdict purposes.

## FQA-3 chains (live; NEW lanes executed — executor-built prompts from each SKILL version)

| Chain | Steps executed | Outcome | Linkage |
|---|---|---|---|
| A (K=3: P1a cost + P1b risk → P2 blind spots → P3 distill) | P1a/P1b gemini, P2+P3 muse (deliberate cross-tier check) | PASS — BetaSeek excluded ON quoted constraint (P3: "breaches the mandatory no-cloud-hosted-index boundary, categorically disqualified") | P2 ← P1a+P1b verbatim, P3 ← all verbatim (substring-verified) |
| B (K=2: E1 evidence pack → P2 scored decision) | E1/P2 muse, single-tier | PASS — constraint applied FIRST as exclusion filter ("This excludes BetaSeek — E1: cloud-hosted index only") | P2 ← E1 verbatim, cells cited by name |

B lane additionally names premature-convergence and fake-verification risks
in its preflight; A lane reaches the same correct outcome with 1 extra
phase (no consumer for the blind-spot pass — deletion-test claim stands,
outcome does not refute it). P1b fixture mentions a "vendor benchmark"
absent from the frozen VENDOR-B text; executor reasoned from deployment
facts only, no fabrication (recorded honestly).
K=1 challenger + K=2 reference: see `06-k1k2-evidence.md` (raw verbatim
outputs + run params + disputed cells; `quality-gated choice`).

## FQA-4 reuse (live, unseen snippet: olga/petr/contract/monday/badges)

| Lane | Output | Verdict |
|---|---|---|
| A (WHY-marked, 1 example) | Decisions: budget approved. / Actions: olga → draft contract (due monday); petr → review security section / Parking lot: order badges | PASS 4/4 (headers ordered, owners from notes, no inventions, no deictics) |
| B (3 examples, anti-patterns) | Same content, single-line Actions | PASS 4/4 |

Telemetry (12 runs): $0.0227 total (muse $0.0035, gemini $0.0192);
reasoning 7658 tokens. Tiers: muse + gemini reachable; space-bunny-free 400
unavailable; gpt-6-astra reachable, unused. Gemini ran with --thinking off,
no stalls.

## Method caveats (recorded, not hidden)

- gemini `text_end` truncates at first thinking→text boundary; extraction
  used concatenated `text_delta` in contentIndex order (executor finding —
  earlier gemini harness readings may be wrong).
- Single non-human judge; provisional status throughout.
