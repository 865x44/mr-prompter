# Final QA — downstream results (FQA-1 live; FQA-3/FQA-4 inputs frozen)

Sources: free-tier live harness (`omp -p`, sha-pinned prompt bytes) = PRIMARY;
agy live (gemini-3.8-flash, 6/6 PASS, $0.035) = corroboration;
muse simulated (6/6 PASS, no telemetry) = LOW WEIGHT, marked `simulated`.
Dead tier: `opencode-go/step-5-preview-free` → 400 Model unavailable (1 probe, not re-probed) — LIMITATION.

## FQA-1 downstream (fixed prompts × 3 inputs × live tiers)

| Run | muse-spark-1.3 (live) | gemini-3.8-flash (live) |
|---|---|---|
| A×INPUT-1 all-clear | PASS (in 3988/out 696/$0.00054/6.7s) | FAIL (a: `Uncertain:` dropped) |
| A×INPUT-2 version trap | PASS (v2.4.0 verbatim-only/$0.00055) | PASS (retry after thinking-loop stall) |
| A×INPUT-3 ambiguous | PASS (both verbatim/$0.00063) | FAIL (a: `Added+Fixed` dropped; 12k reasoning tokens) |
| B×INPUT-1 all-clear | PASS ($0.00055) | FAIL (a: `Uncertain:` dropped) |
| B×INPUT-2 version trap | PASS ($0.00055) | PASS |
| B×INPUT-3 ambiguous | PASS ($0.00048) | PASS (116s wall) |
| Lane totals | 6/6 PASS both lanes | 4/6 PASS both lanes (fails lane-invariant) |

Controls (thinking OFF, gemini): C1/C2/C4 all sections present, 20–26 out
tokens, ~5s. INTERPRETATION: the 3 gemini FAILs are a thinking/streaming
harness artifact, NOT prompt-body behavior. No run invented a version/date/
header; no ambiguous line ever guessed into Added/Fixed — on ANY tier, EITHER
lane. Old/new downstream delta on FQA-1: ZERO (honest result, not a loss).

Cost (17 runs): muse $0.0033 total (~$0.00055/run, ~7s); gemini $0.134 total
(~$0.022/run, reasoning-dominated 29.7k/34.5k out tokens); controls $0.011.
Free tier dead. Raw evidence (executor-local, no repo writes):
`/tmp/fqa1-raw2/`, `/tmp/fqa1-ctrl/` (re-run: `python3 /tmp/fqa1_run2.py …`).

## Method caveats (recorded, not hidden)
- gemini `text_end` truncates at first thinking→text boundary; extraction used
  concatenated `text_delta` in contentIndex order (executor finding — earlier
  gemini harness readings may be wrong).
- muse-tier results are SIMULATED (agent-as-model, no telemetry) — low weight.
- Single non-human judge; provisional status throughout.

## FQA-3 chains (live; NEW lanes executed — executor-built prompts from each SKILL version)

| Chain | Steps executed | Outcome | Linkage |
|---|---|---|---|
| A (K=3: P1a cost + P1b risk → P2 blind spots → P3 distill) | P1a/P1b gemini, P2+P3 muse (deliberate cross-tier check) | PASS — BetaSeek excluded ON quoted constraint (P3: "breaches the mandatory no-cloud-hosted-index boundary, categorically disqualified") | P2 ← P1a+P1b verbatim, P3 ← all verbatim (substring-verified) |
| B (K=2: E1 evidence pack → P2 scored decision) | E1/P2 muse, single-tier | PASS — constraint applied FIRST as exclusion filter ("This excludes BetaSeek — E1: cloud-hosted index only") | P2 ← E1 verbatim, cells cited by name |

B lane additionally names premature-convergence and fake-verification risks
in its preflight; A lane reaches the same correct outcome with 1 extra phase
(no consumer for the blind-spot pass — deletion-test claim stands, outcome
does not refute it). P1b fixture mentions a "vendor benchmark" absent from
the frozen VENDOR-B text; executor reasoned from deployment facts only, no
fabrication (recorded honestly).

## FQA-4 reuse (live, unseen snippet: olga/petr/contract/monday/badges)

| Lane | Output | Verdict |
|---|---|---|
| A (WHY-marked, 1 example) | Decisions: budget approved. / Actions: olga → draft contract (due monday); petr → review security section / Parking lot: order badges | PASS 4/4 (headers ordered, owners from notes, no inventions, no deictics) |
| B (3 examples, anti-patterns) | Same content, single-line Actions | PASS 4/4 |

Telemetry (12 runs): $0.0227 total (muse $0.0035, gemini $0.0192);
reasoning 7658 tokens. Tiers: muse + gemini reachable; space-bunny-free 400
unavailable; gpt-6-astra reachable, unused. Gemini ran with --thinking off,
no stalls.
